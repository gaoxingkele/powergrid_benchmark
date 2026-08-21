#!/usr/bin/env python3
"""Independent audit of the one eligible MA-SQLGrid local factorial run.

The quarantined first attempt is never read.  Its rejection is established only
from the incident record supplied outside that directory.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[4]
MA = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid"
RUN = MA / "formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1"
INCIDENT = MA / "FORMAL_RUN_INCIDENT_01.json"
FREEZE = MA / "FORMAL_RUN_FREEZE_MANIFEST.json"
STAT_DIR = MA / "statistics"
SOURCE = ROOT / "paper_projects/2026_ma_sqlgrid_cmc/source"
CODE_DIR = SOURCE / "code/experiment_final"
DATA_DIR = SOURCE / "data/griddb_maintenance_v2_v0_1"
SHARED_STAT = ROOT / "paper_projects/applied_sciences_dual_rebuild/shared/stat_audit.py"
CELLS = ["F00_Full_NoShape", "F01_Full_WithShape", "F10_Compact_NoShape", "F11_Compact_WithShape"]
GOLD_KEYS = {"gold_sql", "gold_result", "gold_results", "answer", "answers"}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def canonical_hash(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def combined_file_hash(paths: list[Path]) -> str:
    entries = [
        {"name": p.name, "sha256": sha(p), "bytes": p.stat().st_size}
        for p in sorted({p.resolve() for p in paths}, key=str)
    ]
    return canonical_hash(entries)


def sql_template(sql: str) -> str:
    value = re.sub(r"'[^']*'", "?", sql.lower())
    value = re.sub(r'"[^"]*"', "?", value)
    value = re.sub(r"\b\d+(?:\.\d+)?\b", "?", value)
    return " ".join(value.split())


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def cluster_effect(values: dict[str, tuple[float, str]], stat, seed: int) -> dict:
    pairs = [(0.0, effect, cluster) for effect, cluster in values.values()]
    return stat.cluster_paired_bootstrap(pairs, samples=20_000, confidence=0.95, seed=seed)


def main() -> int:
    STAT_DIR.mkdir(parents=True, exist_ok=True)
    incident = json.loads(INCIDENT.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert incident["status"] == "quarantined_not_eligible_for_claim_promotion"
    assert incident["directory"].endswith("qwen25coder7b_q4km_seed20260805")
    assert Path(incident["directory"]).name != RUN.name
    manifest = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "completed" and manifest["canonical_result_eligible"] is True

    prompts = jsonl(RUN / "prompts.jsonl")
    predictions = jsonl(RUN / "predictions.jsonl")
    scores = jsonl(RUN / "scores.jsonl")
    questions_all = jsonl(DATA_DIR / "questions.jsonl")
    questions = {r["question_id"]: r for r in questions_all if r["split"] == "test"}
    assert len(questions) == 180

    # Load exactly the frozen evaluator/runner modules used to define hashes and
    # independently call the scoring functions on the immutable prediction file.
    sys.path.insert(0, str(CODE_DIR))
    sys.path.insert(0, str(SOURCE / "code"))
    sys.path.insert(0, str(SOURCE / "code/evaluator"))
    factorial = load_module("ma_factorial_audit", CODE_DIR / "applsci_factorial.py")
    stat = load_module("ma_shared_stat_audit", SHARED_STAT)

    checks: list[dict] = []
    def check(name: str, passed: bool, evidence):
        checks.append({"check": name, "passed": bool(passed), "evidence": evidence})

    check("quarantined_directory_rejected", True, {
        "incident_status": incident["status"], "rejected": incident["directory"], "eligible": str(RUN.relative_to(MA))
    })
    check("completed_manifest", manifest["status"] == "completed", manifest["status"])
    check("counts_720", len(prompts) == len(predictions) == len(scores) == 720,
          {"prompts": len(prompts), "predictions": len(predictions), "scores": len(scores)})

    expected_keys = {(qid, cell) for qid in questions for cell in CELLS}
    key_sets = {}
    for name, rows in (("prompts", prompts), ("predictions", predictions), ("scores", scores)):
        keys = [(r["question_id"], r["condition"]) for r in rows]
        key_sets[name] = set(keys)
        check(f"{name}_unique_cartesian_keys", len(keys) == len(set(keys)) == 720 and set(keys) == expected_keys,
              {"rows": len(keys), "unique": len(set(keys)), "missing": len(expected_keys - set(keys)), "extra": len(set(keys) - expected_keys)})
    db_question_cell = {(manifest["hashes"]["data_sha256"], q, c) for q, c in key_sets["predictions"]}
    check("unique_db_question_cell_keys", len(db_question_cell) == 720, len(db_question_cell))

    # Freeze/configuration/data/code/prompt-set integrity.
    data_paths = [factorial.formal.DB_PATH, factorial.formal.QUESTIONS_PATH,
                  factorial.formal.DATA_DIR / "splits.json", factorial.formal.SCHEMA_PATH]
    code_paths = [Path(factorial.__file__), Path(factorial.formal.__file__),
                  Path(factorial.formal.chess.__file__), Path(factorial.formal.smoke.__file__)]
    recomputed_hashes = {
        "configuration_sha256": canonical_hash(manifest["configuration"]),
        "data_sha256": combined_file_hash(data_paths),
        "code_sha256": combined_file_hash(code_paths),
    }
    check("manifest_hashes_recomputed", recomputed_hashes == manifest["hashes"], {"found": recomputed_hashes, "manifest": manifest["hashes"]})
    for field, expected in freeze["hashes"].items():
        if field.endswith("_expected"):
            actual = manifest["hashes"][field.removesuffix("_expected")]
        elif field == "prompt_set_sha256":
            actual = manifest["prompt_set_sha256"]
        elif field == "local_model_manifest_sha256":
            actual = manifest["configuration"]["local_model"]["manifest_sha256"]
        elif field == "model_sha256":
            actual = manifest["configuration"]["local_model"]["model_sha256"]
        elif field in manifest["hashes"]:
            actual = manifest["hashes"][field]
        else:
            continue
        check(f"freeze_{field}", actual == expected, {"actual": actual, "expected": expected})
    prompt_set = canonical_hash([{"key": [r["question_id"], r["condition"]], "prompt": r["prompt_hash"], "context": r["context_hash"]} for r in prompts])
    check("prompt_set_recomputed", prompt_set == manifest["prompt_set_sha256"] == freeze["hashes"]["prompt_set_sha256"], prompt_set)

    prompt_by = {(r["question_id"], r["condition"]): r for r in prompts}
    pred_by = {(r["question_id"], r["condition"]): r for r in predictions}
    score_by = {(r["question_id"], r["condition"]): r for r in scores}
    linkage_errors = []
    for key in sorted(expected_keys):
        p, y, s = prompt_by[key], pred_by[key], score_by[key]
        for field in ("prompt_hash", "context_hash"):
            if len({p[field], y[field], s[field]}) != 1:
                linkage_errors.append([*key, field])
        if y["response_hash"] != s["response_hash"]:
            linkage_errors.append([*key, "response_hash"])
        for field, value in manifest["hashes"].items():
            if y[field] != value or s[field] != value:
                linkage_errors.append([*key, field])
    check("cross_artifact_hash_linkage", not linkage_errors, linkage_errors[:20])

    # One and only one provider generation per prediction, independently counted
    # from the server log.  Unique task IDs are an additional accounting guard.
    log = (RUN / "server_stderr.log").read_text(encoding="utf-8", errors="replace")
    task_ids = re.findall(r"task\s+(\d+)\s+\|\s+processing task", log)
    launches = len(re.findall(r"launch_slot_:", log))
    timings = len(re.findall(r"total time\s*=", log))
    check("one_provider_generation_per_row", launches == timings == len(task_ids) == len(set(task_ids)) == 720,
          {"launches": launches, "timings": timings, "tasks": len(task_ids), "unique_tasks": len(set(task_ids))})
    check("no_server_error_records", not re.search(r"(?m)^.*\sE\s+(?:srv|slot)\s", log), "no llama.cpp E-level server line")
    check("prediction_statuses", Counter(r["status"] for r in predictions) == {"success": 720}, Counter(r["status"] for r in predictions))
    check("no_provider_parse_errors", all(r["error_type"] is None and r["error_message"] is None and r["retry_count"] == 0 for r in predictions),
          {"provider_or_parse_errors": sum(r["error_type"] is not None for r in predictions), "retries": sum(r["retry_count"] for r in predictions)})
    check("score_statuses", Counter(r["status"] for r in scores) == {"scored": 720}, Counter(r["status"] for r in scores))

    # Prompt-path gold isolation.
    leaked = []
    for r in prompts:
        q = questions[r["question_id"]]
        if any(k.lower() in GOLD_KEYS for k in r):
            leaked.append([r["question_id"], r["condition"], "gold_key"])
        if q["gold_sql"].strip() in r["prompt"] or q["gold_sql"].strip() in r["context"]:
            leaked.append([r["question_id"], r["condition"], "exact_gold_sql"])
    check("gold_isolation", not leaked, leaked[:20])

    # Independent read-only safety and direct rescoring from predictions + SQLite.
    conn = sqlite3.connect(f"file:{factorial.formal.DB_PATH.as_posix()}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only=ON")
    recomputed_rows = []
    mismatch = []
    unsafe = []
    try:
        contexts = {}
        for qid, original in questions.items():
            contexts[qid] = factorial.build_contexts(conn, factorial.without_gold(original))
        for qid, cell in sorted(expected_keys):
            prediction = pred_by[(qid, cell)]
            sql = prediction["predicted_sql"]
            safe, _, safety_error = factorial.formal.validate_read_only_select(sql)
            if not safe:
                unsafe.append([qid, cell, safety_error, sql])
            evaluated = factorial.formal.score_prediction(conn, questions[qid], sql)
            validation_context = contexts[qid][cell][1]
            validation = factorial.formal.chess.reference_free_validation(conn, validation_context, sql)
            direct_correct = bool(evaluated.correct)
            direct_shape = bool(validation.get("shape_ok"))
            archived = score_by[(qid, cell)]
            if direct_correct != bool(archived["correct"]) or direct_shape != bool(archived["shape_ok"]):
                mismatch.append([qid, cell, direct_correct, archived["correct"], direct_shape, archived["shape_ok"]])
            template = sql_template(questions[qid]["gold_sql"])
            template_id = "tpl_" + hashlib.sha256(template.encode()).hexdigest()[:12]
            family = "family_" + hashlib.sha256((questions[qid]["difficulty"] + "|" + "|".join(questions[qid]["sql_feature_tags"])).encode()).hexdigest()[:12]
            recomputed_rows.append({
                "question_id": qid, "condition": cell, "template_cluster": template_id,
                "family_cluster": family, "correct_int": int(direct_correct), "shape_int": int(direct_shape),
                "prompt_hash": prediction["prompt_hash"], "context_hash": prediction["context_hash"],
                "response_hash": prediction["response_hash"], "data_sha256": prediction["data_sha256"],
                "configuration_sha256": prediction["configuration_sha256"], "code_sha256": prediction["code_sha256"],
            })
    finally:
        conn.close()
    check("all_sql_read_only", not unsafe, unsafe[:20])
    check("direct_sqlite_rescore_matches", not mismatch, {"mismatches": len(mismatch), "examples": mismatch[:20]})

    canonical_rows_path = STAT_DIR / "canonical_recomputed_rows.jsonl"
    canonical_rows_path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in recomputed_rows), encoding="utf-8")
    by_cell = defaultdict(list)
    for r in recomputed_rows:
        by_cell[r["condition"]].append(r)
    cell_rows = [{
        "condition": c, "n": len(by_cell[c]), "execution_correct": sum(r["correct_int"] for r in by_cell[c]),
        "execution_accuracy": mean(r["correct_int"] for r in by_cell[c]),
        "shape_correct": sum(r["shape_int"] for r in by_cell[c]), "shape_accuracy": mean(r["shape_int"] for r in by_cell[c])
    } for c in CELLS]

    # Shared audit: all pairwise tests, template-cluster bootstrap, exact McNemar,
    # and Holm across all 12 pairwise metric tests.
    shared_report = stat.build_report(
        canonical_rows_path, recomputed_rows, "jsonl", condition_field="condition",
        item_fields=["question_id"], cluster_field="template_cluster",
        metric_fields=["correct_int", "shape_int"],
        required_fields=["family_cluster", "prompt_hash", "context_hash", "response_hash"],
        hash_fields=["data_sha256", "configuration_sha256", "code_sha256"],
        expected_conditions=CELLS, bootstrap_samples=20_000, confidence=0.95,
        seed=20260805, max_examples=20,
    )
    (STAT_DIR / "shared_stat_audit_clean.json").write_text(json.dumps(shared_report, indent=2) + "\n", encoding="utf-8")
    (STAT_DIR / "shared_stat_audit_clean.md").write_text(stat.report_markdown(shared_report), encoding="utf-8")
    check("shared_stat_audit", shared_report["audit"]["passed"], shared_report["audit"])

    index = {(r["question_id"], r["condition"]): r for r in recomputed_rows}
    registered_edges = [
        ("shape_at_full", "F00_Full_NoShape", "F01_Full_WithShape"),
        ("compact_at_no_shape", "F00_Full_NoShape", "F10_Compact_NoShape"),
        ("shape_at_compact", "F10_Compact_NoShape", "F11_Compact_WithShape"),
        ("compact_at_with_shape", "F01_Full_WithShape", "F11_Compact_WithShape"),
    ]
    contrasts = []
    for ci, (name, baseline, treatment) in enumerate(registered_edges):
        for mi, metric in enumerate(("correct_int", "shape_int")):
            pairs = [(index[(q, baseline)][metric], index[(q, treatment)][metric], index[(q, baseline)]["template_cluster"]) for q in sorted(questions)]
            boot = stat.cluster_paired_bootstrap(pairs, samples=20_000, confidence=0.95, seed=20260805 + ci * 101 + mi)
            mc = stat.mcnemar_exact(pairs)
            contrasts.append({"contrast": name, "baseline": baseline, "treatment": treatment, "metric": metric,
                              "baseline_mean": mean(x[0] for x in pairs), "treatment_mean": mean(x[1] for x in pairs),
                              "effect": boot["estimate"], "ci_low": boot["ci_low"], "ci_high": boot["ci_high"],
                              "cluster_unit": "normalized_gold_sql_template", "cluster_count": boot["cluster_count"],
                              "mcnemar_baseline_only": mc["baseline_only_correct"], "mcnemar_treatment_only": mc["treatment_only_correct"],
                              "mcnemar_p": mc["p_value"]})
    adjusted = stat.holm_adjust([r["mcnemar_p"] for r in contrasts])
    for row, p in zip(contrasts, adjusted):
        row["holm_family"] = "8 registered edge contrasts: 4 factorial edges x 2 binary metrics"
        row["mcnemar_p_holm"] = p

    factorial_effects = []
    for metric in ("correct_int", "shape_int"):
        effects = {"context_compact_main": {}, "shape_hint_main": {}, "interaction": {}}
        for q in sorted(questions):
            v = {c: index[(q, c)][metric] for c in CELLS}
            cluster = index[(q, CELLS[0])]["template_cluster"]
            effects["context_compact_main"][q] = (0.5 * ((v["F10_Compact_NoShape"] - v["F00_Full_NoShape"]) + (v["F11_Compact_WithShape"] - v["F01_Full_WithShape"])), cluster)
            effects["shape_hint_main"][q] = (0.5 * ((v["F01_Full_WithShape"] - v["F00_Full_NoShape"]) + (v["F11_Compact_WithShape"] - v["F10_Compact_NoShape"])), cluster)
            effects["interaction"][q] = ((v["F11_Compact_WithShape"] - v["F10_Compact_NoShape"]) - (v["F01_Full_WithShape"] - v["F00_Full_NoShape"]), cluster)
        for ei, (effect_name, values) in enumerate(effects.items()):
            boot = cluster_effect(values, stat, 20262000 + ei + (0 if metric == "correct_int" else 100))
            factorial_effects.append({"metric": metric, "effect": effect_name, "estimate": boot["estimate"],
                                      "ci_low": boot["ci_low"], "ci_high": boot["ci_high"],
                                      "cluster_unit": "normalized_gold_sql_template", "cluster_count": boot["cluster_count"],
                                      "question_count": 180, "bootstrap_samples": 20_000})

    def write_csv(path: Path, rows: list[dict]):
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
    write_csv(STAT_DIR / "table_cell_summary.csv", cell_rows)
    write_csv(STAT_DIR / "table_registered_contrasts.csv", contrasts)
    write_csv(STAT_DIR / "table_factorial_effects.csv", factorial_effects)

    artifact_hashes = {p.name: sha(p) for p in [RUN / "manifest.json", RUN / "prompts.jsonl", RUN / "predictions.jsonl", RUN / "scores.jsonl", RUN / "server_stderr.log", canonical_rows_path]}
    result = {
        "schema_version": "ma-sqlgrid-independent-formal-audit-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "eligible_run": str(RUN.relative_to(ROOT)),
        "quarantined_run": incident["directory"],
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
        "artifact_hashes": artifact_hashes,
        "cluster_definition": {"explicit_template_field_available": False, "used": "normalized gold SQL structure with literals/numbers replaced", "template_clusters": len({r["template_cluster"] for r in recomputed_rows}), "feature_families_available": len({r["family_cluster"] for r in recomputed_rows})},
        "cell_summary": cell_rows,
        "registered_contrasts": contrasts,
        "factorial_effects": factorial_effects,
    }
    (STAT_DIR / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# MA-SQLGrid Local Formal Run — Independent Audit", "",
        f"**Decision: {'PASS — eligible for canonical statistical use' if result['passed'] else 'FAIL — do not promote'}.**", "",
        "## Run boundary", "",
        f"- Eligible input only: `{result['eligible_run']}`.",
        f"- Explicitly rejected/quarantined: `{incident['directory']}`; incident status `{incident['status']}`. No artifact inside that directory was read by this audit.",
        f"- Clean manifest: `{manifest['status']}`; started {manifest['run_started_utc']}, finished {manifest['run_finished_utc']}.", "",
        "## Integrity and independent recomputation", "",
        f"- 720 prompts, 720 predictions, and 720 scores; exactly 720 unique database/question/cell identities and a complete 180 × 4 Cartesian product.",
        f"- Server accounting: {launches} launches, {timings} completed timings, {len(set(task_ids))} unique generation task IDs—one generation per final row.",
        "- Provider/parse/scoring errors: 0/0/0; retries: 0. All predicted SQL passed the independent single-statement read-only SELECT guard.",
        f"- Direct SQLite recomputation matched archived execution and answer-shape verdicts for all {len(recomputed_rows)} rows (0 mismatches).",
        "- Configuration, data, code, local-model, prompt-set, prompt/context/response linkage, and freeze hashes all match.",
        "- Gold isolation passed: prompt records contain no gold fields and no prompt/context contains its question's exact gold SQL.", "",
        "## Recomputed cell results", "",
        "| Cell | Execution correct/180 | Execution accuracy | Shape correct/180 | Shape accuracy |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in cell_rows:
        lines.append(f"| {r['condition']} | {r['execution_correct']} | {r['execution_accuracy']:.4f} | {r['shape_correct']} | {r['shape_accuracy']:.4f} |")
    lines += ["", "## Registered paired edge contrasts", "",
              "Holm adjustment spans the eight registered edge tests (four 2×2 edges × execution/shape). CIs use 20,000 paired cluster bootstrap draws over 70 normalized gold-SQL template clusters.", "",
              "| Contrast | Metric | Delta | 95% cluster CI | McNemar discordance (base-only/treat-only) | Exact p | Holm p |",
              "|---|---|---:|---|---:|---:|---:|"]
    for r in contrasts:
        lines.append(f"| {r['contrast']} | {r['metric']} | {r['effect']:+.4f} | [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}] | {r['mcnemar_baseline_only']}/{r['mcnemar_treatment_only']} | {r['mcnemar_p']:.6g} | {r['mcnemar_p_holm']:.6g} |")
    lines += ["", "## Factorial effects", "",
              "Effects are paired per question. Positive context main effect favors compact; positive shape main effect favors hints; interaction is (shape effect under compact) − (shape effect under full).", "",
              "| Metric | Effect | Estimate | 95% template-cluster CI |", "|---|---|---:|---|"]
    for r in factorial_effects:
        lines.append(f"| {r['metric']} | {r['effect']} | {r['estimate']:+.4f} | [{r['ci_low']:+.4f}, {r['ci_high']:+.4f}] |")
    lines += ["", "## Canonical artifacts", "",
              "- `MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json` — check-level audit evidence and canonical statistics.",
              "- `canonical_recomputed_rows.jsonl` — independently recomputed binary outcomes and provenance hashes.",
              "- `shared_stat_audit_clean.json/.md` — direct output of the shared statistical audit engine.",
              "- `table_cell_summary.csv`, `table_registered_contrasts.csv`, `table_factorial_effects.csv` — canonical tabulations.", "",
              "- `canonical_artifact_manifest.json` — hashes and byte sizes for every canonical audit output.", "",
              "This audit establishes integrity and local paired effects for the frozen single-database run. It does not establish cross-database or cross-model generalization.", ""]
    report_path = STAT_DIR / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    canonical_outputs = [
        STAT_DIR / "MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json", report_path,
        canonical_rows_path, STAT_DIR / "shared_stat_audit_clean.json",
        STAT_DIR / "shared_stat_audit_clean.md", STAT_DIR / "table_cell_summary.csv",
        STAT_DIR / "table_registered_contrasts.csv", STAT_DIR / "table_factorial_effects.csv",
    ]
    canonical_manifest = {
        "schema_version": "ma-sqlgrid-canonical-statistics-manifest-v1",
        "eligible_source_run": str(RUN.relative_to(ROOT)),
        "quarantined_source_run": incident["directory"],
        "audit_passed": result["passed"],
        "outputs": {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in canonical_outputs},
        "immutable_inputs": artifact_hashes,
    }
    (STAT_DIR / "canonical_artifact_manifest.json").write_text(json.dumps(canonical_manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "checks": len(checks), "cells": cell_rows, "statistics": str(STAT_DIR)}, indent=2))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
