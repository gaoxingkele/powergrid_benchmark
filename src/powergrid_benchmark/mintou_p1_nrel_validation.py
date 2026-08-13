"""Pre-registered NREL-118 transportability check for the P1 benchmark.

The reference acceptance cap is intentionally identical to the RTS-GMLC
benchmark. If the resulting target is degenerate, that is reported as an
applicability failure; the cap is not retuned after inspecting the dataset.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from powergrid_benchmark.mintou_real_curtailment import (
    P1_ROOT,
    REFERENCE_BIAS,
    REFERENCE_RESERVE,
)

ROOT = Path(__file__).resolve().parents[2]
NREL_ROOT = ROOT / "data" / "public_datasets" / "grid_cases" / "nrel118"
STATUS = "public_nrel118_transportability_v1_frozen_070_cap"


def _sum_folder(folder: Path) -> tuple[dict[str, float], int]:
    files = sorted(folder.glob("*.csv"))
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for path in files:
        with path.open(encoding="utf-8-sig", errors="ignore", newline="") as handle:
            for row in csv.DictReader(handle):
                timestamp = row.get("DATETIME") or ""
                try:
                    value = float(row.get("value") or "")
                except ValueError:
                    continue
                totals[timestamp] = totals.get(timestamp, 0.0) + value
                counts[timestamp] = counts.get(timestamp, 0) + 1
    complete = {timestamp: value for timestamp, value in totals.items() if counts[timestamp] == len(files)}
    return complete, len(files)


def build_nrel_series() -> tuple[list[dict[str, str]], dict[str, object]]:
    load, n_load = _sum_folder(NREL_ROOT / "Load" / "DA")
    wind, n_wind = _sum_folder(NREL_ROOT / "Wind" / "DA")
    solar, n_solar = _sum_folder(NREL_ROOT / "Solar" / "DA")
    timestamps = sorted(set(load) & set(wind) & set(solar))
    rows: list[dict[str, str]] = []
    shares: list[float] = []
    targets: list[float] = []
    for timestamp in timestamps:
        renewable = wind[timestamp] + solar[timestamp]
        share = renewable / max(load[timestamp], 1.0)
        target = max(0.0, renewable - REFERENCE_BIAS * load[timestamp]) / max(renewable, 1.0)
        shares.append(share)
        targets.append(target)
        rows.append(
            {
                "timestamp": timestamp,
                "load_mw": f"{load[timestamp]:.8f}",
                "wind_mw": f"{wind[timestamp]:.8f}",
                "solar_mw": f"{solar[timestamp]:.8f}",
                "renewable_share": f"{share:.8f}",
                "curtailment_risk_target": f"{target:.8f}",
                "source_status": STATUS,
            }
        )
    arr = np.asarray(shares)
    target_arr = np.asarray(targets)
    profile: dict[str, object] = {
        "hours": len(timestamps),
        "load_files": n_load,
        "wind_files": n_wind,
        "solar_files": n_solar,
        "reference_acceptance_cap": REFERENCE_BIAS,
        "reference_reserve": REFERENCE_RESERVE,
        "renewable_share_mean": float(arr.mean()),
        "renewable_share_q95": float(np.quantile(arr, 0.95)),
        "renewable_share_max": float(arr.max()),
        "positive_target_hours": int((target_arr > 0).sum()),
        "positive_target_share": float((target_arr > 0).mean()),
        "transportability_status": "not_identifiable_at_frozen_cap" if not np.any(target_arr > 0) else "identifiable",
        "status": STATUS,
    }
    return rows, profile


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows, profile = build_nrel_series()
    out = P1_ROOT / "evidence" / "runs"
    tables = P1_ROOT / "evidence" / "tables"
    configs = P1_ROOT / "src" / "configs"
    write_csv(out / "nrel118_transportability_target.csv", rows)
    write_csv(
        tables / "nrel118_transportability_summary.csv",
        [{key: str(value) for key, value in profile.items()}],
    )
    configs.mkdir(parents=True, exist_ok=True)
    (configs / "nrel118_transportability_config.json").write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    conclusion = (
        "The frozen 70% reference cap yields no positive target hours on the raw NREL-118 year. "
        "The P1 forecasting task is therefore not identifiable on this dataset without changing its operational definition. "
        "No model ranking is reported and the cap is not retuned."
        if profile["transportability_status"] == "not_identifiable_at_frozen_cap"
        else "The target is non-degenerate and may proceed to the pre-registered model comparison."
    )
    (out / "nrel118_transportability_analysis.md").write_text(
        "# NREL-118 Transportability Check\n\n"
        f"Status: `{STATUS}`.\n\n"
        f"- Hours: {profile['hours']}\n"
        f"- Mean / 95th percentile / maximum renewable share: {profile['renewable_share_mean']:.4f} / "
        f"{profile['renewable_share_q95']:.4f} / {profile['renewable_share_max']:.4f}\n"
        f"- Positive target hours at the frozen {REFERENCE_BIAS:.0%} cap: {profile['positive_target_hours']}\n\n"
        f"{conclusion}\n",
        encoding="utf-8",
    )
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
