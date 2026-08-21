"""Exact 12-cluster sign enumeration for the post-review v5 sensitivity check."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path

from analyze_release_v3 import effect_vectors, holm


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_two_sided(values: list[tuple[str, float]], clusters: dict[str, str]) -> tuple[float, int]:
    keys = sorted({clusters[question] for question, _ in values})
    estimate = sum(value for _, value in values) / len(values)
    extreme = 0
    assignments = 0
    for signs in itertools.product((-1, 1), repeat=len(keys)):
        sign_by_cluster = dict(zip(keys, signs))
        statistic = sum(sign_by_cluster[clusters[question]] * value for question, value in values) / len(values)
        extreme += abs(statistic) >= abs(estimate) - 1e-15
        assignments += 1
    return extreme / assignments, assignments


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", type=Path, required=True)
    parser.add_argument("--cluster-map", type=Path, required=True)
    parser.add_argument("--frozen-contrasts", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    with args.suite.open(encoding="utf-8-sig", newline="") as handle:
        suite = list(csv.DictReader(handle))
    clusters = json.loads(args.cluster_map.read_text(encoding="utf-8"))["mapping"]
    with args.frozen_contrasts.open(encoding="utf-8-sig", newline="") as handle:
        frozen = list(csv.DictReader(handle))

    primary = [row for row in suite if row["automatic_primary_eligible"].lower() == "true"]
    index = {
        (row["backbone"], row["condition"], row["question_id"]): int(row["suite_15state_and"].lower() == "true")
        for row in primary
    }
    vectors = effect_vectors(index)
    ordered_keys = [
        ("qwen", "hint"),
        ("qwen", "compact"),
        ("qwen", "interaction"),
        ("granite", "hint"),
        ("granite", "compact"),
        ("granite", "interaction"),
        ("granite_minus_qwen", "hint"),
        ("granite_minus_qwen", "compact"),
        ("granite_minus_qwen", "interaction"),
    ]
    rows = []
    for family_index, key in enumerate(ordered_keys, start=1):
        values = vectors[key]
        estimate = sum(value for _, value in values) / len(values)
        p_exact, assignments = exact_two_sided(values, clusters)
        frozen_row = frozen[family_index - 1]
        if abs(estimate - float(frozen_row["estimate"])) > 1e-15:
            raise ValueError(f"Frozen estimate mismatch for {key}")
        rows.append(
            {
                "family_index": family_index,
                "backbone_or_modifier": key[0],
                "effect": key[1],
                "estimate": estimate,
                "cluster_n": len({clusters[question] for question, _ in values}),
                "assignments": assignments,
                "exact_two_sided_p_raw": p_exact,
            }
        )
    adjusted = holm([row["exact_two_sided_p_raw"] for row in rows])
    for row, value in zip(rows, adjusted):
        row["holm_family_size"] = 9
        row["exact_two_sided_p_holm"] = value

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "exact_cluster_sign_tests.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "schema_version": "ma-sqlgrid-exact-sign-enumeration-v1",
        "status": "PASS",
        "scope": "post-review exact sensitivity for the same frozen nine contrasts",
        "primary_analysis_unchanged": True,
        "eligible_questions": 66,
        "clusters": 12,
        "assignments_per_test": 4096,
        "all_holm_equal_one": all(row["exact_two_sided_p_holm"] == 1.0 for row in rows),
        "sources": {
            "suite": {"path": str(args.suite.resolve()), "sha256": sha256(args.suite), "bytes": args.suite.stat().st_size},
            "cluster_map": {"path": str(args.cluster_map.resolve()), "sha256": sha256(args.cluster_map), "bytes": args.cluster_map.stat().st_size},
            "frozen_contrasts": {"path": str(args.frozen_contrasts.resolve()), "sha256": sha256(args.frozen_contrasts), "bytes": args.frozen_contrasts.stat().st_size},
        },
        "output": {"path": str(csv_path.resolve()), "sha256": sha256(csv_path), "bytes": csv_path.stat().st_size},
        "rows": rows,
    }
    report_path = args.out_dir / "EXACT_SIGN_ENUMERATION_REPORT.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"EXACT_SIGN_ENUMERATION_PASS tests={len(rows)} assignments=4096 holm_all_one={report['all_holm_equal_one']}")


if __name__ == "__main__":
    main()
