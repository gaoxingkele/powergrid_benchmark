"""Outcome-aware finite-pool diagnosis; never an online selection feature.

Reads frozen records without modifying them. Outputs no SQL or source text.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from run_role_ablation_audit import (
    BLACKBOARDS, CANONICAL, SLOTS, SLOT_TO_CELL, choose, load_jsonl,
    messages, original_decision,
)


def classify(pool_correct, eligible_correct, top_correct, selected_correct):
    if selected_correct:
        if not (pool_correct and eligible_correct and top_correct):
            raise ValueError("Non-nested correctness sets")
        return "selected_correct"
    if not pool_correct:
        if eligible_correct or top_correct:
            raise ValueError("Non-nested correctness sets")
        return "no_correct_candidate"
    if not eligible_correct:
        if top_correct:
            raise ValueError("Non-nested correctness sets")
        return "all_correct_candidates_gated_out"
    if not top_correct:
        return "correct_candidates_below_top_score"
    return "correct_top_candidate_lost_by_tie_order"


def run(output):
    paths = [BLACKBOARDS, CANONICAL]
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    boards, canonical = load_jsonl(BLACKBOARDS), load_jsonl(CANONICAL)
    cell_slots = {v: k for k, v in SLOT_TO_CELL.items()}
    correct = {(r["question_id"], cell_slots[(r["backbone"], r["condition"])]):
               bool(r["execution"]) for r in canonical}
    assert len(boards) == len({b["question_id"] for b in boards}) == 180
    assert len(canonical) == len(correct) == 1440
    rows = []
    for board in boards:
        qid = board["question_id"]
        v = {r["candidate_id"]: r for r in messages(board, "validation_evidence")}
        w = {r["candidate_id"]: r for r in messages(board, "counterfactual_evidence")}
        assert set(v) == set(w) == set(SLOTS)
        pool = {s for s in SLOTS if correct[qid, s]}
        for required, name, decision in [
            (False, "validation_only", "validation_rank_equal_budget_no_cf"),
            (True, "complete_witness", "full_coordination_complete_metamorphic"),
        ]:
            eligible = {s for s in SLOTS if v[s]["safe"] and v[s]["executable"] and
                        (not required or (w[s]["coverage_complete"] and
                         w[s]["evaluated_states"] == 3 and w[s]["passed_states"] >= 3))}
            assert eligible, "Frozen study was fully covered"
            scores = {s: 10 * int(v[s]["shape_ok"]) + 5 * int(v[s]["order_ok"]) +
                      min(int(v[s]["value_hits"]), 5) for s in eligible}
            top = {s for s in eligible if scores[s] == max(scores.values())}
            selected = choose(v, w, require_constructed_state=required)
            assert selected == next(s for s in SLOTS if s in top)
            assert selected == original_decision(board, decision)["selected_candidate_id"]
            ec, tc = eligible & pool, top & pool
            rows.append(dict(question_id=qid, selector=name,
                pool_correct_slots=len(pool), eligible_correct_slots=len(ec),
                gated_correct_slots=len(pool - eligible), top_slots=len(top),
                correct_top_slots=len(tc), mixed_correctness_top=bool(tc and top - pool),
                selected_correct=correct[qid, selected],
                category=classify(bool(pool), bool(ec), bool(tc), correct[qid, selected])))
    summaries = {}
    for name, expected in [("validation_only", 99), ("complete_witness", 100)]:
        subset = [r for r in rows if r["selector"] == name]
        counts = Counter(r["category"] for r in subset)
        assert sum(counts.values()) == 180 and counts["selected_correct"] == expected
        summaries[name] = dict(n=180, categories=dict(counts),
            questions_with_any_correct=sum(r["pool_correct_slots"] > 0 for r in subset),
            questions_with_eligible_correct=sum(r["eligible_correct_slots"] > 0 for r in subset),
            questions_with_any_correct_gate_loss=sum(r["gated_correct_slots"] > 0 for r in subset),
            gated_correct_slot_instances=sum(r["gated_correct_slots"] for r in subset),
            mixed_correctness_top_questions=sum(r["mixed_correctness_top"] for r in subset))
    assert hashes == {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result = dict(analysis_status="post_result_exploratory", unit="question",
        source_sha256=hashes, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        interpretation="Finite-pool evaluator agreement, not expert-semantic correctness or causal attribution",
        summaries=summaries, items=rows)
    output.mkdir(parents=True, exist_ok=True)
    target = output / "selection_failure_decomposition.json"
    if target.exists():
        raise FileExistsError("Use a new versioned output directory")
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
