#!/usr/bin/env python3
"""Aggregate real API token, latency, and retry statistics per condition.

Reads outputs/predictions.jsonl (which stores the provider-reported
token_input/token_output counts and end-to-end latency for every one of the
900 archived API calls) and outputs/scores.jsonl (which stores the runner's
prompt-token estimates). No model calls are made.
"""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs_deepseek_chat"

CONDITIONS = [
    "C1_SchemaOnly_Direct",
    "C2_FullSchemaValues_Direct",
    "C3_CHESSLite_Generic",
    "C4_MASQLGrid_DomainContext",
    "C5_MASQLGrid_DomainContext_Validated",
]


def main() -> None:
    preds = [json.loads(line) for line in (OUT_DIR / "predictions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    scores = [json.loads(line) for line in (OUT_DIR / "scores.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    est_by_cond: dict[str, list[float]] = {}
    for s in scores:
        if "prompt_token_estimate" in s:
            est_by_cond.setdefault(s["condition"], []).append(float(s["prompt_token_estimate"]))

    result = {}
    hdr = f"{'condition':<42} {'n':>4} {'in/med':>7} {'in/mean':>8} {'out/mean':>9} {'lat/mean':>9} {'lat/med':>8} {'est':>7} {'retries':>8}"
    print(hdr)
    for cond in CONDITIONS:
        rows = [p for p in preds if p["condition"] == cond]
        if not rows:
            continue
        ti = [int(p["token_input"]) for p in rows]
        to = [int(p["token_output"]) for p in rows]
        lat = [int(p["latency_ms"]) for p in rows]
        retries = Counter(int(p["retry_count"]) for p in rows)
        errors = sum(1 for p in rows if p.get("error"))
        result[cond] = {
            "n": len(rows),
            "token_input_mean": round(statistics.mean(ti), 1),
            "token_input_median": statistics.median(ti),
            "token_input_total": sum(ti),
            "token_output_mean": round(statistics.mean(to), 1),
            "token_output_total": sum(to),
            "latency_ms_mean": round(statistics.mean(lat), 1),
            "latency_ms_median": statistics.median(lat),
            "prompt_token_estimate_mean": round(statistics.mean(est_by_cond[cond]), 1) if cond in est_by_cond else None,
            "retry_count_distribution": dict(sorted(retries.items())),
            "error_records": errors,
        }
        r = result[cond]
        print(f"{cond:<42} {r['n']:>4} {r['token_input_median']:>7} {r['token_input_mean']:>8} {r['token_output_mean']:>9} "
              f"{r['latency_ms_mean']:>9} {r['latency_ms_median']:>8} {str(r['prompt_token_estimate_mean']):>7} {dict(sorted(retries.items()))!s:>8}")

    c2 = result["C2_FullSchemaValues_Direct"]
    c4 = result["C4_MASQLGrid_DomainContext"]
    reduction = 1 - c4["token_input_mean"] / c2["token_input_mean"]
    est_reduction = (1 - c4["prompt_token_estimate_mean"] / c2["prompt_token_estimate_mean"]) if c2.get("prompt_token_estimate_mean") and c4.get("prompt_token_estimate_mean") else float("nan")
    result["derived"] = {
        "c4_vs_c2_real_input_token_reduction": round(reduction, 4),
        "c4_vs_c2_estimated_prompt_token_reduction": round(est_reduction, 4),
        "note": "real input tokens include serving-side fixed overhead shared by all conditions",
    }
    print(f"\nC4 vs C2 real API input-token reduction:      {reduction:.4f}")
    print(f"C4 vs C2 estimated prompt-token reduction:    {est_reduction:.4f}")

    out = HERE / "efficiency_stats_deepseek.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
