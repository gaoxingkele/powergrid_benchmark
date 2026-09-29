#!/usr/bin/env python3
"""Publish non-verbatim agreement diagnostics for two machine annotators."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter
from pathlib import Path

from human_validation import cohen_kappa


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--deepseek", type=Path, required=True)
    parser.add_argument("--codex", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--disagreements-csv", type=Path, required=True)
    args = parser.parse_args()
    manifest = {row["sample_id"]: row for row in csv.DictReader(args.manifest.open(encoding="utf-8-sig", newline=""))}
    deepseek_value = json.loads(args.deepseek.read_text(encoding="utf-8"))
    codex_value = json.loads(args.codex.read_text(encoding="utf-8"))
    deepseek = {row["sample_id"]: row for row in deepseek_value["labels"]}
    codex = {row["sample_id"]: row for row in codex_value["labels"]}
    if set(manifest) != set(deepseek) or set(manifest) != set(codex):
        raise ValueError("sample sets differ")
    ids = sorted(manifest)
    ds_roles = [deepseek[key]["role"] for key in ids]; cx_roles = [codex[key]["role"] for key in ids]
    ds_valid = [deepseek[key]["unit_validity"] for key in ids]; cx_valid = [codex[key]["unit_validity"] for key in ids]
    heuristic = [manifest[key]["heuristic_role"] for key in ids]
    disagreements = []
    for key in ids:
        if deepseek[key]["role"] != codex[key]["role"] or deepseek[key]["unit_validity"] != codex[key]["unit_validity"]:
            disagreements.append({
                "sample_id": key, "doc_id": manifest[key]["doc_id"], "report_series_id": manifest[key]["report_series_id"],
                "heuristic_role": manifest[key]["heuristic_role"], "deepseek_role": deepseek[key]["role"],
                "codex_role": codex[key]["role"], "deepseek_validity": deepseek[key]["unit_validity"],
                "codex_validity": codex[key]["unit_validity"], "deepseek_confidence": deepseek[key]["confidence"],
                "codex_confidence": codex[key]["confidence"],
            })
    fields = list(disagreements[0]) if disagreements else ["sample_id"]
    with args.disagreements_csv.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(disagreements)
    result = {
        "schema": "c2ges-two-model-annotation-agreement-v1", "status": "AUTOMATED_PILOT_ONLY",
        "counts_as_human_validation": False, "scientific_construct_validation_allowed": False,
        "samples": len(ids), "series": len({manifest[key]["report_series_id"] for key in ids}),
        "role": {"raw_agreement": sum(a == b for a, b in zip(ds_roles, cx_roles)) / len(ids),
                 "cohen_kappa": cohen_kappa(ds_roles, cx_roles),
                 "deepseek_distribution": Counter(ds_roles), "codex_distribution": Counter(cx_roles),
                 "deepseek_vs_heuristic_raw": sum(a == b for a, b in zip(ds_roles, heuristic)) / len(ids),
                 "codex_vs_heuristic_raw": sum(a == b for a, b in zip(cx_roles, heuristic)) / len(ids)},
        "unit_validity": {"raw_agreement": sum(a == b for a, b in zip(ds_valid, cx_valid)) / len(ids),
                          "cohen_kappa": cohen_kappa(ds_valid, cx_valid),
                          "deepseek_distribution": Counter(ds_valid), "codex_distribution": Counter(cx_valid)},
        "confidence": {"deepseek_mean_1_to_5": statistics.fmean(float(deepseek[key]["confidence"]) for key in ids),
                       "codex_mean_1_to_5": statistics.fmean(float(codex[key]["confidence"]) for key in ids)},
        "samples_with_any_disagreement": len(disagreements),
        "interpretation_boundary": "Agreement between two LLMs is an error-discovery diagnostic, not independent human or expert validation.",
    }
    args.output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=dict))


if __name__ == "__main__":
    main()
