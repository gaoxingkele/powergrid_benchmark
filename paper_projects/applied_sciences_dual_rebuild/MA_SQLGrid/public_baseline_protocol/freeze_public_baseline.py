"""Build the frozen, not-yet-run BIRD Mini-Dev public-baseline package.

This module performs no LLM generation.  It materializes deterministic prompt
templates, audits schema selection and leakage boundaries, freezes call order,
and provides the safe SQLite/official-EX compatibility boundary used later by
the formal harness.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
META = ROOT / "official_metadata" / "bird_mini_dev_sqlite.json"
DB_ROOT = ROOT / "official_downloads" / "bird_dev_databases_extracted" / "dev_databases"
PROMPT_ROOT = ROOT / "materialized_prompts"
PROTOCOL_ID = "MA-PUBLIC-BIRD-MINIDEV-v1.0"
METHODS = ("B0_DIRECT", "B1_DECOMP", "B2_SCHEMA_SELECT", "B3_EXEC_REPAIR")
FEEDBACK = (
    "SAFE_EXECUTED", "PARSE_ERROR", "UNKNOWN_TABLE", "UNKNOWN_COLUMN",
    "AMBIGUOUS_COLUMN", "TYPE_OR_FUNCTION_ERROR", "TIMEOUT", "OTHER_EXECUTION_ERROR",
)
SYSTEM = (
    "You translate natural-language questions into one read-only SQLite query. "
    "Use only the supplied schema and evidence. Never modify the database."
)
TOKENIZER = Path(r"D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3\bin\llama-tokenize.exe")
SERVER = Path(r"D:\aicoding\models\ma_sqlgrid_local\llama.cpp-b9637-cuda13.3\bin\llama-server.exe")
MODELS = {
    "qwen": Path(r"D:\aicoding\models\ma_sqlgrid_local\Qwen2.5-Coder-7B-Instruct-GGUF-13fb94bf\qwen2.5-coder-7b-instruct-q4_k_m.gguf"),
    "granite": Path(r"D:\aicoding\models\ma_sqlgrid_local\ibm-granite-3.3-8b-instruct-GGUF-e40e9dd\granite-3.3-8b-instruct-Q4_K_M.gguf"),
}


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", text).lower())


def quote_identifier(name: str) -> str:
    if name is None:
        return '"<implicit-primary-key>"'
    return '"' + name.replace('"', '""') + '"'


def load_rows() -> list[dict[str, Any]]:
    rows = json.loads(META.read_text(encoding="utf-8"))
    assert len(rows) == 500 and len({r["question_id"] for r in rows}) == 500
    return rows


def db_path(db_id: str) -> Path:
    return DB_ROOT / db_id / f"{db_id}.sqlite"


def schema_catalog(db_id: str) -> dict[str, Any]:
    path = db_path(db_id)
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    con.execute("PRAGMA query_only=ON")
    tables: dict[str, Any] = {}
    try:
        names = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY lower(name), name"
        )]
        for table in names:
            columns = []
            for cid, name, typ, notnull, default, pk in con.execute(f"PRAGMA table_info({quote_identifier(table)})"):
                columns.append({"name": name, "type": typ or "", "pk": bool(pk), "notnull": bool(notnull)})
            fks = []
            for _, _, target, source_col, target_col, *_ in con.execute(f"PRAGMA foreign_key_list({quote_identifier(table)})"):
                fks.append({"source": source_col, "target_table": target, "target_column": target_col})
            descriptions = load_descriptions(db_id, table)
            for col in columns:
                col["description"] = descriptions.get(col["name"].lower(), "")
                col["examples"] = deterministic_examples(con, table, col["name"])
            tables[table] = {"columns": columns, "foreign_keys": fks}
    finally:
        con.close()
    return {"db_id": db_id, "tables": tables}


def load_descriptions(db_id: str, table: str) -> dict[str, str]:
    directory = DB_ROOT / db_id / "database_description"
    candidates = [directory / f"{table}.csv"]
    candidates.extend(sorted(directory.glob("*.csv")))
    target = next((p for p in candidates if p.is_file() and p.stem.lower() == table.lower()), None)
    if target is None:
        return {}
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            with target.open("r", encoding=encoding, newline="") as handle:
                records = list(csv.DictReader(handle))
            break
        except UnicodeDecodeError:
            continue
    else:
        return {}
    out = {}
    for row in records:
        lower = {str(k).strip().lower(): str(v or "").strip() for k, v in row.items()}
        name = lower.get("original_column_name") or lower.get("column_name") or lower.get("field name")
        desc = lower.get("column_description") or lower.get("description") or lower.get("column description") or ""
        if name:
            out[name.lower()] = re.sub(r"\s+", " ", desc)[:160]
    return out


def deterministic_examples(con: sqlite3.Connection, table: str, column: str) -> list[str]:
    sql = (
        f"SELECT DISTINCT CAST({quote_identifier(column)} AS TEXT) AS v "
        f"FROM {quote_identifier(table)} WHERE {quote_identifier(column)} IS NOT NULL "
        "ORDER BY lower(v), v LIMIT 3"
    )
    try:
        return [re.sub(r"\s+", " ", str(r[0]))[:64] for r in con.execute(sql)]
    except sqlite3.Error:
        return []


def serialize_schema(catalog: dict[str, Any], selected: dict[str, set[str]] | None = None) -> str:
    lines = []
    for table, info in catalog["tables"].items():
        if selected is not None and table not in selected:
            continue
        lines.append(f"TABLE {quote_identifier(table)}")
        allowed = None if selected is None else selected[table]
        for col in info["columns"]:
            if allowed is not None and col["name"] not in allowed:
                continue
            tags = []
            if col["pk"]:
                tags.append("PK")
            desc = f" -- {col['description']}" if col["description"] else ""
            examples = f" examples={stable_json(col['examples'])}" if col["examples"] else ""
            lines.append(f"  {quote_identifier(col['name'])} {col['type']} {' '.join(tags)}{desc}{examples}".rstrip())
        for fk in info["foreign_keys"]:
            if allowed is None or fk["source"] in allowed:
                lines.append(
                    f"  FK {quote_identifier(fk['source'])} -> "
                    f"{quote_identifier(fk['target_table'])}.{quote_identifier(fk['target_column'])}"
                )
    return "\n".join(lines)


def bm25_select(catalog: dict[str, Any], question: str, evidence: str) -> dict[str, set[str]]:
    query = norm_terms(question + " " + evidence)
    documents: list[tuple[str, str, list[str]]] = []
    for table, info in catalog["tables"].items():
        for col in info["columns"]:
            text = " ".join([table, col["name"], col["description"], *col["examples"]])
            documents.append((table, col["name"], norm_terms(text)))
    df = Counter(term for term in set(query) for _, _, doc in documents if term in doc)
    avgdl = sum(map(lambda x: len(x[2]), documents)) / max(1, len(documents))
    scores = []
    for table, column, doc in documents:
        counts = Counter(doc)
        score = 0.0
        for term in query:
            n = df.get(term, 0)
            idf = math.log(1 + (len(documents) - n + 0.5) / (n + 0.5))
            tf = counts.get(term, 0)
            score += idf * tf * 2.2 / (tf + 1.2 * (1 - 0.75 + 0.75 * len(doc) / max(avgdl, 1))) if tf else 0
        scores.append((score, table.lower(), column.lower(), table, column))
    scores.sort(key=lambda x: (-x[0], x[1], x[2]))
    table_scores: dict[str, float] = defaultdict(float)
    for score, _, _, table, _ in scores:
        table_scores[table] = max(table_scores[table], score)
    ranked_tables = sorted(table_scores, key=lambda t: (-table_scores[t], t.lower()))
    chosen_tables = set(ranked_tables[: min(6, len(ranked_tables))])
    selected: dict[str, set[str]] = {t: set() for t in chosen_tables}
    for score, _, _, table, column in scores:
        if table in selected and len(selected[table]) < 12 and (score > 0 or not selected[table]):
            selected[table].add(column)
    # Keys are mandatory; selected tables are then closed over shortest deterministic FK paths.
    graph: dict[str, list[str]] = defaultdict(list)
    for table, info in catalog["tables"].items():
        for fk in info["foreign_keys"]:
            if fk["target_table"] in catalog["tables"]:
                graph[table].append(fk["target_table"])
                graph[fk["target_table"]].append(table)
    anchors = sorted(chosen_tables)
    for start, goal in zip(anchors, anchors[1:]):
        queue = [(start, [start])]
        seen = {start}
        while queue:
            node, path = queue.pop(0)
            if node == goal:
                for t in path:
                    selected.setdefault(t, set())
                break
            for nxt in sorted(set(graph[node]), key=str.lower):
                if nxt not in seen:
                    seen.add(nxt); queue.append((nxt, path + [nxt]))
    for table in list(selected):
        info = catalog["tables"][table]
        for col in info["columns"]:
            if col["pk"]:
                selected[table].add(col["name"])
        for fk in info["foreign_keys"]:
            selected[table].add(fk["source"])
            if fk["target_table"] in selected:
                if fk["target_column"] is not None:
                    selected[fk["target_table"]].add(fk["target_column"])
    return selected


def user_prompt(method: str, row: dict[str, Any], schema: str, *, second: bool = False) -> str:
    common = f"DATABASE: {row['db_id']}\nQUESTION: {row['question']}\nEVIDENCE: {row['evidence']}\nSCHEMA:\n{schema}"
    if method == "B0_DIRECT":
        return common + "\nReturn exactly one SQLite SELECT/WITH query, without markdown or prose."
    if method == "B1_DECOMP":
        return common + ('\nReturn one JSON object with keys "schema_links" (array), "clause_plan" (array), and "final_sql" (string). No text outside JSON.')
    if method == "B2_SCHEMA_SELECT":
        return common + "\nThis is the deterministically selected schema. Return exactly one SQLite SELECT/WITH query, without markdown or prose."
    if method == "B3_EXEC_REPAIR" and not second:
        return common + "\nProduce candidate 1 as exactly one SQLite SELECT/WITH query, without markdown or prose."
    if method == "B3_EXEC_REPAIR" and second:
        return common + (
            "\nCANDIDATE_1: {{FIRST_CANDIDATE_RUNTIME_MAX_400_TOKENS}}"
            "\nVALIDATOR_FEEDBACK: {{ONE_OF_FROZEN_FEEDBACK_VOCABULARY}}"
            "\nAlways return a final SQLite SELECT/WITH query, even when feedback is SAFE_EXECUTED. No markdown or prose."
        )
    raise ValueError(method)


def render_chat(model: str, user: str) -> str:
    if model == "qwen":
        return f"<|im_start|>system\n{SYSTEM}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"
    if model == "granite":
        return (
            f"<|start_of_role|>system<|end_of_role|>{SYSTEM}<|end_of_text|>\n"
            f"<|start_of_role|>user<|end_of_role|>{user}<|end_of_text|>\n"
            "<|start_of_role|>assistant<|end_of_role|>"
        )
    raise ValueError(model)


def tokenize_records_with_pinned_server(model: str, records: list[dict[str, Any]]) -> None:
    """Apply one pinned GGUF tokenizer to all prompts; never call completion endpoints."""
    port = 8091 if model == "qwen" else 8092
    base = f"http://127.0.0.1:{port}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    log_path = ROOT / f"TOKENIZER_ONLY_{model}.log"
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            [str(SERVER), "--model", str(MODELS[model]), "--alias", f"freeze-tokenizer-{model}",
             "--host", "127.0.0.1", "--port", str(port), "--ctx-size", "16384",
             "--n-gpu-layers", "99", "--parallel", "1", "--no-warmup"],
            stdout=log, stderr=subprocess.STDOUT, creationflags=creationflags,
        )
        try:
            for _ in range(180):
                if process.poll() is not None:
                    raise RuntimeError(f"Tokenizer-only server {model} exited; inspect {log_path}")
                try:
                    with opener.open(base + "/health", timeout=1) as response:
                        if response.status == 200:
                            break
                except Exception:
                    time.sleep(1)
            else:
                raise RuntimeError(f"Tokenizer-only server {model} did not become healthy")
            for index, record in enumerate(records):
                payload = json.dumps({"content": record["_rendered"], "add_special": False}, ensure_ascii=False).encode("utf-8")
                request = urllib.request.Request(base + "/tokenize", data=payload, headers={"Content-Type": "application/json"})
                with opener.open(request, timeout=120) as response:
                    answer = json.loads(response.read().decode("utf-8"))
                tokens = answer.get("tokens")
                if not isinstance(tokens, list):
                    raise RuntimeError(f"Unexpected /tokenize response at {model} record {index}: {answer}")
                record["token_count_static"] = len(tokens)
                record["token_upper_bound"] = len(tokens) + (400 if record["call"] == 2 else 0)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill(); process.wait(timeout=30)


def classify_sqlite_error(message: str) -> str:
    value = message.lower()
    if "no such table" in value: return "UNKNOWN_TABLE"
    if "no such column" in value: return "UNKNOWN_COLUMN"
    if "ambiguous column" in value: return "AMBIGUOUS_COLUMN"
    if "interrupted" in value: return "TIMEOUT"
    if "syntax" in value or "incomplete input" in value: return "PARSE_ERROR"
    if "function" in value or "datatype" in value or "type" in value: return "TYPE_OR_FUNCTION_ERROR"
    return "OTHER_EXECUTION_ERROR"


def extract_sql(output: str, method: str) -> str:
    text = output.strip()
    text = re.sub(r"^```(?:sql|json)?\s*|\s*```$", "", text, flags=re.I | re.S).strip()
    if method == "B1_DECOMP":
        try:
            value = json.loads(text)
            sql = value["final_sql"]
            return sql.strip() if isinstance(sql, str) else ""
        except (json.JSONDecodeError, KeyError, TypeError):
            return ""
    match = re.search(r"(?is)\b(?:select|with)\b.*", text)
    return match.group(0).strip() if match else ""


def safe_execute(sql: str, path: Path, timeout_seconds: float = 30.0) -> tuple[str, list[tuple[Any, ...]] | None]:
    candidate = sql.strip()
    if not re.match(r"(?is)^(select|with)\b", candidate) or "\x00" in candidate:
        return "PARSE_ERROR", None
    if len(candidate.encode("utf-8")) > 64 * 1024:
        return "PARSE_ERROR", None
    started = time.perf_counter()
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        con.execute("PRAGMA query_only=ON")
        denied = {
            sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE,
            sqlite3.SQLITE_CREATE_INDEX, sqlite3.SQLITE_CREATE_TABLE, sqlite3.SQLITE_CREATE_TEMP_INDEX,
            sqlite3.SQLITE_CREATE_TEMP_TABLE, sqlite3.SQLITE_CREATE_TEMP_TRIGGER, sqlite3.SQLITE_CREATE_TEMP_VIEW,
            sqlite3.SQLITE_CREATE_TRIGGER, sqlite3.SQLITE_CREATE_VIEW, sqlite3.SQLITE_DROP_INDEX,
            sqlite3.SQLITE_DROP_TABLE, sqlite3.SQLITE_DROP_TEMP_INDEX, sqlite3.SQLITE_DROP_TEMP_TABLE,
            sqlite3.SQLITE_DROP_TEMP_TRIGGER, sqlite3.SQLITE_DROP_TEMP_VIEW, sqlite3.SQLITE_DROP_TRIGGER,
            sqlite3.SQLITE_DROP_VIEW, sqlite3.SQLITE_ALTER_TABLE, sqlite3.SQLITE_REINDEX,
            sqlite3.SQLITE_ANALYZE, sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH,
        }
        con.set_authorizer(lambda action, *_: sqlite3.SQLITE_DENY if action in denied or action == sqlite3.SQLITE_PRAGMA else sqlite3.SQLITE_OK)
        con.set_progress_handler(lambda: 1 if time.perf_counter() - started > timeout_seconds else 0, 10_000)
        cursor = con.execute(candidate)
        return "SAFE_EXECUTED", cursor.fetchall()
    except (sqlite3.Error, sqlite3.Warning) as exc:
        # sqlite3.Warning is NOT a subclass of sqlite3.Error; multi-statement
        # model outputs raise it ("You can only execute one statement at a
        # time") and must be classified, not crash the run.
        return classify_sqlite_error(str(exc)), None
    finally:
        con.close()


def official_ex(predicted: Iterable[tuple[Any, ...]], gold: Iterable[tuple[Any, ...]]) -> int:
    """Exact boundary in pinned official evaluation_ex.py: set(row tuples)."""
    return int(set(predicted) == set(gold))


def sql_identifiers(sql: str, catalog: dict[str, Any]) -> tuple[set[str], set[tuple[str, str]]]:
    lowered = sql.lower()
    tables = {t for t in catalog["tables"] if re.search(rf"(?<![\w]){re.escape(t.lower())}(?![\w])", lowered)}
    columns = set()
    for table, info in catalog["tables"].items():
        for col in info["columns"]:
            if re.search(rf"(?<![\w]){re.escape(col['name'].lower())}(?![\w])", lowered):
                columns.add((table, col["name"]))
    return tables, columns


def build(*, exact_tokens: bool) -> dict[str, Any]:
    rows = load_rows()
    catalog_cache = ROOT / "SCHEMA_CATALOG_CACHE.json"
    if catalog_cache.is_file():
        catalogs = json.loads(catalog_cache.read_text(encoding="utf-8"))
    else:
        catalogs = {db: schema_catalog(db) for db in sorted({r["db_id"] for r in rows})}
        catalog_cache.write_text(json.dumps(catalogs, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    order = sorted(rows, key=lambda r: hashlib.sha256(f"{PROTOCOL_ID}|{r['question_id']}".encode()).hexdigest())
    call_order = []
    prompt_records: dict[str, list[dict[str, Any]]] = {m: [] for m in MODELS}
    leakage_failures = []
    selector_audit = []
    for item_index, row in enumerate(order):
        method_order = METHODS[item_index % len(METHODS):] + METHODS[:item_index % len(METHODS)]
        catalog = catalogs[row["db_id"]]
        full = serialize_schema(catalog)
        selected = bm25_select(catalog, row["question"], row["evidence"])
        compact = serialize_schema(catalog, selected)
        gold_tables, gold_columns = sql_identifiers(row["SQL"], catalog)
        chosen_columns = {(t, c) for t, cs in selected.items() for c in cs}
        selector_audit.append({
            "question_id": row["question_id"], "db_id": row["db_id"],
            "selected_tables": len(selected), "selected_columns": len(chosen_columns),
            "gold_table_recall": 1.0 if not gold_tables else len(gold_tables & set(selected)) / len(gold_tables),
            "gold_column_recall": 1.0 if not gold_columns else len(gold_columns & chosen_columns) / len(gold_columns),
        })
        for method in method_order:
            calls = (1, 2) if method == "B3_EXEC_REPAIR" else (1,)
            for call in calls:
                schema = compact if method in ("B2_SCHEMA_SELECT", "B3_EXEC_REPAIR") else full
                user = user_prompt(method, row, schema, second=call == 2)
                forbidden = [row["SQL"], str(row["difficulty"])]
                hits = ["gold_sql" if x == row["SQL"] else "difficulty" for x in forbidden if x and x in user]
                if hits:
                    leakage_failures.append({"question_id": row["question_id"], "method": method, "call": call, "hits": hits})
                call_order.append({"item_index": item_index, "question_id": row["question_id"], "db_id": row["db_id"], "method": method, "call": call})
                for model in MODELS:
                    rendered = render_chat(model, user)
                    prompt_records[model].append({
                        "question_id": row["question_id"], "db_id": row["db_id"], "method": method, "call": call,
                        "dynamic_fields": ["first_candidate", "validator_feedback"] if call == 2 else [],
                        "user_sha256": text_sha(user), "rendered_sha256": text_sha(rendered),
                        "rendered_utf8_bytes": len(rendered.encode("utf-8")), "token_count_static": None,
                        "token_upper_bound": None, "_rendered": rendered,
                    })
    if exact_tokens:
        for model in MODELS:
            tokenize_records_with_pinned_server(model, prompt_records[model])
    else:
        for records in prompt_records.values():
            for record in records:
                record.pop("_rendered")
    PROMPT_ROOT.mkdir(exist_ok=True)
    outputs = {}
    for model, records in prompt_records.items():
        content_path = PROMPT_ROOT / f"{model}_prompts.jsonl.gz"
        content = "".join(
            stable_json({
                    "question_id": record["question_id"], "db_id": record["db_id"],
                    "method": record["method"], "call": record["call"],
                    "rendered_prompt": record["_rendered"],
                }) + "\n" for record in records
        )
        content_path.write_bytes(gzip.compress(content.encode("utf-8"), compresslevel=9, mtime=0))
        for record in records:
            record.pop("_rendered", None)
        path = PROMPT_ROOT / f"{model}_prompt_manifest.jsonl"
        path.write_text("".join(stable_json(r) + "\n" for r in records), encoding="utf-8")
        outputs[path.name] = {"rows": len(records), "bytes": path.stat().st_size, "sha256": sha256(path)}
        outputs[content_path.name] = {"rows": len(records), "bytes": content_path.stat().st_size, "sha256": sha256(content_path), "compression": "gzip_mtime_0"}
    order_path = ROOT / "DETERMINISTIC_CALL_ORDER.jsonl"
    order_path.write_text("".join(stable_json(r) + "\n" for r in call_order), encoding="utf-8")
    selector_path = ROOT / "SCHEMA_SELECTOR_OFFLINE_AUDIT.jsonl"
    selector_path.write_text("".join(stable_json(r) + "\n" for r in selector_audit), encoding="utf-8")
    token_summaries = {}
    for model, records in prompt_records.items():
        values = [r["token_upper_bound"] for r in records if r["token_upper_bound"] is not None]
        aggregate_by_item_method: dict[tuple[Any, str], int] = defaultdict(int)
        for record in records:
            if record["token_upper_bound"] is not None:
                aggregate_by_item_method[(record["question_id"], record["method"])] += record["token_upper_bound"]
        aggregate_values = list(aggregate_by_item_method.values())
        token_summaries[model] = {
            "records": len(records), "exact_counts_available": len(values) == len(records),
            "maximum_call_upper_bound": max(values) if values else None,
            "maximum_item_method_aggregate_upper_bound": max(aggregate_values) if aggregate_values else None,
            "item_methods": len(aggregate_values),
            "over_12000": sum(v > 12000 for v in aggregate_values),
            "over_context_minus_512": sum(v > 15872 for v in values),
        }
    result = {
        "schema_version": "ma-public-baseline-materialization-v1", "protocol_id": PROTOCOL_ID,
        "formal_model_calls": 0, "generation_calls": 0, "items": len(rows),
        "logical_calls_per_model": len(call_order), "expected_formal_generation_calls": len(call_order) * 2,
        "leakage_failures": leakage_failures,
        "selector": {
            "rows": len(selector_audit),
            "mean_gold_table_recall": sum(r["gold_table_recall"] for r in selector_audit) / len(selector_audit),
            "mean_gold_column_recall": sum(r["gold_column_recall"] for r in selector_audit) / len(selector_audit),
            "zero_gold_table_recall": sum(r["gold_table_recall"] == 0 for r in selector_audit),
            "zero_gold_column_recall": sum(r["gold_column_recall"] == 0 for r in selector_audit),
        },
        "token_budget": token_summaries, "prompt_manifests": outputs,
        "call_order": {"rows": len(call_order), "sha256": sha256(order_path)},
        "selector_ledger": {"rows": len(selector_audit), "sha256": sha256(selector_path)},
        "feedback_vocabulary": FEEDBACK,
        "decision": "PASS" if not leakage_failures and all(s["over_12000"] == 0 and s["exact_counts_available"] for s in token_summaries.values()) else "BLOCK",
    }
    (ROOT / "PROMPT_MATERIALIZATION_AUDIT.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-tokens", action="store_true", help="Use pinned llama-tokenize for both GGUF tokenizers.")
    args = parser.parse_args()
    report = build(exact_tokens=args.exact_tokens)
    print(json.dumps({"decision": report["decision"], "calls_per_model": report["logical_calls_per_model"], "token_budget": report["token_budget"], "generation_calls": 0}, ensure_ascii=False))
    if report["decision"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
