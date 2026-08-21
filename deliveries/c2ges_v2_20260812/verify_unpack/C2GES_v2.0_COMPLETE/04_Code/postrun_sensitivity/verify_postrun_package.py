#!/usr/bin/env python3
"""Independent mechanical verifier for the post-run sensitivity package."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    last = 0.0
    for rank, idx in enumerate(order):
        last = max(last, min(1.0, (len(values) - rank) * values[idx]))
        out[idx] = last
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions", type=Path)
    ap.add_argument("package_dir", type=Path)
    args = ap.parse_args()
    failures: list[str] = []
    result_path = args.package_dir / "artifacts/exact_signflip_results.json"
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    if payload["input"]["sha256"] != digest(args.predictions):
        failures.append("prediction hash mismatch")

    values = {}
    for line in args.predictions.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        values[(row["doc_id"], int(row["budget"]), row["condition"])] = float(row["metrics"]["rougeL_f1"])
    if len(values) != 210:
        failures.append(f"prediction key count {len(values)} != 210")

    raw = []
    for row in payload["results"]:
        docs = sorted(d for d, k, c in values if k == row["budget"] and c == row["left_condition"])
        deltas = [values[(d, row["budget"], row["left_condition"])] - values[(d, row["budget"], row["right_condition"])] for d in docs]
        obs_sum = abs(sum(deltas))
        null_sums = (abs(sum(sign * d for sign, d in zip(signs, deltas)))
                     for signs in itertools.product((-1.0, 1.0), repeat=len(deltas)))
        extreme = sum(x + 1e-15 >= obs_sum for x in null_sums)
        p = extreme / (2 ** len(deltas))
        raw.append(p)
        checks = {
            "n_reports": len(docs),
            "extreme_assignments": extreme,
            "enumerated_assignments": 2 ** len(deltas),
        }
        for key, expected in checks.items():
            if row[key] != expected:
                failures.append(f"{row['contrast']} K={row['budget']} {key} mismatch")
        if abs(row["exact_two_sided_signflip_p"] - p) > 1e-15:
            failures.append(f"{row['contrast']} K={row['budget']} exact p mismatch")
    adjusted = holm(raw)
    for row, p in zip(payload["results"], adjusted):
        if abs(row["holm_adjusted_p_six_tests"] - p) > 1e-15:
            failures.append(f"{row['contrast']} K={row['budget']} Holm mismatch")

    manifest = json.loads((args.package_dir / "artifacts/OUTPUT_MANIFEST.json").read_text(encoding="utf-8"))
    for name, expected in manifest["output_sha256"].items():
        if digest(args.package_dir / "artifacts" / name) != expected:
            failures.append(f"artifact hash mismatch: {name}")
    meta = json.loads((args.package_dir / "rights_safe_metadata/rights_safe_report_metadata.json").read_text(encoding="utf-8"))
    if len(meta) != 40 or sum(r["inclusion_status"] == "included" for r in meta) != 27:
        failures.append("rights-safe metadata accounting mismatch")

    report = {
        "verifier": "independent_product_enumeration_v1",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "prediction_sha256": digest(args.predictions),
        "verified_contrasts": len(payload["results"]),
        "verified_assignments_per_contrast": 32768,
        "verified_metadata_rows": len(meta),
    }
    out = args.package_dir / "INDEPENDENT_MECHANICAL_VERIFY.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
