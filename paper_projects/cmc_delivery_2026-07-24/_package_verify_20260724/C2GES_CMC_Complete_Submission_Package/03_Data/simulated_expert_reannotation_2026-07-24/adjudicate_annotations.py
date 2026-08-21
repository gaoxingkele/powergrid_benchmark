#!/usr/bin/env python3
"""Validate three blind annotations and create majority-adjudicated labels."""

from __future__ import annotations

import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
from statistics import mean


HERE = Path(__file__).resolve().parent
ANNOTATOR_FILES = {
    "simexpert_A": HERE / "annotator_A.jsonl",
    "simexpert_B": HERE / "annotator_B.jsonl",
    "simexpert_C": HERE / "annotator_C.jsonl",
}


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def set_f1(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return 2 * len(a & b) / (len(a) + len(b))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def cohen_kappa(xs: list[int], ys: list[int]) -> float:
    if len(xs) != len(ys) or not xs:
        return float("nan")
    po = sum(x == y for x, y in zip(xs, ys)) / len(xs)
    px = sum(xs) / len(xs)
    py = sum(ys) / len(ys)
    pe = px * py + (1 - px) * (1 - py)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main() -> None:
    packet = read_jsonl(HERE / "blind_packet.jsonl")
    q_order: list[str] = []
    q_meta: dict[str, dict] = {}
    sid_order: dict[str, dict[str, int]] = {}
    for doc in packet:
        sid_order[doc["doc_id"]] = {
            sentence["sid"]: index for index, sentence in enumerate(doc["sentences"])
        }
        for q in doc["questions"]:
            qid = q["qid"]
            q_order.append(qid)
            q_meta[qid] = {
                **q,
                "doc_id": doc["doc_id"],
                "valid_sids": set(sid_order[doc["doc_id"]]),
            }
    if len(q_order) != 75 or len(set(q_order)) != 75:
        raise RuntimeError("Blind packet must contain 75 unique questions")

    annotations: dict[str, dict[str, dict]] = {}
    validation_errors: list[str] = []
    for expected_id, path in ANNOTATOR_FILES.items():
        rows = read_jsonl(path)
        by_qid = {row.get("qid"): row for row in rows}
        annotations[expected_id] = by_qid
        if len(rows) != 75 or len(by_qid) != 75:
            validation_errors.append(
                f"{expected_id}: expected 75 unique rows, got {len(rows)}/{len(by_qid)}"
            )
        for qid in q_order:
            row = by_qid.get(qid)
            if row is None:
                validation_errors.append(f"{expected_id}: missing {qid}")
                continue
            if row.get("annotator_id") != expected_id:
                validation_errors.append(f"{expected_id}: wrong annotator_id for {qid}")
            if row.get("role") != q_meta[qid]["role"]:
                validation_errors.append(f"{expected_id}: wrong role for {qid}")
            ids = row.get("evidence_sentence_ids")
            if not isinstance(ids, list) or len(ids) > 4 or len(ids) != len(set(ids)):
                validation_errors.append(f"{expected_id}: invalid evidence list for {qid}")
                continue
            invalid = set(ids) - q_meta[qid]["valid_sids"]
            if invalid:
                validation_errors.append(
                    f"{expected_id}: unknown evidence IDs for {qid}: {sorted(invalid)}"
                )
            confidence = row.get("confidence")
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                validation_errors.append(f"{expected_id}: invalid confidence for {qid}")
            if bool(row.get("answerable")) != bool(ids):
                validation_errors.append(
                    f"{expected_id}: answerable/evidence mismatch for {qid}"
                )
    if validation_errors:
        (HERE / "validation_errors.json").write_text(
            json.dumps(validation_errors, indent=2) + "\n", encoding="utf-8"
        )
        raise RuntimeError(
            f"Annotation validation failed with {len(validation_errors)} errors; "
            "see validation_errors.json"
        )

    pair_names = list(combinations(ANNOTATOR_FILES, 2))
    pair_exact = {f"{a}__{b}": [] for a, b in pair_names}
    pair_jaccard = {f"{a}__{b}": [] for a, b in pair_names}
    pair_f1 = {f"{a}__{b}": [] for a, b in pair_names}
    binary_vectors = {
        f"{a}__{b}": ([], []) for a, b in pair_names
    }
    adjudicated: list[dict] = []
    disagreements: list[dict] = []

    for qid in q_order:
        rows = {aid: annotations[aid][qid] for aid in ANNOTATOR_FILES}
        sets = {
            aid: set(row["evidence_sentence_ids"]) for aid, row in rows.items()
        }
        for a, b in pair_names:
            key = f"{a}__{b}"
            pair_exact[key].append(sets[a] == sets[b])
            pair_jaccard[key].append(jaccard(sets[a], sets[b]))
            pair_f1[key].append(set_f1(sets[a], sets[b]))
            for sid in q_meta[qid]["valid_sids"]:
                binary_vectors[key][0].append(int(sid in sets[a]))
                binary_vectors[key][1].append(int(sid in sets[b]))

        votes = Counter(sid for sids in sets.values() for sid in sids)
        doc_id = q_meta[qid]["doc_id"]
        majority = [sid for sid, count in votes.items() if count >= 2]
        majority.sort(key=lambda sid: sid_order[doc_id][sid])
        fallback = False
        if not majority and any(sets.values()):
            fallback = True
            ranked = sorted(
                votes,
                key=lambda sid: (
                    -votes[sid],
                    -mean(
                        rows[aid]["confidence"]
                        for aid in rows
                        if sid in sets[aid]
                    ),
                    sid_order[doc_id][sid],
                ),
            )
            majority = ranked[: min(3, len(ranked))]
        if len(majority) > 4:
            majority = sorted(
                majority,
                key=lambda sid: (
                    -votes[sid],
                    sid_order[doc_id][sid],
                ),
            )[:4]
            majority.sort(key=lambda sid: sid_order[doc_id][sid])

        representative = max(
            rows,
            key=lambda aid: (
                set_f1(sets[aid], set(majority)),
                rows[aid]["confidence"],
            ),
        )
        exact_all = len({tuple(sorted(s)) for s in sets.values()}) == 1
        any_pair_exact = any(sets[a] == sets[b] for a, b in pair_names)
        record = {
            "qid": qid,
            "doc_id": doc_id,
            "role": q_meta[qid]["role"],
            "evidence_sentence_ids": majority,
            "answerable": bool(majority),
            "answer_summary": rows[representative]["answer_summary"],
            "confidence": round(mean(row["confidence"] for row in rows.values()), 4),
            "label_status": "simulated_expert_adjudicated",
            "adjudication": {
                "method": (
                    "sentence_level_majority_vote"
                    if not fallback
                    else "confidence_weighted_fallback_no_sentence_majority"
                ),
                "exact_all_three": exact_all,
                "any_pair_exact": any_pair_exact,
                "vote_counts": dict(sorted(votes.items())),
                "representative_annotator": representative,
                "annotator_sets": {
                    aid: rows[aid]["evidence_sentence_ids"] for aid in rows
                },
            },
        }
        adjudicated.append(record)
        if not exact_all:
            disagreements.append(record)

    pairwise = {}
    for key in pair_exact:
        xs, ys = binary_vectors[key]
        pairwise[key] = {
            "exact_set_agreement": mean(pair_exact[key]),
            "mean_jaccard": mean(pair_jaccard[key]),
            "mean_set_f1": mean(pair_f1[key]),
            "binary_sentence_cohen_kappa": cohen_kappa(xs, ys),
        }
    summary = {
        "annotation_type": "three_AI_simulated_experts_not_human_gold",
        "documents": 15,
        "questions": 75,
        "all_three_exact_set_agreement": mean(
            row["adjudication"]["exact_all_three"] for row in adjudicated
        ),
        "any_pair_exact_set_agreement": mean(
            row["adjudication"]["any_pair_exact"] for row in adjudicated
        ),
        "questions_with_disagreement": len(disagreements),
        "questions_using_no_majority_fallback": sum(
            row["adjudication"]["method"].startswith("confidence_weighted")
            for row in adjudicated
        ),
        "mean_adjudicated_evidence_count": mean(
            len(row["evidence_sentence_ids"]) for row in adjudicated
        ),
        "unanswerable_questions": sum(not row["answerable"] for row in adjudicated),
        "pairwise": pairwise,
    }

    (HERE / "adjudicated_labels.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in adjudicated) + "\n",
        encoding="utf-8",
    )
    (HERE / "disagreements.json").write_text(
        json.dumps(disagreements, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (HERE / "agreement_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Simulated-Expert Agreement Report",
        "",
        "**Disclosure:** all three annotators are AI simulations, not human experts.",
        "",
        f"- Documents: {summary['documents']}",
        f"- Questions: {summary['questions']}",
        f"- All-three exact-set agreement: {summary['all_three_exact_set_agreement']:.3f}",
        f"- Any-pair exact-set agreement: {summary['any_pair_exact_set_agreement']:.3f}",
        f"- Questions with disagreement: {summary['questions_with_disagreement']}",
        f"- No-majority fallbacks: {summary['questions_using_no_majority_fallback']}",
        f"- Mean adjudicated evidence count: {summary['mean_adjudicated_evidence_count']:.3f}",
        f"- Unanswerable questions: {summary['unanswerable_questions']}",
        "",
        "## Pairwise agreement",
        "",
        "| Pair | Exact set | Mean Jaccard | Mean set F1 | Binary sentence Cohen kappa |",
        "|---|---:|---:|---:|---:|",
    ]
    for key, values in pairwise.items():
        lines.append(
            f"| {key} | {values['exact_set_agreement']:.3f} | "
            f"{values['mean_jaccard']:.3f} | {values['mean_set_f1']:.3f} | "
            f"{values['binary_sentence_cohen_kappa']:.3f} |"
        )
    (HERE / "agreement_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
