#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Negative-control generator for MA-SQLGrid stage 2 (protocol v1.1).

Samples 30 source items (15 RTS + 15 SimBench) with random.Random(20260807),
applies exactly one deterministic SQL perturbation per item from the five frozen
families, verifies each control in the read-only SQLite sandbox, and writes
runs/ma_stage2/negative_controls_manifest.json.

Equivalence guard: if the perturbed SQL returns exactly the same result set as
the original (degenerate case, e.g. dropping a redundant predicate), the next
family is tried. If no family works for a source item, a replacement source is
drawn deterministically from the remaining pool. All decisions are logged in
the manifest; nothing is deleted.
"""
import json
import random
import re
import sqlite3
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_annotation_pilot import (  # noqa: E402
    SEED, MA_DBS, PILOT_DIR, load_ma_items, utc_now,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FAMILIES = ["drop_filter", "wrong_filter_value", "wrong_column",
            "drop_order", "wrong_aggregation"]

ORDER_CUES = re.compile(
    r"\b(top|most|least|highest|lowest|largest|smallest|latest|earliest|"
    r"recent|first|last|order(?:ed)?|rank|bottom)\b", re.I)

AGG_SWAP = {"SUM": "AVG", "AVG": "MAX", "MAX": "MIN", "MIN": "SUM", "COUNT": "SUM"}


# ---------------------------------------------------------------------------
# read-only helpers
# ---------------------------------------------------------------------------

def _ro_uri(db_path):
    p = str(Path(db_path).resolve()).replace("\\", "/")
    return "file:" + urllib.parse.quote(p, safe="/:") + "?mode=ro"


def ro_connect(db_path):
    conn = sqlite3.connect(_ro_uri(db_path), uri=True, timeout=10)
    conn.execute("PRAGMA query_only=ON")
    return conn


def exec_rows(db_path, sql, timeout_s=10, row_cap=5000):
    """Execute read-only, return (ok, rows_as_tuples, cols, error)."""
    t0 = time.monotonic()
    try:
        conn = ro_connect(db_path)
        try:
            deadline = t0 + timeout_s
            conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
            cur = conn.execute(sql)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = [tuple(r) for r in cur.fetchmany(row_cap + 1)][:row_cap]
            return True, rows, cols, None
        finally:
            conn.close()
    except Exception as e:
        return False, None, None, f"{type(e).__name__}: {e}"[:200]


def table_columns(db_path, table):
    conn = ro_connect(db_path)
    try:
        return [r[1] for r in conn.execute(f'PRAGMA table_info("{table}")')]
    finally:
        conn.close()


def distinct_values(db_path, table, column, cap=200):
    conn = ro_connect(db_path)
    try:
        rows = conn.execute(
            f'SELECT DISTINCT "{column}" FROM "{table}" WHERE "{column}" IS NOT NULL '
            f'LIMIT {cap}').fetchall()
        return sorted(r[0] for r in rows)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# SQL string transforms (each returns perturbed SQL or None if inapplicable)
# ---------------------------------------------------------------------------

def _strip_semi(sql):
    s = sql.strip()
    if s.endswith(";"):
        return s[:-1], True
    return s, False


def _clause_bounds(body, keyword_regex):
    """Return (match_start, match_end, tail_after_clause) for a clause like WHERE."""
    m = re.search(keyword_regex, body, re.I)
    if not m:
        return None
    tail = body[m.end():]
    em = re.search(r"\b(GROUP\s+BY|ORDER\s+BY|LIMIT|HAVING)\b", tail, re.I)
    clause = tail[:em.start()] if em else tail
    rest = tail[em.start():] if em else ""
    return m, clause, rest


def t_drop_filter(sql, **_):
    body, semi = _strip_semi(sql)
    b = _clause_bounds(body, r"\bWHERE\b")
    if not b:
        return None
    m, clause, rest = b
    if re.search(r"\bOR\b", clause, re.I):
        return None  # OR logic too risky to split safely
    parts = [p.strip() for p in re.split(r"\bAND\b", clause, flags=re.I) if p.strip()]
    if len(parts) > 1:
        new = (body[:m.start()] + "WHERE " + " AND ".join(parts[:-1])
               + (" " + rest.strip() if rest.strip() else ""))
    else:
        new = body[:m.start()].rstrip() + (" " + rest.strip() if rest.strip() else "")
    return new + (";" if semi else "")


def t_wrong_filter_value(sql, db_path=None, **_):
    body, semi = _strip_semi(sql)
    b = _clause_bounds(body, r"\bWHERE\b")
    if not b:
        return None
    m, clause, rest = b
    lm = re.search(r"((?:\w+\.)?(\w+))\s*=\s*'([^']*)'", clause)
    if not lm:
        return None
    col, cur_val = lm.group(2), lm.group(3)
    tm = re.search(r'\bFROM\s+"?(\w+)"?', body, re.I)
    if not tm:
        return None
    table = tm.group(1)
    try:
        cols = table_columns(db_path, table)
    except Exception:
        return None
    if col not in cols:
        return None
    try:
        vals = [v for v in distinct_values(db_path, table, col) if isinstance(v, str)]
    except Exception:
        return None
    alt = next((v for v in vals if v != cur_val), None)
    if alt is None:
        return None
    new_clause = clause[:lm.start()] + clause[lm.start():].replace(
        f"'{cur_val}'", f"'{alt}'", 1) + clause[lm.end():]
    new = body[:m.end()] + new_clause + rest
    return new + (";" if semi else "")


def _split_top_level(s, sep=","):
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def t_wrong_column(sql, db_path=None, **_):
    body, semi = _strip_semi(sql)
    sm = re.search(r"\bSELECT\b", body, re.I)
    fm = re.search(r"\bFROM\b", body, re.I)
    if not sm or not fm or fm.start() <= sm.end():
        return None
    sel = body[sm.end():fm.start()]
    tm = re.search(r'\bFROM\s+"?(\w+)"?', body, re.I)
    if not tm:
        return None
    table = tm.group(1)
    try:
        cols = table_columns(db_path, table)
    except Exception:
        return None
    items = _split_top_level(sel)
    for i, it in enumerate(items):
        im = re.match(r'^\s*(?:(\w+)\.)?"?(\w+)"?\s*(?:AS\s+"?\w+"?)?\s*$', it, re.I)
        if not im:
            continue  # not a bare column (aggregate, *, expression)
        col = im.group(2)
        if col not in cols:
            continue
        used = {m2.group(2).lower() for m2 in
                (re.match(r'^\s*(?:(\w+)\.)?"?(\w+)"?', x) for x in items) if m2}
        alt = next((c for c in cols if c.lower() != col.lower()
                    and c.lower() not in used), None)
        if alt is None:
            return None
        items[i] = it.replace(col, alt, 1)
        new = body[:sm.end()] + ",".join(items) + body[fm.start():]
        return new + (";" if semi else "")
    return None


def t_drop_order(sql, question="", **_):
    if not re.search(r"\bORDER\s+BY\b", sql, re.I):
        return None
    # protocol: only when the question implies ordering/limit
    if not (ORDER_CUES.search(question or "") or re.search(r"\bLIMIT\b", sql, re.I)):
        return None
    body, semi = _strip_semi(sql)
    m = re.search(r"\bORDER\s+BY\b", body, re.I)
    tail = body[m.end():]
    em = re.search(r"\bLIMIT\b", tail, re.I)
    rest = tail[em.start():] if em else ""
    new = body[:m.start()].rstrip() + (" " + rest.strip() if rest.strip() else "")
    return new + (";" if semi else "")


def t_wrong_aggregation(sql, **_):
    m = re.search(r"\b(AVG|SUM|MAX|MIN|COUNT)\s*\(\s*([^*][^)]*?)\s*\)", sql, re.I)
    if not m:
        return None  # no aggregate, or only COUNT(*)
    fn = m.group(1).upper()
    new_fn = AGG_SWAP[fn]
    return sql[:m.start(1)] + new_fn + sql[m.end(1):]


TRANSFORMS = {
    "drop_filter": t_drop_filter,
    "wrong_filter_value": t_wrong_filter_value,
    "wrong_column": t_wrong_column,
    "drop_order": t_drop_order,
    "wrong_aggregation": t_wrong_aggregation,
}


# ---------------------------------------------------------------------------
# control construction
# ---------------------------------------------------------------------------

def try_make_control(item, row_cache, family_counts=None):
    """Try families in a deterministic balancing order: least-used family first
    (ties broken by frozen FAMILIES order). Returns (record, log)."""
    db_path = MA_DBS[item["dataset_id"]]
    qid = item["question_id"]
    if family_counts:
        fam_order = sorted(FAMILIES, key=lambda f: (family_counts.get(f, 0),
                                                    FAMILIES.index(f)))
    else:
        fam_order = FAMILIES[:]
    log = []
    if qid not in row_cache:
        row_cache[qid] = exec_rows(db_path, item["sql"])
    ok1, rows1, cols1, err1 = row_cache[qid]
    if not ok1:
        return None, [{"family": None, "verdict": "source_not_executable", "error": err1}]
    for fam in fam_order:
        try:
            sql2 = TRANSFORMS[fam](sql=item["sql"], db_path=db_path,
                                   question=item["question"])
        except Exception as e:
            log.append({"family": fam, "verdict": "transform_error",
                        "error": f"{type(e).__name__}: {e}"[:150]})
            continue
        if not sql2 or sql2.strip() == item["sql"].strip():
            log.append({"family": fam, "verdict": "inapplicable"})
            continue
        ok2, rows2, cols2, err2 = exec_rows(db_path, sql2)
        if not ok2:
            log.append({"family": fam, "verdict": "perturbed_not_executable", "error": err2})
            continue
        if rows1 == rows2 and cols1 == cols2:
            # degenerate: perturbation did not change the result -> semantically equivalent
            log.append({"family": fam, "verdict": "equivalent_result_rejected"})
            continue
        log.append({"family": fam, "verdict": "accepted",
                    "row_count_orig": len(rows1), "row_count_neg": len(rows2)})
        rec = {
            "control_id": f"NEG_{qid}__{fam}",
            "source_question_id": qid,
            "dataset_id": item["dataset_id"],
            "template_family": item.get("template_family"),
            "family": fam,
            "question": item["question"],
            "original_sql": item["sql"],
            "perturbed_sql": sql2,
            "expected": {"semantically_correct": False},
            "sandbox_check": {"executable": True, "row_count_orig": len(rows1),
                              "row_count_neg": len(rows2),
                              "result_sets_differ": True},
        }
        return rec, log
    return None, log


def load_sealed_ma_items():
    """Stage-3 sealed items normalized to the generator's item shape."""
    pkt = PILOT_DIR / "runs/ma_stage3/sealed_questions.jsonl"
    items = []
    for line in pkt.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        items.append({"question_id": r["question_id"], "dataset_id": r["dataset_id"],
                      "question": r["question"], "sql": r["gold_sql"],
                      "template_family": r["template_family"]})
    return items


def build_controls(rts, sb, out_dir, stage_label, protocol_sha256, sampling_rule):
    rng = random.Random(SEED)
    rts_sel = rng.sample(rts, 15)
    sb_sel = rng.sample(sb, 15)
    # deterministic fallback pools (original file order, excluding selected)
    rts_pool = [it for it in rts if it not in rts_sel]
    sb_pool = [it for it in sb if it not in sb_sel]

    controls, gen_log = [], []
    row_cache = {}
    family_counts = {f: 0 for f in FAMILIES}
    for pool_name, selected, pool in (("RTS", rts_sel, rts_pool), ("SB", sb_sel, sb_pool)):
        made = 0
        queue = list(selected)
        while made < 15 and queue:
            item = queue.pop(0)
            rec, log = try_make_control(item, row_cache, family_counts)
            gen_log.append({"source": item["question_id"], "accepted": rec is not None,
                            "attempts": log})
            if rec is not None:
                controls.append(rec)
                family_counts[rec["family"]] += 1
                made += 1
            elif pool:
                replacement = pool.pop(0)
                gen_log.append({"source": item["question_id"], "accepted": False,
                                "note": f"all families failed; replaced by {replacement['question_id']}"})
                queue.append(replacement)
        if made < 15:
            raise SystemExit(f"FATAL: could only build {made}/15 controls for {pool_name}")

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "stage": stage_label, "seed": SEED, "generated_at": utc_now(),
        "protocol_sha256": protocol_sha256,
        "sampling_rule": sampling_rule,
        "n_controls": len(controls),
        "family_distribution": {f: sum(1 for c in controls if c["family"] == f)
                                for f in FAMILIES},
        "controls": controls,
        "generation_log": gen_log,
    }
    with open(out_dir / "negative_controls_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[ok] {len(controls)} controls -> {out_dir / 'negative_controls_manifest.json'}")
    print("[ok] family distribution:", manifest["family_distribution"])
    replaced = [g for g in gen_log if g.get("note")]
    print(f"[ok] sources replaced: {len(replaced)}; "
          f"transform attempts logged: {sum(len(g.get('attempts', [])) for g in gen_log)}")


def main():
    if "--stage3" in sys.argv:
        items = load_sealed_ma_items()
        rts = [it for it in items if it["dataset_id"] == "RTS_GMLC_AUTO_PILOT"]
        sb = [it for it in items if it["dataset_id"] == "SIMBENCH_AUTO_PILOT"]
        build_controls(
            rts, sb, PILOT_DIR / "runs/ma_stage3",
            stage_label="ma_stage3_negative_controls",
            protocol_sha256="FC422FEF02B278D60B6E3850604EAB2E02F0683F7AF02115B6153FB36DC32A4E",
            sampling_rule="same rules as stage 2: Random(20260807).sample(45 sealed RTS, 15) "
                          "then .sample(40 sealed SimBench, 15); least-used family first; "
                          "fallback from unselected pool in file order")
        return
    items = load_ma_items()
    rts = [it for it in items if it["dataset_id"] == "RTS_GMLC_AUTO_PILOT"]
    sb = [it for it in items if it["dataset_id"] == "SIMBENCH_AUTO_PILOT"]
    build_controls(
        rts, sb, PILOT_DIR / "runs/ma_stage2",
        stage_label="ma_stage2_negative_controls",
        protocol_sha256="926a08269217ef8337a8819ffd38db2433ebe6065be208240d1e40c938c7b75c",
        sampling_rule="Random(20260807).sample(55 RTS, 15) then .sample(36 SimBench, 15); "
                      "per-item family order = least-used family first, ties by frozen family "
                      "order (deterministic balancing); "
                      "fallback: next item from the unselected pool in file order")


if __name__ == "__main__":
    main()
