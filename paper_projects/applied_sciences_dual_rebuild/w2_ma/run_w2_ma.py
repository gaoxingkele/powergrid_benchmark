#!/usr/bin/env python3
"""Zero-cost W2 audit and deterministic baselines for MA-SQLGrid.

This runner never calls a model endpoint.  It emits separate artifacts for new
deterministic baselines and for rescored legacy model predictions so that the
two evidence classes cannot be accidentally pooled.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
MA_SOURCE = WORKSPACE / "paper_projects" / "2026_ma_sqlgrid_cmc" / "source"
EXPERIMENT = MA_SOURCE / "code" / "experiment_final"
SHARED = HERE.parent / "shared"
sys.path.insert(0, str(EXPERIMENT))
sys.path.insert(0, str(SHARED))

import applsci_factorial as factorial  # noqa: E402
import main as formal  # noqa: E402
import stat_audit  # noqa: E402


RUN_ID = "w2-ma-zero-cost-20260805"
ENV_NAMES = [
    "OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL",
    "DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "KRILL_API_KEY",
    "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT",
    "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
    "OLLAMA_HOST", "VLLM_API_KEY", "LM_STUDIO_API_KEY",
]
RUNTIME_COMMANDS = ["ollama", "llama-server", "llamafile", "vllm", "docker", "podman"]
PROCESS_MARKERS = ("ollama", "llama", "lm studio", "lmstudio", "vllm", "text-generation", "kobold")


DATASETS = [
    {
        "dataset_id": "griddb-maintenance-v2-v0.1",
        "path": MA_SOURCE / "data" / "griddb_maintenance_v2_v0_1",
        "origin": "project-authored synthetic SQLite benchmark",
        "source_url": None,
        "license": "not declared in dataset directory",
        "license_status": "BLOCKER_missing_explicit_license",
        "scientific_role": "primary in-domain Text-to-SQL benchmark",
        "sql_benchmark_readiness": "ready_existing_200_questions_180_test",
        "provenance_evidence": ["annotation_protocol.md", "verification_log.md", "splits.json"],
    },
    {
        "dataset_id": "griddb-maintenance-v2-x10",
        "path": MA_SOURCE / "data" / "griddb_maintenance_v2_x10",
        "origin": "deterministic project-authored expansion of GridDB-Maintenance-v2",
        "source_url": None,
        "license": "inherits unresolved parent status",
        "license_status": "BLOCKER_parent_license_unresolved",
        "scientific_role": "scale and distractor robustness only",
        "sql_benchmark_readiness": "ready_existing_queries_but_factorial_symmetry_must_be_enforced",
        "provenance_evidence": ["expansion_manifest.json", "annotation_protocol.md", "splits.json"],
    },
    {
        "dataset_id": "rts-gmlc",
        "path": WORKSPACE / "data" / "public_datasets" / "production_cost" / "rts-gmlc",
        "origin": "GridMod/RTS-GMLC GitHub clone",
        "source_url": "https://github.com/GridMod/RTS-GMLC.git",
        "license": "NREL/DOE data-use disclaimer in README.md",
        "license_status": "present_review_notice_before_redistribution",
        "scientific_role": "external transmission/operations database candidate",
        "sql_benchmark_readiness": "source_present_requires_SQL_ETL_questions_and_sealed_split",
        "provenance_evidence": ["README.md", "RTS_Data/README.md"],
    },
    {
        "dataset_id": "simbench",
        "path": WORKSPACE / "data" / "public_datasets" / "grid_cases" / "simbench",
        "origin": "e2nIEE/simbench GitHub clone",
        "source_url": "https://github.com/e2nIEE/simbench.git",
        "license": "ODbL data / BSD-3-Clause code",
        "license_status": "present_attribution_and_share_alike_review_required",
        "scientific_role": "external distribution asset/topology database candidate",
        "sql_benchmark_readiness": "source_present_requires_SQL_ETL_questions_and_sealed_split",
        "provenance_evidence": ["README.rst", "LICENSE", "doc/about/license.rst"],
    },
    {
        "dataset_id": "matpower-cases",
        "path": WORKSPACE / "data" / "public_datasets" / "grid_cases" / "matpower",
        "origin": "MATPOWER/matpower sparse GitHub clone",
        "source_url": "https://github.com/MATPOWER/matpower.git",
        "license": "MATPOWER license file",
        "license_status": "present_review_before_redistribution",
        "scientific_role": "auxiliary standard-grid schema diversity",
        "sql_benchmark_readiness": "case_files_present_requires_parser_SQL_ETL_and_questions",
        "provenance_evidence": ["README.md", "LICENSE", "CITATION"],
    },
    {
        "dataset_id": "pandapower-networks",
        "path": WORKSPACE / "data" / "public_datasets" / "grid_cases" / "pandapower",
        "origin": "e2nIEE/pandapower sparse GitHub clone",
        "source_url": "https://github.com/e2nIEE/pandapower.git",
        "license": "BSD-3-Clause",
        "license_status": "present",
        "scientific_role": "auxiliary network-schema diversity",
        "sql_benchmark_readiness": "network_files_present_requires_SQL_ETL_and_questions",
        "provenance_evidence": ["README.rst", "LICENSE", "CITATION.bib"],
    },
    {
        "dataset_id": "gridstage",
        "path": WORKSPACE / "data" / "public_datasets" / "equipment_fault_pmu" / "gridstage",
        "origin": "PNNL/GridSTAGE GitHub clone",
        "source_url": "https://github.com/pnnl/GridSTAGE.git",
        "license": "license file present",
        "license_status": "present_review_before_redistribution",
        "scientific_role": "optional fault/PMU extension; lower Text-to-SQL priority",
        "sql_benchmark_readiness": "source_present_but_MATLAB_dependent_and_requires_SQL_ETL",
        "provenance_evidence": ["README.md", "LICENSE"],
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    return sha256_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values: Iterable[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values), encoding="utf-8")


def relative(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def git_commit(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", value) else None


def endpoint_audit() -> dict[str, Any]:
    processes: set[str] = set()
    if os.name == "nt":
        completed = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=False,
        )
        for line in completed.stdout.splitlines():
            name = line.split(",", 1)[0].strip('"').lower()
            if any(marker in name for marker in PROCESS_MARKERS):
                processes.add(name)
    return {
        "generated_at_utc": now_utc(),
        "zero_secret_policy": "Only boolean presence/non-empty status is recorded; values are never read into this artifact.",
        "environment": [
            {"name": name, "present": name in os.environ, "non_empty": bool(os.environ.get(name))}
            for name in ENV_NAMES
        ],
        "runtime_commands": [{"name": name, "available": shutil.which(name) is not None} for name in RUNTIME_COMMANDS],
        "matching_local_model_process_present": bool(processes),
        "matching_local_model_process_count": len(processes),
        "usable_configured_cloud_endpoint_present": bool(
            os.environ.get("OPENAI_API_KEY") and os.environ.get("OPENAI_BASE_URL") and os.environ.get("OPENAI_MODEL")
        ),
        "local_runtime_detected": bool(processes) or any(shutil.which(name) for name in RUNTIME_COMMANDS[:4]),
        "network_probe_performed": False,
        "paid_call_performed": False,
    }


def visible_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    ) if root.exists() else []


def sqlite_profile(path: Path) -> dict[str, Any] | None:
    database = path / "database.sqlite"
    questions = path / "questions.jsonl"
    if not database.exists() or not questions.exists():
        return None
    records = [json.loads(line) for line in questions.read_text(encoding="utf-8").splitlines() if line.strip()]
    conn = sqlite3.connect(database)
    try:
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )]
        table_rows = {table: conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0] for table in tables}
    finally:
        conn.close()
    return {
        "table_count": len(tables),
        "table_rows": table_rows,
        "question_count": len(records),
        "split_counts": dict(sorted(Counter(record["split"] for record in records).items())),
        "difficulty_counts": dict(sorted(Counter(record["difficulty"] for record in records).items())),
        "question_id_set_sha256": canonical_hash(sorted(record["question_id"] for record in records)),
    }


def dataset_inventory() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    datasets = []
    file_rows = []
    for specification in DATASETS:
        root = specification["path"]
        files = visible_files(root)
        extension_counts = Counter((path.suffix.lower() or "<none>") for path in files)
        per_dataset_rows = []
        for path in files:
            row = {
                "dataset_id": specification["dataset_id"],
                "relative_path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            per_dataset_rows.append(row)
            file_rows.append(row)
        evidence = []
        for name in specification["provenance_evidence"]:
            evidence_path = root / name
            evidence.append({
                "relative_path": name,
                "present": evidence_path.exists(),
                "sha256": sha256_file(evidence_path) if evidence_path.exists() else None,
            })
        datasets.append({
            **{key: value for key, value in specification.items() if key not in {"path", "provenance_evidence"}},
            "local_path": relative(root),
            "present": root.exists(),
            "file_count": len(files),
            "total_bytes": sum(path.stat().st_size for path in files),
            "extension_counts": dict(sorted(extension_counts.items())),
            "file_manifest_sha256": canonical_hash(per_dataset_rows),
            "git_commit": git_commit(root),
            "provenance_evidence": evidence,
            "sqlite_profile": sqlite_profile(root),
        })
    return {
        "schema_version": "w2-ma-dataset-inventory-v1",
        "generated_at_utc": now_utc(),
        "scope": "local datasets relevant to MA-SQLGrid maintenance, topology, operations, and external-schema evaluation",
        "dataset_count": len(datasets),
        "datasets": datasets,
        "priority_order": ["griddb-maintenance-v2-v0.1", "rts-gmlc", "simbench", "griddb-maintenance-v2-x10"],
        "important_limit": "Presence is not benchmark readiness; RTS-GMLC and SimBench still require frozen ETL, questions, annotation, and sealed splits.",
    }, file_rows


TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def char_ngrams(text: str, size: int = 3) -> Counter[str]:
    normalized = " " + re.sub(r"\s+", " ", text.lower()).strip() + " "
    return Counter(normalized[index:index + size] for index in range(max(0, len(normalized) - size + 1)))


def cosine(left: Counter[str], right: Counter[str]) -> float:
    dot = sum(value * right.get(key, 0) for key, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def nearest_dev(record: dict[str, Any], dev: list[dict[str, Any]]) -> tuple[dict[str, Any], float]:
    target_chars = char_ngrams(record["question"])
    target_words = tokens(record["question"])
    ranked = []
    for candidate in dev:
        chars = cosine(target_chars, char_ngrams(candidate["question"]))
        words = len(target_words & tokens(candidate["question"])) / max(1, len(target_words | tokens(candidate["question"])))
        ranked.append((0.75 * chars + 0.25 * words, candidate["question_id"], candidate))
    score, _, winner = max(ranked, key=lambda item: (item[0], item[1]))
    return winner, score


def database_lexicons(conn: sqlite3.Connection) -> dict[str, list[str]]:
    columns = {
        "asset_name": ("assets", "asset_name"), "status": ("assets", "status"),
        "type_name": ("asset_types", "type_name"), "voltage_class": ("asset_types", "voltage_class"),
        "manufacturer": ("asset_types", "manufacturer"), "location_name": ("locations", "location_name"),
        "region": ("locations", "region"), "criticality": ("locations", "criticality"),
        "technician_name": ("technicians", "technician_name"), "specialty": ("technicians", "specialty"),
        "priority": ("work_orders", "priority"), "work_status": ("work_orders", "status"),
        "fault_code": ("work_orders", "fault_code"), "sensor_type": ("sensor_readings", "sensor_type"),
        "unit": ("sensor_readings", "unit"), "connection_type": ("grid_topology", "connection_type"),
        "switch_status": ("grid_topology", "switch_status"), "action_type": ("maintenance_logs", "action_type"),
        "notes": ("maintenance_logs", "notes"),
    }
    result = {}
    for category, (table, column) in columns.items():
        result[category] = [str(row[0]) for row in conn.execute(
            f'SELECT DISTINCT "{column}" FROM "{table}" WHERE "{column}" IS NOT NULL'
        )]
    return result


def mentioned(question: str, values: list[str]) -> list[str]:
    lowered = question.lower()
    return sorted((value for value in values if value.lower().replace("_", " ") in lowered.replace("_", " ")), key=len, reverse=True)


def transfer_literals(sql: str, source_question: str, target_question: str, lexicons: dict[str, list[str]]) -> str:
    transferred = sql
    for values in lexicons.values():
        source = mentioned(source_question, values)
        target = mentioned(target_question, values)
        if len(source) == 1 and len(target) == 1 and source[0].lower() != target[0].lower():
            transferred = re.sub(re.escape("'" + source[0] + "'"), "'" + target[0].replace("'", "''") + "'", transferred, flags=re.IGNORECASE)
    source_years = re.findall(r"\b(?:19|20)\d{2}\b", source_question)
    target_years = re.findall(r"\b(?:19|20)\d{2}\b", target_question)
    if len(source_years) == len(target_years) == 1 and source_years[0] != target_years[0]:
        transferred = transferred.replace(source_years[0], target_years[0])
    return transferred


def evaluate_sql(conn: sqlite3.Connection, record: dict[str, Any], sql: str) -> dict[str, Any]:
    safe, _, _ = formal.validate_read_only_select(sql)
    execution = formal.execute_sql(conn, sql)
    scored = formal.score_prediction(conn, record, sql)
    expected = int(record["answer_shape"]["column_count"])
    return {
        "strict_execution_correct": int(scored.correct),
        "projection_contract_correct": int(execution.ok and len(execution.columns) == expected),
        "sql_executable": int(execution.ok),
        "safe_sql": int(safe),
        "error_type": scored.error_type,
        "predicted_column_count": len(execution.columns) if execution.ok else None,
        "expected_column_count": expected,
    }


def new_deterministic_baselines() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records = formal.load_questions(formal.QUESTIONS_PATH)
    dev = [record for record in records if record["split"] == "dev"]
    test = [record for record in records if record["split"] == "test"]
    data_hash = factorial.combined_file_hash([formal.DB_PATH, formal.QUESTIONS_PATH, formal.DATA_DIR / "splits.json", formal.SCHEMA_PATH])
    code_hash = sha256_file(Path(__file__))
    rows = []
    conn = sqlite3.connect(formal.DB_PATH)
    try:
        lexicons = database_lexicons(conn)
        for record in test:
            neighbor, similarity = nearest_dev(record, dev)
            candidates = {
                "DEV_1NN_SQL_COPY": neighbor["gold_sql"],
                "DEV_1NN_LITERAL_TRANSFER": transfer_literals(
                    neighbor["gold_sql"], neighbor["question"], record["question"], lexicons
                ),
            }
            for condition, sql in candidates.items():
                rows.append({
                    "evidence_origin": "NEW_zero_cost_deterministic_baseline",
                    "claim_status": "diagnostic_nonconfirmatory_existing_test_was_previously_inspected",
                    "run_id": RUN_ID,
                    "condition": condition,
                    "question_id": record["question_id"],
                    "cluster_id": record["question_id"],
                    "database_id": "griddb-maintenance-v2-v0.1",
                    "model": "none_non_llm",
                    "seed": 0,
                    "predicted_sql": sql,
                    "retrieved_dev_question_id": neighbor["question_id"],
                    "retrieval_similarity": round(similarity, 12),
                    "question_hash": sha256_text(record["question"]),
                    "data_hash": data_hash,
                    "code_hash": code_hash,
                    **evaluate_sql(conn, record, sql),
                })
    finally:
        conn.close()
    summary = {}
    for condition in sorted({row["condition"] for row in rows}):
        selected = [row for row in rows if row["condition"] == condition]
        summary[condition] = {
            "n": len(selected),
            "strict_execution_accuracy": sum(row["strict_execution_correct"] for row in selected) / len(selected),
            "projection_contract_accuracy": sum(row["projection_contract_correct"] for row in selected) / len(selected),
            "sql_executable_rate": sum(row["sql_executable"] for row in selected) / len(selected),
            "safe_sql_rate": sum(row["safe_sql"] for row in selected) / len(selected),
            "error_types": dict(sorted(Counter(row["error_type"] for row in selected).items())),
        }
    return rows, {
        "schema_version": "w2-ma-deterministic-baseline-v1",
        "generated_at_utc": now_utc(),
        "run_id": RUN_ID,
        "evidence_origin": "NEW_zero_cost_deterministic_baseline",
        "paid_calls": 0,
        "test_gold_used_for_generation": False,
        "development_source": "20 dev questions and their SQL only",
        "methods": {
            "DEV_1NN_SQL_COPY": "weighted char-trigram/word-set 1NN; copy dev SQL",
            "DEV_1NN_LITERAL_TRANSFER": "same 1NN plus deterministic DB-lexicon literal/year transfer",
        },
        "interpretation_limit": "Diagnostic lower bounds only. The existing test set has previously been inspected; do not present these new results as sealed confirmatory evidence.",
        "summary": summary,
        "row_count": len(rows),
        "data_hash": data_hash,
        "code_hash": code_hash,
    }


def audit_rows(
    path: Path, rows: list[dict[str, Any]], *, conditions: list[str], metrics: list[str],
    required: list[str], hashes: list[str], prefix: str,
) -> dict[str, Any]:
    write_jsonl(path, rows)
    report = stat_audit.build_report(
        path, rows, "jsonl", condition_field="condition", item_fields=["question_id"],
        cluster_field="cluster_id", metric_fields=metrics, required_fields=required,
        hash_fields=hashes, expected_conditions=conditions, bootstrap_samples=2000,
        confidence=0.95, seed=20260805, max_examples=20,
    )
    write_json(HERE / f"{prefix}_stat_audit.json", report)
    (HERE / f"{prefix}_stat_audit.md").write_text(stat_audit.report_markdown(report), encoding="utf-8")
    return report


def legacy_sources() -> list[dict[str, Any]]:
    base = EXPERIMENT
    return [
        {"run_id": "legacy-gpt54mini-v01", "dataset": "v0.1", "path": base / "outputs" / "predictions.jsonl"},
        {"run_id": "legacy-deepseek-v01", "dataset": "v0.1", "path": base / "outputs_deepseek_chat" / "predictions.jsonl"},
        {"run_id": "legacy-deepseek-x10", "dataset": "x10", "path": base / "outputs_deepseek_x10" / "predictions.jsonl"},
    ]


def rescore_legacy() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    roots = {
        "v0.1": MA_SOURCE / "data" / "griddb_maintenance_v2_v0_1",
        "x10": MA_SOURCE / "data" / "griddb_maintenance_v2_x10",
    }
    all_rows = []
    runs = []
    for source in legacy_sources():
        path = source["path"]
        if not path.exists():
            runs.append({**source, "path": relative(path), "present": False})
            continue
        root = roots[source["dataset"]]
        records = {
            record["question_id"]: record
            for record in (json.loads(line) for line in (root / "questions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
        }
        predictions = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        conn = sqlite3.connect(root / "database.sqlite")
        run_rows = []
        try:
            for prediction in predictions:
                record = records.get(prediction.get("question_id"))
                sql = prediction.get("predicted_sql")
                if record is None or not isinstance(sql, str) or not sql.strip():
                    evaluated = {
                        "strict_execution_correct": 0, "projection_contract_correct": 0,
                        "sql_executable": 0, "safe_sql": 0,
                        "error_type": "missing_record_or_prediction", "predicted_column_count": None,
                        "expected_column_count": record["answer_shape"]["column_count"] if record else None,
                    }
                else:
                    evaluated = evaluate_sql(conn, record, sql)
                row = {
                    "evidence_origin": "LEGACY_model_prediction_rescored_no_new_inference",
                    "claim_status": "legacy_nonconfirmatory_not_factorial_2x2",
                    "rescore_run_id": RUN_ID,
                    "legacy_run_id": source["run_id"],
                    "legacy_dataset": source["dataset"],
                    "legacy_source_sha256": sha256_file(path),
                    "legacy_row_index": len(run_rows),
                    "question_id": prediction.get("question_id"),
                    "condition": prediction.get("condition"),
                    "seed": prediction.get("seed"),
                    "provider": prediction.get("provider"),
                    "model": prediction.get("model"),
                    "predicted_sql": sql,
                    **evaluated,
                }
                run_rows.append(row)
                all_rows.append(row)
        finally:
            conn.close()
        groups = {}
        for condition in sorted({row["condition"] for row in run_rows}):
            selected = [row for row in run_rows if row["condition"] == condition]
            groups[condition] = {
                "n": len(selected),
                "strict_execution_accuracy_current_evaluator": sum(row["strict_execution_correct"] for row in selected) / len(selected),
                "projection_contract_accuracy_current_evaluator": sum(row["projection_contract_correct"] for row in selected) / len(selected),
                "executable_rate_current_evaluator": sum(row["sql_executable"] for row in selected) / len(selected),
                "error_types": dict(sorted(Counter(row["error_type"] for row in selected).items())),
            }
        runs.append({
            "legacy_run_id": source["run_id"], "dataset": source["dataset"],
            "path": relative(path), "present": True, "source_sha256": sha256_file(path),
            "prediction_count": len(run_rows), "summary": groups,
        })
    return all_rows, {
        "schema_version": "w2-ma-legacy-rescore-v1",
        "generated_at_utc": now_utc(),
        "evidence_origin": "LEGACY_model_prediction_rescored_no_new_inference",
        "paid_calls": 0,
        "separation_policy": "Never pool these rows with NEW deterministic baselines or the pending 2x2 factorial.",
        "evaluator_code": relative(MA_SOURCE / "code" / "evaluator" / "evaluator.py"),
        "evaluator_sha256": sha256_file(MA_SOURCE / "code" / "evaluator" / "evaluator.py"),
        "runs": runs,
        "rescored_row_count": len(all_rows),
    }


def factorial_design_audit() -> tuple[dict[str, Any], dict[str, Any]]:
    out = HERE / "factorial_dry_run"
    factorial.run(["--out", str(out), "--overwrite"])
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    prompt_rows = [json.loads(line) for line in (out / "prompts.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    records = {record["question_id"]: record for record in formal.load_split_records("formal")}
    audit_rows_data = []
    for row in prompt_rows:
        record = records[row["question_id"]]
        audit_rows_data.append({
            "run_id": RUN_ID,
            "condition": row["condition"],
            "question_id": row["question_id"],
            "cluster_id": row["question_id"],
            "database_id": "griddb-maintenance-v2-v0.1",
            "registered_cell": 1,
            "prompt_hash": row["prompt_hash"],
            "context_hash": row["context_hash"],
            "question_hash": sha256_text(record["question"]),
            "data_hash": manifest["hashes"]["data_sha256"],
            "code_hash": manifest["hashes"]["code_sha256"],
        })
    report = audit_rows(
        HERE / "factorial_design_matrix.jsonl", audit_rows_data,
        conditions=factorial.CELL_NAMES, metrics=["registered_cell"],
        required=["run_id", "database_id", "prompt_hash", "context_hash"],
        hashes=["question_hash", "data_hash", "code_hash"], prefix="factorial_design",
    )
    verification = {
        "schema_version": "w2-ma-factorial-dry-run-verification-v1",
        "generated_at_utc": now_utc(),
        "paid_calls": 0,
        "manifest_status": manifest["status"],
        "question_count": manifest["question_count"],
        "prompt_count": manifest["prompt_count"],
        "prompt_counts_by_cell": manifest["prompt_counts_by_cell"],
        "is_full_registered_run": manifest["is_full_registered_run"],
        "prompt_set_sha256": manifest["prompt_set_sha256"],
        "shared_stat_audit_passed": report["audit"]["passed"],
        "shared_stat_audit_rows": report["audit"]["row_count"],
        "shared_stat_audit_cartesian": {
            "observed": report["audit"]["observed_unique_cells"],
            "expected": report["audit"]["expected_cartesian_cells"],
        },
    }
    return verification, report


def build_markdown(
    runtime: dict[str, Any], inventory: dict[str, Any], baseline: dict[str, Any],
    legacy: dict[str, Any], factorial_verification: dict[str, Any], baseline_audit: dict[str, Any],
) -> str:
    env_present = sum(item["non_empty"] for item in runtime["environment"])
    commands_present = sum(item["available"] for item in runtime["runtime_commands"])
    lines = [
        "# W2 MA-SQLGrid Zero-Cost Audit",
        "",
        "## Outcome",
        "",
        f"- Configured model environment variables (non-empty): **{env_present}** of {len(runtime['environment'])} audited names.",
        f"- Local model/runtime commands available: **{commands_present}** of {len(runtime['runtime_commands'])}; matching process present: **{runtime['matching_local_model_process_present']}**.",
        "- Network probes and paid model calls: **0**.",
        f"- Dataset entries inventoried: **{inventory['dataset_count']}**.",
        f"- New deterministic result rows: **{baseline['row_count']}**; paired artifact audit: **{'PASS' if baseline_audit['audit']['passed'] else 'FAIL'}**.",
        f"- Legacy prediction rows rescored without inference: **{legacy['rescored_row_count']}**.",
        f"- Factorial dry-run: **{factorial_verification['prompt_count']}** cells; shared statistical audit: **{'PASS' if factorial_verification['shared_stat_audit_passed'] else 'FAIL'}**.",
        "",
        "## New deterministic baselines",
        "",
        "These are explicitly diagnostic, non-confirmatory lower bounds. Generation uses only the 20-question development partition and database lexicons; test gold SQL is used only after prediction for scoring.",
        "",
        "| Method | N | Strict execution | Projection contract | Executable | Safe |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in baseline["summary"].items():
        lines.append(
            f"| `{name}` | {metrics['n']} | {metrics['strict_execution_accuracy']:.4f} | "
            f"{metrics['projection_contract_accuracy']:.4f} | {metrics['sql_executable_rate']:.4f} | {metrics['safe_sql_rate']:.4f} |"
        )
    lines.extend([
        "", "## Dataset readiness", "",
        "| Dataset | Present | Files | Size (MB) | Intended role | SQL benchmark readiness | License status |",
        "|---|---|---:|---:|---|---|---|",
    ])
    for dataset in inventory["datasets"]:
        lines.append(
            f"| `{dataset['dataset_id']}` | {dataset['present']} | {dataset['file_count']} | "
            f"{dataset['total_bytes'] / 1024 / 1024:.1f} | {dataset['scientific_role']} | "
            f"{dataset['sql_benchmark_readiness']} | {dataset['license_status']} |"
        )
    lines.extend([
        "", "## Evidence separation", "",
        "- `new_deterministic_*` contains newly generated zero-cost predictions.",
        "- `legacy_rescored_*` contains old model outputs evaluated by the current evaluator; no new inference occurred.",
        "- `factorial_*` proves design completeness only and contains no model predictions or accuracy claims.",
        "- None of these artifacts changes manuscript values. The confirmatory 2×2 execution remains pending an explicitly supplied endpoint/model/key.",
        "", "## Blocking items carried forward", "",
        "1. No usable configured endpoint or local model runtime was found in this process environment.",
        "2. GridDB-Maintenance-v2 lacks an explicit dataset license in its local dataset directory.",
        "3. RTS-GMLC and SimBench are source datasets, not yet frozen SQL/NL-to-SQL benchmarks.",
        "4. Existing GridDB test questions have already been inspected; a new sealed external split is required for confirmatory claims.",
        "",
    ])
    # Normalize the multiplication marker to portable ASCII in generated reports.
    return re.sub(r"confirmatory 2.*?2 execution", "confirmatory 2x2 execution", "\n".join(lines))


def main() -> int:
    HERE.mkdir(parents=True, exist_ok=True)
    runtime = endpoint_audit()
    write_json(HERE / "model_endpoint_inventory.json", runtime)

    inventory, files = dataset_inventory()
    write_json(HERE / "dataset_inventory.json", inventory)
    write_jsonl(HERE / "dataset_file_manifest.jsonl", files)

    baseline_rows, baseline_manifest = new_deterministic_baselines()
    write_json(HERE / "new_deterministic_manifest.json", baseline_manifest)
    baseline_audit = audit_rows(
        HERE / "new_deterministic_predictions_scores.jsonl", baseline_rows,
        conditions=["DEV_1NN_SQL_COPY", "DEV_1NN_LITERAL_TRANSFER"],
        metrics=["strict_execution_correct", "projection_contract_correct", "sql_executable", "safe_sql"],
        required=["run_id", "database_id", "model", "seed", "predicted_sql"],
        hashes=["question_hash", "data_hash", "code_hash"], prefix="new_deterministic",
    )

    legacy_rows, legacy_manifest = rescore_legacy()
    write_jsonl(HERE / "legacy_rescored_rows.jsonl", legacy_rows)
    write_json(HERE / "legacy_rescore_summary.json", legacy_manifest)

    factorial_verification, _ = factorial_design_audit()
    write_json(HERE / "factorial_verification.json", factorial_verification)

    report = build_markdown(runtime, inventory, baseline_manifest, legacy_manifest, factorial_verification, baseline_audit)
    (HERE / "W2_REPORT.md").write_text(report, encoding="utf-8")
    completion = {
        "generated_at_utc": now_utc(),
        "paid_calls": 0,
        "network_probes": 0,
        "new_baseline_audit_passed": baseline_audit["audit"]["passed"],
        "factorial_audit_passed": factorial_verification["shared_stat_audit_passed"],
        "factorial_cells": factorial_verification["prompt_count"],
        "inventory_dataset_count": inventory["dataset_count"],
        "legacy_and_new_separated": True,
    }
    write_json(HERE / "completion.json", completion)
    print(json.dumps(completion, indent=2))
    return 0 if all([
        completion["paid_calls"] == 0,
        completion["new_baseline_audit_passed"],
        completion["factorial_audit_passed"],
        completion["factorial_cells"] == 720,
        completion["legacy_and_new_separated"],
    ]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
