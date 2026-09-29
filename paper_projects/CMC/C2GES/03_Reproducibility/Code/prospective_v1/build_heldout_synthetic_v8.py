"""Build a four-series held-out synthetic stress set on unused fictional themes.

This is software stress material only. It cannot replace unseen real series,
human annotation, or confirmatory claims.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path

from generate_deepseek_synthetic import (
    CORE_ROLES,
    expand_report,
    hash_bytes,
    read_numeric_rows,
    sha256,
    validate_core,
    validate_dataset,
    words,
)

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
HELD_OUT_THEMES = (
    (12, "transformer cooling-control failure during a heat wave"),
    (13, "inverter ride-through response to a fictional voltage depression"),
    (14, "frequency response following fictional generator separation"),
    (15, "battery dispatch conflict during peak shaving"),
)
REGIMES = ("explicit", "paraphrased", "ambiguous", "explicit")
FACILITIES = (
    "Synthetic Cedar Tap",
    "Synthetic Quartz Bank",
    "Synthetic Willow Inverter Yard",
    "Synthetic Granite Feeder",
    "Synthetic Osprey Hydro",
    "Synthetic Nimbus Bus",
    "Synthetic Amber Storage",
    "Synthetic Pinion Substation",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sentence(text: str) -> str:
    text = " ".join(text.split())
    n = words(text)
    if n < 12:
        text = text.rstrip(".") + " under the recorded fictional operating window."
    if words(text) > 24:
        text = " ".join(text.split()[:24]).rstrip(",;") + "."
    return text[0].upper() + text[1:]


def core_units(theme: str, facility: str, report_index: int, rng: random.Random) -> list[dict]:
    mw = 18 + report_index * 7 + rng.randint(0, 5)
    kv = 69 if report_index % 2 == 0 else 138
    seconds = 1.2 + 0.35 * report_index
    minutes = 11 + 3 * report_index
    amp = 420 + 15 * report_index
    hz = 59.82 - 0.04 * report_index
    bank = 2 + report_index % 3
    templates = {
        "trigger_event": [
            f"{facility} recorded a {kv} kV depression at 14:{10+report_index:02d}:08 during the fictional {theme}.",
            f"A feeder lockout at {facility} opened breaker {bank}A after {seconds:.2f} seconds of measured undervoltage.",
            f"The sequence log at {facility} marked the initiating trip when residual current reached {amp} A.",
            f"Operators at {facility} noted the first alarm  {minutes} minutes after the fictional initiating discontinuity.",
        ],
        "root_cause": [
            f"The assigned cause at {facility} was a cooling-setpoint mismatch on bank {bank} during the heat-wave fixture.",
            f"A firmware deadband of {0.8+0.1*report_index:.1f} percent kept the {facility} controller from releasing reactive support.",
            f"Tagging records show bank {bank} remained in local mode at {facility}, blocking the remote cooling command.",
            f"The {facility} current-transformer ratio used {200+20*report_index}:5 while the relay file still assumed 400:5.",
        ],
        "propagation_or_response": [
            f"Adjacent {kv} kV buses at {facility} absorbed {mw} MW of redirected flow for {minutes} minutes.",
            f"Automatic reclosing at {facility} was blocked after the second unsuccessful attempt at 14:{20+report_index:02d}:40.",
            f"The {facility} plant ramped {mw} MW in {seconds+4:.1f} seconds once the indicated frequency reached {hz:.2f} Hz.",
            f"A neighboring capacitor bank at {facility} switched in {seconds:.2f} seconds later and reduced the voltage lag.",
        ],
        "impact": [
            f"The fixture at {facility} interrupted {mw} MW of synthetic load for {minutes} minutes before restoration.",
            f"Measured frequency at {facility} stayed below 59.90 Hz for {seconds+8:.1f} seconds after separation.",
            f"The {facility} storage inverter curtailed {mw//2} MW because its ride-through timer expired.",
            f"Customers on the fictional {facility} lateral saw a {minutes}-minute interruption recorded by the meter log.",
        ],
        "mitigation": [
            f"The corrective action at {facility} restored remote control of bank {bank} and verified the {200+20*report_index}:5 ratio.",
            f"Operators revised the {facility} ride-through timer to {seconds+1.5:.2f} seconds and retested the sequence.",
            f"A written check at {facility} now requires matching cooling setpoints before peak-shaving dispatch.",
            f"The {facility} after-action note requires independent telemetry on the reserve ramp, not the stale RTU channel.",
        ],
    }
    units: list[dict] = []
    for role in CORE_ROLES:
        chosen = list(templates[role])
        rng.shuffle(chosen)
        count = 4
        for index, text in enumerate(chosen[:count]):
            units.append(
                {
                    "text": sentence(text),
                    "role": role,
                    "causal_predecessors": [],
                    "summary_priority": 2 if index == 0 else 1,
                }
            )
    # stage-monotone acyclic edges by role order, not document order
    by_role = {role: [i for i, row in enumerate(units) if row["role"] == role] for role in CORE_ROLES}
    order = ["root_cause", "trigger_event", "propagation_or_response", "impact", "mitigation"]
    for src_role, dst_role in zip(order, order[1:]):
        for src in by_role[src_role][:2]:
            dst = by_role[dst_role][0]
            units[dst]["causal_predecessors"] = sorted(set(units[dst]["causal_predecessors"] + [src]))
    rng.shuffle(units)
    # remap predecessors after shuffle
    # rebuild from role links on the shuffled list
    index_by_id = {id(row): i for i, row in enumerate(units)}
    # predecessors currently store old indices; rebuild cleanly
    for row in units:
        row["causal_predecessors"] = []
    positions = {role: [i for i, row in enumerate(units) if row["role"] == role] for role in CORE_ROLES}
    for src_role, dst_role in zip(order, order[1:]):
        src = positions[src_role][0]
        dst = positions[dst_role][0]
        units[dst]["causal_predecessors"] = [src]
    return units


def distractors(theme: str, facility: str, rng: random.Random) -> list[str]:
    seeds = []
    for i in range(30):
        hour = (7 + i) % 24
        channel = 11 + (i * 3) % 29
        text = (
            f"{facility} archive channel {channel} stored a routine {theme.split()[0]} inspection "
            f"reading at {hour:02d}:{(i*7)%60:02d} with no incident attribution."
        )
        seeds.append(sentence(text))
    rng.shuffle(seeds)
    unique = list(dict.fromkeys(seeds))
    while len(unique) < 24:
        unique.append(sentence(f"{facility} spare log {len(unique)+1} kept an unrelated seasonal test note."))
    return unique[:30]


def local_pair(series_number: int, theme: str, rng: random.Random) -> dict:
    reports = []
    for report_index in range(2):
        facility = FACILITIES[(series_number + report_index * 3) % len(FACILITIES)]
        reports.append(
            {
                "title": f"{facility} {theme}",
                "core_units": core_units(theme, facility, report_index, rng),
                "distractor_seeds": distractors(theme, facility, rng),
            }
        )
    return {"reports": reports}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-csv", type=Path, required=True)
    parser.add_argument("--layout-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260918)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing existing output directory: {args.output}")
    profiles = read_numeric_rows(args.metadata_csv, args.layout_csv)
    args.output.mkdir(parents=True)
    rng = random.Random(args.seed)
    report_total = 8
    selected_profiles = [
        profiles[min(len(profiles) - 1, math.floor((i + 0.5) * len(profiles) / report_total))]
        for i in range(report_total)
    ]
    all_reports = []
    started = utc_now()
    for call_number, (series_number, theme) in enumerate(HELD_OUT_THEMES, 1):
        regime = REGIMES[call_number - 1]
        cores = validate_core(local_pair(series_number, theme, rng), require_distractor_seeds=True)
        for report_number, core_report in enumerate(cores, 1):
            profile = selected_profiles[2 * (call_number - 1) + report_number - 1]
            all_reports.append(
                expand_report(
                    core_report,
                    profile,
                    f"synthetic_s{series_number:02d}_r{report_number:02d}",
                    f"synthetic_series_{series_number:02d}",
                    regime,
                    theme,
                    rng,
                )
            )
    validation = validate_dataset(all_reports)
    if not validation["two_reports_per_series"]:
        raise ValueError("series cardinality gate failed")
    dataset_path = args.output / "synthetic_reports.jsonl"
    with dataset_path.open("x", encoding="utf-8", newline="\n") as stream:
        for report in sorted(all_reports, key=lambda row: row["doc_id"]):
            stream.write(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    manifest = {
        "schema": "c2ges-heldout-synthetic-stress-v8",
        "synthetic": True,
        "external_test_accessed": False,
        "confirmatory_claims_allowed": False,
        "generator": "local_deterministic_heldout_v8",
        "version_id": "heldout-v8",
        "seed": args.seed,
        "themes": [theme for _, theme in HELD_OUT_THEMES],
        "theme_status": "unused_in_v6_network_calibrated_series",
        "started_at": started,
        "completed_at": utc_now(),
        **validation,
        "dataset_sha256": sha256(dataset_path),
        "interpretation": "Fictional stress fixtures only; not real incident reports and not confirmatory evidence.",
    }
    (args.output / "SYNTHETIC_RUN_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS", "output": str(args.output), **validation}, ensure_ascii=False))


if __name__ == "__main__":
    main()
