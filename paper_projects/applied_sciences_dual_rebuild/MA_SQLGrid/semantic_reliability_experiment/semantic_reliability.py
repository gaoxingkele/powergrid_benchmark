#!/usr/bin/env python3
"""Freeze and run a deterministic multi-state SQL semantic reliability suite."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / "paper_projects/2026_ma_sqlgrid_cmc/source"
DATA = SOURCE / "data/griddb_maintenance_v2_v0_1"
DB = DATA / "database.sqlite"
QUESTIONS = DATA / "questions.jsonl"
PREDICTIONS = {
    "qwen": ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1/predictions.jsonl",
    "granite": ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/granite_formal/granite33_8b_q4km_seed20260805_clean1/predictions.jsonl",
}
PROTOCOL = HERE / "PROTOCOL.md"
CODE = HERE / "semantic_reliability.py"
STATES = HERE / "states"
LOGS = HERE / "logs"
TABLES = HERE / "tables"
FREEZE = HERE / "PROTOCOL_FREEZE_DRAFT.json"
INDEPENDENT_AUDIT = HERE / "INDEPENDENT_DESIGN_AUDIT.json"
RESULTS = HERE / "RESULTS.json"

TABLE_ORDER = [
    "asset_types", "locations", "technicians", "assets", "work_orders",
    "maintenance_logs", "sensor_readings", "grid_topology",
]
STATE_SPECS = [
    ("S0_original", []),
    ("P1_exact_clone", ["exact"]),
    ("P2_attribute_rotation", ["rotate"]),
    ("P3_relation_rewire", ["rewire"]),
    ("P4_numeric_time_shift", ["shift"]),
    ("P5_combined", ["combined"]),
    ("P6_two_cohorts", ["exact", "combined"]),
]
FORBIDDEN = re.compile(
    r"\b(insert|update|delete|replace|drop|alter|create|attach|detach|vacuum|pragma|reindex|analyze|begin|commit|rollback|savepoint|release)\b",
    re.I,
)
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(.*)$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def state_metadata(conn: sqlite3.Connection) -> dict[str, Any]:
    integrity = conn.execute("PRAGMA integrity_check").fetchall()
    fk = conn.execute("PRAGMA foreign_key_check").fetchall()
    counts = {t: conn.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in TABLE_ORDER}
    return {"integrity_check": [r[0] for r in integrity], "foreign_key_violations": len(fk), "row_counts": counts}


def schema_info(conn: sqlite3.Connection) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for table in TABLE_ORDER:
        cols = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
        fks = conn.execute(f'PRAGMA foreign_key_list("{table}")').fetchall()
        pk = next(c[1] for c in cols if c[5] == 1)
        out[table] = {
            "columns": [c[1] for c in cols],
            "types": {c[1]: (c[2] or "").upper() for c in cols},
            "not_null": {c[1]: bool(c[3]) for c in cols},
            "pk": pk,
            "fks": {r[3]: {"table": r[2], "column": r[4]} for r in fks},
        }
    return out


def shifted(value: Any, declared_type: str, cohort_index: int) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        match = DATE_RE.match(value)
        if match:
            try:
                day = datetime.strptime(match.group(1), "%Y-%m-%d") + timedelta(days=37 * cohort_index)
                return day.strftime("%Y-%m-%d") + match.group(2)
            except ValueError:
                return value
        return value
    if isinstance(value, bool):
        return value
    if isinstance(value, float) or "REAL" in declared_type:
        return round(float(value) * (1.0 + 0.125 * cohort_index) + 0.25 * cohort_index, 6)
    if isinstance(value, int) and "INT" in declared_type:
        return value + 3 * cohort_index
    return value


def append_cohort(conn: sqlite3.Connection, info: dict[str, dict[str, Any]], mode: str, cohort_index: int) -> None:
    """Append one cohort; transformation depends only on the original database."""
    offset = cohort_index * 100000
    originals: dict[str, list[dict[str, Any]]] = {}
    keys: dict[str, list[Any]] = {}
    for table in TABLE_ORDER:
        cols = info[table]["columns"]
        originals[table] = [dict(zip(cols, row)) for row in conn.execute(f'SELECT * FROM "{table}" ORDER BY "{info[table]["pk"]}"').fetchall() if row[cols.index(info[table]["pk"])] < 100000]
        keys[table] = [r[info[table]["pk"]] for r in originals[table]]

    do_rotate = mode in {"rotate", "combined"}
    do_rewire = mode in {"rewire", "combined"}
    do_shift = mode in {"shift", "combined"}
    for table in TABLE_ORDER:
        meta = info[table]
        cols, pk, fks = meta["columns"], meta["pk"], meta["fks"]
        rows = originals[table]
        placeholders = ",".join("?" for _ in cols)
        col_sql = ",".join(f'"{c}"' for c in cols)
        for i, original in enumerate(rows):
            rotated = rows[(i + 1) % len(rows)] if do_rotate and len(rows) > 1 else original
            values = []
            for col in cols:
                if col == pk:
                    value = original[col] + offset
                elif col in fks:
                    ref = fks[col]["table"]
                    base = original[col]
                    ref_keys = keys[ref]
                    if do_rewire and len(ref_keys) > 1:
                        pos = ref_keys.index(base)
                        # Column-specific deterministic rotation avoids moving two FKs in lockstep.
                        step = 1 + (sum(ord(ch) for ch in table + "." + col) % (len(ref_keys) - 1))
                        base = ref_keys[(pos + step) % len(ref_keys)]
                    value = base + offset
                else:
                    value = rotated[col] if do_rotate else original[col]
                    if do_shift:
                        value = shifted(value, meta["types"][col], cohort_index)
                values.append(value)
            conn.execute(f'INSERT INTO "{table}" ({col_sql}) VALUES ({placeholders})', values)


def build_state(target: Path, modes: list[str]) -> dict[str, Any]:
    shutil.copy2(DB, target)
    conn = sqlite3.connect(target)
    try:
        conn.execute("PRAGMA foreign_keys=ON")
        info = schema_info(conn)
        for i, mode in enumerate(modes, start=1):
            append_cohort(conn, info, mode, i)
        conn.commit()
        meta = state_metadata(conn)
        if meta["integrity_check"] != ["ok"] or meta["foreign_key_violations"]:
            raise RuntimeError(f"invalid generated state {target.name}: {meta}")
        return meta
    finally:
        conn.close()


def freeze() -> None:
    # Prospective firewall: this function deliberately has no prediction path access.
    for path in (DB, QUESTIONS, PROTOCOL, CODE):
        if not path.is_file():
            raise FileNotFoundError(path)
    questions = [r for r in load_jsonl(QUESTIONS) if r["split"] == "test"]
    if len(questions) != 180 or len({r["question_id"] for r in questions}) != 180:
        raise RuntimeError("expected exactly 180 unique test questions")
    STATES.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    freeze_log = LOGS / "freeze.jsonl"
    freeze_log.write_text("", encoding="utf-8")
    state_records = []
    for name, modes in STATE_SPECS:
        target = STATES / f"{name}.sqlite"
        meta = build_state(target, modes)
        rec = {"state": name, "modes": modes, "path": target.relative_to(HERE).as_posix(), "sha256": sha(target), "bytes": target.stat().st_size, **meta}
        state_records.append(rec)
        append_jsonl(freeze_log, {"event": "state_frozen", "at_utc": now(), **rec})
    lock = {
        "schema_version": "ma-sqlgrid-semantic-reliability-freeze-v1",
        "status": "READY_AWAITING_INDEPENDENT_DESIGN_AUDIT",
        "frozen_at_utc": now(),
        "claim_boundary": "automated multi-state execution-agreement stress test; not human semantic audit",
        "design": {
            "questions": 180,
            "predictions_planned": 1440,
            "states": len(state_records),
            "state_specs": [{"state": n, "modes": m} for n, m in STATE_SPECS],
            "float_abs_tol": 1e-6,
            "all_predictions_all_states": True,
            "primary_estimand": "base-agreeing predictions that disagree on >=1 perturbation / all base-agreeing predictions",
        },
        "inputs_available_to_freeze": {
            str(DB.relative_to(ROOT)).replace("\\", "/"): {"sha256": sha(DB), "bytes": DB.stat().st_size},
            str(QUESTIONS.relative_to(ROOT)).replace("\\", "/"): {"sha256": sha(QUESTIONS), "bytes": QUESTIONS.stat().st_size},
            "PROTOCOL.md": {"sha256": sha(PROTOCOL), "bytes": PROTOCOL.stat().st_size},
            "semantic_reliability.py": {"sha256": sha(CODE), "bytes": CODE.stat().st_size},
        },
        "prediction_files_accessed_during_freeze": False,
        "states_manifest": state_records,
    }
    lock["freeze_content_sha256"] = canonical_hash(lock)
    write_json(FREEZE, lock)
    append_jsonl(freeze_log, {"event": "freeze_complete", "at_utc": now(), "freeze_content_sha256": lock["freeze_content_sha256"]})
    print(f"READY_AWAITING_INDEPENDENT_DESIGN_AUDIT {lock['freeze_content_sha256']} states={len(state_records)}")


def validate_freeze() -> dict[str, Any]:
    lock = json.loads(FREEZE.read_text(encoding="utf-8"))
    expected = lock.pop("freeze_content_sha256")
    actual = canonical_hash(lock)
    lock["freeze_content_sha256"] = expected
    if actual != expected:
        raise RuntimeError("freeze content hash mismatch")
    inputs = lock["inputs_available_to_freeze"]
    for label, path in [("PROTOCOL.md", PROTOCOL), ("semantic_reliability.py", CODE)]:
        if sha(path) != inputs[label]["sha256"]:
            raise RuntimeError(f"frozen input changed: {label}")
    for rec in lock["states_manifest"]:
        path = HERE / rec["path"]
        if sha(path) != rec["sha256"]:
            raise RuntimeError(f"state hash mismatch: {rec['state']}")
    return lock


def clean_sql(sql: str) -> tuple[bool, str, str]:
    text = sql.strip()
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", text, re.I | re.S)
    if fenced:
        text = fenced.group(1).strip()
    # The archived SQL contains no semicolons inside literals; fail closed here.
    statements = [s.strip() for s in text.split(";") if s.strip()]
    if len(statements) != 1:
        return False, text, "not_exactly_one_statement"
    statement = statements[0]
    if not re.match(r"^(select|with)\b", statement, re.I):
        return False, statement, "not_select_or_with"
    if FORBIDDEN.search(statement):
        return False, statement, "forbidden_token"
    return True, statement, ""


def normalize_value(v: Any, tol: float = 1e-6) -> Any:
    if v is None:
        return ["__NULL__"]
    if isinstance(v, float):
        if math.isnan(v):
            return ["__NAN__"]
        return round(v / tol) * tol
    return v


def norm_rows(rows: list[tuple[Any, ...]]) -> list[tuple[Any, ...]]:
    return [tuple(json.dumps(normalize_value(v), ensure_ascii=False, sort_keys=True) for v in row) for row in rows]


def rows_equal(a: list[tuple[Any, ...]], b: list[tuple[Any, ...]], ordered: bool) -> bool:
    aa, bb = norm_rows(a), norm_rows(b)
    return aa == bb if ordered else Counter(aa) == Counter(bb)


def result_hash(rows: list[tuple[Any, ...]], ordered: bool) -> str:
    normalized = norm_rows(rows)
    if not ordered:
        normalized = sorted(normalized)
    return canonical_hash(normalized)


def readonly_conn(path: Path) -> sqlite3.Connection:
    uri = path.resolve().as_uri() + "?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION}
    if hasattr(sqlite3, "SQLITE_RECURSIVE"):
        allowed.add(sqlite3.SQLITE_RECURSIVE)
    conn.set_authorizer(lambda action, _a, _b, _db, _src: sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY)
    return conn


def execute(conn: sqlite3.Connection, sql: str, timeout_s: float = 3.0) -> dict[str, Any]:
    safe, statement, error = clean_sql(sql)
    if not safe:
        return {"ok": False, "error_type": "safety_rejection", "error": error, "columns": [], "rows": []}
    deadline = time.monotonic() + timeout_s
    conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
    try:
        cur = conn.execute(statement)
        return {"ok": True, "error_type": None, "error": None, "columns": [d[0] for d in cur.description or []], "rows": [tuple(r) for r in cur.fetchall()]}
    except sqlite3.Error as exc:
        return {"ok": False, "error_type": "execution_error", "error": str(exc), "columns": [], "rows": []}
    finally:
        conn.set_progress_handler(None, 0)


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    try:
        from scipy.stats import beta
        lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
        hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
        return lo, hi
    except ImportError:
        # Wilson fallback is explicitly labeled in the output if SciPy is absent.
        p, z = k / n, 1.959963984540054
        den = 1 + z * z / n
        center = (p + z * z / (2 * n)) / den
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
        return max(0.0, center - half), min(1.0, center + half)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def run() -> None:
    lock = validate_freeze()
    if not INDEPENDENT_AUDIT.is_file():
        raise RuntimeError("formal scoring is locked until INDEPENDENT_DESIGN_AUDIT.json exists")
    audit = json.loads(INDEPENDENT_AUDIT.read_text(encoding="utf-8"))
    if audit.get("decision") != "PASS" or audit.get("freeze_content_sha256") != lock["freeze_content_sha256"]:
        raise RuntimeError("independent design audit must PASS this exact freeze SHA before scoring")
    questions = {r["question_id"]: r for r in load_jsonl(QUESTIONS) if r["split"] == "test"}
    predictions: list[dict[str, Any]] = []
    prediction_inputs = {}
    for backbone, path in PREDICTIONS.items():
        rows = load_jsonl(path)
        if len(rows) != 720 or any(r.get("status") != "success" for r in rows):
            raise RuntimeError(f"{backbone}: expected 720 successful archived predictions")
        if len({(r["question_id"], r["condition"]) for r in rows}) != 720:
            raise RuntimeError(f"{backbone}: duplicate or missing question-condition cell")
        for r in rows:
            r = dict(r); r["backbone"] = backbone; predictions.append(r)
        prediction_inputs[str(path.relative_to(ROOT)).replace("\\", "/")] = {"sha256": sha(path), "bytes": path.stat().st_size, "rows": len(rows)}
    if len(predictions) != 1440:
        raise RuntimeError("full denominator is not 1440")

    LOGS.mkdir(parents=True, exist_ok=True); TABLES.mkdir(parents=True, exist_ok=True)
    execution_log = LOGS / "execution.jsonl"; execution_log.write_text("", encoding="utf-8")
    per_prediction: dict[tuple[str, str, str], dict[str, Any]] = {}
    gold_cache: dict[tuple[str, str], dict[str, Any]] = {}
    all_records = []
    state_validity = []
    for state_rec in lock["states_manifest"]:
        state, path = state_rec["state"], HERE / state_rec["path"]
        # Integrity is checked on a separate unrestricted read-only connection before guarded execution.
        audit = sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
        try:
            meta = state_metadata(audit)
        finally:
            audit.close()
        valid = meta["integrity_check"] == ["ok"] and meta["foreign_key_violations"] == 0
        state_validity.append({"state": state, "valid": valid, **meta})
        if not valid:
            raise RuntimeError(f"state validation failed: {state}")
        conn = readonly_conn(path)
        try:
            for qid, q in sorted(questions.items()):
                g = execute(conn, q["gold_sql"])
                gold_cache[(state, qid)] = g
                if not g["ok"] or len(g["columns"]) != int(q["answer_shape"]["column_count"]):
                    raise RuntimeError(f"gold failed on {state}/{qid}: {g}")
            for pred in predictions:
                qid, q = pred["question_id"], questions[pred["question_id"]]
                gold = gold_cache[(state, qid)]
                got = execute(conn, pred["predicted_sql"])
                shape_ok = bool(got["ok"] and len(got["columns"]) == int(q["answer_shape"]["column_count"]))
                agree = bool(shape_ok and rows_equal(got["rows"], gold["rows"], bool(q["order_sensitive"])))
                key = (pred["backbone"], qid, pred["condition"])
                per_prediction.setdefault(key, {"backbone": pred["backbone"], "question_id": qid, "condition": pred["condition"], "features": q["sql_feature_tags"], "states": {}})
                per_prediction[key]["states"][state] = agree
                rec = {
                    "backbone": pred["backbone"], "question_id": qid, "condition": pred["condition"], "state": state,
                    "prediction_sql_sha256": hashlib.sha256(pred["predicted_sql"].encode()).hexdigest(),
                    "gold_ok": gold["ok"], "gold_columns": len(gold["columns"]), "gold_rows": len(gold["rows"]),
                    "gold_result_sha256": result_hash(gold["rows"], bool(q["order_sensitive"])),
                    "prediction_ok": got["ok"], "prediction_columns": len(got["columns"]), "prediction_rows": len(got["rows"]),
                    "prediction_result_sha256": result_hash(got["rows"], bool(q["order_sensitive"])) if got["ok"] else None,
                    "shape_ok": shape_ok, "agreement": agree, "error_type": got["error_type"], "error": got["error"],
                }
                all_records.append(rec); append_jsonl(execution_log, rec)
        finally:
            conn.close()

    expected_records = 1440 * len(STATE_SPECS)
    if len(all_records) != expected_records or len(per_prediction) != 1440:
        raise RuntimeError("incomplete full-denominator execution ledger")
    base = "S0_original"; perturbations = [n for n, _ in STATE_SPECS if n != base]
    row_summary = []
    for key in sorted(per_prediction):
        item = per_prediction[key]; states = item["states"]
        base_agree = bool(states[base]); suite_pass = bool(all(states[s] for s, _ in STATE_SPECS))
        failed = [s for s in perturbations if not states[s]]
        row_summary.append({
            "backbone": item["backbone"], "question_id": item["question_id"], "condition": item["condition"],
            "base_agreement": base_agree, "suite_pass": suite_pass,
            "false_frozen_state_agreement": bool(base_agree and not suite_pass),
            "failed_perturbation_count": len(failed) if base_agree else 0,
            "failed_perturbations": "|".join(failed) if base_agree else "",
            "features": "|".join(item["features"]),
        })

    base_n = sum(r["base_agreement"] for r in row_summary)
    false_n = sum(r["false_frozen_state_agreement"] for r in row_summary)
    suite_n = sum(r["suite_pass"] for r in row_summary)
    ci_lo, ci_hi = clopper_pearson(false_n, base_n)
    state_summary = []
    for state, _ in STATE_SPECS:
        agreement = sum(per_prediction[k]["states"][state] for k in per_prediction)
        false_from_base = sum(per_prediction[k]["states"][base] and not per_prediction[k]["states"][state] for k in per_prediction)
        state_summary.append({"state": state, "agreement_n": agreement, "denominator": 1440, "agreement_rate": agreement / 1440, "base_agreements_lost_n": false_from_base, "base_agreement_denominator": base_n})

    strata = []
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in row_summary: groups[(r["backbone"], r["condition"])].append(r)
    for (backbone, condition), rr in sorted(groups.items()):
        bn = sum(x["base_agreement"] for x in rr); fn = sum(x["false_frozen_state_agreement"] for x in rr)
        lo, hi = clopper_pearson(fn, bn)
        strata.append({"backbone": backbone, "condition": condition, "n": len(rr), "base_agreement_n": bn, "suite_pass_n": sum(x["suite_pass"] for x in rr), "false_agreement_n": fn, "false_agreement_rate_among_base": fn / bn if bn else None, "ci95_low": lo, "ci95_high": hi})

    feature_rows = []
    features = sorted({f for q in questions.values() for f in q["sql_feature_tags"]})
    for feature in features:
        rr = [r for r in row_summary if feature in r["features"].split("|")]
        bn = sum(x["base_agreement"] for x in rr); fn = sum(x["false_frozen_state_agreement"] for x in rr)
        feature_rows.append({"feature": feature, "prediction_n": len(rr), "base_agreement_n": bn, "false_agreement_n": fn, "false_agreement_rate_among_base": fn / bn if bn else None})

    write_csv(TABLES / "prediction_level_outcomes.csv", row_summary, list(row_summary[0]))
    write_csv(TABLES / "false_frozen_state_agreements.csv", [r for r in row_summary if r["false_frozen_state_agreement"]], list(row_summary[0]))
    write_csv(TABLES / "state_summary.csv", state_summary, list(state_summary[0]))
    write_csv(TABLES / "backbone_condition_summary.csv", strata, list(strata[0]))
    write_csv(TABLES / "feature_summary.csv", feature_rows, list(feature_rows[0]))

    errors = Counter((r["state"], r["error_type"]) for r in all_records if r["error_type"])
    result = {
        "schema_version": "ma-sqlgrid-semantic-reliability-results-v1",
        "completed_at_utc": now(), "freeze_content_sha256": lock["freeze_content_sha256"],
        "claim_boundary": lock["claim_boundary"], "prediction_inputs": prediction_inputs,
        "denominators": {"questions": 180, "predictions": 1440, "states": len(STATE_SPECS), "prediction_state_executions": expected_records},
        "primary": {"original_state_agreement_n": base_n, "original_state_agreement_rate": base_n / 1440, "multi_state_suite_pass_n": suite_n, "multi_state_suite_pass_rate": suite_n / 1440, "false_frozen_state_agreement_n": false_n, "false_agreement_denominator": base_n, "false_agreement_rate": false_n / base_n if base_n else None, "false_agreement_ci95_clopper_pearson": [ci_lo, ci_hi]},
        "gold": {"executions": 180 * len(STATE_SPECS), "failures": 0, "shape_failures": 0},
        "prediction_execution_errors": [{"state": s, "error_type": e, "n": n} for (s, e), n in sorted(errors.items())],
        "state_validity": state_validity, "state_summary": state_summary,
        "backbone_condition_summary": strata, "feature_summary": feature_rows,
        "limitations": [
            "Automated SQL-to-gold execution agreement is not a human audit of question-to-gold semantic correctness.",
            "Perturbed states are schema-valid synthetic stress states, not operator-certified grid snapshots.",
            "The suite can reveal some accidental agreements but cannot prove semantic equivalence over all possible database states.",
        ],
    }
    write_json(RESULTS, result)
    report = f"""# Multi-state SQL reliability result\n\n## Outcome\n\nThe frozen run evaluated all **1,440 predictions on all {len(STATE_SPECS)} states** ({expected_records:,} prediction-state executions), plus {180 * len(STATE_SPECS):,} gold executions.  All gold queries executed with their declared width; no records were excluded.\n\nOn the original frozen database, **{base_n}/{1440}** predictions agreed with gold.  Across all states, **{suite_n}/{1440}** passed the complete suite.  Among the {base_n} original-state agreements, **{false_n}/{base_n} ({false_n/base_n:.1%})** failed on at least one perturbation (exact 95% Clopper--Pearson interval {ci_lo:.1%}--{ci_hi:.1%}).  These are false *frozen-state execution agreements* under the prespecified test suite, not proof that the prediction is linguistically wrong.\n\n## Interpretation boundary\n\nThis prospectively frozen automated suite addresses single-snapshot fragility.  It does **not** replace manual semantic review of the 180 natural-language/gold pairs.  Passing all states is stronger evidence than passing one state, but is not proof of equivalence over arbitrary databases.  Generated states satisfy unchanged-schema integrity, foreign keys, NOT NULL constraints, and gold executability; they are not operator-certified power-grid records.\n\n## Reproducibility\n\nFreeze SHA-256: `{lock['freeze_content_sha256']}`.  State files and hashes are locked in `FREEZE_LOCK.json`.  `logs/execution.jsonl` contains the full {expected_records:,}-row execution ledger; CSV tables preserve the 1,440-row denominator and every detected false agreement.\n"""
    (HERE / "REPORT.md").write_text(report, encoding="utf-8")
    release_files = [FREEZE, RESULTS, HERE / "REPORT.md", execution_log, LOGS / "freeze.jsonl", *sorted(TABLES.glob("*.csv")), *sorted(STATES.glob("*.sqlite"))]
    manifest = {"schema_version": "ma-sqlgrid-semantic-reliability-release-v1", "created_at_utc": now(), "freeze_content_sha256": lock["freeze_content_sha256"], "artifacts": [{"path": p.relative_to(HERE).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size} for p in release_files]}
    write_json(HERE / "release_manifest.json", manifest)
    print(f"COMPLETE base={base_n}/1440 suite={suite_n}/1440 false={false_n}/{base_n}")


def verify() -> None:
    lock = validate_freeze()
    for rec in lock["states_manifest"]:
        conn = sqlite3.connect((HERE / rec["path"]).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)
        try:
            meta = state_metadata(conn)
        finally:
            conn.close()
        assert meta["integrity_check"] == ["ok"] and meta["foreign_key_violations"] == 0
    if RESULTS.exists():
        res = json.loads(RESULTS.read_text(encoding="utf-8"))
        assert res["denominators"] == {"questions": 180, "predictions": 1440, "states": 7, "prediction_state_executions": 10080}
        assert res["gold"]["failures"] == 0 and res["gold"]["shape_failures"] == 0
        assert sum(1 for _ in (LOGS / "execution.jsonl").open(encoding="utf-8")) == 10080
        manifest = json.loads((HERE / "release_manifest.json").read_text(encoding="utf-8"))
        for item in manifest["artifacts"]:
            assert sha(HERE / item["path"]) == item["sha256"]
    print("VERIFY PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["freeze", "run", "verify"])
    args = parser.parse_args()
    {"freeze": freeze, "run": run, "verify": verify}[args.command]()


if __name__ == "__main__":
    main()
