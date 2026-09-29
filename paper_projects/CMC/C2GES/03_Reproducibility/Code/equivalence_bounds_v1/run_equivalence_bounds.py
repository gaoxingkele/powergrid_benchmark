"""G1a: turn the external "not significant" results into bounded statements.

The frozen external record is zero-inflated (many exactly-tied documents) and
heavy-tailed (a handful of documents move the mean).  Mean-based tests therefore
have very little power, which invites the reading "no effect was found, so there
is no effect".  This script computes what the same data *can* support:

  * the one-sided 95% bootstrap upper confidence limit of each paired contrast,
    i.e. "the gain is no larger than X";
  * a leave-one-out envelope for both the mean and that upper limit, so a reader
    can see which quantities depend on single documents;
  * the exact (or randomised) sign-flip p-value next to the sign share, so the
    weak power of the mean test is visible rather than implied.

Nothing is tuned on outcomes and no new corpus is touched: the input is the
frozen `external_arms_v3.json` produced by `run_external_arms_v3.py`.

Usage:
    python -B run_equivalence_bounds.py --json ../../Data/equivalence_bounds_v1/equivalence_bounds_v1.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "Data"
SOURCE = DATA / "external_prospective_v1" / "external_arms_v3.json"

CONTRASTS = (
    ("AB2", "AB0", "role layer"),
    ("AB1", "AB0", "role evidence only"),
    ("Full", "no_path", "path layer"),
    ("TextRank", "no_path", "TextRank baseline"),
    ("Lead", "no_path", "Lead baseline"),
)
KEY_ORDER = ("word:110", "word:180", "word:260", "word:400", "word:600", "unit:5", "unit:10", "unit:15")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cells(path: Path) -> tuple[dict, dict, dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in payload["rows"]:
        cells[(row["doc_id"], row["key"])][row["condition"]] = row
    return payload, cells, {c["contrast"] + "@" + c["budget"]: c for c in payload["contrasts"]}


def paired(cells, cand: str, ref: str, key: str) -> list[tuple[str, float]]:
    out = []
    for (doc_id, row_key), conditions in cells.items():
        if row_key != key or cand not in conditions or ref not in conditions:
            continue
        out.append((doc_id, conditions[cand]["rougeL_f1"] - conditions[ref]["rougeL_f1"]))
    return sorted(out)


def boot_upper(values: list[float], *, draws: int = 200000, seed: int = 20260926, alpha: float = 0.05) -> float:
    rng = random.Random(seed)
    n = len(values)
    means = [statistics.fmean(rng.choices(values, k=n)) for _ in range(draws)]
    means.sort()
    return means[int(math.ceil((1 - alpha) * draws)) - 1]


def exact_signflip(values: list[float]) -> float | None:
    n = len(values)
    if n > 18:
        return None
    observed = abs(statistics.fmean(values))
    hits = total = 0
    for signs in itertools.product((1, -1), repeat=n):
        total += 1
        if abs(statistics.fmean(s * v for s, v in zip(signs, values))) >= observed - 1e-12:
            hits += 1
    return hits / total


def randomized_signflip(values: list[float], *, draws: int = 100000, seed: int = 20260926) -> float:
    rng = random.Random(seed)
    observed = abs(statistics.fmean(values))
    hits = sum(
        1
        for _ in range(draws)
        if abs(statistics.fmean(v if rng.random() < 0.5 else -v for v in values)) >= observed - 1e-12
    )
    return (hits + 1) / (draws + 1)


def summarise(pairs: list[tuple[str, float]], *, draws: int, loo: bool = True) -> dict:
    """Summarise one paired contrast.

    ``loo=False`` skips the leave-one-out envelope, which is O(n) bootstraps and
    therefore inappropriate once n runs into the hundreds.
    """
    values = [v for _, v in pairs]
    n = len(values)
    negative = sum(1 for v in values if v < -1e-12)
    positive = sum(1 for v in values if v > 1e-12)
    zero = n - negative - positive
    p_exact = exact_signflip(values)
    item = {
        "n": n,
        "mean": round(statistics.fmean(values), 6),
        "median": round(statistics.median(values), 6),
        "sd": round(statistics.pstdev(values), 6),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "negative": negative,
        "positive": positive,
        "zero": zero,
        "positive_share_of_discordant": round(positive / (negative + positive), 3) if negative + positive else None,
        "signflip_p_exact": round(p_exact, 6) if p_exact is not None else None,
        "signflip_p_randomised": round(randomized_signflip(values), 6) if p_exact is None else None,
        "upper_limit_one_sided_95": round(boot_upper(values, draws=draws), 6),
        "largest_negative_document": min(pairs, key=lambda kv: kv[1])[0] if negative else None,
        "largest_positive_document": max(pairs, key=lambda kv: kv[1])[0] if positive else None,
    }
    if loo:
        loo_mean = []
        loo_upper = []
        for drop_index in range(n):
            rest = values[:drop_index] + values[drop_index + 1 :]
            loo_mean.append(statistics.fmean(rest))
            loo_upper.append(boot_upper(rest, draws=max(4000, draws // 20)))
        item["leave_one_out"] = {
            "mean_min": round(min(loo_mean), 6),
            "mean_max": round(max(loo_mean), 6),
            "mean_span": round(max(loo_mean) - min(loo_mean), 6),
            "upper_limit_max": round(max(loo_upper), 6),
        }
    else:
        item["leave_one_out"] = None
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="output JSON path")
    parser.add_argument("--csv", default=None, help="optional flat CSV path")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--draws", type=int, default=200000)
    args = parser.parse_args()

    payload, cells, frozen = load_cells(args.source)
    keys = [k for k in KEY_ORDER if any(k == row_key for _, row_key in cells)]
    records = []
    for cand, ref, label in CONTRASTS:
        for key in keys:
            pairs = paired(cells, cand, ref, key)
            if not pairs:
                continue
            item = summarise(pairs, draws=args.draws)
            item.update({"contrast": f"{cand} - {ref}", "label": label, "budget": key})
            records.append(item)

    out = {
        "schema": "c2ges-equivalence-bounds-v1",
        "purpose": "One-sided bootstrap bounds and leave-one-out envelopes for the frozen external contrasts.",
        "source_file": args.source.name,
        "source_sha256": sha256(args.source),
        "source_documents": payload["documents"],
        "bootstrap_draws": args.draws,
        "bootstrap_seed": 20260926,
        "records": records,
        "headline": {},
    }
    for cand, ref, label in CONTRASTS:
        sub = [r for r in records if r["contrast"] == f"{cand} - {ref}"]
        if sub:
            worst = max(sub, key=lambda r: r["upper_limit_one_sided_95"])
            out["headline"][f"{cand} - {ref}"] = {
                "max_upper_limit_one_sided_95": worst["upper_limit_one_sided_95"],
                "max_upper_limit_budget": worst["budget"],
                "upper_limit_max_under_leave_one_out": max(r["leave_one_out"]["upper_limit_max"] for r in sub),
            }

    target = Path(args.json)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    if args.csv:
        csv_path = Path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        fields = [
            "label",
            "budget",
            "n",
            "mean",
            "median",
            "sd",
            "negative",
            "positive",
            "zero",
            "positive_share_of_discordant",
            "signflip_p_exact",
            "signflip_p_randomised",
            "upper_limit_one_sided_95",
            "leave_one_out_mean_min",
            "leave_one_out_mean_max",
            "leave_one_out_upper_limit_max",
        ]
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(fields)
            for r in records:
                writer.writerow(
                    [
                        r["label"],
                        r["budget"],
                        r["n"],
                        r["mean"],
                        r["median"],
                        r["sd"],
                        r["negative"],
                        r["positive"],
                        r["zero"],
                        r["positive_share_of_discordant"],
                        r["signflip_p_exact"],
                        r["signflip_p_randomised"],
                        r["upper_limit_one_sided_95"],
                        r["leave_one_out"]["mean_min"],
                        r["leave_one_out"]["mean_max"],
                        r["leave_one_out"]["upper_limit_max"],
                    ]
                )

    print(json.dumps(out["headline"], indent=2))
    for r in records:
        print(
            f"  {r['label']:18s} {r['budget']:9s} mean={r['mean']:+.5f} "
            f"neg/pos/zero={r['negative']}/{r['positive']}/{r['zero']} "
            f"UB95={r['upper_limit_one_sided_95']:+.5f} LOOmean=[{r['leave_one_out']['mean_min']:+.5f},"
            f"{r['leave_one_out']['mean_max']:+.5f}] LOOUB_max={r['leave_one_out']['upper_limit_max']:+.5f}"
        )


if __name__ == "__main__":
    main()
