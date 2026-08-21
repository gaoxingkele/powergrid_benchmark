#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the MA-SQLGrid sealed question set per MA-SEALED-SET-FREEZE-v1.0
(SHA-256 FC422FEF02B278D60B6E3850604EAB2E02F0683F7AF02115B6153FB36DC32A4E).

- 45 RTS + 40 SimBench items, seed 20260807.
- ALL template families are NEW (dev uses F01-F11 / 6 SimBench ids; sealed uses
  RS*/SS* ids) and target dev-underused tables/operations.
- Parameters are grounded in read-only DISTINCT/range probes of the pilot DBs.
- Every gold_sql is executed in the read-only sandbox: must be executable AND
  return a non-empty, non-all-NULL result; failures/empties are dropped and
  logged, never silently fixed.
- Freeze artifact: runs/ma_stage3/sealed_questions.jsonl + sealed_manifest.json
  (bytes write -- Windows CRLF lesson from the C2GES sealed batch).
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_annotation_pilot import PILOT_DIR, MA_DBS, utc_now  # noqa: E402
from generate_negative_controls import ro_connect, exec_rows  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SEED = 20260807
OUT_DIR = PILOT_DIR / "runs/ma_stage3"

YEAR_DATES = ["2020-03-15", "2020-06-20", "2020-09-10", "2020-11-25", "2020-01-20",
              "2020-05-05", "2020-08-12"]
JULY_DATES = ["2020-07-06", "2020-07-08", "2020-07-10", "2020-07-12", "2020-07-14",
              "2020-07-16", "2020-07-07"]


def day_window(date):
    return (f"timestamp >= '{date} 00:00:00' AND "
            f"timestamp < datetime('{date} 00:00:00', '+1 day')")


# ---------------------------------------------------------------------------
# template instances: (family, difficulty, question, sql, tables)
# ---------------------------------------------------------------------------

def rts_instances():
    out = []
    spin = ["Spin_Up_R1", "Spin_Up_R2", "Spin_Up_R3"]
    # RS01 reserve product daily peak
    combos = [(p, d) for p in spin for d in YEAR_DATES[:2]]  # 6 combos, take 5
    for p, d in combos[:5]:
        out.append(("RS01_reserve_product_daily_peak", "easy",
                    f"What was the peak day-ahead requirement in MW for the {p} reserve product on {d}?",
                    ("SELECT reserve_product, ROUND(MAX(requirement_mw), 3) AS peak_requirement_mw "
                     "FROM reserve_requirements_da WHERE reserve_product = '" + p + "' AND "
                     + day_window(d) + " GROUP BY reserve_product;"),
                    ["reserve_requirements_da"]))
    # RS02 reserve daily average by product
    for d in YEAR_DATES[:5]:
        out.append(("RS02_reserve_daily_avg_by_product", "easy",
                    f"What was the average day-ahead requirement for each spinning reserve product on {d}?",
                    ("SELECT reserve_product, ROUND(AVG(requirement_mw), 3) AS avg_requirement_mw "
                     "FROM reserve_requirements_da WHERE " + day_window(d) +
                     " GROUP BY reserve_product ORDER BY reserve_product;"),
                    ["reserve_requirements_da"]))
    # RS03 dispatch fuel window total (July only: dispatch_da covers 2020-07-05..18)
    fuels = ["NG", "Coal", "Solar", "Wind", "Oil"]
    for f, d in zip(fuels, JULY_DATES):
        out.append(("RS03_dispatch_fuel_daily_total", "medium",
                    f"What was the total day-ahead dispatched generation in MW for {f}-fueled units on {d}?",
                    ("SELECT g.fuel, ROUND(SUM(d.generation_mw), 2) AS total_generation_mw "
                     "FROM dispatch_da d JOIN generators g ON d.generator_uid = g.generator_uid "
                     "WHERE g.fuel = '" + f + "' AND d." + day_window(d).replace("timestamp", "timestamp")
                     + " GROUP BY g.fuel;"),
                    ["dispatch_da", "generators"]))
    # RS04 committed unit-hours
    for f, d in zip(["NG", "Coal", "Hydro", "Oil", "Solar"], JULY_DATES[1:6]):
        out.append(("RS04_committed_unit_hours_by_fuel", "medium",
                    f"How many committed unit-hours did {f}-fueled units have in the day-ahead dispatch on {d}?",
                    ("SELECT COUNT(*) AS committed_unit_hours "
                     "FROM dispatch_da d JOIN generators g ON d.generator_uid = g.generator_uid "
                     "WHERE d.committed = 1 AND g.fuel = '" + f + "' AND d." + day_window(d) + ";"),
                    ["dispatch_da", "generators"]))
    # RS05 branch rating threshold count
    for x in [200, 300, 400, 500, 600]:
        out.append(("RS05_branch_rating_threshold_count", "easy",
                    f"How many branches have a continuous rating above {x} MVA?",
                    ("SELECT COUNT(*) AS branch_count FROM branches "
                     f"WHERE continuous_rating_mva > {x};"),
                    ["branches"]))
    # RS06 branch rating list
    for x in [650, 550, 450, 350, 250]:
        out.append(("RS06_branch_rating_list", "easy",
                    f"List the branch identifiers and continuous ratings of branches rated above {x} MVA, ordered by rating descending.",
                    ("SELECT branch_uid, continuous_rating_mva FROM branches "
                     f"WHERE continuous_rating_mva > {x} ORDER BY continuous_rating_mva DESC;"),
                    ["branches"]))
    # RS07 start-up cost top-k per fuel
    for f, n in zip(["NG", "Coal", "Oil", "Hydro", "Solar"], [3, 3, 5, 5, 3]):
        out.append(("RS07_startup_cost_topk_by_fuel", "medium",
                    f"Which {n} {f}-fueled generators have the highest non-fuel start-up costs, and what are those costs?",
                    ("SELECT c.generator_uid, c.nonfuel_start_cost_usd FROM generator_costs c "
                     "JOIN generators g ON c.generator_uid = g.generator_uid "
                     f"WHERE g.fuel = '{f}' ORDER BY c.nonfuel_start_cost_usd DESC LIMIT {n};"),
                    ["generator_costs", "generators"]))
    # RS08 regional load daily peak
    combos = [(r, d) for r in (1, 2, 3) for d in YEAR_DATES[:2]]
    for r, d in combos[:5]:
        out.append(("RS08_regional_load_daily_peak", "easy",
                    f"What was the peak day-ahead load in MW in region {r} on {d}?",
                    ("SELECT region, ROUND(MAX(load_mw), 3) AS peak_load_mw "
                     f"FROM load_timeseries_da WHERE region = {r} AND " + day_window(d) +
                     " GROUP BY region;"),
                    ["load_timeseries_da"]))
    # RS09 renewable availability daily mean
    combos = [(t, d) for t in ("PV", "WIND") for d in YEAR_DATES[:3]]
    for t, d in combos[:5]:
        out.append(("RS09_renewable_availability_daily_mean", "easy",
                    f"What was the average available power in MW of {t} resources on {d}?",
                    ("SELECT resource_type, ROUND(AVG(available_mw), 3) AS avg_available_mw "
                     "FROM renewable_availability_da WHERE resource_type = '" + t + "' AND "
                     + day_window(d) + " GROUP BY resource_type;"),
                    ["renewable_availability_da"]))
    return out


def sb_instances():
    out = []
    # SS01 line length threshold count
    for x in [0.3, 0.5, 0.6, 0.7, 0.8]:
        out.append(("SS01_line_length_threshold_count", "easy",
                    f"How many lines are longer than {x} km?",
                    f"SELECT COUNT(*) AS line_count FROM lines WHERE length_km > {x};",
                    ["lines"]))
    # SS02 line current capacity list
    for x in [0.33, 0.35, 0.4, 0.45, 0.5]:
        out.append(("SS02_line_current_capacity_list", "easy",
                    f"List the names and maximum current capacities of lines rated below {x} kA, ordered by capacity ascending.",
                    ("SELECT name, max_current_ka FROM lines "
                     f"WHERE max_current_ka < {x} ORDER BY max_current_ka;"),
                    ["lines"]))
    # SS03 transformer capacity questions (2 transformers, both 63 MVA / 110->10 kV)
    out.append(("SS03_transformer_capacity", "easy",
                "What is the rated power in MVA of the largest transformer in the network?",
                "SELECT MAX(rated_power_mva) AS max_rated_power_mva FROM transformers;",
                ["transformers"]))
    out.append(("SS03_transformer_capacity", "easy",
                "What is the combined rated power in MVA of all in-service transformers?",
                ("SELECT ROUND(SUM(rated_power_mva), 3) AS total_rated_power_mva "
                 "FROM transformers WHERE in_service = 1;"),
                ["transformers"]))
    out.append(("SS03_transformer_capacity", "easy",
                "How many transformers are equipped with an on-load tap changer?",
                ("SELECT COUNT(*) AS oltc_transformer_count FROM transformers "
                 "WHERE on_load_tap_changer = 1;"),
                ["transformers"]))
    out.append(("SS03_transformer_capacity", "easy",
                "List the transformer names and rated powers ordered by rated power descending.",
                ("SELECT name, rated_power_mva FROM transformers "
                 "ORDER BY rated_power_mva DESC;"),
                ["transformers"]))
    out.append(("SS03_transformer_capacity", "easy",
                "What are the high-voltage and low-voltage nominal ratings of the transformers?",
                ("SELECT name, hv_nominal_kv, lv_nominal_kv FROM transformers ORDER BY name;"),
                ["transformers"]))
    out.append(("SS03_transformer_capacity", "easy",
                "How many transformers are recorded in this SimBench network?",
                "SELECT COUNT(*) AS transformer_count FROM transformers;",
                ["transformers"]))
    # SS04 load aggregation by voltage level
    out.append(("SS04_load_by_voltage_level", "medium",
                "How many loads are connected at each voltage level?",
                ("SELECT voltage_level_code, COUNT(*) AS load_count FROM loads "
                 "GROUP BY voltage_level_code ORDER BY voltage_level_code;"),
                ["loads"]))
    out.append(("SS04_load_by_voltage_level", "medium",
                "What is the total active power demand in MW at each voltage level?",
                ("SELECT voltage_level_code, ROUND(SUM(active_power_mw), 4) AS total_active_power_mw "
                 "FROM loads GROUP BY voltage_level_code ORDER BY voltage_level_code;"),
                ["loads"]))
    for code in (3, 5):
        out.append(("SS04_load_by_voltage_level", "easy",
                    f"How many loads are connected at voltage level {code}?",
                    ("SELECT COUNT(*) AS load_count FROM loads "
                     f"WHERE voltage_level_code = {code};"),
                    ["loads"]))
    out.append(("SS04_load_by_voltage_level", "easy",
                "What is the average per-load active power in MW at voltage level 5?",
                ("SELECT ROUND(AVG(active_power_mw), 6) AS avg_load_mw FROM loads "
                 "WHERE voltage_level_code = 5;"),
                ["loads"]))
    out.append(("SS04_load_by_voltage_level", "easy",
                "What is the largest single-load active power in MW at voltage level 5?",
                ("SELECT ROUND(MAX(active_power_mw), 4) AS max_load_mw FROM loads "
                 "WHERE voltage_level_code = 5;"),
                ["loads"]))
    # SS05 switch state counts
    out.append(("SS05_switch_state_count", "easy",
                "How many switches are currently closed?",
                "SELECT COUNT(*) AS closed_switch_count FROM switches WHERE closed = 1;",
                ["switches"]))
    out.append(("SS05_switch_state_count", "easy",
                "How many switches are currently open?",
                "SELECT COUNT(*) AS open_switch_count FROM switches WHERE closed = 0;",
                ["switches"]))
    out.append(("SS05_switch_state_count", "easy",
                "How many load-break switches (LBS) are recorded?",
                "SELECT COUNT(*) AS lbs_count FROM switches WHERE switch_type = 'LBS';",
                ["switches"]))
    out.append(("SS05_switch_state_count", "easy",
                "How many open switches are attached to lines?",
                ("SELECT COUNT(*) AS open_line_switch_count FROM switches "
                 "WHERE closed = 0 AND element_type = 'l';"),
                ["switches"]))
    out.append(("SS05_switch_state_count", "medium",
                "How many switches of each type are recorded?",
                ("SELECT switch_type, COUNT(*) AS switch_count FROM switches "
                 "GROUP BY switch_type ORDER BY switch_type;"),
                ["switches"]))
    # SS06 bus counts by voltage
    out.append(("SS06_bus_voltage_count", "medium",
                "How many buses are there at each voltage level?",
                ("SELECT voltage_level_code, COUNT(*) AS bus_count FROM buses "
                 "GROUP BY voltage_level_code ORDER BY voltage_level_code;"),
                ["buses"]))
    for kv in (10.0, 110.0):
        out.append(("SS06_bus_voltage_count", "easy",
                    f"How many in-service buses operate at a nominal voltage of {kv:g} kV?",
                    ("SELECT COUNT(*) AS bus_count FROM buses "
                     f"WHERE nominal_kv = {kv} AND in_service = 1;"),
                    ["buses"]))
    out.append(("SS06_bus_voltage_count", "easy",
                "How many buses are of bus type 'db' (double busbar)?",
                "SELECT COUNT(*) AS db_bus_count FROM buses WHERE bus_type = 'db';",
                ["buses"]))
    out.append(("SS06_bus_voltage_count", "easy",
                "What is the highest nominal bus voltage in kV in this network?",
                "SELECT MAX(nominal_kv) AS max_nominal_kv FROM buses;",
                ["buses"]))
    # SS07 line loading rank
    for n in (3, 5, 10):
        out.append(("SS07_line_loading_rank", "easy",
                    f"List the {n} lines with the highest maximum loading percent.",
                    ("SELECT name, max_loading_percent FROM lines "
                     f"ORDER BY max_loading_percent DESC LIMIT {n};"),
                    ["lines"]))
    out.append(("SS07_line_loading_rank", "easy",
                "What is the highest maximum loading percent among all lines?",
                "SELECT MAX(max_loading_percent) AS peak_max_loading_percent FROM lines;",
                ["lines"]))
    out.append(("SS07_line_loading_rank", "easy",
                "What is the average maximum loading percent across all lines?",
                "SELECT ROUND(AVG(max_loading_percent), 4) AS avg_max_loading_percent FROM lines;",
                ["lines"]))
    # SS08 load power threshold
    for x in (0.25, 0.3, 0.35, 0.4, 0.45):
        out.append(("SS08_load_power_threshold_count", "easy",
                    f"How many loads draw more than {x} MW of active power?",
                    f"SELECT COUNT(*) AS load_count FROM loads WHERE active_power_mw > {x};",
                    ["loads"]))
    return out


# ---------------------------------------------------------------------------
# build + verify + freeze
# ---------------------------------------------------------------------------

def build():
    rts = [dict(family=f, difficulty=d, question=q, sql=s, tables=t,
                dataset_id="RTS_GMLC_AUTO_PILOT") for f, d, q, s, t in rts_instances()]
    sb = [dict(family=f, difficulty=d, question=q, sql=s, tables=t,
               dataset_id="SIMBENCH_AUTO_PILOT") for f, d, q, s, t in sb_instances()]
    assert len(rts) == 45 and len(sb) == 42, (len(rts), len(sb))  # 42 SB candidates -> 40 kept
    return rts, sb


def main():
    import random
    rng = random.Random(SEED)
    rts, sb = build()
    # deterministic presentation order (shuffled), ids assigned after verification
    all_items = rts + sb
    for it in all_items:
        rng.shuffle(it["tables"])
    records, gen_log = [], []
    seen_sql = set()
    for it in all_items:
        ok, rows, cols, err = exec_rows(MA_DBS[it["dataset_id"]], it["sql"])
        entry = {"family": it["family"], "question": it["question"][:80]}
        if not ok:
            gen_log.append({**entry, "verdict": "dropped_exec_error", "error": err})
            continue
        if not rows:
            gen_log.append({**entry, "verdict": "dropped_empty_result"})
            continue
        if all(v is None for v in rows[0]):
            gen_log.append({**entry, "verdict": "dropped_all_null_result"})
            continue
        if it["sql"] in seen_sql:
            gen_log.append({**entry, "verdict": "dropped_duplicate_sql"})
            continue
        if it["sql"].lstrip().upper().startswith("SELECT COUNT") and rows[0][0] == 0:
            gen_log.append({**entry, "verdict": "dropped_zero_count"})
            continue
        seen_sql.add(it["sql"])
        gen_log.append({**entry, "verdict": "accepted", "row_count": len(rows)})
        records.append({**it, "answer_shape": {"columns": list(cols),
                                               "column_count": len(cols)},
                        "row_count": len(rows)})

    n_rts = sum(1 for r in records if r["dataset_id"] == "RTS_GMLC_AUTO_PILOT")
    n_sb = len(records) - n_rts
    print(f"[ok] verified: RTS {n_rts}/45, SB {n_sb}/40; "
          f"dropped {sum(1 for g in gen_log if g['verdict'] != 'accepted')}")
    if n_rts != 45 or n_sb != 40:
        print("[warn] target sizes not met; freezing what passed verification")

    # assign ids in deterministic shuffled order
    order = list(range(len(records)))
    rng.shuffle(order)
    final = []
    counters = {"RTS_GMLC_AUTO_PILOT": 0, "SIMBENCH_AUTO_PILOT": 0}
    for i in order:
        r = records[i]
        counters[r["dataset_id"]] += 1
        prefix = "RTS_SEALED_" if r["dataset_id"] == "RTS_GMLC_AUTO_PILOT" else "SB_SEALED_"
        qid = f"{prefix}{counters[r['dataset_id']]:03d}"
        final.append({
            "question_id": qid,
            "dataset_id": r["dataset_id"],
            "question": r["question"],
            "gold_sql": r["sql"],
            "template_family": r["family"],
            "tables": r["tables"],
            "answer_shape": r["answer_shape"],
            "difficulty": r["difficulty"],
            "annotation_status": "SEALED_AUTO_CANDIDATE",
            "human_reviewed": False,
            "split": "sealed_test",
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r, ensure_ascii=False) for r in final]
    packet_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    (OUT_DIR / "sealed_questions.jsonl").write_bytes(packet_bytes)  # no CRLF translation
    set_sha = hashlib.sha256(packet_bytes).hexdigest()
    per_item = [{"question_id": r["question_id"],
                 "sha256": hashlib.sha256((l + "\n").encode("utf-8")).hexdigest()}
                for r, l in zip(final, lines)]
    manifest = {
        "protocol_id": "MA-SEALED-SET-FREEZE-v1.0",
        "protocol_sha256": "FC422FEF02B278D60B6E3850604EAB2E02F0683F7AF02115B6153FB36DC32A4E",
        "frozen_at": utc_now(),
        "custodian": "annotation-pipeline",
        "seed": SEED,
        "novelty_rule": "all template families are new RS*/SS* ids; none of the 17 dev "
                        "template_family ids (F01-F11, asset_*, cross_asset_join, "
                        "network_topology, ranked_assets, threshold_filter) is reused",
        "target_size": "45 RTS + 40 SimBench",
        "n_items": len(final),
        "n_rts": counters["RTS_GMLC_AUTO_PILOT"],
        "n_simbench": counters["SIMBENCH_AUTO_PILOT"],
        "family_counts": {f: sum(1 for r in final if r["template_family"] == f)
                          for f in sorted({r["template_family"] for r in final})},
        "per_item": per_item,
        "packet_file": "sealed_questions.jsonl",
        "packet_sha256": set_sha,
        "no_leakage_declaration": (
            "Items were generated deterministically from the two pilot databases with "
            "read-only domain probes. Every gold_sql was sandbox-verified (executable, "
            "non-empty, non-all-NULL result). answer_shape comes from actual execution. "
            "No dev-candidate text was copied into sealed items. Annotator calls may only "
            "start after this manifest with packet_sha256 is written; the runner re-verifies "
            "the hash before annotating."),
        "generation_log": gen_log,
    }
    with open(OUT_DIR / "sealed_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[ok] FROZEN {len(final)} items -> {OUT_DIR / 'sealed_questions.jsonl'}")
    print(f"[ok] set sha256={set_sha}")
    print("[ok] families:", json.dumps(manifest["family_counts"]))


if __name__ == "__main__":
    main()
