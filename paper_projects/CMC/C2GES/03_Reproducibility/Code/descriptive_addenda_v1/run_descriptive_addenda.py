"""Descriptive addenda for the C2GES Information manuscript (2026-09-25).

Answers three reviewer questions with deterministic, aggregate-only analyses over
already-packaged artifacts.  No new claims: every output is descriptive, and no
verbatim report or reference text is written to disk.

  Q1  path-change error profile: for cells where Full (AB-5) changed selections
      versus no-path (AB-6) in the seven-series matched-budget pilot, decompose
      changed units by typed-edge incidence, chronology-violating incident edges,
      incident-edge distance profile, and role-compatible pairs blocked by the
      12-position window.
  Q6  per-role precision/coverage: align selected units and reference sentences
      under the SAME lexical role cues (cue-vs-cue alignment, not expert-validated
      correctness).  Alignment is token-level on stopword-filtered content tokens
      (the pipeline's own tokenizer): precision_r = share of role-r selected-unit
      tokens that also occur in role-r reference sentences; coverage_r = share of
      role-r reference-sentence tokens recovered by the whole extract.  Token
      alignment is used because sentence-level ROUGE-L recall against differently
      worded executive-summary sentences essentially never fires (verified 2026-09-25).
  Q10 long-block audit detail: distribution of remaining long blocks under the
      block-preserving extraction rule versus the legacy splitter, and non-verbatim
      examples of long selected units (word counts, table markers, reference-token
      overlap).  The block-preserving segmentation was never used to rerun ranking;
      this script cannot and does not answer whether ordering would change.

Run from anywhere (paths resolve from __file__); writes to
03_Reproducibility/Data/descriptive_addenda_v1/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[3]  # 03_Reproducibility/Code/descriptive_addenda_v1 -> Workspace
REPO = SCRIPT.parents[6]     # Workspace -> C2GES -> paper_projects -> repo root
DATA = PROJECT / "03_Reproducibility" / "Data"
CORE = PROJECT / "03_Reproducibility" / "Code" / "core"
for _p in (CORE, CORE / "R2_v0_3"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from c2ges_offline import CAUSAL_TRANSITIONS, ROLES, _role_hits, _tokens, _unit_scale  # noqa: E402
from v03_methods import build_graph_v03  # noqa: E402

PILOT_DATASET = DATA / "exploratory_external_v0" / "derived_private" / "exploratory_reports_v3.jsonl"
PILOT_DIR = DATA / "exploratory_external_v0" / "e3_factorial_exploratory_v3"
HIST_DATASET = REPO / "paper_projects" / "applied_sciences_dual_rebuild" / "C2GES" / "original_title_rebuild" / "R2_v0_3" / "diagnostic_build_08" / "nerc_full_pdf_test_v0_3.jsonl"
HIST_PREDICTIONS = REPO / "paper_projects" / "applied_sciences_dual_rebuild" / "C2GES" / "original_title_rebuild" / "R2_v0_3" / "formal_runs_v0_3_1" / "c2ges_v031_formal_20260808" / "predictions.jsonl"
LAYOUT_PER_REPORT = DATA / "postrun_layout_audit" / "pymupdf_blocks_v1" / "layout_unit_per_report.csv"
OUTPUT_LENGTH = DATA / "postrun_diagnostics" / "output_length_per_report.csv"
OUT_DIR = DATA / "descriptive_addenda_v1"

MATCH_NOTE = "token-level alignment on stopword-filtered content tokens (no threshold)"
WINDOW = 12

ROLE_LABELS = {
    "root_cause": "Root cause",
    "trigger_event": "Trigger event",
    "propagation_or_response": "Propagation or response",
    "impact": "Impact",
    "mitigation": "Mitigation",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def split_reference_sentences(text: str) -> list[str]:
    """Deterministic regex sentence split used only for this descriptive addendum."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", text.strip())
    return [p.strip() for p in parts if len(p.strip()) >= 5]


def dominant_roles_for_texts(texts: list[str]) -> list[str | None]:
    """Assign dominant roles with the same cues and abstention rule as the pipeline,
    unit-scaled within the given text set."""
    if not texts:
        return []
    raw = {role: [_role_hits(t, role) for t in texts] for role in ROLES}
    scaled = {role: _unit_scale(values) for role, values in raw.items()}
    out: list[str | None] = []
    for i in range(len(texts)):
        scores = {role: scaled[role][i] for role in ROLES}
        best = max(scores.values())
        maxima = [role for role in ROLES if best > 0 and abs(scores[role] - best) <= 1e-12]
        out.append(maxima[0] if len(maxima) == 1 else None)
    return out


# ---------------------------------------------------------------- Q1

def q1_error_profile(reports: list[dict], selections: dict[tuple[str, int, str], set[str]],
                     deltas: dict[tuple[str, int], float]) -> tuple[list[dict], list[dict]]:
    """Return (per-cell rows, aggregate rows) for the AB-5 vs AB-6 change profile."""
    cell_rows: list[dict] = []
    for report in reports:
        doc = report["doc_id"]
        graph = build_graph_v03(report["candidate_sentences"], max_distance=WINDOW)
        nodes = {n.sid: n for n in graph.nodes}
        incident: dict[str, list] = {n.sid: [] for n in graph.nodes}
        for edge in graph.edges:
            incident[edge.source].append(edge)
            incident[edge.target].append(edge)
        # role-compatible ordered pairs blocked by the 12-position window
        blocked: Counter[str] = Counter()
        role_nodes = [n for n in graph.nodes if n.dominant_role is not None]
        for a in role_nodes:
            for b in role_nodes:
                if a.sid >= b.sid:
                    continue
                if abs(a.position - b.position) <= WINDOW:
                    continue
                if (a.dominant_role, b.dominant_role) in CAUSAL_TRANSITIONS:
                    blocked[a.sid] += 1
                    blocked[b.sid] += 1
                if (b.dominant_role, a.dominant_role) in CAUSAL_TRANSITIONS:
                    blocked[a.sid] += 1
                    blocked[b.sid] += 1
        for budget in (110, 260):
            full = selections.get((doc, budget, "AB-5"), set())
            nopath = selections.get((doc, budget, "AB-6"), set())
            changed = full ^ nopath
            delta = deltas.get((doc, budget))
            if delta is None:
                raise RuntimeError(f"missing item metrics for {doc} budget {budget}")
            rows = []
            for sid in sorted(changed):
                node = nodes.get(sid)
                if node is None:
                    raise RuntimeError(f"selected id {sid} not in graph of {doc}")
                edges = incident.get(sid, [])
                chrono = sum(1 for e in edges if nodes[e.source].position > nodes[e.target].position)
                dists = [abs(nodes[e.source].position - nodes[e.target].position) for e in edges]
                rows.append({
                    "doc_id": doc,
                    "word_budget": budget,
                    "delta_rougeL_full_minus_nopath": delta,
                    "sign": "negative" if delta < -1e-9 else ("positive" if delta > 1e-9 else "zero"),
                    "unit": sid,
                    "direction": "added_by_full" if sid in full else "dropped_by_full",
                    "role": node.dominant_role or "abstain",
                    "incident_edges": len(edges),
                    "chronology_violating_incident": chrono,
                    "max_incident_distance": max(dists) if dists else 0,
                    "blocked_beyond_window_pairs": blocked.get(sid, 0),
                })
            cell_rows.extend(rows)

    agg_rows: list[dict] = []
    for budget in (110, 260):
        for sign in ("negative", "zero", "positive", "all"):
            pool = [r for r in cell_rows if r["word_budget"] == budget and (sign == "all" or r["sign"] == sign)]
            if not pool:
                continue
            cells = {(r["doc_id"], r["word_budget"]) for r in pool}
            edge_incident = [r for r in pool if r["incident_edges"] > 0]
            agg_rows.append({
                "word_budget": budget,
                "delta_sign": sign,
                "cells": len(cells),
                "changed_units": len(pool),
                "share_edge_incident": round(len(edge_incident) / len(pool), 4),
                "share_chronology_violating_given_incident": round(
                    sum(1 for r in edge_incident if r["chronology_violating_incident"] > 0) / len(edge_incident), 4)
                if edge_incident else "",
                "mean_max_incident_distance": round(statistics.mean(r["max_incident_distance"] for r in edge_incident), 2)
                if edge_incident else "",
                "mean_blocked_beyond_window_pairs": round(statistics.mean(r["blocked_beyond_window_pairs"] for r in pool), 2),
                "role_hist_added": json.dumps(Counter(r["role"] for r in pool if r["direction"] == "added_by_full"), sort_keys=True),
                "role_hist_dropped": json.dumps(Counter(r["role"] for r in pool if r["direction"] == "dropped_by_full"), sort_keys=True),
            })
    return cell_rows, agg_rows


# ---------------------------------------------------------------- Q6

def q6_per_role(reports: list[dict], selections: dict[tuple[str, int, str], set[str]]) -> list[dict]:
    rows: list[dict] = []
    for report in reports:
        doc = report["doc_id"]
        texts = {c["sid"]: c["text"] for c in report["candidate_sentences"]}
        cand_roles = dict(zip(texts.keys(), dominant_roles_for_texts(list(texts.values()))))
        ref_sentences = split_reference_sentences(report["reference_summary"])
        ref_roles = dominant_roles_for_texts(ref_sentences)
        ref_tokens_by_role: dict[str, set[str]] = {r: set() for r in ROLES}
        for sent, role in zip(ref_sentences, ref_roles):
            if role is not None:
                ref_tokens_by_role[role] |= set(_tokens(sent))
        ref_counts = Counter(ref_roles)
        for budget in (110, 260):
            for cond in ("AB-5", "AB-6"):
                selected = selections.get((doc, budget, cond), set())
                extract_tokens = set().union(*(set(_tokens(texts[s])) for s in sorted(selected))) if selected else set()
                for role in ROLES:
                    sel_units = [texts[s] for s in sorted(selected) if cand_roles.get(s) == role]
                    ref_tokens = ref_tokens_by_role[role]
                    if sel_units:
                        sel_tokens = set().union(*(set(_tokens(u)) for u in sel_units))
                        prec = len(sel_tokens & ref_tokens) / len(sel_tokens) if sel_tokens else None
                    else:
                        prec = None
                    cov = len(ref_tokens & extract_tokens) / len(ref_tokens) if ref_tokens else None
                    rows.append({
                        "doc_id": doc, "word_budget": budget, "condition": cond, "role": role,
                        "selected_units_with_role": len(sel_units),
                        "reference_sentences_with_role": ref_counts.get(role, 0),
                        "token_precision": None if prec is None else round(prec, 4),
                        "token_coverage": None if cov is None else round(cov, 4),
                    })
    return rows


def q6_aggregate(rows: list[dict]) -> list[dict]:
    agg: list[dict] = []
    for budget in (110, 260):
        for cond in ("AB-5", "AB-6"):
            for role in ROLES:
                pool = [r for r in rows if r["word_budget"] == budget and r["condition"] == cond
                        and r["role"] == role]
                prec = [r["token_precision"] for r in pool if r["token_precision"] is not None]
                cov = [r["token_coverage"] for r in pool if r["token_coverage"] is not None]
                agg.append({
                    "word_budget": budget, "condition": cond, "role": role,
                    "reports_with_role_selected": len(prec),
                    "reports_with_role_in_reference": len(cov),
                    "macro_token_precision": round(statistics.mean(prec), 4) if prec else "",
                    "macro_token_coverage": round(statistics.mean(cov), 4) if cov else "",
                })
    return agg


# ---------------------------------------------------------------- Q10

def q10_long_blocks() -> tuple[list[dict], list[dict], list[dict]]:
    # (a) block-preserving audit distribution across the 27 historical reports
    with LAYOUT_PER_REPORT.open(encoding="utf-8-sig", newline="") as handle:
        layout = list(csv.DictReader(handle))
    dist_rows = []
    for r in layout:
        dist_rows.append({
            "doc_id": r["doc_id"], "split": r["split"],
            "layout_units": int(r["layout_units"]),
            "layout_units_over_100_words": int(r["layout_units_over_100_words"]),
            "maximum_layout_unit_words": int(r["maximum_layout_unit_words"]),
            "legacy_units": int(r["legacy_units"]),
            "detected_tables": int(r["detected_tables"]),
        })
    # (b) legacy per-condition long-unit counts
    with OUTPUT_LENGTH.open(encoding="utf-8-sig", newline="") as handle:
        legacy = list(csv.DictReader(handle))
    legacy_rows: dict[tuple[str, str], dict] = {}
    for r in legacy:
        key = (r["condition"], r["budget"])
        slot = legacy_rows.setdefault(key, {"condition": r["condition"], "unit_budget": r["budget"],
                                            "reports": 0, "units_over_100_words": 0,
                                            "table_marker_units": 0, "max_unit_words": 0})
        slot["reports"] += 1
        slot["units_over_100_words"] += int(r["units_over_100_words"])
        slot["table_marker_units"] += int(r["table_marker_units"])
        slot["max_unit_words"] = max(slot["max_unit_words"], int(r["maximum_unit_words"]))
    # (c) non-verbatim examples: longest selected units, reference-token content
    test = {r["doc_id"]: r for r in read_jsonl(HIST_DATASET)}
    predictions = read_jsonl(HIST_PREDICTIONS)
    examples: list[dict] = []
    for pred in predictions:
        if pred["condition"] not in ("c2ges_full", "textrank", "lead"):
            continue
        doc = test.get(pred["doc_id"])
        if doc is None:
            raise RuntimeError(f"prediction for unknown doc {pred['doc_id']}")
        texts = {c["sid"]: c["text"] for c in doc["candidate_sentences"]}
        ref_tokens = set(_tokens(doc["reference_summary"]))
        for sid in pred["selected_sentence_ids"]:
            words = len(texts[sid].split())
            if words <= 60:
                continue
            overlap = len(set(_tokens(texts[sid])) & ref_tokens)
            examples.append({
                "doc_id": pred["doc_id"], "condition": pred["condition"], "unit_budget": pred["budget"],
                "unit_words": words, "contains_table_marker": int("Table" in texts[sid]),
                "reference_token_overlap": overlap,
                "rougeL_f1_cell": round(pred["metrics"]["rougeL_f1"], 4),
            })
    examples.sort(key=lambda e: (-e["unit_words"], e["doc_id"], e["condition"]))
    return dist_rows, sorted(legacy_rows.values(), key=lambda r: (r["condition"], r["unit_budget"])), examples


# ---------------------------------------------------------------- main

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise RuntimeError(f"no rows for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    for path in (PILOT_DATASET, PILOT_DIR / "factorial_selected_ids.jsonl",
                 PILOT_DIR / "factorial_item_metrics.csv", HIST_DATASET, HIST_PREDICTIONS,
                 LAYOUT_PER_REPORT, OUTPUT_LENGTH):
        if not path.is_file():
            raise FileNotFoundError(path)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    reports = read_jsonl(PILOT_DATASET)
    selections: dict[tuple[str, int, str], set[str]] = {}
    for row in read_jsonl(PILOT_DIR / "factorial_selected_ids.jsonl"):
        key = (row["doc_id"], int(row["word_budget"]), row["condition"])
        selections[key] = set(row["selected_sentence_ids"])
    deltas: dict[tuple[str, int], float] = {}
    with (PILOT_DIR / "factorial_item_metrics.csv").open(encoding="utf-8-sig", newline="") as handle:
        per: dict[tuple[str, int], dict[str, float]] = {}
        for r in csv.DictReader(handle):
            if r["condition"] in ("AB-5", "AB-6"):
                per.setdefault((r["doc_id"], int(r["word_budget"])), {})[r["condition"]] = float(r["rougeL_f1"])
    for key, pair in per.items():
        deltas[key] = pair["AB-5"] - pair["AB-6"]

    q1_cells, q1_agg = q1_error_profile(reports, selections, deltas)
    write_csv(OUT_DIR / "q1_path_change_error_profile_per_unit.csv", q1_cells)
    write_csv(OUT_DIR / "q1_path_change_error_profile_aggregate.csv", q1_agg)

    q6_rows = q6_per_role(reports, selections)
    write_csv(OUT_DIR / "q6_per_role_precision_coverage_per_report.csv", q6_rows)
    write_csv(OUT_DIR / "q6_per_role_precision_coverage_aggregate.csv", q6_aggregate(q6_rows))

    q10_dist, q10_legacy, q10_examples = q10_long_blocks()
    write_csv(OUT_DIR / "q10_long_block_distribution_per_report.csv", q10_dist)
    write_csv(OUT_DIR / "q10_legacy_long_unit_by_condition.csv", q10_legacy)
    write_csv(OUT_DIR / "q10_long_unit_examples_nonverbatim.csv", q10_examples)

    manifest = {
        "schema": "c2ges-descriptive-addenda-v1",
        "created_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "status": "COMPLETE",
        "confirmatory_claims_allowed": False,
        "inputs": {p.name: {"path": str(p), "sha256": sha256(p)} for p in
                   (PILOT_DATASET, PILOT_DIR / "factorial_selected_ids.jsonl",
                    PILOT_DIR / "factorial_item_metrics.csv", HIST_DATASET, HIST_PREDICTIONS,
                    LAYOUT_PER_REPORT, OUTPUT_LENGTH)},
        "parameters": {
            "window": WINDOW, "match_rule": MATCH_NOTE,
            "reference_sentence_split": "regex (?<=[.!?])\\s+(?=[A-Z0-9\"(])",
            "role_labeling": "same lexical cues as pipeline, unit-scaled within each text set, abstain on ties",
        },
        "outputs": sorted(p.name for p in OUT_DIR.glob("*.csv")),
    }
    (OUT_DIR / "ADDENDA_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "COMPLETE", "out": str(OUT_DIR),
                      "rows": {"q1_units": len(q1_cells), "q1_agg": len(q1_agg),
                               "q6_reports": len(q6_rows), "q6_agg": len(q6_aggregate(q6_rows)),
                               "q10_dist": len(q10_dist), "q10_legacy": len(q10_legacy),
                               "q10_examples": len(q10_examples)}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
