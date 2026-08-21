#!/usr/bin/env python3
"""Build the zero-cost MA-SQLGrid external-database factorial dry run.

The protocol consumes the accepted RTS-GMLC and SimBench development pilots.
Their natural-language/SQL pairs remain AUTO_CANDIDATE, non-human, and
non-sealed.  This module performs no network or model calls.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
MA_DATA = WORKSPACE / "paper_projects" / "applied_sciences_dual_rebuild" / "MA_SQLGrid" / "data"
RTS = MA_DATA / "rts_gmlc_pilot"
SIMBENCH = MA_DATA / "simbench_pilot"
SHARED = WORKSPACE / "paper_projects" / "applied_sciences_dual_rebuild" / "shared"
sys.path.insert(0, str(SHARED))
import stat_audit  # noqa: E402


OUTPUT = ROOT / "artifacts"
RUN_ID = "w4-ma-external-factorial-dryrun-v1"
CELLS = [
    ("F00_Full_NoShape", "full", False),
    ("F01_Full_WithShape", "full", True),
    ("F10_Compact_NoShape", "compact", False),
    ("F11_Compact_WithShape", "compact", True),
]

DATASETS = {
    "RTS_GMLC_AUTO_PILOT": {
        "database": RTS / "artifacts" / "database.sqlite",
        "schema": RTS / "artifacts" / "schema.sql",
        "questions": RTS / "artifacts" / "questions_auto_candidate.jsonl",
        "source_manifest": RTS / "artifacts" / "source_manifest.json",
        "expected_questions": 55,
        "license_status": "NREL data-use notice retained; upstream pinned notice is truncated and requires redistribution review",
    },
    "SIMBENCH_AUTO_PILOT": {
        "database": SIMBENCH / "simbench_mv_urban.sqlite",
        "schema": SIMBENCH / "schema.sql",
        "questions": SIMBENCH / "questions_auto_candidate.csv",
        "source_manifest": SIMBENCH / "source_manifest.json",
        "expected_questions": 36,
        "license_status": "ODbL/DbCL derived-database obligations require redistribution review",
    },
}

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|attach|detach|pragma|vacuum|replace\s+into|reindex)\b",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def canonical_hash(value: Any) -> str:
    return sha256_text(canonical_json(value))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def load_questions(dataset_id: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    path = config["questions"]
    records = []
    if path.suffix == ".jsonl":
        source_rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for row in source_rows:
            records.append({
                "dataset_id": dataset_id,
                "question_id": row["question_id"],
                "question": row["question"],
                "registered_reference_sql": row["gold_sql"],
                "template_family": row["template_family"],
                "source_split": row["split"],
                "annotation_status": row["annotation_status"],
                "human_reviewed": bool(row["human_reviewed"]),
                "sealed": bool(row["sealed"]),
            })
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                records.append({
                    "dataset_id": dataset_id,
                    "question_id": row["question_id"],
                    "question": row["natural_language"],
                    "registered_reference_sql": row["gold_sql"],
                    "template_family": row["template_family_id"],
                    "source_split": row["split"],
                    "annotation_status": row["provenance_label"],
                    "human_reviewed": as_bool(row["human_gold"]),
                    "sealed": as_bool(row["sealed"]),
                })
    if len(records) != config["expected_questions"]:
        raise RuntimeError(f"{dataset_id}: expected {config['expected_questions']} questions, found {len(records)}")
    for row in records:
        if row["annotation_status"] != "AUTO_CANDIDATE" or row["human_reviewed"] or row["sealed"]:
            raise RuntimeError(f"{dataset_id}/{row['question_id']} is not an unsealed AUTO_CANDIDATE")
    return records


def connect_read_only(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only = ON")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def schema_catalog(conn: sqlite3.Connection) -> dict[str, dict[str, Any]]:
    result = {}
    tables = [row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )]
    for table in tables:
        columns = [
            {
                "name": row[1], "type": row[2] or "ANY", "not_null": bool(row[3]),
                "primary_key": bool(row[5]),
            }
            for row in conn.execute(f'PRAGMA table_info("{table}")')
        ]
        foreign_keys = [
            {"from": row[3], "to_table": row[2], "to_column": row[4]}
            for row in conn.execute(f'PRAGMA foreign_key_list("{table}")')
        ]
        result[table] = {
            "columns": columns,
            "foreign_keys": foreign_keys,
            "row_count": conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0],
        }
    return result


def tokens(value: str) -> set[str]:
    raw = {token.lower() for token in TOKEN_RE.findall(value.replace("_", " "))}
    expanded = set(raw)
    for token in raw:
        if token.endswith("ies") and len(token) > 3:
            expanded.add(token[:-3] + "y")
        if token.endswith("s") and len(token) > 3:
            expanded.add(token[:-1])
    return expanded


CONCEPT_TOKENS = {
    "dispatch_da": {"dispatch", "produced", "generation", "committed", "output", "solution"},
    "load_timeseries_da": {"load", "regional", "region"},
    "renewable_availability_da": {"renewable", "wind", "solar", "pv", "available", "availability"},
    "reserve_requirements_da": {"reserve", "requirement", "spinning"},
    "generator_constraints": {"constraint", "capacity", "maximum", "minimum", "ramp", "up", "down"},
    "generator_costs": {"cost", "fuel", "heat", "price", "start"},
    "buses": {"bus", "buses", "node", "voltage"},
    "lines": {"line", "lines", "branch", "topology", "connected"},
    "branches": {"line", "branch", "topology", "connected", "rating"},
    "transformers": {"transformer", "transformers", "tap"},
    "generators": {"generator", "generators", "fuel", "renewable"},
    "loads": {"load", "loads", "asset"},
    "switches": {"switch", "switches", "closed", "open", "topology"},
}


def table_scores(question: str, catalog: dict[str, dict[str, Any]]) -> dict[str, int]:
    question_tokens = tokens(question)
    scores = {}
    for table, metadata in catalog.items():
        schema_tokens = tokens(table)
        for column in metadata["columns"]:
            schema_tokens.update(tokens(column["name"]))
        score = 3 * len(question_tokens & tokens(table)) + len(question_tokens & schema_tokens)
        score += 2 * len(question_tokens & CONCEPT_TOKENS.get(table, set()))
        scores[table] = score
    return scores


def compact_tables(question: str, catalog: dict[str, dict[str, Any]], limit: int = 3) -> list[str]:
    scores = table_scores(question, catalog)
    ordered = sorted(catalog, key=lambda table: (-scores[table], table))
    selected = ordered[:limit]
    # Prefer a direct FK neighbor when it can replace a zero-score tail table.
    if selected and scores[selected[-1]] == 0:
        neighbors = sorted({
            foreign_key["to_table"]
            for table in selected
            for foreign_key in catalog[table]["foreign_keys"]
            if foreign_key["to_table"] not in selected
        })
        if neighbors:
            selected[-1] = neighbors[0]
    return sorted(set(selected), key=lambda table: (-scores.get(table, 0), table))


def render_schema(catalog: dict[str, dict[str, Any]], tables: list[str]) -> str:
    blocks = []
    for table in tables:
        metadata = catalog[table]
        columns = []
        for column in metadata["columns"]:
            qualifiers = []
            if column["primary_key"]:
                qualifiers.append("PK")
            if column["not_null"]:
                qualifiers.append("NOT NULL")
            suffix = f" [{' '.join(qualifiers)}]" if qualifiers else ""
            columns.append(f"  {column['name']} {column['type']}{suffix}")
        foreign_keys = [
            f"  FK {item['from']} -> {item['to_table']}.{item['to_column']}"
            for item in metadata["foreign_keys"]
        ]
        blocks.append(
            f"TABLE {table} (rows={metadata['row_count']})\n" + "\n".join(columns + foreign_keys)
        )
    return "\n\n".join(blocks)


def infer_question_shape(question: str) -> dict[str, Any]:
    """Infer a coarse projection count from NL only; never consult reference metadata."""
    text = re.sub(r"\s+", " ", question.lower()).strip()
    rules = [
        (r"^how many\b", 1, "how_many"),
        (r"^what (?:was|is) the (?:average|maximum|minimum|total) .+ (?:for each|by)\b", 2, "grouped_scalar"),
        (r"\bsummarize .+ by\b", 2, "grouped_summary"),
        (r"identifiers? and unit types", 2, "explicit_two_fields"),
        (r"with their bus names and fuels", 3, "explicit_three_fields"),
        (r"with bus names and base voltage", 3, "explicit_three_fields"),
        (r"require at least .+ minimum up time", 3, "entity_type_value"),
        (r"top \d+ generators by maximum", 3, "ranked_entity_attribute"),
        (r"produced positive output", 2, "entity_value"),
        (r"renewable generators .+ including their fuel", 3, "entity_label_value"),
        (r"top \d+ generators by non-fuel start cost", 3, "entity_label_value"),
    ]
    for pattern, count, rule in rules:
        if re.search(pattern, text):
            return {"projection_count": count, "confidence": "heuristic", "rule": rule, "source": "question_text_only"}
    return {"projection_count": None, "confidence": "unknown", "rule": "no_rule", "source": "question_text_only"}


def choose_symmetric_perturbation(
    question_id: str, question: str, catalog: dict[str, dict[str, Any]], selected: list[str]
) -> tuple[str, str, str]:
    """Choose one real low-relevance schema table and render one shared block."""
    scores = table_scores(question, catalog)
    candidates = [table for table in catalog if table not in selected] or list(catalog)
    minimum = min(scores[table] for table in candidates)
    tied = [table for table in candidates if scores[table] == minimum]
    table = min(tied, key=lambda name: sha256_text(f"{question_id}|{name}"))
    metadata = catalog[table]
    column_names = [column["name"] for column in metadata["columns"]]
    block = (
        "Additional registered schema candidate (identical across factorial cells):\n"
        f"TABLE {table} (rows={metadata['row_count']}): " + ", ".join(column_names)
    )
    perturbation_id = f"REAL_TABLE_CANDIDATE_V1::{table}"
    return perturbation_id, canonical_hash({"id": perturbation_id, "block": block}), block


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)
    return re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL).strip()


def split_sql_statements(sql: str) -> list[str]:
    statements, buffer = [], []
    quote: str | None = None
    index = 0
    while index < len(sql):
        character = sql[index]
        if quote:
            buffer.append(character)
            if character == quote:
                if index + 1 < len(sql) and sql[index + 1] == quote:
                    buffer.append(sql[index + 1])
                    index += 1
                else:
                    quote = None
        elif character in {"'", '"'}:
            quote = character
            buffer.append(character)
        elif character == ";":
            statement = "".join(buffer).strip()
            if statement:
                statements.append(statement)
            buffer = []
        else:
            buffer.append(character)
        index += 1
    statement = "".join(buffer).strip()
    if statement:
        statements.append(statement)
    return statements


def validate_read_only_sql(sql: str) -> tuple[bool, str, str]:
    normalized = strip_sql_comments(sql)
    statements = split_sql_statements(normalized)
    if len(statements) != 1:
        return False, normalized, "exactly one statement is required"
    statement = statements[0]
    if not re.match(r"^(select|with)\b", statement, flags=re.IGNORECASE):
        return False, statement, "only SELECT or WITH ... SELECT is permitted"
    if FORBIDDEN.search(statement):
        return False, statement, "write/schema-changing token is forbidden"
    return True, statement, ""


def evaluate_sql(database: Path, sql: str) -> dict[str, Any]:
    safe, statement, safety_error = validate_read_only_sql(sql)
    if not safe:
        return {
            "safe": False, "executable": False, "error_type": "unsafe_sql",
            "error_message": safety_error, "column_count": 0, "row_count": 0, "result_sha256": None,
        }
    conn = connect_read_only(database)
    try:
        cursor = conn.execute(statement)
        columns = [column[0] for column in cursor.description or []]
        rows = [list(row) for row in cursor.fetchall()]
    except sqlite3.Error as exc:
        return {
            "safe": True, "executable": False, "error_type": "execution_error",
            "error_message": str(exc), "column_count": 0, "row_count": 0, "result_sha256": None,
        }
    finally:
        conn.close()
    return {
        "safe": True, "executable": True, "error_type": None, "error_message": None,
        "columns": columns, "column_count": len(columns), "row_count": len(rows),
        "result_sha256": canonical_hash({"columns": columns, "rows": rows}),
    }


def dataset_provenance(dataset_id: str, config: dict[str, Any]) -> dict[str, Any]:
    source = json.loads(config["source_manifest"].read_text(encoding="utf-8"))
    commit = source.get("git_commit")
    return {
        "dataset_id": dataset_id,
        "database_path": config["database"].relative_to(WORKSPACE).as_posix(),
        "database_sha256": sha256_file(config["database"]),
        "schema_sha256": sha256_file(config["schema"]),
        "questions_sha256": sha256_file(config["questions"]),
        "source_manifest_sha256": sha256_file(config["source_manifest"]),
        "source_commit": commit,
        "license_status": config["license_status"],
        "annotation_status": "AUTO_CANDIDATE",
        "human_reviewed": False,
        "sealed": False,
    }


def build_prompt(
    record: dict[str, Any], condition: str, context: str,
) -> str:
    return f"""You are evaluating a development-only Text-to-SQL protocol over a power-system SQLite database.

Return exactly one read-only SQLite SELECT query. Do not include markdown or explanation.
Do not use INSERT, UPDATE, DELETE, DROP, PRAGMA, ATTACH, or multiple statements.

Evidence status: AUTO_CANDIDATE; not human-reviewed; not sealed; not eligible for confirmatory benchmark claims.
Dataset: {record['dataset_id']}
Condition: {condition}

{context}

Question ID: {record['question_id']}
Question: {record['question']}
"""


def run_protocol() -> dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    all_prompts = []
    reference_rows = []
    provenance = {}
    gold_leakage = []
    source_records: dict[str, dict[str, Any]] = {}
    code_hash = sha256_file(Path(__file__))

    for dataset_id, config in DATASETS.items():
        provenance[dataset_id] = dataset_provenance(dataset_id, config)
        records = load_questions(dataset_id, config)
        conn = connect_read_only(config["database"])
        try:
            catalog = schema_catalog(conn)
        finally:
            conn.close()
        full_tables = sorted(catalog)
        for record in records:
            instance_id = f"{dataset_id}::{record['question_id']}"
            source_records[instance_id] = record
            selected = compact_tables(record["question"], catalog)
            perturbation_id, perturbation_hash, perturbation_block = choose_symmetric_perturbation(
                record["question_id"], record["question"], catalog, selected
            )
            shape = infer_question_shape(record["question"])
            question_hash = sha256_text(record["question"])
            for condition, scope, with_shape in CELLS:
                scope_tables = full_tables if scope == "full" else selected
                base_context = (
                    f"SQLite schema context ({scope} scope):\n"
                    + render_schema(catalog, scope_tables)
                    + "\n\n"
                    + perturbation_block
                )
                if with_shape:
                    context = base_context + "\n\nQuestion-derived answer-shape heuristic:\n" + canonical_json(shape)
                else:
                    context = base_context
                prompt = build_prompt(record, condition, context)
                reference_sql = record["registered_reference_sql"].strip()
                if reference_sql and reference_sql in prompt:
                    gold_leakage.append({"instance_id": instance_id, "condition": condition, "type": "exact_reference_sql"})
                all_prompts.append({
                    "run_id": RUN_ID,
                    "instance_id": instance_id,
                    "question_id": record["question_id"],
                    "dataset_id": dataset_id,
                    "database_id": provenance[dataset_id]["database_sha256"],
                    "condition": condition,
                    "context_scope": scope,
                    "answer_shape_hints": with_shape,
                    "annotation_status": "AUTO_CANDIDATE",
                    "human_reviewed": False,
                    "sealed": False,
                    "source_split": record["source_split"],
                    "template_family": record["template_family"],
                    "compact_selected_tables": selected,
                    "context_tables": scope_tables,
                    "shape_heuristic": shape if with_shape else None,
                    "perturbation_id": perturbation_id,
                    "perturbation_hash": perturbation_hash,
                    "perturbation_block": perturbation_block,
                    "question_hash": question_hash,
                    "database_hash": provenance[dataset_id]["database_sha256"],
                    "schema_hash": provenance[dataset_id]["schema_sha256"],
                    "questions_file_hash": provenance[dataset_id]["questions_sha256"],
                    "source_manifest_hash": provenance[dataset_id]["source_manifest_sha256"],
                    "code_hash": code_hash,
                    "context_hash": sha256_text(context),
                    "prompt_hash": sha256_text(prompt),
                    "context": context,
                    "prompt": prompt,
                    "registered_cell": 1,
                })
            evaluation = evaluate_sql(config["database"], record["registered_reference_sql"])
            reference_rows.append({
                "evidence_status": "AUTO_CANDIDATE_REGISTERED_REFERENCE_NOT_HUMAN_GOLD",
                "instance_id": instance_id,
                "question_id": record["question_id"],
                "dataset_id": dataset_id,
                "template_family": record["template_family"],
                "source_split": record["source_split"],
                "human_reviewed": False,
                "sealed": False,
                "registered_reference_sql": record["registered_reference_sql"],
                "registered_reference_sql_sha256": sha256_text(record["registered_reference_sql"].strip()),
                **evaluation,
            })

    all_prompts.sort(key=lambda row: (row["instance_id"], row["condition"]))
    reference_rows.sort(key=lambda row: row["instance_id"])
    write_jsonl(OUTPUT / "factorial_prompts.jsonl", all_prompts)
    write_jsonl(OUTPUT / "reference_sql_evaluation.jsonl", reference_rows)

    design_rows = [
        {
            key: row[key]
            for key in (
                "run_id", "instance_id", "question_id", "dataset_id", "database_id", "condition",
                "annotation_status", "prompt_hash", "context_hash", "perturbation_id", "perturbation_hash",
                "question_hash", "database_hash", "schema_hash", "questions_file_hash",
                "source_manifest_hash", "code_hash", "registered_cell",
            )
        }
        for row in all_prompts
    ]
    design_path = OUTPUT / "factorial_design_matrix.jsonl"
    write_jsonl(design_path, design_rows)
    audit = stat_audit.build_report(
        design_path, design_rows, "jsonl", condition_field="condition", item_fields=["instance_id"],
        cluster_field="instance_id", metric_fields=["registered_cell"],
        required_fields=["run_id", "dataset_id", "database_id", "annotation_status", "prompt_hash", "context_hash", "perturbation_id"],
        hash_fields=["question_hash", "database_hash", "schema_hash", "questions_file_hash", "source_manifest_hash", "code_hash", "perturbation_hash"],
        expected_conditions=[cell[0] for cell in CELLS], bootstrap_samples=2000,
        confidence=0.95, seed=20260805, max_examples=20,
    )
    write_json(OUTPUT / "shared_stat_audit.json", audit)
    (OUTPUT / "shared_stat_audit.md").write_text(stat_audit.report_markdown(audit), encoding="utf-8")

    grouped = defaultdict(list)
    for row in all_prompts:
        grouped[row["instance_id"]].append(row)
    symmetry_failures = []
    factor_failures = []
    for instance_id, rows in grouped.items():
        if len(rows) != 4 or {row["condition"] for row in rows} != {cell[0] for cell in CELLS}:
            factor_failures.append({"instance_id": instance_id, "reason": "missing_or_duplicate_cell"})
        for field in ("database_hash", "question_hash", "perturbation_id", "perturbation_hash"):
            if len({row[field] for row in rows}) != 1:
                symmetry_failures.append({"instance_id": instance_id, "field": field})
        mapping = {(row["context_scope"], row["answer_shape_hints"]) for row in rows}
        if mapping != {("full", False), ("full", True), ("compact", False), ("compact", True)}:
            factor_failures.append({"instance_id": instance_id, "reason": "factor_mapping"})

    manifest = {
        "schema_version": "w4-ma-external-protocol-v1",
        "run_id": RUN_ID,
        "design": "full/compact context scope x absent/present question-only shape heuristic",
        "development_evidence_only": True,
        "paid_model_calls": 0,
        "network_calls": 0,
        "question_count": len(grouped),
        "dataset_question_counts": dict(sorted(Counter(row["dataset_id"] for row in reference_rows).items())),
        "cell_count": len(all_prompts),
        "cell_counts_by_condition": dict(sorted(Counter(row["condition"] for row in all_prompts).items())),
        "annotation_status_counts": dict(sorted(Counter(row["annotation_status"] for row in all_prompts).items())),
        "human_reviewed_cell_count": sum(row["human_reviewed"] for row in all_prompts),
        "sealed_cell_count": sum(row["sealed"] for row in all_prompts),
        "gold_leakage_count": len(gold_leakage),
        "gold_leakage_findings": gold_leakage,
        "symmetric_perturbation_failure_count": len(symmetry_failures),
        "symmetric_perturbation_failures": symmetry_failures,
        "factor_mapping_failure_count": len(factor_failures),
        "factor_mapping_failures": factor_failures,
        "reference_sql_count": len(reference_rows),
        "reference_sql_safe_count": sum(row["safe"] for row in reference_rows),
        "reference_sql_executable_count": sum(row["executable"] for row in reference_rows),
        "reference_sql_empty_result_count": sum(row.get("row_count") == 0 for row in reference_rows),
        "shared_stat_audit_passed": audit["audit"]["passed"],
        "shared_stat_audit_cartesian": {
            "observed": audit["audit"]["observed_unique_cells"],
            "expected": audit["audit"]["expected_cartesian_cells"],
        },
        "prompt_set_sha256": canonical_hash([
            {"instance_id": row["instance_id"], "condition": row["condition"], "prompt_hash": row["prompt_hash"], "context_hash": row["context_hash"]}
            for row in all_prompts
        ]),
        "reference_result_set_sha256": canonical_hash([
            {"instance_id": row["instance_id"], "sql": row["registered_reference_sql_sha256"], "result": row["result_sha256"]}
            for row in reference_rows
        ]),
        "code_sha256": code_hash,
        "datasets": provenance,
        "interpretation_contract": [
            "All 91 records are AUTO_CANDIDATE and development-visible.",
            "Registered reference SQL execution validates protocol plumbing; it does not establish human-gold language quality.",
            "No accuracy result exists until separately authorized model predictions are produced.",
            "Neither candidate holdout label is a sealed confirmatory test.",
        ],
    }
    write_json(OUTPUT / "manifest.json", manifest)
    return manifest


def report_markdown(manifest: dict[str, Any]) -> str:
    return "\n".join([
        "# W4 MA External-Database Protocol Report",
        "",
        "## Outcome",
        "",
        f"- External development candidates: **{manifest['question_count']}** (RTS-GMLC 55; SimBench 36).",
        f"- Registered factorial cells: **{manifest['cell_count']}**, four conditions x 91 questions.",
        f"- Exact registered-reference SQL leakage into prompts: **{manifest['gold_leakage_count']}**.",
        f"- Symmetric perturbation failures: **{manifest['symmetric_perturbation_failure_count']}**.",
        f"- Reference SQL safe/executable: **{manifest['reference_sql_safe_count']}/{manifest['reference_sql_executable_count']}** of {manifest['reference_sql_count']}.",
        f"- Shared Cartesian/hash audit: **{'PASS' if manifest['shared_stat_audit_passed'] else 'FAIL'}** ({manifest['shared_stat_audit_cartesian']['observed']}/{manifest['shared_stat_audit_cartesian']['expected']}).",
        "- Model, network, and paid API calls: **0**.",
        "",
        "## Protocol",
        "",
        "Each question receives full/no-shape, full/shape, compact/no-shape, and compact/shape prompts. Full and compact schemas are generated from SQLite introspection. Compact selection uses only question tokens and schema metadata. Shape hints are coarse heuristics derived only from natural-language text; stored answer shape and registered SQL are never consulted.",
        "",
        "A real low-relevance table is deterministically registered as an additional schema candidate. Its ID and exact block hash are identical in all four cells for the same question. Database, schema, question, source-manifest, perturbation, context, prompt, and code hashes are retained per cell.",
        "",
        "## Evaluation interface",
        "",
        "The reusable evaluator permits one read-only `SELECT` or `WITH ... SELECT`, rejects write/schema-changing tokens and multiple statements, opens SQLite in read-only/query-only mode, and returns execution status, shape, row count, and canonical result SHA-256. In this dry run it evaluates only the registered automatic reference SQL, not model predictions.",
        "",
        "## Evidence boundary",
        "",
        "All inputs remain `AUTO_CANDIDATE`, non-human-reviewed, nonsealed development artifacts. Reference SQL execution proves mechanical consistency only. It does not justify benchmark accuracy, natural-language validity, external generalization, or main-table claims. Human review, adjudication, family-isolated sealing, and an untouched evaluation run remain required.",
        "",
        "## Redistribution",
        "",
        "RTS-GMLC carries an NREL data-use notice whose pinned local text is truncated; SimBench is governed by ODbL/DbCL for database content. Both require a redistribution decision before publishing derived databases.",
        "",
    ])


def main() -> int:
    manifest = run_protocol()
    (ROOT / "W4_MA_EXTERNAL_PROTOCOL_REPORT.md").write_text(report_markdown(manifest), encoding="utf-8")
    artifacts = [
        path for path in sorted(OUTPUT.iterdir()) if path.is_file() and path.name != "artifact_manifest.json"
    ] + [ROOT / "W4_MA_EXTERNAL_PROTOCOL_REPORT.md"]
    rows = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in artifacts
    ]
    write_json(OUTPUT / "artifact_manifest.json", {
        "schema_version": "w4-ma-external-artifact-manifest-v1",
        "artifacts": rows,
        "artifact_set_sha256": canonical_hash(rows),
    })
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    gates = [
        manifest["question_count"] == 91,
        manifest["cell_count"] == 364,
        manifest["gold_leakage_count"] == 0,
        manifest["symmetric_perturbation_failure_count"] == 0,
        manifest["factor_mapping_failure_count"] == 0,
        manifest["reference_sql_safe_count"] == 91,
        manifest["reference_sql_executable_count"] == 91,
        manifest["shared_stat_audit_passed"],
        manifest["human_reviewed_cell_count"] == 0,
        manifest["sealed_cell_count"] == 0,
        manifest["paid_model_calls"] == 0,
    ]
    return 0 if all(gates) else 2


if __name__ == "__main__":
    raise SystemExit(main())
