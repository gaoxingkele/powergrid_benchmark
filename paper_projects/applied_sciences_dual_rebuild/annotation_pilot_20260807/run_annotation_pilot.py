#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual-annotator (A: DeepSeek, B: Gemini) + adjudicator (C: GPT via Cloubic)
annotation pilot runner, per frozen protocols:
  - C2GES_ANNOTATION_PROTOCOL_v1.json   (sha256 030AE44A...)
  - MA_SQLGRID_ANNOTATION_PROTOCOL_v1.json (sha256 6D5A0398...)

Governance red lines enforced here:
  - outputs are machine-adjudicated SILVER labels, never human/expert gold
  - failed / disagreed records are never deleted (append-only ledgers)
  - no retry because a result is "disliked"; only one retry on technical
    failure (timeout / 5xx / network error)
  - API keys are read from .env / .env.cloubic at runtime and never logged

Usage:
  python run_annotation_pilot.py --paper c2ges|ma|both [--limit N]
Resume: items with both A and B labels already recorded are skipped.
"""

import argparse
import csv
import datetime
import hashlib
import json
import random
import sqlite3
import sys
import time
import urllib.parse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None
    import urllib.request

ROOT = Path("D:/aicoding/powergrid_benchmark")
PILOT_DIR = ROOT / "paper_projects/applied_sciences_dual_rebuild/annotation_pilot_20260807"

# frozen protocol hashes (task-frozen, verified 2026-08-07)
PROTOCOLS = {
    "c2ges": {
        "path": PILOT_DIR / "C2GES_ANNOTATION_PROTOCOL_v1.json",
        "sha256": "030ae44abe53975cb3838fbc898723523c4bec7be11a433edb8654aea2dc706d",
    },
    "ma": {
        "path": PILOT_DIR / "MA_SQLGRID_ANNOTATION_PROTOCOL_v1.json",
        "sha256": "6d5a0398083def9762295e13365636ca4ae9434b785371e88df9773ac1dd1ff5",
    },
}

C2GES_PACKET = ROOT / "paper_projects/2026_c2ges_engineeringletters/workspace/simulated_expert_reannotation_2026-07-24/blind_packet.jsonl"

MA_BASE = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid"
MA_RTS_QUESTIONS = MA_BASE / "data/rts_gmlc_pilot/artifacts/questions_auto_candidate.jsonl"
MA_SB_QUESTIONS = MA_BASE / "data/simbench_pilot/questions_auto_candidate.csv"
MA_SQL_STATUS = MA_BASE / "external_protocol/artifacts/reference_sql_evaluation.jsonl"
MA_DBS = {
    "RTS_GMLC_AUTO_PILOT": MA_BASE / "data/rts_gmlc_pilot/artifacts/database.sqlite",
    "SIMBENCH_AUTO_PILOT": MA_BASE / "data/simbench_pilot/simbench_mv_urban.sqlite",
}

SEED = 20260807
MAX_TOTAL_CALLS = 400
CONSEC_FAIL_LIMIT = 5
HTTP_TIMEOUT = (10, 120)  # (connect, read) seconds; raised to 120s for stage 2 (Cloubic read-timeouts)
MAX_TECHNICAL_RETRIES = 2  # stage-2 policy: up to 2 retries on timeout/5xx/network, all recorded

C2GES_EVIDENCE_ROLES = ["direct_answer", "partial_answer", "background", "insufficient"]
C2GES_FLAG_KEYS = ["cross_sentence", "negation", "condition", "time_qualifier", "entity_ambiguity"]
CONFIDENCE_LEVELS = ["high", "medium", "low"]
MA_ERROR_CLASSES = ["none", "semantic_mismatch", "syntax_risk", "unsafe",
                    "incomplete_answer", "not_answerable", "other"]
MA_ISSUE_KEYS = ["wrong_columns", "wrong_filter", "wrong_aggregation", "wrong_join",
                 "wrong_order_or_limit", "wrong_units_or_time_range", "incomplete_answer"]

# ---------------------------------------------------------------------------
# env / config
# ---------------------------------------------------------------------------

def load_env():
    env = {}
    for name in (".env", ".env.cloubic"):
        p = ROOT / name
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def verify_protocols():
    for key, spec in PROTOCOLS.items():
        h = hashlib.sha256(spec["path"].read_bytes()).hexdigest()
        if h != spec["sha256"]:
            raise SystemExit(f"FATAL: protocol hash mismatch for {key}: {h} != {spec['sha256']}")
    print("[ok] protocol hashes verified")


# ---------------------------------------------------------------------------
# stop gates
# ---------------------------------------------------------------------------

class Gates:
    def __init__(self, max_calls=MAX_TOTAL_CALLS):
        self.max_calls = max_calls
        self.total_calls = 0
        self.consec_fail = {"A": 0, "B": 0, "C": 0}
        self.halted = {}          # role -> reason
        self.events = []          # gate event log entries

    def log_event(self, msg):
        entry = {"ts": utc_now(), "event": msg}
        self.events.append(entry)
        print(f"[gate] {msg}")

    def can_call(self, role):
        if role in self.halted:
            return False, f"model {role} halted: {self.halted[role]}"
        if "ALL" in self.halted:
            return False, self.halted["ALL"]
        if self.total_calls >= self.max_calls:
            self.halted["ALL"] = f"total call cap {self.max_calls} reached"
            self.log_event(self.halted["ALL"])
            return False, self.halted["ALL"]
        return True, None

    def record_success(self, role):
        self.consec_fail[role] = 0

    def record_failure(self, role, kind):
        # kind in {"auth", "format"} counts toward consecutive-failure gate
        if kind in ("auth", "format"):
            self.consec_fail[role] += 1
            if self.consec_fail[role] >= CONSEC_FAIL_LIMIT and role not in self.halted:
                self.halted[role] = f"{CONSEC_FAIL_LIMIT} consecutive {kind} failures"
                self.log_event(f"HALT model {role}: {self.halted[role]}")
        # technical failures (timeout/5xx/network) do not increment the counter

    def check_served_id(self, role, served):
        """Return True if acceptable. DeepSeek v4-flash rolling alias is allowed."""
        if not served:
            return True  # not reported; nothing to check
        expected = {"A": "deepseek-chat", "B": "gemini-2.5-flash", "C": "gpt-5.4"}[role]
        if served == expected:
            return True
        if role == "A" and served == "deepseek-v4-flash":
            self.log_event(f"note: DeepSeek served id 'deepseek-v4-flash' (rolling alias of deepseek-chat, expected per briefing)")
            return True
        # versioned variant of the frozen id (e.g. gpt-5.4-2026-xx): warn, continue, recorded
        if served.startswith(expected + "-") or served.startswith(expected + ":"):
            self.log_event(f"warning: model {role} served id '{served}' is a versioned variant of frozen '{expected}' (recorded, continuing)")
            return True
        self.halted[role] = f"served model id '{served}' differs from frozen '{expected}'"
        self.log_event(f"HALT model {role}: {self.halted[role]}")
        return False


GATES = Gates()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# ledger
# ---------------------------------------------------------------------------

class Ledger:
    """Append-only raw call ledger for one pilot run directory."""

    def __init__(self, run_dir, filename="raw_ledger.jsonl"):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.run_dir / filename

    def append(self, record):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def count_calls(self):
        if not self.path.exists():
            return 0
        n = 0
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                try:
                    if json.loads(line).get("record_type") == "llm_call":
                        n += 1
                except Exception:
                    pass
        return n


def append_jsonl(path, record):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path):
    out = []
    if not Path(path).exists():
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


# ---------------------------------------------------------------------------
# LLM clients
# ---------------------------------------------------------------------------

def _http_post_json(url, headers, payload, timeout):
    """Returns (status_code, response_json_or_none, raw_text, error_kind)."""
    if requests is not None:
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            try:
                body = r.json()
            except Exception:
                body = None
            kind = None
            if r.status_code in (401, 403):
                kind = "auth"
            elif r.status_code >= 500:
                kind = "server"
            elif r.status_code >= 400:
                kind = "client"
            return r.status_code, body, r.text, kind
        except requests.exceptions.Timeout:
            return None, None, "", "timeout"
        except requests.exceptions.RequestException:
            return None, None, "", "network"
    else:  # urllib fallback
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout[1] if isinstance(timeout, tuple) else timeout) as resp:
                text = resp.read().decode("utf-8", errors="replace")
                try:
                    body = json.loads(text)
                except Exception:
                    body = None
                return resp.status, body, text, None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", errors="replace") if e.fp else ""
            kind = "auth" if e.code in (401, 403) else ("server" if e.code >= 500 else "client")
            return e.code, None, text, kind
        except Exception:
            return None, None, "", "timeout"


def llm_call(role, prompt, env, ledger, item_id):
    """
    One LLM call with stop gates, one allowed retry on technical failure.
    Returns dict: {ok, text, served_model_id, usage_in, usage_out, latency_s, error}
    Never logs API keys.
    """
    ok, reason = GATES.can_call(role)
    if not ok:
        return {"ok": False, "error": f"gate blocked: {reason}", "skipped": True}

    if role == "A":
        url = env["DEEPSEEK_BASE_URL"].rstrip("/") + "/chat/completions"
        headers = {"Authorization": "Bearer " + env["DEEPSEEK_API_KEY"]}
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 1024,
        }
        extract = lambda b: (
            b["choices"][0]["message"]["content"],
            b.get("model"),
            (b.get("usage") or {}).get("prompt_tokens"),
            (b.get("usage") or {}).get("completion_tokens"),
        )
    elif role == "B":
        url = ("https://generativelanguage.googleapis.com/v1beta/models/"
               "gemini-2.5-flash:generateContent")
        headers = {"x-goog-api-key": env["GEMINI_API_KEY"], "Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            # thinkingBudget=0: gemini-2.5-flash is a thinking model; without this the
            # thinking tokens consume the frozen 1024-token output budget and truncate
            # the JSON (observed in smoke run). Output cap stays maxOutputTokens=1024.
            "generationConfig": {"temperature": 0, "maxOutputTokens": 1024,
                                 "thinkingConfig": {"thinkingBudget": 0}},
        }
        def extract(b):
            text = b["candidates"][0]["content"]["parts"][0]["text"]
            um = b.get("usageMetadata") or {}
            return text, b.get("modelVersion"), um.get("promptTokenCount"), um.get("candidatesTokenCount")
    else:  # role == "C"
        url = env["CLOUBIC_BASE_URL"]  # already the full /v1/chat/completions URL
        headers = {"Authorization": "Bearer " + env["CLOUBIC_API_KEY"]}
        payload = {
            "model": "gpt-5.4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 1024,
        }
        extract = lambda b: (
            b["choices"][0]["message"]["content"],
            b.get("model"),
            (b.get("usage") or {}).get("prompt_tokens"),
            (b.get("usage") or {}).get("completion_tokens"),
        )

    prompt_sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    attempts = []
    final = {"ok": False, "error": "not attempted"}
    for attempt in range(1, MAX_TECHNICAL_RETRIES + 2):  # 1 initial + up to 2 retries
        GATES.total_calls += 1
        t0 = time.monotonic()
        status, body, raw_text, err_kind = _http_post_json(url, headers, payload, HTTP_TIMEOUT)
        latency = round(time.monotonic() - t0, 3)

        served, usage_in, usage_out, text = None, None, None, None
        call_error = None
        if err_kind is None and status == 200 and body is not None:
            try:
                text, served, usage_in, usage_out = extract(body)
            except Exception as e:
                call_error = f"response_shape_error: {type(e).__name__}"
                err_kind = "format"
        else:
            call_error = f"http_{status}" if status else f"{err_kind}_error"

        rec = {
            "record_type": "llm_call",
            "ts": utc_now(),
            "pilot": ledger.run_dir.name,
            "item_id": item_id,
            "model_role": role,
            "attempt": attempt,
            "served_model_id": served,
            "prompt_sha256": prompt_sha,
            "input_tokens": usage_in,
            "output_tokens": usage_out,
            "latency_s": latency,
            "http_status": status,
            "error": call_error,
            "raw_response_text": text if text is not None else (raw_text[:4000] if raw_text else None),
        }
        ledger.append(rec)
        attempts.append(rec)

        if call_error is None:
            if not GATES.check_served_id(role, served):
                return {"ok": False, "error": f"served id gate halt: {served}", "attempts": len(attempts)}
            GATES.record_success(role)
            final = {"ok": True, "text": text, "served_model_id": served,
                     "usage_in": usage_in, "usage_out": usage_out,
                     "latency_s": latency, "attempts": len(attempts)}
            break

        # failure path
        if err_kind == "auth":
            GATES.record_failure(role, "auth")
            final = {"ok": False, "error": call_error, "error_kind": "auth", "attempts": len(attempts)}
            break  # no retry on auth failure
        if err_kind in ("timeout", "server", "network") and attempt <= MAX_TECHNICAL_RETRIES and role not in GATES.halted:
            ok2, _ = GATES.can_call(role)
            if ok2:
                continue  # technical retry, recorded above
        if err_kind == "format":
            GATES.record_failure(role, "format")
        final = {"ok": False, "error": call_error, "error_kind": err_kind or "http", "attempts": len(attempts)}
        break
    return final


# ---------------------------------------------------------------------------
# JSON extraction + schema validation
# ---------------------------------------------------------------------------

def extract_json(text):
    """Strip markdown fences and extract the first JSON object."""
    if text is None:
        return None, "empty response"
    t = text.strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        t = "\n".join(lines).strip()
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None, "no JSON object found"
    try:
        return json.loads(t[start:end + 1]), None
    except json.JSONDecodeError as e:
        return None, f"json parse error: {e}"


def _norm_enum(v, allowed):
    if isinstance(v, str):
        v2 = v.strip().lower().replace(" ", "_").replace("-", "_")
        if v2 in allowed:
            return v2
    return None


def validate_c2ges_label(obj, qid, valid_sids):
    """Returns (normalized_label_or_none, checks_dict)."""
    checks = {"json_parses": True, "schema_ok": True, "sids_exist": True,
              "evidence_nonempty_when_answerable": True, "no_duplicate_sids": True,
              "qid_echo": True, "warnings": []}
    if not isinstance(obj, dict):
        checks["schema_ok"] = False
        return None, checks
    required = ["qid", "answerable", "evidence_sentence_ids", "evidence_role", "flags",
                "answer_summary", "confidence", "rationale", "abstain", "abstain_reason"]
    for k in required:
        if k not in obj:
            checks["schema_ok"] = False
            checks["warnings"].append(f"missing key {k}")
    if not checks["schema_ok"]:
        return None, checks
    lab = {}
    lab["qid"] = obj.get("qid")
    if lab["qid"] != qid:
        checks["qid_echo"] = False
    lab["answerable"] = obj["answerable"] if isinstance(obj["answerable"], bool) else None
    lab["abstain"] = obj["abstain"] if isinstance(obj["abstain"], bool) else None
    if lab["answerable"] is None or lab["abstain"] is None:
        checks["schema_ok"] = False
        return None, checks
    sids = obj["evidence_sentence_ids"]
    if not isinstance(sids, list) or not all(isinstance(s, str) for s in sids):
        checks["schema_ok"] = False
        return None, checks
    norm_sids, seen = [], set()
    for s in sids:
        s2 = s.strip()
        if s2 in seen:
            checks["no_duplicate_sids"] = False
            continue
        seen.add(s2)
        norm_sids.append(s2)
    lab["evidence_sentence_ids"] = norm_sids
    for s in norm_sids:
        if s not in valid_sids:
            checks["sids_exist"] = False
    role = _norm_enum(obj["evidence_role"], C2GES_EVIDENCE_ROLES)
    if role is None:
        checks["schema_ok"] = False
        return None, checks
    lab["evidence_role"] = role
    flags = obj["flags"]
    if not isinstance(flags, dict):
        checks["schema_ok"] = False
        return None, checks
    lab["flags"] = {}
    for k in C2GES_FLAG_KEYS:
        v = flags.get(k)
        lab["flags"][k] = bool(v) if isinstance(v, bool) else None
        if lab["flags"][k] is None:
            checks["schema_ok"] = False
    conf = _norm_enum(obj["confidence"], CONFIDENCE_LEVELS)
    if conf is None:
        checks["schema_ok"] = False
    lab["confidence"] = conf
    lab["answer_summary"] = str(obj["answer_summary"] or "")
    lab["rationale"] = str(obj["rationale"] or "")
    ar = obj["abstain_reason"]
    lab["abstain_reason"] = None if ar in (None, "", "null") else str(ar)
    if len(lab["answer_summary"].split()) > 60 or len(lab["rationale"].split()) > 60:
        checks["warnings"].append("word limit exceeded")
    if lab["answerable"] and not lab["abstain"] and not lab["evidence_sentence_ids"]:
        checks["evidence_nonempty_when_answerable"] = False
    if not checks["schema_ok"]:
        return None, checks
    return lab, checks


def checks_passed(checks):
    return all(checks[k] for k in ("json_parses", "schema_ok", "sids_exist",
                                   "evidence_nonempty_when_answerable",
                                   "no_duplicate_sids", "qid_echo"))


def validate_ma_label(obj, qid, schema_tables):
    checks = {"json_parses": True, "schema_ok": True, "required_tables_subset": True,
              "qid_echo": True, "warnings": []}
    if not isinstance(obj, dict):
        checks["schema_ok"] = False
        return None, checks
    required = ["question_id", "answerable_by_schema", "required_tables", "sql_readonly",
                "semantically_correct", "issues", "error_classification", "minimal_fix",
                "confidence", "abstain", "abstain_reason"]
    for k in required:
        if k not in obj:
            checks["schema_ok"] = False
            checks["warnings"].append(f"missing key {k}")
    if not checks["schema_ok"]:
        return None, checks
    lab = {}
    lab["question_id"] = obj.get("question_id")
    if lab["question_id"] != qid:
        checks["qid_echo"] = False
    for k in ("answerable_by_schema", "sql_readonly", "semantically_correct", "abstain"):
        lab[k] = obj[k] if isinstance(obj[k], bool) else None
        if lab[k] is None:
            checks["schema_ok"] = False
    rt = obj["required_tables"]
    if not isinstance(rt, list) or not all(isinstance(t, str) for t in rt):
        checks["schema_ok"] = False
        rt = []
    lab["required_tables"] = [t.strip() for t in rt]
    for t in lab["required_tables"]:
        if t not in schema_tables:
            checks["required_tables_subset"] = False
    issues = obj["issues"]
    if not isinstance(issues, dict):
        checks["schema_ok"] = False
        issues = {}
    lab["issues"] = {k: (bool(issues.get(k)) if isinstance(issues.get(k), bool) else None)
                     for k in MA_ISSUE_KEYS}
    if any(v is None for v in lab["issues"].values()):
        checks["schema_ok"] = False
    ec = _norm_enum(obj["error_classification"], MA_ERROR_CLASSES)
    if ec is None:
        checks["schema_ok"] = False
    lab["error_classification"] = ec
    mf = obj["minimal_fix"]
    lab["minimal_fix"] = None if mf in (None, "", "null") else str(mf)
    if lab["minimal_fix"] and len(lab["minimal_fix"].split()) > 40:
        checks["warnings"].append("minimal_fix word limit exceeded")
    conf = _norm_enum(obj["confidence"], CONFIDENCE_LEVELS)
    if conf is None:
        checks["schema_ok"] = False
    lab["confidence"] = conf
    ar = obj["abstain_reason"]
    lab["abstain_reason"] = None if ar in (None, "", "null") else str(ar)
    if not checks["schema_ok"]:
        return None, checks
    return lab, checks


def ma_checks_passed(checks):
    return all(checks[k] for k in ("json_parses", "schema_ok",
                                   "required_tables_subset", "qid_echo"))


# ---------------------------------------------------------------------------
# sampling
# ---------------------------------------------------------------------------

def sample_c2ges(docs):
    """Stratified deterministic sample: cover all 15 docs and all 5 roles, size 25."""
    items = []
    for d in docs:
        for q in d["questions"]:
            items.append({"doc_id": d["doc_id"], "title": d["title"],
                          "qid": q["qid"], "role": q["role"], "question": q["question"]})
    rng = random.Random(SEED)
    order = list(range(len(items)))
    rng.shuffle(order)
    picked, picked_set = [], set()
    covered_docs, covered_roles = set(), set()
    for i in order:  # pass 1: one question per document
        it = items[i]
        if it["doc_id"] not in covered_docs:
            picked.append(i); picked_set.add(i)
            covered_docs.add(it["doc_id"]); covered_roles.add(it["role"])
    for i in order:  # pass 2: cover any missing role
        if len(covered_roles) >= 5:
            break
        it = items[i]
        if i not in picked_set and it["role"] not in covered_roles:
            picked.append(i); picked_set.add(i); covered_roles.add(it["role"])
    for i in order:  # pass 3: fill to 25
        if len(picked) >= 25:
            break
        if i not in picked_set:
            picked.append(i); picked_set.add(i)
    return [items[i] for i in picked]


def _spread_over_families(items, family_key, n, rng):
    fams = {}
    for it in items:
        fams.setdefault(it[family_key], []).append(it)
    names = sorted(fams)
    rng.shuffle(names)
    for f in names:
        rng.shuffle(fams[f])
    picked = []
    i = 0
    while len(picked) < n and i < 100000:
        f = names[i % len(names)]
        if fams[f]:
            picked.append(fams[f].pop())
        i += 1
    return picked


def sample_ma(rts_items, sb_items):
    rng = random.Random(SEED)
    rts = _spread_over_families(rts_items, "template_family", 14, rng)
    sb = _spread_over_families(sb_items, "template_family", 11, rng)
    return rts + sb


# ---------------------------------------------------------------------------
# SQLite sandbox (read-only)
# ---------------------------------------------------------------------------

def _ro_uri(db_path):
    p = str(Path(db_path).resolve()).replace("\\", "/")
    return "file:" + urllib.parse.quote(p, safe="/:") + "?mode=ro"


def execute_sql_sandbox(db_path, sql, timeout_s=10, row_cap=5000):
    facts = {"executable": False, "row_count": None, "columns": None,
             "error": None, "elapsed_s": None, "row_cap": row_cap, "truncated": False}
    t0 = time.monotonic()
    try:
        conn = sqlite3.connect(_ro_uri(db_path), uri=True, timeout=timeout_s)
        try:
            conn.execute("PRAGMA query_only=ON")
            deny = {sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE,
                    sqlite3.SQLITE_ALTER_TABLE, sqlite3.SQLITE_DROP_TABLE,
                    sqlite3.SQLITE_CREATE_TABLE, sqlite3.SQLITE_CREATE_INDEX,
                    sqlite3.SQLITE_CREATE_VIEW, sqlite3.SQLITE_CREATE_TRIGGER,
                    sqlite3.SQLITE_DROP_INDEX, sqlite3.SQLITE_DROP_VIEW,
                    sqlite3.SQLITE_DROP_TRIGGER, sqlite3.SQLITE_ATTACH,
                    sqlite3.SQLITE_DETACH, sqlite3.SQLITE_REINDEX}
            conn.set_authorizer(
                lambda action, a1, a2, db, src: sqlite3.SQLITE_DENY if action in deny else sqlite3.SQLITE_OK)
            deadline = t0 + timeout_s
            conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 1000)
            cur = conn.execute(sql)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchmany(row_cap + 1)
            facts["truncated"] = len(rows) > row_cap
            facts["row_count"] = min(len(rows), row_cap)
            facts["columns"] = cols
            facts["executable"] = True
        finally:
            conn.close()
    except Exception as e:
        facts["error"] = f"{type(e).__name__}: {e}"[:300]
    facts["elapsed_s"] = round(time.monotonic() - t0, 3)
    return facts


def compact_schema(db_path):
    conn = sqlite3.connect(_ro_uri(db_path), uri=True)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        lines = []
        for t in tables:
            cols = conn.execute(f'PRAGMA table_info("{t}")').fetchall()
            col_str = ", ".join(f"{c[1]} {c[2]}".strip() for c in cols)
            lines.append(f"TABLE {t} ({col_str})")
            for fk in conn.execute(f'PRAGMA foreign_key_list("{t}")').fetchall():
                lines.append(f"FK {t}.{fk[3]} -> {fk[2]}.{fk[4]}")
        return "\n".join(lines), tables
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# prompts
# ---------------------------------------------------------------------------

def c2ges_schema_text():
    return (
        '{"qid": string, "answerable": boolean, "evidence_sentence_ids": [sid strings], '
        '"evidence_role": "direct_answer|partial_answer|background|insufficient", '
        '"flags": {"cross_sentence": bool, "negation": bool, "condition": bool, '
        '"time_qualifier": bool, "entity_ambiguity": bool}, '
        '"answer_summary": string <=60 words (empty when answerable=false), '
        '"confidence": "high|medium|low", "rationale": string <=60 words referencing sids, '
        '"abstain": boolean, "abstain_reason": string or null}'
    )


def c2ges_prompt(doc, item):
    sents = "\n".join(f"[{s['sid']}] {s['text']}" for s in doc["sentences"])
    return (
        "You are annotating evidence for a question about a public NERC power-system event report.\n\n"
        f"[DOCUMENT {doc['doc_id']}: {doc['title']}]\n{sents}\n\n"
        f"[QUESTION] (qid: {item['qid']}, role: {item['role']}) {item['question']}\n\n"
        "Task: decide whether the document answers the question; select the minimal sufficient "
        "evidence sentence ids; classify evidence role; set flags; give a short answer summary.\n"
        "Rules: cite only existing sids; if the document lacks the information set answerable=false "
        "and evidence_role=insufficient; you may abstain. The \"qid\" field of your JSON output must "
        f'exactly echo the given qid "{item["qid"]}".\n'
        f'Return ONLY one JSON object matching this schema: {c2ges_schema_text()}'
    )


def c2ges_adjudication_prompt(doc, item, lab1, chk1, lab2, chk2):
    sents = "\n".join(f"[{s['sid']}] {s['text']}" for s in doc["sentences"])
    return (
        "You are adjudicating between two annotators on evidence annotation for a question about a "
        "public NERC power-system event report. The annotator labels are anonymized; you do not know "
        "which model produced which label.\n\n"
        f"[DOCUMENT {doc['doc_id']}: {doc['title']}]\n{sents}\n\n"
        f"[QUESTION] (qid: {item['qid']}, role: {item['role']}) {item['question']}\n\n"
        f"[ANNOTATOR_1 LABEL]\n{json.dumps(lab1, ensure_ascii=False)}\n"
        f"[ANNOTATOR_1 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk1, ensure_ascii=False)}\n\n"
        f"[ANNOTATOR_2 LABEL]\n{json.dumps(lab2, ensure_ascii=False)}\n"
        f"[ANNOTATOR_2 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk2, ensure_ascii=False)}\n\n"
        "Task: produce the FINAL label following the same schema below, plus one extra field "
        '"adjudication_note" (string, <=60 words, justify the decision). If neither label is '
        'acceptable and no defensible label can be produced, return an object with "abstain": true, '
        '"abstain_reason" and "adjudication_note" filled (other fields minimally filled). The "qid" '
        f'field must exactly echo "{item["qid"]}".\n'
        f'Schema: {c2ges_schema_text()} plus "adjudication_note".\n'
        "Return ONLY one JSON object."
    )


def ma_schema_text():
    return (
        '{"question_id": string, "answerable_by_schema": boolean, '
        '"required_tables": [table names from schema], "sql_readonly": boolean, '
        '"semantically_correct": boolean, '
        '"issues": {"wrong_columns": bool, "wrong_filter": bool, "wrong_aggregation": bool, '
        '"wrong_join": bool, "wrong_order_or_limit": bool, "wrong_units_or_time_range": bool, '
        '"incomplete_answer": bool}, '
        '"error_classification": "none|semantic_mismatch|syntax_risk|unsafe|incomplete_answer|'
        'not_answerable|other", "minimal_fix": string or null <=40 words, '
        '"confidence": "high|medium|low", "abstain": boolean, "abstain_reason": string or null}'
    )


def ma_prompt(schema_text, item, facts):
    return (
        "You are auditing a candidate reference SQL for a power-grid text-to-SQL benchmark item.\n\n"
        f"[DATABASE SCHEMA]\n{schema_text}\n\n"
        f"[QUESTION] (question_id: {item['question_id']}) {item['question']}\n\n"
        f"[CANDIDATE SQL]\n{item['sql']}\n\n"
        f"[DETERMINISTIC EXECUTION FACTS] executable={facts['executable']}, "
        f"row_count={facts['row_count']}, result_columns={json.dumps(facts['columns'])}\n\n"
        "Task: judge whether the candidate SQL semantically and completely answers the question "
        "under this schema. Executability alone is NOT sufficient. The \"question_id\" field of "
        f'your JSON output must exactly echo "{item["question_id"]}".\n'
        f'Return ONLY one JSON object matching this schema: {ma_schema_text()}'
    )


def ma_adjudication_prompt(schema_text, item, facts, lab1, chk1, lab2, chk2):
    return (
        "You are adjudicating between two annotators auditing a candidate reference SQL for a "
        "power-grid text-to-SQL benchmark item. The annotator labels are anonymized; you do not "
        "know which model produced which label.\n\n"
        f"[DATABASE SCHEMA]\n{schema_text}\n\n"
        f"[QUESTION] (question_id: {item['question_id']}) {item['question']}\n\n"
        f"[CANDIDATE SQL]\n{item['sql']}\n\n"
        f"[DETERMINISTIC EXECUTION FACTS] executable={facts['executable']}, "
        f"row_count={facts['row_count']}, result_columns={json.dumps(facts['columns'])}\n\n"
        f"[ANNOTATOR_1 LABEL]\n{json.dumps(lab1, ensure_ascii=False)}\n"
        f"[ANNOTATOR_1 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk1, ensure_ascii=False)}\n\n"
        f"[ANNOTATOR_2 LABEL]\n{json.dumps(lab2, ensure_ascii=False)}\n"
        f"[ANNOTATOR_2 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk2, ensure_ascii=False)}\n\n"
        "Task: produce the FINAL label following the same schema below, plus one extra field "
        '"adjudication_note" (string, <=60 words). If neither label is acceptable and no defensible '
        'label can be produced, return an object with "abstain": true, "abstain_reason" and '
        '"adjudication_note" filled (other fields minimally filled). The "question_id" field must '
        f'exactly echo "{item["question_id"]}".\n'
        f'Schema: {ma_schema_text()} plus "adjudication_note".\n'
        "Return ONLY one JSON object."
    )


# ---------------------------------------------------------------------------
# anonymization
# ---------------------------------------------------------------------------

def anon_mapping(item_id):
    h = int(hashlib.sha256(f"{SEED}:{item_id}".encode()).hexdigest()[:8], 16)
    rng = random.Random(h)
    if rng.random() < 0.5:
        return {"annotator_1": "A", "annotator_2": "B"}
    return {"annotator_1": "B", "annotator_2": "A"}


# ---------------------------------------------------------------------------
# stats helpers
# ---------------------------------------------------------------------------

def cohens_kappa(pairs):
    """pairs: list of (a, b) booleans. Returns kappa or None."""
    n = len(pairs)
    if n == 0:
        return None
    po = sum(1 for a, b in pairs if a == b) / n
    pa = sum(1 for a, _ in pairs if a) / n
    pb = sum(1 for _, b in pairs if b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    if pe == 1.0:
        return None  # undefined (single category observed)
    return (po - pe) / (1 - pe)


def jaccard(s1, s2):
    a, b = set(s1), set(s2)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def latency_stats(vals):
    if not vals:
        return {"n": 0, "mean_s": None, "median_s": None}
    vs = sorted(vals)
    mid = len(vs) // 2
    med = vs[mid] if len(vs) % 2 else (vs[mid - 1] + vs[mid]) / 2
    return {"n": len(vs), "mean_s": round(sum(vs) / len(vs), 3), "median_s": round(med, 3)}


def model_usage_from_ledger(run_dir):
    usage = {}
    for rec in read_jsonl(Path(run_dir) / "raw_ledger.jsonl"):
        if rec.get("record_type") != "llm_call":
            continue
        role = rec["model_role"]
        u = usage.setdefault(role, {"calls": 0, "api_failures": 0, "input_tokens": 0,
                                    "output_tokens": 0, "input_tokens_null": 0,
                                    "output_tokens_null": 0, "latencies": [],
                                    "served_model_ids": []})
        u["calls"] += 1
        if rec.get("error"):
            u["api_failures"] += 1
        if rec.get("input_tokens") is None:
            u["input_tokens_null"] += 1
        else:
            u["input_tokens"] += rec["input_tokens"]
        if rec.get("output_tokens") is None:
            u["output_tokens_null"] += 1
        else:
            u["output_tokens"] += rec["output_tokens"]
        if rec.get("latency_s") is not None:
            u["latencies"].append(rec["latency_s"])
        sid = rec.get("served_model_id")
        if sid and sid not in u["served_model_ids"]:
            u["served_model_ids"].append(sid)
    for u in usage.values():
        u["latency"] = latency_stats(u.pop("latencies"))
    return usage


# ---------------------------------------------------------------------------
# C2GES pilot
# ---------------------------------------------------------------------------

def run_c2ges(env, limit=None):
    run_dir = PILOT_DIR / "runs/c2ges_pilot"
    ledger = Ledger(run_dir)
    labels_a_path = run_dir / "labels_A.jsonl"
    labels_b_path = run_dir / "labels_B.jsonl"
    adj_path = run_dir / "adjudicated.jsonl"
    final_path = run_dir / "final_labels.jsonl"

    docs = {}
    with open(C2GES_PACKET, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            docs[d["doc_id"]] = d
    sample = sample_c2ges(list(docs.values()))
    manifest = {
        "pilot": "c2ges", "seed": SEED, "pilot_size": 25,
        "protocol_sha256": PROTOCOLS["c2ges"]["sha256"],
        "sampling_rule": "Random(20260807) shuffle of 75 (doc,qid) pairs; pass1 one per document "
                         "(15), pass2 cover missing roles, pass3 fill to 25 in shuffled order",
        "n_docs_covered": len({it["doc_id"] for it in sample}),
        "roles_covered": sorted({it["role"] for it in sample}),
        "items": sample,
    }
    if limit:
        sample = sample[:limit]
        manifest["limited_to"] = limit
    with open(run_dir / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    done = {r["qid"] for r in read_jsonl(labels_a_path)} & {r["qid"] for r in read_jsonl(labels_b_path)}
    print(f"[c2ges] sample={len(sample)} already_done={len(done)}")

    for idx, item in enumerate(sample):
        qid = item["qid"]
        if qid in done:
            continue
        doc = docs[item["doc_id"]]
        valid_sids = {s["sid"] for s in doc["sentences"]}
        prompt = c2ges_prompt(doc, item)
        results = {}
        for role, path in (("A", labels_a_path), ("B", labels_b_path)):
            call = llm_call(role, prompt, env, ledger, qid)
            rec = {"qid": qid, "doc_id": item["doc_id"], "role_q": item["role"],
                   "annotator": role, "ts": utc_now(),
                   "call_ok": call.get("ok", False), "call_error": call.get("error"),
                   "served_model_id": call.get("served_model_id"),
                   "format_failure": False, "label": None, "checks": None}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    rec["format_failure"] = True
                    rec["checks"] = {"json_parses": False, "parse_error": perr}
                    GATES.record_failure(role, "format")
                else:
                    lab, checks = validate_c2ges_label(obj, qid, valid_sids)
                    rec["checks"] = checks
                    if lab is None or not checks_passed(checks):
                        rec["format_failure"] = True
                        rec["label"] = lab  # keep whatever parsed (may be None)
                        GATES.record_failure(role, "format")
                    else:
                        rec["label"] = lab
            append_jsonl(path, rec)
            results[role] = rec
            print(f"[c2ges {idx+1}/{len(sample)}] {qid} {role}: "
                  f"{'ok' if rec['label'] else 'FAIL:' + str(rec['call_error'] or 'format')}")

        la, lb = results["A"]["label"], results["B"]["label"]
        disagree = True
        if la is not None and lb is not None:
            disagree = (la["answerable"] != lb["answerable"]
                        or set(la["evidence_sentence_ids"]) != set(lb["evidence_sentence_ids"])
                        or la["evidence_role"] != lb["evidence_role"]
                        or la["abstain"] or lb["abstain"])
        final_rec = {"qid": qid, "doc_id": item["doc_id"], "role_q": item["role"],
                     "ts": utc_now(), "disagreement": disagree}
        if not disagree:
            final_rec.update({"final_source": "agreement", "final_label": la})
        else:
            mapping = anon_mapping(qid)
            lab1 = results[mapping["annotator_1"]]["label"]
            chk1 = results[mapping["annotator_1"]]["checks"]
            lab2 = results[mapping["annotator_2"]]["label"]
            chk2 = results[mapping["annotator_2"]]["checks"]
            adj_prompt = c2ges_adjudication_prompt(doc, item, lab1, chk1, lab2, chk2)
            call = llm_call("C", adj_prompt, env, ledger, qid)
            adj_rec = {"qid": qid, "ts": utc_now(), "anon_mapping": mapping,
                       "call_ok": call.get("ok", False), "call_error": call.get("error"),
                       "served_model_id": call.get("served_model_id"),
                       "format_failure": False, "label": None, "abstain": False}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    adj_rec["format_failure"] = True
                    GATES.record_failure("C", "format")
                else:
                    note = obj.get("adjudication_note")
                    if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                        adj_rec["abstain"] = True
                        adj_rec["label"] = {"abstain": True,
                                            "abstain_reason": obj.get("abstain_reason"),
                                            "adjudication_note": note}
                    else:
                        lab, checks = validate_c2ges_label(obj, qid, valid_sids)
                        adj_rec["checks"] = checks
                        if lab is not None and checks_passed(checks) and note:
                            lab["adjudication_note"] = note
                            adj_rec["label"] = lab
                        else:
                            adj_rec["format_failure"] = True
                            adj_rec["label"] = lab
                            GATES.record_failure("C", "format")
            append_jsonl(adj_path, adj_rec)
            if adj_rec["label"] is not None:
                final_rec.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                                  "adjudicator_abstain": adj_rec["abstain"]})
            else:
                final_rec.update({"final_source": "unresolved",
                                  "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(final_path, final_rec)

    stats = c2ges_stats(run_dir, len(sample))
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[c2ges] done. stats -> {run_dir / 'stats.json'}")
    return stats


def c2ges_stats(run_dir, sample_n):
    run_dir = Path(run_dir)
    la = {r["qid"]: r for r in read_jsonl(run_dir / "labels_A.jsonl")}
    lb = {r["qid"]: r for r in read_jsonl(run_dir / "labels_B.jsonl")}
    adj = read_jsonl(run_dir / "adjudicated.jsonl")
    finals = read_jsonl(run_dir / "final_labels.jsonl")
    qids = sorted(set(la) & set(lb))
    valid_pairs, ans_pairs, jac, exact = 0, [], [], []
    abstain_a = abstain_b = 0
    for q in qids:
        a, b = la[q]["label"], lb[q]["label"]
        if a and a.get("abstain"):
            abstain_a += 1
        if b and b.get("abstain"):
            abstain_b += 1
        if a is None or b is None:
            continue
        valid_pairs += 1
        ans_pairs.append((a["answerable"], b["answerable"]))
        jac.append(jaccard(a["evidence_sentence_ids"], b["evidence_sentence_ids"]))
        exact.append(set(a["evidence_sentence_ids"]) == set(b["evidence_sentence_ids"]))
    fmt_fail = sum(1 for q in qids if la[q]["format_failure"] or lb[q]["format_failure"])
    n_completed = len(finals)
    stats = {
        "pilot": "c2ges",
        "sample_size": sample_n,
        "completed": n_completed,
        "valid_ab_pairs": valid_pairs,
        "answerable_raw_agreement": (sum(1 for a, b in ans_pairs if a == b) / len(ans_pairs)) if ans_pairs else None,
        "answerable_cohens_kappa": cohens_kappa(ans_pairs),
        "evidence_jaccard_mean": round(sum(jac) / len(jac), 4) if jac else None,
        "evidence_exact_match_rate": sum(exact) / len(exact) if exact else None,
        "adjudications": len(adj),
        "adjudication_rate": len(adj) / n_completed if n_completed else None,
        "adjudicator_abstains": sum(1 for r in adj if r.get("abstain")),
        "abstain_A": abstain_a, "abstain_B": abstain_b,
        "format_failure_items": fmt_fail,
        "format_failure_rate": fmt_fail / len(qids) if qids else None,
        "model_usage": model_usage_from_ledger(run_dir),
        "gate_events": GATES.events,
        "halted_models": GATES.halted,
        "total_llm_calls_this_run": GATES.total_calls,
        "final_table": [
            {"qid": r["qid"], "doc_id": r["doc_id"], "role": r["role_q"],
             "A": _brief(la.get(r["qid"])), "B": _brief(lb.get(r["qid"])),
             "C": ("abstain" if any((x.get("qid") or x.get("question_id")) == r["qid"] and x.get("abstain") for x in adj)
                   else ("adjudicated" if any((x.get("qid") or x.get("question_id")) == r["qid"] for x in adj) else "-")),
             "final_source": r.get("final_source"),
             "final_answerable": (r.get("final_label") or {}).get("answerable"),
             "final_evidence": (r.get("final_label") or {}).get("evidence_sentence_ids")}
            for r in finals],
    }
    return stats


def _brief(rec):
    if rec is None:
        return "missing"
    if rec.get("format_failure"):
        return "format_failure"
    lab = rec.get("label")
    if lab is None:
        return "api_failure"
    if lab.get("abstain"):
        return "abstain"
    return f"ans={lab.get('answerable')}"


def _brief_ma(rec):
    if rec is None:
        return "missing"
    if rec.get("format_failure"):
        return "format_failure"
    lab = rec.get("label")
    if lab is None:
        return "api_failure"
    if lab.get("abstain"):
        return "abstain"
    return f"sem={lab.get('semantically_correct')}"


# ---------------------------------------------------------------------------
# MA-SQLGrid pilot
# ---------------------------------------------------------------------------

def load_ma_items():
    status = {}
    for rec in read_jsonl(MA_SQL_STATUS):
        status[rec["question_id"]] = rec
    items = []
    for rec in read_jsonl(MA_RTS_QUESTIONS):
        qid = rec["question_id"]
        st = status.get(qid, {})
        items.append({
            "question_id": qid, "dataset_id": "RTS_GMLC_AUTO_PILOT",
            "question": rec["question"], "sql": st.get("registered_reference_sql") or rec["gold_sql"],
            "template_family": rec.get("template_family"),
        })
    with open(MA_SB_QUESTIONS, encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            qid = rec["question_id"]
            st = status.get(qid, {})
            items.append({
                "question_id": qid, "dataset_id": "SIMBENCH_AUTO_PILOT",
                "question": rec["natural_language"],
                "sql": st.get("registered_reference_sql") or rec["gold_sql"],
                "template_family": rec.get("template_family_id"),
            })
    return items


def run_ma(env, limit=None):
    run_dir = PILOT_DIR / "runs/ma_pilot"
    ledger = Ledger(run_dir)
    labels_a_path = run_dir / "labels_A.jsonl"
    labels_b_path = run_dir / "labels_B.jsonl"
    adj_path = run_dir / "adjudicated.jsonl"
    final_path = run_dir / "final_labels.jsonl"
    exec_path = run_dir / "execution_facts.jsonl"

    items = load_ma_items()
    rts = [it for it in items if it["dataset_id"] == "RTS_GMLC_AUTO_PILOT"]
    sb = [it for it in items if it["dataset_id"] == "SIMBENCH_AUTO_PILOT"]
    sample = sample_ma(rts, sb)
    manifest = {
        "pilot": "ma_sqlgrid", "seed": SEED, "pilot_size": 25,
        "protocol_sha256": PROTOCOLS["ma"]["sha256"],
        "sampling_rule": "Random(20260807); RTS: shuffle family list + items within family, "
                         "round-robin pick 14; then SimBench same procedure pick 11",
        "n_rts": sum(1 for it in sample if it["dataset_id"] == "RTS_GMLC_AUTO_PILOT"),
        "n_simbench": sum(1 for it in sample if it["dataset_id"] == "SIMBENCH_AUTO_PILOT"),
        "items": sample,
    }
    if limit:
        sample = sample[:limit]
        manifest["limited_to"] = limit
    with open(run_dir / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    schema_cache = {}
    def get_schema(dataset_id):
        if dataset_id not in schema_cache:
            schema_cache[dataset_id] = compact_schema(MA_DBS[dataset_id])
        return schema_cache[dataset_id]

    done = {r["question_id"] for r in read_jsonl(labels_a_path)} & \
           {r["question_id"] for r in read_jsonl(labels_b_path)}
    print(f"[ma] sample={len(sample)} already_done={len(done)}")

    for idx, item in enumerate(sample):
        qid = item["question_id"]
        if qid in done:
            continue
        schema_text, schema_tables = get_schema(item["dataset_id"])
        # deterministic sandbox execution BEFORE any LLM prompt for this item
        facts = execute_sql_sandbox(MA_DBS[item["dataset_id"]], item["sql"])
        append_jsonl(exec_path, {"question_id": qid, "dataset_id": item["dataset_id"],
                                 "ts": utc_now(), "facts": facts})
        prompt = ma_prompt(schema_text, item, facts)
        results = {}
        for role, path in (("A", labels_a_path), ("B", labels_b_path)):
            call = llm_call(role, prompt, env, ledger, qid)
            rec = {"question_id": qid, "dataset_id": item["dataset_id"],
                   "annotator": role, "ts": utc_now(),
                   "call_ok": call.get("ok", False), "call_error": call.get("error"),
                   "served_model_id": call.get("served_model_id"),
                   "format_failure": False, "label": None, "checks": None}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    rec["format_failure"] = True
                    rec["checks"] = {"json_parses": False, "parse_error": perr}
                    GATES.record_failure(role, "format")
                else:
                    lab, checks = validate_ma_label(obj, qid, set(schema_tables))
                    rec["checks"] = checks
                    if lab is None or not ma_checks_passed(checks):
                        rec["format_failure"] = True
                        rec["label"] = lab
                        GATES.record_failure(role, "format")
                    else:
                        rec["label"] = lab
            append_jsonl(path, rec)
            results[role] = rec
            print(f"[ma {idx+1}/{len(sample)}] {qid} {role}: "
                  f"{'ok' if rec['label'] else 'FAIL:' + str(rec['call_error'] or 'format')}")

        la, lb = results["A"]["label"], results["B"]["label"]
        disagree = True
        if la is not None and lb is not None:
            disagree = (la["answerable_by_schema"] != lb["answerable_by_schema"]
                        or la["semantically_correct"] != lb["semantically_correct"]
                        or la["error_classification"] != lb["error_classification"]
                        or la["abstain"] or lb["abstain"])
        final_rec = {"question_id": qid, "dataset_id": item["dataset_id"],
                     "ts": utc_now(), "disagreement": disagree}
        if not disagree:
            final_rec.update({"final_source": "agreement", "final_label": la})
        else:
            mapping = anon_mapping(qid)
            lab1 = results[mapping["annotator_1"]]["label"]
            chk1 = results[mapping["annotator_1"]]["checks"]
            lab2 = results[mapping["annotator_2"]]["label"]
            chk2 = results[mapping["annotator_2"]]["checks"]
            adj_prompt = ma_adjudication_prompt(schema_text, item, facts, lab1, chk1, lab2, chk2)
            call = llm_call("C", adj_prompt, env, ledger, qid)
            adj_rec = {"question_id": qid, "ts": utc_now(), "anon_mapping": mapping,
                       "call_ok": call.get("ok", False), "call_error": call.get("error"),
                       "served_model_id": call.get("served_model_id"),
                       "format_failure": False, "label": None, "abstain": False}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    adj_rec["format_failure"] = True
                    GATES.record_failure("C", "format")
                else:
                    note = obj.get("adjudication_note")
                    if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                        adj_rec["abstain"] = True
                        adj_rec["label"] = {"abstain": True,
                                            "abstain_reason": obj.get("abstain_reason"),
                                            "adjudication_note": note}
                    else:
                        lab, checks = validate_ma_label(obj, qid, set(schema_tables))
                        adj_rec["checks"] = checks
                        if lab is not None and ma_checks_passed(checks) and note:
                            lab["adjudication_note"] = note
                            adj_rec["label"] = lab
                        else:
                            adj_rec["format_failure"] = True
                            adj_rec["label"] = lab
                            GATES.record_failure("C", "format")
            append_jsonl(adj_path, adj_rec)
            if adj_rec["label"] is not None:
                final_rec.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                                  "adjudicator_abstain": adj_rec["abstain"]})
            else:
                final_rec.update({"final_source": "unresolved",
                                  "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(final_path, final_rec)

    stats = ma_stats(run_dir, len(sample))
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[ma] done. stats -> {run_dir / 'stats.json'}")
    return stats


def ma_stats(run_dir, sample_n):
    run_dir = Path(run_dir)
    la = {r["question_id"]: r for r in read_jsonl(run_dir / "labels_A.jsonl")}
    lb = {r["question_id"]: r for r in read_jsonl(run_dir / "labels_B.jsonl")}
    adj = read_jsonl(run_dir / "adjudicated.jsonl")
    finals = read_jsonl(run_dir / "final_labels.jsonl")
    execs = {r["question_id"]: r["facts"] for r in read_jsonl(run_dir / "execution_facts.jsonl")}
    qids = sorted(set(la) & set(lb))
    valid_pairs, sem_pairs = 0, []
    abstain_a = abstain_b = 0
    for q in qids:
        a, b = la[q]["label"], lb[q]["label"]
        if a and a.get("abstain"):
            abstain_a += 1
        if b and b.get("abstain"):
            abstain_b += 1
        if a is None or b is None:
            continue
        valid_pairs += 1
        sem_pairs.append((a["semantically_correct"], b["semantically_correct"]))
    fmt_fail = sum(1 for q in qids if la[q]["format_failure"] or lb[q]["format_failure"])
    n_completed = len(finals)
    return {
        "pilot": "ma_sqlgrid",
        "sample_size": sample_n,
        "completed": n_completed,
        "sandbox_executable": sum(1 for f in execs.values() if f.get("executable")),
        "sandbox_errors": {q: f["error"] for q, f in execs.items() if f.get("error")},
        "valid_ab_pairs": valid_pairs,
        "semantically_correct_raw_agreement":
            (sum(1 for a, b in sem_pairs if a == b) / len(sem_pairs)) if sem_pairs else None,
        "semantically_correct_cohens_kappa": cohens_kappa(sem_pairs),
        "adjudications": len(adj),
        "adjudication_rate": len(adj) / n_completed if n_completed else None,
        "adjudicator_abstains": sum(1 for r in adj if r.get("abstain")),
        "abstain_A": abstain_a, "abstain_B": abstain_b,
        "format_failure_items": fmt_fail,
        "format_failure_rate": fmt_fail / len(qids) if qids else None,
        "model_usage": model_usage_from_ledger(run_dir),
        "gate_events": GATES.events,
        "halted_models": GATES.halted,
        "total_llm_calls_this_run": GATES.total_calls,
        "final_table": [
            {"question_id": r["question_id"], "dataset_id": r["dataset_id"],
             "A": _brief_ma(la.get(r["question_id"])), "B": _brief_ma(lb.get(r["question_id"])),
             "C": ("abstain" if any(x["question_id"] == r["question_id"] and x.get("abstain") for x in adj)
                   else ("adjudicated" if any(x["question_id"] == r["question_id"] for x in adj) else "-")),
             "final_source": r.get("final_source"),
             "final_semantically_correct": (r.get("final_label") or {}).get("semantically_correct"),
             "final_error_classification": (r.get("final_label") or {}).get("error_classification")}
            for r in finals],
    }


# ---------------------------------------------------------------------------
# STAGE 2 (v1.1 protocols, authorization DUAL-LLM-ANNOTATION-20260807-02)
# ---------------------------------------------------------------------------

PROTOCOLS_V11 = {
    "c2ges": {
        "path": PILOT_DIR / "C2GES_ANNOTATION_PROTOCOL_v1.1.json",
        "sha256": "41053d9bc589ccf0411407072e7b2525847f02c39e514cce6e0c0053c73b994f",
    },
    "ma": {
        "path": PILOT_DIR / "MA_SQLGRID_ANNOTATION_PROTOCOL_v1.1.json",
        "sha256": "926a08269217ef8337a8819ffd38db2433ebe6065be208240d1e40c938c7b75c",
    },
}
# current stage-2 protocols: C2GES v1.2 (supersedes v1.1), MA v1.1
PROTOCOLS_STAGE2 = {
    "c2ges": {
        "path": PILOT_DIR / "C2GES_ANNOTATION_PROTOCOL_v1.2.json",
        "sha256": "40d5cc57981a9a156c74651356d1e2488232c4a49b4fc1c315f3bc7e3858bf38",
    },
    "ma": {
        "path": PILOT_DIR / "MA_SQLGRID_ANNOTATION_PROTOCOL_v1.1.json",
        "sha256": "926a08269217ef8337a8819ffd38db2433ebe6065be208240d1e40c938c7b75c",
    },
}
STAGE2_MAX_CALLS = 700  # STAGE2_AUTHORIZATION_20260807.json

# Frozen v1.1 prompt template (verbatim from C2GES_ANNOTATION_PROTOCOL_v1.1.json).
C2GES_V11_TEMPLATE = (
    "You are annotating evidence for a question about a public NERC power-system event report.\n\n"
    "[DOCUMENT {doc_id}: {title}]\n{sents}\n\n"
    "[QUESTION id={qid}] ({role}) {question}\n\n"
    "Evidence rules:\n"
    "- Select ONLY sentences that directly state the asked fact; a sentence is in only if removing it makes the answer incomplete.\n"
    "- Exclude background/scene-setting/restating sentences. Exception: if the question asks time/place/quantity stated only in a separate sentence, include it.\n"
    "- If several sentences each carry part of the fact, include exactly the minimal covering set.\n"
    "- When unsure about a borderline sentence, EXCLUDE it.\n"
    "- answerable=true only if the document EXPLICITLY states the fact; inference or scattered weak mentions => answerable=false, evidence_role=insufficient, empty evidence.\n"
    "- A section merely saying a topic is discussed elsewhere is not an answer.\n"
    "Echo the question id in field qid. Return ONLY one JSON object matching this schema: {schema}"
)

C2GES_V11_RULES_TEXT = (
    "Evidence rules (v1.1):\n"
    "R1: Select ONLY sentences that directly state the asked fact; a sentence is in only if removing it makes the answer incomplete.\n"
    "R2: Exclude background/scene-setting/restating sentences. Exception (R3): if the question asks time/place/quantity stated only in a separate sentence, include it.\n"
    "R4: If several sentences each carry part of the fact, include exactly the minimal covering set.\n"
    "R5: When unsure about a borderline sentence, EXCLUDE it.\n"
    "R6: answerable=true only if the document EXPLICITLY states the fact; inference or scattered weak mentions => answerable=false, evidence_role=insufficient, empty evidence.\n"
    "R7: A section merely saying a topic is discussed elsewhere is not an answer."
)


def verify_protocols_v11():
    for key, spec in PROTOCOLS_STAGE2.items():
        h = hashlib.sha256(spec["path"].read_bytes()).hexdigest()
        if h != spec["sha256"]:
            raise SystemExit(f"FATAL: stage-2 protocol hash mismatch for {key}: {h}")
    print("[ok] stage-2 protocol hashes verified (c2ges v1.2, ma v1.1)")


def c2ges_resolve_v12(la, lb):
    """v1.2 two-tier disagreement rule. la/lb: valid labels or None (format/api failure).
    Returns {"outcome": "agreement"|"tier1"|"tier2", ...}."""
    if la is None or lb is None:
        return {"outcome": "tier2", "reason": "label_missing_or_format_failure"}
    if la["abstain"] or lb["abstain"]:
        return {"outcome": "tier2", "reason": "abstain"}
    if la["answerable"] != lb["answerable"]:
        return {"outcome": "tier2", "reason": "answerable_differs"}
    if la["evidence_role"] != lb["evidence_role"]:
        return {"outcome": "tier2", "reason": "evidence_role_differs"}
    sa, sb = set(la["evidence_sentence_ids"]), set(lb["evidence_sentence_ids"])
    if sa == sb:
        return {"outcome": "agreement", "final": la}
    # Tier-1 deterministic resolution (answerable and evidence_role agree, no abstain)
    if not la["answerable"]:
        final = dict(la)
        final["evidence_sentence_ids"] = []
        return {"outcome": "tier1", "resolution": "both_unanswerable", "final": final}
    if sa <= sb or sb <= sa:
        smaller = la if len(sa) <= len(sb) else lb
        return {"outcome": "tier1", "resolution": "subset_minimal", "final": dict(smaller)}
    inter = sa & sb
    jac = len(inter) / len(sa | sb)
    if inter and jac >= 0.5:
        final = dict(la)
        final["evidence_sentence_ids"] = sorted(inter)
        return {"outcome": "tier1", "resolution": "intersection_consensus",
                "final": final, "jaccard": round(jac, 4)}
    return {"outcome": "tier2", "reason": f"low_overlap jaccard={jac:.4f}"}


def c2ges_prompt_v11(doc, item):
    sents = "\n".join(f"[{s['sid']}] {s['text']}" for s in doc["sentences"])
    return (C2GES_V11_TEMPLATE
            .replace("{doc_id}", doc["doc_id"]).replace("{title}", doc["title"])
            .replace("{sents}", sents)
            .replace("{qid}", item["qid"]).replace("{role}", item["role"])
            .replace("{question}", item["question"])
            .replace("{schema}", c2ges_schema_text()))


def c2ges_adjudication_prompt_v11(doc, item, lab1, chk1, lab2, chk2):
    sents = "\n".join(f"[{s['sid']}] {s['text']}" for s in doc["sentences"])
    return (
        "You are adjudicating between two annotators on evidence annotation for a question about a "
        "public NERC power-system event report. The annotator labels are anonymized; you do not know "
        "which model produced which label.\n\n"
        f"[DOCUMENT {doc['doc_id']}: {doc['title']}]\n{sents}\n\n"
        f"[QUESTION] (qid: {item['qid']}, role: {item['role']}) {item['question']}\n\n"
        f"{C2GES_V11_RULES_TEXT}\n\n"
        f"[ANNOTATOR_1 LABEL]\n{json.dumps(lab1, ensure_ascii=False)}\n"
        f"[ANNOTATOR_1 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk1, ensure_ascii=False)}\n\n"
        f"[ANNOTATOR_2 LABEL]\n{json.dumps(lab2, ensure_ascii=False)}\n"
        f"[ANNOTATOR_2 DETERMINISTIC CHECK RESULTS]\n{json.dumps(chk2, ensure_ascii=False)}\n\n"
        "Task: produce the FINAL label following the evidence rules above and the schema below, plus "
        'one extra field "adjudication_note" (string, <=60 words, justify the decision). If neither '
        'label is acceptable and no defensible label can be produced, return an object with '
        '"abstain": true, "abstain_reason" and "adjudication_note" filled (other fields minimally '
        f'filled). The "qid" field must exactly echo "{item["qid"]}".\n'
        f'Schema: {c2ges_schema_text()} plus "adjudication_note".\n'
        "Return ONLY one JSON object."
    )


def load_c2ges_packet():
    docs = {}
    with open(C2GES_PACKET, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            docs[d["doc_id"]] = d
    items = []
    for d in docs.values():
        for q in d["questions"]:
            items.append({"doc_id": d["doc_id"], "title": d["title"],
                          "qid": q["qid"], "role": q["role"], "question": q["question"]})
    return docs, items


def run_c2ges_generic(env, items, docs, run_dir, prompt_fn, adj_fn, limit=None,
                      resolver_fn=None):
    """Stage-2 C2GES runner: parameterized prompt + resolution rule.
    resolver_fn(la, lb) implements the v1.2 two-tier rule; when None the v1.0/v1.1
    exact-set-equality trigger is used."""
    run_dir = Path(run_dir)
    ledger = Ledger(run_dir)
    labels_a_path = run_dir / "labels_A.jsonl"
    labels_b_path = run_dir / "labels_B.jsonl"
    adj_path = run_dir / "adjudicated.jsonl"
    final_path = run_dir / "final_labels.jsonl"

    sample = items[:limit] if limit else items
    done = {r["qid"] for r in read_jsonl(labels_a_path)} & {r["qid"] for r in read_jsonl(labels_b_path)}
    print(f"[{run_dir.name}] items={len(sample)} already_done={len(done)}")

    for idx, item in enumerate(sample):
        qid = item["qid"]
        if qid in done:
            continue
        doc = docs[item["doc_id"]]
        valid_sids = {s["sid"] for s in doc["sentences"]}
        prompt = prompt_fn(doc, item)
        results = {}
        for role, path in (("A", labels_a_path), ("B", labels_b_path)):
            call = llm_call(role, prompt, env, ledger, qid)
            rec = {"qid": qid, "doc_id": item["doc_id"], "role_q": item["role"],
                   "annotator": role, "ts": utc_now(),
                   "call_ok": call.get("ok", False), "call_error": call.get("error"),
                   "served_model_id": call.get("served_model_id"),
                   "format_failure": False, "label": None, "checks": None}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    rec["format_failure"] = True
                    rec["checks"] = {"json_parses": False, "parse_error": perr}
                    GATES.record_failure(role, "format")
                else:
                    lab, checks = validate_c2ges_label(obj, qid, valid_sids)
                    rec["checks"] = checks
                    if lab is None or not checks_passed(checks):
                        rec["format_failure"] = True
                        rec["label"] = lab
                        GATES.record_failure(role, "format")
                    else:
                        rec["label"] = lab
            append_jsonl(path, rec)
            results[role] = rec
            print(f"[{run_dir.name} {idx+1}/{len(sample)}] {qid} {role}: "
                  f"{'ok' if rec['label'] else 'FAIL:' + str(rec['call_error'] or 'format')}")

        la, lb = results["A"]["label"], results["B"]["label"]
        if resolver_fn is not None:
            # v1.2 two-tier rule: format-failed labels do not enter Tier-1
            la_v = la if not results["A"]["format_failure"] else None
            lb_v = lb if not results["B"]["format_failure"] else None
            res = resolver_fn(la_v, lb_v)
            outcome = res["outcome"]
            disagree = outcome != "agreement"
        else:
            outcome = None
            disagree = True
            if la is not None and lb is not None:
                disagree = (la["answerable"] != lb["answerable"]
                            or set(la["evidence_sentence_ids"]) != set(lb["evidence_sentence_ids"])
                            or la["evidence_role"] != lb["evidence_role"]
                            or la["abstain"] or lb["abstain"])
        final_rec = {"qid": qid, "doc_id": item["doc_id"], "role_q": item["role"],
                     "ts": utc_now(), "disagreement": disagree}
        if outcome is not None:
            final_rec["resolution_tier"] = outcome
            if outcome == "tier1":
                final_rec["resolution"] = res.get("resolution")
                if "jaccard" in res:
                    final_rec["jaccard"] = res["jaccard"]
            elif outcome == "tier2":
                final_rec["tier2_reason"] = res.get("reason")
        if not disagree:
            final_rec.update({"final_source": "agreement", "final_label": la})
        elif outcome == "tier1":
            final_rec.update({"final_source": "tier1_deterministic",
                              "final_label": res["final"]})
        else:
            mapping = anon_mapping(qid)
            lab1 = results[mapping["annotator_1"]]["label"]
            chk1 = results[mapping["annotator_1"]]["checks"]
            lab2 = results[mapping["annotator_2"]]["label"]
            chk2 = results[mapping["annotator_2"]]["checks"]
            adj_prompt = adj_fn(doc, item, lab1, chk1, lab2, chk2)
            call = llm_call("C", adj_prompt, env, ledger, qid)
            adj_rec = {"qid": qid, "ts": utc_now(), "anon_mapping": mapping,
                       "call_ok": call.get("ok", False), "call_error": call.get("error"),
                       "served_model_id": call.get("served_model_id"),
                       "format_failure": False, "label": None, "abstain": False}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    adj_rec["format_failure"] = True
                    GATES.record_failure("C", "format")
                else:
                    note = obj.get("adjudication_note")
                    if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                        adj_rec["abstain"] = True
                        adj_rec["label"] = {"abstain": True,
                                            "abstain_reason": obj.get("abstain_reason"),
                                            "adjudication_note": note}
                    else:
                        lab, checks = validate_c2ges_label(obj, qid, valid_sids)
                        adj_rec["checks"] = checks
                        if lab is not None and checks_passed(checks) and note:
                            lab["adjudication_note"] = note
                            adj_rec["label"] = lab
                        else:
                            adj_rec["format_failure"] = True
                            adj_rec["label"] = lab
                            GATES.record_failure("C", "format")
            append_jsonl(adj_path, adj_rec)
            if adj_rec["label"] is not None:
                final_rec.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                                  "adjudicator_abstain": adj_rec["abstain"]})
            else:
                final_rec.update({"final_source": "unresolved",
                                  "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(final_path, final_rec)

    stats = c2ges_stats(run_dir, len(sample))
    if resolver_fn is not None:
        stats = c2ges_stats_v12(run_dir, stats)
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[{run_dir.name}] done. stats -> {run_dir / 'stats.json'}")
    return stats


def c2ges_stats_v12(run_dir, stats):
    """Extend base stats with v1.2 tier distribution (from final_labels.jsonl)."""
    finals = read_jsonl(Path(run_dir) / "final_labels.jsonl")
    tiers = {"agreement": 0, "tier1": 0, "tier2": 0}
    res_dist = {}
    tier2_reasons = {}
    for r in finals:
        t = r.get("resolution_tier")
        if t == "agreement":
            tiers["agreement"] += 1
        elif t == "tier1":
            tiers["tier1"] += 1
            res_dist[r.get("resolution")] = res_dist.get(r.get("resolution"), 0) + 1
        elif t == "tier2":
            tiers["tier2"] += 1
            tier2_reasons[r.get("tier2_reason")] = tier2_reasons.get(r.get("tier2_reason"), 0) + 1
        else:  # v1.0/v1.1-style records
            if r.get("final_source") == "agreement":
                tiers["agreement"] += 1
            else:
                tiers["tier2"] += 1
    n = len(finals)
    la = {r["qid"]: r for r in read_jsonl(Path(run_dir) / "labels_A.jsonl")}
    lb = {r["qid"]: r for r in read_jsonl(Path(run_dir) / "labels_B.jsonl")}
    role_pairs = [(la[q]["label"]["evidence_role"], lb[q]["label"]["evidence_role"])
                  for q in set(la) & set(lb)
                  if la[q].get("label") and lb[q].get("label")]
    stats.update({
        "tier_distribution": tiers,
        "tier1_resolution_distribution": res_dist,
        "tier2_reason_distribution": tier2_reasons,
        "tier1_rate": tiers["tier1"] / n if n else None,
        "tier2_adjudication_rate": tiers["tier2"] / n if n else None,
        "evidence_role_raw_agreement":
            (sum(1 for a, b in role_pairs if a == b) / len(role_pairs)) if role_pairs else None,
    })
    return stats


def run_c2ges_gate(env, limit=None):
    """v1.2 validation gate: reuse the 12 v1.1 A/B label pairs, apply the two-tier
    resolution. Tier-2 items reuse an existing successful v1.1 C adjudication when
    one exists (identical inputs, unchanged adjudication rule); C is called only for
    tier-2 items left unresolved by the earlier Cloubic read-timeouts (technical
    retry at a different time, permitted by v1.2)."""
    run_dir = PILOT_DIR / "runs/c2ges_stage2/validation_gate"
    docs, all_items = load_c2ges_packet()
    by_qid = {it["qid"]: it for it in all_items}
    manifest = json.loads((run_dir / "sample_manifest.json").read_text(encoding="utf-8"))
    gate_items = manifest["items"]  # the frozen 12
    la = {r["qid"]: r for r in read_jsonl(run_dir / "labels_A.jsonl")}
    lb = {r["qid"]: r for r in read_jsonl(run_dir / "labels_B.jsonl")}
    v11_finals = {r["qid"]: r for r in read_jsonl(run_dir / "final_labels.jsonl")}
    out_path = run_dir / "final_labels_v1_2.jsonl"
    adj12_path = run_dir / "adjudicated_v1_2.jsonl"
    ledger = Ledger(run_dir)
    done = {r["qid"] for r in read_jsonl(out_path)}

    tiers = {"agreement": 0, "tier1": 0, "tier2": 0}
    res_dist, tier2_reasons = {}, {}
    n_c_reused, n_c_called = 0, 0
    for item in gate_items:
        qid = item["qid"]
        if qid in done:  # resume
            continue
        ra, rb = la.get(qid), lb.get(qid)
        la_lab = ra["label"] if ra and not ra.get("format_failure") else None
        lb_lab = rb["label"] if rb and not rb.get("format_failure") else None
        res = c2ges_resolve_v12(la_lab, lb_lab)
        outcome = res["outcome"]
        final_rec = {"qid": qid, "doc_id": item["doc_id"], "role_q": item["role"],
                     "ts": utc_now(), "protocol": "v1.2", "resolution_tier": outcome}
        if outcome == "tier1":
            final_rec["resolution"] = res.get("resolution")
            if "jaccard" in res:
                final_rec["jaccard"] = res["jaccard"]
        if outcome == "tier2":
            final_rec["tier2_reason"] = res.get("reason")
        if outcome == "agreement":
            final_rec.update({"final_source": "agreement", "final_label": la_lab})
        elif outcome == "tier1":
            final_rec.update({"final_source": "tier1_deterministic",
                              "final_label": res["final"]})
        else:
            v11f = v11_finals.get(qid) or {}
            v11_lab = v11f.get("final_label")
            if v11f.get("final_source") == "adjudication" and v11_lab:
                # reuse the existing successful C adjudication (same inputs, same rule)
                final_rec.update({"final_source": "adjudication_reused_v1_1",
                                  "final_label": v11_lab})
                n_c_reused += 1
            else:
                # technical retry of C for items left unresolved by read-timeouts
                doc = docs[item["doc_id"]]
                valid_sids = {s["sid"] for s in doc["sentences"]}
                mapping = anon_mapping(qid)
                src1 = ra if mapping["annotator_1"] == "A" else rb
                src2 = rb if mapping["annotator_1"] == "A" else ra
                adj_prompt = c2ges_adjudication_prompt_v11(
                    doc, item, src1.get("label") if src1 else None,
                    src1.get("checks") if src1 else None,
                    src2.get("label") if src2 else None,
                    src2.get("checks") if src2 else None)
                call = llm_call("C", adj_prompt, env, ledger, qid)
                n_c_called += 1
                adj_rec = {"qid": qid, "ts": utc_now(), "protocol": "v1.2",
                           "retry_of": "v1.1_unresolved", "anon_mapping": mapping,
                           "call_ok": call.get("ok", False), "call_error": call.get("error"),
                           "served_model_id": call.get("served_model_id"),
                           "format_failure": False, "label": None, "abstain": False}
                if call.get("ok"):
                    obj, perr = extract_json(call["text"])
                    if obj is None:
                        adj_rec["format_failure"] = True
                        GATES.record_failure("C", "format")
                    else:
                        note = obj.get("adjudication_note")
                        if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                            adj_rec["abstain"] = True
                            adj_rec["label"] = {"abstain": True,
                                                "abstain_reason": obj.get("abstain_reason"),
                                                "adjudication_note": note}
                        else:
                            lab, checks = validate_c2ges_label(obj, qid, valid_sids)
                            adj_rec["checks"] = checks
                            if lab is not None and checks_passed(checks) and note:
                                lab["adjudication_note"] = note
                                adj_rec["label"] = lab
                            else:
                                adj_rec["format_failure"] = True
                                adj_rec["label"] = lab
                                GATES.record_failure("C", "format")
                append_jsonl(adj12_path, adj_rec)
                if adj_rec["label"] is not None:
                    final_rec.update({"final_source": "adjudication",
                                      "final_label": adj_rec["label"],
                                      "adjudicator_abstain": adj_rec["abstain"]})
                else:
                    final_rec.update({"final_source": "unresolved",
                                      "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(out_path, final_rec)
        tiers[outcome] += 1
        if outcome == "tier1":
            res_dist[res.get("resolution")] = res_dist.get(res.get("resolution"), 0) + 1
        if outcome == "tier2":
            tier2_reasons[res.get("reason")] = tier2_reasons.get(res.get("reason"), 0) + 1
        print(f"[gate_v12] {qid}: {outcome}"
              + (f" ({res.get('resolution') or res.get('reason')})" if outcome != "agreement" else ""))

    # include resumed records in the totals
    all_finals = read_jsonl(out_path)
    tiers = {"agreement": 0, "tier1": 0, "tier2": 0}
    res_dist, tier2_reasons = {}, {}
    for r in all_finals:
        t = r.get("resolution_tier")
        tiers[t] = tiers.get(t, 0) + 1
        if t == "tier1":
            res_dist[r.get("resolution")] = res_dist.get(r.get("resolution"), 0) + 1
        if t == "tier2":
            tier2_reasons[r.get("tier2_reason")] = tier2_reasons.get(r.get("tier2_reason"), 0) + 1
    n = len(all_finals)
    tier2_rate = tiers["tier2"] / n if n else None
    gate = {"ts": utc_now(), "protocol": "C2GES-NERC-ANNOTATION-STAGE2-v1.2",
            "protocol_sha256": PROTOCOLS_STAGE2["c2ges"]["sha256"],
            "n_items": n, "tier_distribution": tiers,
            "tier1_resolution_distribution": res_dist,
            "tier2_reason_distribution": tier2_reasons,
            "tier2_adjudication_rate": tier2_rate, "threshold": 0.5,
            "c_adjudications_reused_from_v1_1": n_c_reused,
            "c_calls_this_gate": n_c_called,
            "final_sources": {s: sum(1 for r in all_finals if r.get("final_source") == s)
                              for s in sorted({r.get("final_source") for r in all_finals})},
            "passed": (tier2_rate is not None and tier2_rate <= 0.5 and n == 12)}
    with open(run_dir / "gate_result_v1_2.json", "w", encoding="utf-8") as f:
        json.dump(gate, f, ensure_ascii=False, indent=2)
    print(f"[gate_v12] tier2 C-adjudication rate on 12 items: {tier2_rate} "
          f"({'PASS' if gate['passed'] else 'NOT PASSED / incomplete'})")
    return gate


def run_c2ges_stage2(env, limit=None):
    run_dir = PILOT_DIR / "runs/c2ges_stage2"
    docs, items = load_c2ges_packet()
    manifest = {
        "stage": "c2ges_stage2_full", "seed": SEED,
        "scope": "ALL 75 questions; v1.1 (R1-R7) prompts, v1.2 two-tier resolution",
        "protocol_sha256": PROTOCOLS_STAGE2["c2ges"]["sha256"],
        "note": "full dev-visible set; no sampling; pilot v1.0 and gate v1.1 labels NOT reused",
        "n_items": len(items), "items": items,
    }
    if limit:
        manifest["limited_to"] = limit
    run_dir.mkdir(parents=True, exist_ok=True)
    with open(run_dir / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return run_c2ges_generic(env, items, docs, run_dir,
                             c2ges_prompt_v11, c2ges_adjudication_prompt_v11, limit,
                             resolver_fn=c2ges_resolve_v12)


def load_ma_stage2_items():
    """91 originals + 30 negative controls, blinded with opaque ids (full mapping in manifest)."""
    run_dir = PILOT_DIR / "runs/ma_stage2"
    neg_path = run_dir / "negative_controls_manifest.json"
    if not neg_path.exists():
        raise SystemExit("FATAL: run generate_negative_controls.py first "
                         f"(missing {neg_path})")
    neg_manifest = json.loads(neg_path.read_text(encoding="utf-8"))
    combined = []
    for it in load_ma_items():
        combined.append({"question_id": it["question_id"], "dataset_id": it["dataset_id"],
                         "question": it["question"], "sql": it["sql"],
                         "template_family": it["template_family"],
                         "is_control": False, "neg_family": None,
                         "source_id": it["question_id"]})
    for n in neg_manifest["controls"]:
        combined.append({"question_id": n["control_id"], "dataset_id": n["dataset_id"],
                         "question": n["question"], "sql": n["perturbed_sql"],
                         "template_family": n.get("template_family"),
                         "is_control": True, "neg_family": n["family"],
                         "source_id": n["source_question_id"]})
    rng = random.Random(SEED)
    rng.shuffle(combined)
    for i, it in enumerate(combined, 1):
        it["blind_id"] = f"MA2_{i:03d}"
    return combined


def run_ma_stage2(env, limit=None):
    run_dir = PILOT_DIR / "runs/ma_stage2"
    items = load_ma_stage2_items()
    manifest = {
        "stage": "ma_stage2_full", "seed": SEED,
        "protocol_sha256": PROTOCOLS_STAGE2["ma"]["sha256"],
        "scope": "91 original AUTO_CANDIDATE + 30 blinded negative controls = 121",
        "blinding": "Random(20260807) shuffle of the combined 121 items; blind ids MA2_001..MA2_121 "
                    "assigned in shuffled order; annotators only ever see blind ids",
        "n_originals": sum(1 for it in items if not it["is_control"]),
        "n_controls": sum(1 for it in items if it["is_control"]),
        "items": items,
    }
    if limit:
        manifest["limited_to"] = limit
    with open(run_dir / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return run_ma_items_generic(env, items, run_dir, "ma_stage2", limit)


def load_ma_stage3_items():
    """85 sealed originals + 30 sealed negative controls, blinded MA3_001...
    Enforces freeze-before-annotate: the sealed packet hash must match the manifest."""
    run_dir = PILOT_DIR / "runs/ma_stage3"
    man_path = run_dir / "sealed_manifest.json"
    pkt_path = run_dir / "sealed_questions.jsonl"
    if not man_path.exists() or not pkt_path.exists():
        raise SystemExit("FATAL: MA sealed set not frozen (run build_ma_sealed_set.py first)")
    sealed_man = json.loads(man_path.read_text(encoding="utf-8"))
    actual = hashlib.sha256(pkt_path.read_bytes()).hexdigest()
    if actual != sealed_man["packet_sha256"]:
        raise SystemExit(f"FATAL: MA sealed packet hash mismatch: {actual} != "
                         f"{sealed_man['packet_sha256']} -- annotation calls forbidden")
    print(f"[ok] MA sealed packet hash verified: {actual[:16]}... (freeze-before-annotate respected)")
    neg_path = run_dir / "negative_controls_manifest.json"
    if not neg_path.exists():
        raise SystemExit("FATAL: run generate_negative_controls.py --stage3 first")
    neg_manifest = json.loads(neg_path.read_text(encoding="utf-8"))
    combined = []
    for line in pkt_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        combined.append({"question_id": r["question_id"], "dataset_id": r["dataset_id"],
                         "question": r["question"], "sql": r["gold_sql"],
                         "template_family": r["template_family"],
                         "is_control": False, "neg_family": None,
                         "source_id": r["question_id"]})
    for n in neg_manifest["controls"]:
        combined.append({"question_id": n["control_id"], "dataset_id": n["dataset_id"],
                         "question": n["question"], "sql": n["perturbed_sql"],
                         "template_family": n.get("template_family"),
                         "is_control": True, "neg_family": n["family"],
                         "source_id": n["source_question_id"]})
    rng = random.Random(SEED)
    rng.shuffle(combined)
    for i, it in enumerate(combined, 1):
        it["blind_id"] = f"MA3_{i:03d}"
    return combined, sealed_man


def run_ma_stage3(env, limit=None):
    run_dir = PILOT_DIR / "runs/ma_stage3"
    items, sealed_man = load_ma_stage3_items()
    manifest = {
        "stage": "ma_stage3_sealed_full", "seed": SEED,
        "protocol_sha256": "FC422FEF02B278D60B6E3850604EAB2E02F0683F7AF02115B6153FB36DC32A4E",
        "sealed_packet_sha256": sealed_man["packet_sha256"],
        "scope": "85 sealed originals + 30 blinded negative controls = 115",
        "blinding": "Random(20260807) shuffle of the combined 115 items; blind ids "
                    "MA3_001..MA3_115 assigned in shuffled order",
        "n_originals": sum(1 for it in items if not it["is_control"]),
        "n_controls": sum(1 for it in items if it["is_control"]),
        "items": items,
    }
    if limit:
        manifest["limited_to"] = limit
    with open(run_dir / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return run_ma_items_generic(env, items, run_dir, "ma_stage3", limit)


def run_ma_items_generic(env, items, run_dir, tag, limit=None):
    ledger = Ledger(run_dir)
    labels_a_path = run_dir / "labels_A.jsonl"
    labels_b_path = run_dir / "labels_B.jsonl"
    adj_path = run_dir / "adjudicated.jsonl"
    final_path = run_dir / "final_labels.jsonl"
    exec_path = run_dir / "execution_facts.jsonl"

    sample = items[:limit] if limit else items

    schema_cache = {}
    def get_schema(dataset_id):
        if dataset_id not in schema_cache:
            schema_cache[dataset_id] = compact_schema(MA_DBS[dataset_id])
        return schema_cache[dataset_id]

    done = {r["question_id"] for r in read_jsonl(labels_a_path)} & \
           {r["question_id"] for r in read_jsonl(labels_b_path)}
    print(f"[{tag}] items={len(sample)} already_done={len(done)}")

    for idx, item in enumerate(sample):
        bid = item["blind_id"]  # annotators see only this id
        if bid in done:
            continue
        schema_text, schema_tables = get_schema(item["dataset_id"])
        # deterministic sandbox execution BEFORE any LLM prompt for this item
        facts = execute_sql_sandbox(MA_DBS[item["dataset_id"]], item["sql"])
        append_jsonl(exec_path, {"question_id": bid, "dataset_id": item["dataset_id"],
                                 "ts": utc_now(), "facts": facts})
        prompt_item = {"question_id": bid, "question": item["question"], "sql": item["sql"]}
        prompt = ma_prompt(schema_text, prompt_item, facts)
        results = {}
        for role, path in (("A", labels_a_path), ("B", labels_b_path)):
            call = llm_call(role, prompt, env, ledger, bid)
            rec = {"question_id": bid, "source_id": item["source_id"],
                   "is_control": item["is_control"], "dataset_id": item["dataset_id"],
                   "annotator": role, "ts": utc_now(),
                   "call_ok": call.get("ok", False), "call_error": call.get("error"),
                   "served_model_id": call.get("served_model_id"),
                   "format_failure": False, "label": None, "checks": None}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    rec["format_failure"] = True
                    rec["checks"] = {"json_parses": False, "parse_error": perr}
                    GATES.record_failure(role, "format")
                else:
                    lab, checks = validate_ma_label(obj, bid, set(schema_tables))
                    rec["checks"] = checks
                    if lab is None or not ma_checks_passed(checks):
                        rec["format_failure"] = True
                        rec["label"] = lab
                        GATES.record_failure(role, "format")
                    else:
                        rec["label"] = lab
            append_jsonl(path, rec)
            results[role] = rec
            print(f"[{tag} {idx+1}/{len(sample)}] {bid} {role}: "
                  f"{'ok' if rec['label'] else 'FAIL:' + str(rec['call_error'] or 'format')}")

        la, lb = results["A"]["label"], results["B"]["label"]
        disagree = True
        if la is not None and lb is not None:
            disagree = (la["answerable_by_schema"] != lb["answerable_by_schema"]
                        or la["semantically_correct"] != lb["semantically_correct"]
                        or la["error_classification"] != lb["error_classification"]
                        or la["abstain"] or lb["abstain"])
        final_rec = {"question_id": bid, "source_id": item["source_id"],
                     "is_control": item["is_control"], "neg_family": item["neg_family"],
                     "dataset_id": item["dataset_id"], "ts": utc_now(),
                     "disagreement": disagree}
        if not disagree:
            final_rec.update({"final_source": "agreement", "final_label": la})
        else:
            mapping = anon_mapping(bid)
            lab1 = results[mapping["annotator_1"]]["label"]
            chk1 = results[mapping["annotator_1"]]["checks"]
            lab2 = results[mapping["annotator_2"]]["label"]
            chk2 = results[mapping["annotator_2"]]["checks"]
            adj_prompt = ma_adjudication_prompt(schema_text, prompt_item, facts,
                                                lab1, chk1, lab2, chk2)
            call = llm_call("C", adj_prompt, env, ledger, bid)
            adj_rec = {"question_id": bid, "ts": utc_now(), "anon_mapping": mapping,
                       "call_ok": call.get("ok", False), "call_error": call.get("error"),
                       "served_model_id": call.get("served_model_id"),
                       "format_failure": False, "label": None, "abstain": False}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    adj_rec["format_failure"] = True
                    GATES.record_failure("C", "format")
                else:
                    note = obj.get("adjudication_note")
                    if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                        adj_rec["abstain"] = True
                        adj_rec["label"] = {"abstain": True,
                                            "abstain_reason": obj.get("abstain_reason"),
                                            "adjudication_note": note}
                    else:
                        lab, checks = validate_ma_label(obj, bid, set(schema_tables))
                        adj_rec["checks"] = checks
                        if lab is not None and ma_checks_passed(checks) and note:
                            lab["adjudication_note"] = note
                            adj_rec["label"] = lab
                        else:
                            adj_rec["format_failure"] = True
                            adj_rec["label"] = lab
                            GATES.record_failure("C", "format")
            append_jsonl(adj_path, adj_rec)
            if adj_rec["label"] is not None:
                final_rec.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                                  "adjudicator_abstain": adj_rec["abstain"]})
            else:
                final_rec.update({"final_source": "unresolved",
                                  "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(final_path, final_rec)

    stats = ma_stats_stage2(run_dir, len(sample))
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[{tag}] done. stats -> {run_dir / 'stats.json'}")
    return stats


def ma_stats_stage2(run_dir, sample_n):
    base = ma_stats(run_dir, sample_n)
    run_dir = Path(run_dir)
    finals = read_jsonl(run_dir / "final_labels.jsonl")
    controls = [r for r in finals if r.get("is_control")]
    originals = [r for r in finals if not r.get("is_control")]

    def detected(r):
        lab = r.get("final_label") or {}
        return lab.get("semantically_correct") is False

    per_family = {}
    for r in controls:
        fam = r.get("neg_family") or "unknown"
        d = per_family.setdefault(fam, {"n": 0, "detected": 0})
        d["n"] += 1
        d["detected"] += 1 if detected(r) else 0
    for fam, d in per_family.items():
        d["detection_rate"] = round(d["detected"] / d["n"], 4) if d["n"] else None
    n_det = sum(1 for r in controls if detected(r))
    orig_false = [r for r in originals
                  if (r.get("final_label") or {}).get("semantically_correct") is False]
    base.update({
        "n_originals": len(originals),
        "n_controls": len(controls),
        "negative_detection_overall": round(n_det / len(controls), 4) if controls else None,
        "negative_detection_per_family": per_family,
        "negative_missed_ids": [r["question_id"] for r in controls if not detected(r)],
        "originals_semantically_false": len(orig_false),
        "originals_semantically_false_ids": [
            {"question_id": r["question_id"], "source_id": r.get("source_id"),
             "error_classification": (r.get("final_label") or {}).get("error_classification")}
            for r in orig_false],
        "originals_error_classification_distribution": _err_dist(originals),
    })
    return base


def _err_dist(originals):
    dist = {}
    for r in originals:
        ec = (r.get("final_label") or {}).get("error_classification")
        dist[ec] = dist.get(ec, 0) + 1
    return dist


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

RETRY_NOTE = "resolved_by_technical_retry_20260807"


def _retry_c_for_item(env, ledger, qid, adj_prompt, validate_fn, checks_fn, validate_ctx,
                      id_field="question_id"):
    """One C adjudication call (llm_call already applies timeout + <=2 technical
    retries). Returns the adjudication record (same shape as the main runners)."""
    call = llm_call("C", adj_prompt, env, ledger, qid)
    adj_rec = {id_field: qid, "ts": utc_now(),
               "retry_note": RETRY_NOTE,
               "call_ok": call.get("ok", False), "call_error": call.get("error"),
               "served_model_id": call.get("served_model_id"),
               "format_failure": False, "label": None, "abstain": False}
    if call.get("ok"):
        obj, perr = extract_json(call["text"])
        if obj is None:
            adj_rec["format_failure"] = True
            GATES.record_failure("C", "format")
        else:
            note = obj.get("adjudication_note")
            if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                adj_rec["abstain"] = True
                adj_rec["label"] = {"abstain": True,
                                    "abstain_reason": obj.get("abstain_reason"),
                                    "adjudication_note": note}
            else:
                lab, checks = validate_fn(obj, qid, validate_ctx)
                adj_rec["checks"] = checks
                if lab is not None and checks_fn(checks) and note:
                    lab["adjudication_note"] = note
                    adj_rec["label"] = lab
                else:
                    adj_rec["format_failure"] = True
                    adj_rec["label"] = lab
                    GATES.record_failure("C", "format")
    return adj_rec


def run_stage2_retry_unresolved(env):
    """Technical retry of stage-2 items whose final label is 'unresolved' because
    the adjudicator channel timed out. Same inputs, same anonymization, same
    adjudication rule; C never returned a successful response for these items, so
    this is NOT a content-based retry. final_labels.jsonl entries are updated in
    place with a note field; the append-only raw ledger keeps the full history."""
    summary = {}

    # ---- C2GES ----
    run_dir = PILOT_DIR / "runs/c2ges_stage2"
    ledger = Ledger(run_dir)
    docs, all_items = load_c2ges_packet()
    by_qid = {it["qid"]: it for it in all_items}
    la = {r["qid"]: r for r in read_jsonl(run_dir / "labels_A.jsonl")}
    lb = {r["qid"]: r for r in read_jsonl(run_dir / "labels_B.jsonl")}
    finals = read_jsonl(run_dir / "final_labels.jsonl")
    resolved, still_unresolved = [], []
    for r in finals:
        if r.get("final_source") != "unresolved":
            continue
        qid = r["qid"]
        item = by_qid[qid]
        doc = docs[item["doc_id"]]
        valid_sids = {s["sid"] for s in doc["sentences"]}
        mapping = anon_mapping(qid)  # deterministic: identical to the original run
        src = {"A": la.get(qid), "B": lb.get(qid)}
        s1, s2 = src[mapping["annotator_1"]], src[mapping["annotator_2"]]
        adj_prompt = c2ges_adjudication_prompt_v11(
            doc, item,
            s1.get("label") if s1 else None, s1.get("checks") if s1 else None,
            s2.get("label") if s2 else None, s2.get("checks") if s2 else None)
        adj_rec = _retry_c_for_item(env, ledger, qid, adj_prompt,
                                    validate_c2ges_label, checks_passed, valid_sids,
                                    id_field="qid")
        adj_rec["anon_mapping"] = mapping
        append_jsonl(run_dir / "adjudicated.jsonl", adj_rec)
        if adj_rec["label"] is not None:
            r.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                      "adjudicator_abstain": adj_rec["abstain"], "note": RETRY_NOTE})
            resolved.append(qid)
        else:
            r["note"] = f"still_unresolved_after_technical_retry_20260807: {adj_rec['call_error'] or 'format_failure'}"
            still_unresolved.append(qid)
        print(f"[retry c2ges] {qid}: {'resolved' if adj_rec['label'] is not None else 'STILL UNRESOLVED'}")
    with open(run_dir / "final_labels.jsonl", "w", encoding="utf-8") as f:
        for r in finals:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    stats = c2ges_stats_v12(run_dir, c2ges_stats(run_dir, len(finals)))
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    summary["c2ges"] = {"resolved": resolved, "still_unresolved": still_unresolved}

    # ---- MA ----
    run_dir = PILOT_DIR / "runs/ma_stage2"
    ledger = Ledger(run_dir)
    items = {it["blind_id"]: it for it in load_ma_stage2_items()}
    la = {r["question_id"]: r for r in read_jsonl(run_dir / "labels_A.jsonl")}
    lb = {r["question_id"]: r for r in read_jsonl(run_dir / "labels_B.jsonl")}
    execs = {r["question_id"]: r["facts"] for r in read_jsonl(run_dir / "execution_facts.jsonl")}
    finals = read_jsonl(run_dir / "final_labels.jsonl")
    schema_cache = {}
    resolved, still_unresolved = [], []
    for r in finals:
        if r.get("final_source") != "unresolved":
            continue
        bid = r["question_id"]
        item = items[bid]
        if item["dataset_id"] not in schema_cache:
            schema_cache[item["dataset_id"]] = compact_schema(MA_DBS[item["dataset_id"]])
        schema_text, schema_tables = schema_cache[item["dataset_id"]]
        prompt_item = {"question_id": bid, "question": item["question"], "sql": item["sql"]}
        facts = execs[bid]  # reuse the recorded deterministic facts (identical inputs)
        mapping = anon_mapping(bid)
        src = {"A": la.get(bid), "B": lb.get(bid)}
        s1, s2 = src[mapping["annotator_1"]], src[mapping["annotator_2"]]
        adj_prompt = ma_adjudication_prompt(
            schema_text, prompt_item, facts,
            s1.get("label") if s1 else None, s1.get("checks") if s1 else None,
            s2.get("label") if s2 else None, s2.get("checks") if s2 else None)
        adj_rec = _retry_c_for_item(env, ledger, bid, adj_prompt,
                                    validate_ma_label, ma_checks_passed, set(schema_tables))
        adj_rec["anon_mapping"] = mapping
        append_jsonl(run_dir / "adjudicated.jsonl", adj_rec)
        if adj_rec["label"] is not None:
            r.update({"final_source": "adjudication", "final_label": adj_rec["label"],
                      "adjudicator_abstain": adj_rec["abstain"], "note": RETRY_NOTE})
            resolved.append(bid)
        else:
            r["note"] = f"still_unresolved_after_technical_retry_20260807: {adj_rec['call_error'] or 'format_failure'}"
            still_unresolved.append(bid)
        print(f"[retry ma] {bid}: {'resolved' if adj_rec['label'] is not None else 'STILL UNRESOLVED'}")
    with open(run_dir / "final_labels.jsonl", "w", encoding="utf-8") as f:
        for r in finals:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    stats = ma_stats_stage2(run_dir, len(finals))
    with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    summary["ma"] = {"resolved": resolved, "still_unresolved": still_unresolved}

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


# ---------------------------------------------------------------------------
# STAGE 3 (sealed-set protocols, authorization DUAL-LLM-ANNOTATION-20260807-03)
# ---------------------------------------------------------------------------

PROTOCOLS_STAGE3 = {
    "c2ges_sealed": {
        "path": PILOT_DIR / "C2GES_SEALED_SET_PROTOCOL_v1.json",
        "sha256": "f1929ee62529d96794082a8868b628837ed51ef8a628fccfaa812efbd3d14eb0",
    },
    "ma_sealed": {
        "path": PILOT_DIR / "MA_SEALED_SET_PROTOCOL_v1.json",
        "sha256": "fc422fef02b278d60b6e3850604eab2e02f0683f7af02115b6153fb36dc32a4e",
    },
}
STAGE3_MAX_CALLS = 550  # STAGE3_AUTHORIZATION_20260807.json (independent count)
SEALED_DIR = PILOT_DIR / "runs/c2ges_stage3"


def verify_protocols_stage3():
    for key, spec in PROTOCOLS_STAGE3.items():
        h = hashlib.sha256(spec["path"].read_bytes()).hexdigest()
        if h != spec["sha256"]:
            raise SystemExit(f"FATAL: stage-3 protocol hash mismatch for {key}: {h}")
    print("[ok] stage-3 protocol hashes verified (c2ges sealed v1, ma sealed v1)")


def load_sealed_packet():
    """Load the frozen sealed packet; abort unless its hash matches the frozen manifest."""
    man_path = SEALED_DIR / "sealed_manifest.json"
    pkt_path = SEALED_DIR / "sealed_packet.jsonl"
    if not man_path.exists() or not pkt_path.exists():
        raise SystemExit("FATAL: sealed packet not frozen yet (run build_sealed_packet.py first)")
    manifest = json.loads(man_path.read_text(encoding="utf-8"))
    actual = hashlib.sha256(pkt_path.read_bytes()).hexdigest()
    if actual != manifest["packet_sha256"]:
        raise SystemExit(f"FATAL: sealed packet hash mismatch: {actual} != "
                         f"{manifest['packet_sha256']} -- annotation calls forbidden")
    print(f"[ok] sealed packet hash verified: {actual[:16]}... (freeze-before-annotate respected)")
    docs = {}
    with open(pkt_path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            docs[d["doc_id"]] = d
    items = []
    for d in docs.values():
        for q in d["questions"]:
            items.append({"doc_id": d["doc_id"], "title": d["title"],
                          "qid": q["qid"], "role": q["role"], "question": q["question"]})
    return docs, items, manifest


def run_c2ges_stage3(env, limit=None):
    docs, items, sealed_manifest = load_sealed_packet()
    manifest = {
        "stage": "c2ges_stage3_sealed_full", "seed": SEED,
        "scope": "sealed set: 15 unused docs x 5 roles = 75 questions",
        "protocol_sha256": PROTOCOLS_STAGE3["c2ges_sealed"]["sha256"],
        "sealed_packet_sha256": sealed_manifest["packet_sha256"],
        "prompt": "v1.1 (R1-R7, qid echo)", "resolution": "v1.2 two-tier",
        "n_items": len(items), "items": items,
    }
    if limit:
        manifest["limited_to"] = limit
    with open(SEALED_DIR / "sample_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return run_c2ges_generic(env, items, docs, SEALED_DIR,
                             c2ges_prompt_v11, c2ges_adjudication_prompt_v11, limit,
                             resolver_fn=c2ges_resolve_v12)


def run_fix_reannotation(env):
    """Re-annotate the 3 fixed v2 candidate SQLs (A/B blind; C only on disagreement)."""
    run_dir = PILOT_DIR / "runs/ma_stage2"
    fixes = read_jsonl(run_dir / "candidate_fixes_v2.jsonl")
    if not fixes:
        raise SystemExit("FATAL: run fix_candidates_v2.py first")
    ledger = Ledger(run_dir, filename="fix_reannotation.raw_ledger.jsonl")
    out_path = run_dir / "fix_reannotation.jsonl"
    exec_path = run_dir / "fix_reannotation.execution_facts.jsonl"
    items_by_id = {it["question_id"]: it for it in load_ma_items()}
    schema_cache = {}
    done = {r["question_id"] for r in read_jsonl(out_path)}
    for fix in fixes:
        qid = "FIX_" + fix["question_id"]
        if qid in done:
            continue
        src = items_by_id[fix["question_id"]]
        if fix["dataset_id"] not in schema_cache:
            schema_cache[fix["dataset_id"]] = compact_schema(MA_DBS[fix["dataset_id"]])
        schema_text, schema_tables = schema_cache[fix["dataset_id"]]
        facts = execute_sql_sandbox(MA_DBS[fix["dataset_id"]], fix["fixed_sql"])
        append_jsonl(exec_path, {"question_id": qid, "dataset_id": fix["dataset_id"],
                                 "ts": utc_now(), "facts": facts})
        prompt_item = {"question_id": qid, "question": src["question"],
                       "sql": fix["fixed_sql"]}
        prompt = ma_prompt(schema_text, prompt_item, facts)
        results = {}
        for role in ("A", "B"):
            call = llm_call(role, prompt, env, ledger, qid)
            rec = {"annotator": role, "call_ok": call.get("ok", False),
                   "call_error": call.get("error"),
                   "served_model_id": call.get("served_model_id"),
                   "format_failure": False, "label": None, "checks": None}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    rec["format_failure"] = True
                    rec["checks"] = {"json_parses": False, "parse_error": perr}
                    GATES.record_failure(role, "format")
                else:
                    lab, checks = validate_ma_label(obj, qid, set(schema_tables))
                    rec["checks"] = checks
                    if lab is None or not ma_checks_passed(checks):
                        rec["format_failure"] = True
                        rec["label"] = lab
                        GATES.record_failure(role, "format")
                    else:
                        rec["label"] = lab
            results[role] = rec
            print(f"[fix {qid}] {role}: "
                  f"{'ok' if rec['label'] else 'FAIL:' + str(rec['call_error'] or 'format')}")
        la, lb = results["A"]["label"], results["B"]["label"]
        disagree = True
        if la is not None and lb is not None:
            disagree = (la["answerable_by_schema"] != lb["answerable_by_schema"]
                        or la["semantically_correct"] != lb["semantically_correct"]
                        or la["error_classification"] != lb["error_classification"]
                        or la["abstain"] or lb["abstain"])
        out = {"question_id": qid, "source_id": fix["question_id"],
               "dataset_id": fix["dataset_id"], "ts": utc_now(),
               "fixed_sql": fix["fixed_sql"], "disagreement": disagree,
               "label_A": la, "label_B": lb,
               "format_failure_A": results["A"]["format_failure"],
               "format_failure_B": results["B"]["format_failure"]}
        if not disagree:
            out.update({"final_source": "agreement", "final_label": la})
        else:
            mapping = anon_mapping(qid)
            s1 = results[mapping["annotator_1"]]
            s2 = results[mapping["annotator_2"]]
            adj_prompt = ma_adjudication_prompt(schema_text, prompt_item, facts,
                                                s1["label"], s1["checks"],
                                                s2["label"], s2["checks"])
            call = llm_call("C", adj_prompt, env, ledger, qid)
            adj_rec = {"anon_mapping": mapping, "call_ok": call.get("ok", False),
                       "call_error": call.get("error"), "label": None, "abstain": False}
            if call.get("ok"):
                obj, perr = extract_json(call["text"])
                if obj is None:
                    adj_rec["format_failure"] = True
                    GATES.record_failure("C", "format")
                else:
                    note = obj.get("adjudication_note")
                    if obj.get("abstain") is True and (note or obj.get("abstain_reason")):
                        adj_rec["abstain"] = True
                        adj_rec["label"] = {"abstain": True,
                                            "abstain_reason": obj.get("abstain_reason"),
                                            "adjudication_note": note}
                    else:
                        lab, checks = validate_ma_label(obj, qid, set(schema_tables))
                        adj_rec["checks"] = checks
                        if lab is not None and ma_checks_passed(checks) and note:
                            lab["adjudication_note"] = note
                            adj_rec["label"] = lab
                        else:
                            adj_rec["format_failure"] = True
                            adj_rec["label"] = lab
                            GATES.record_failure("C", "format")
            out["adjudication"] = adj_rec
            if adj_rec["label"] is not None:
                out.update({"final_source": "adjudication", "final_label": adj_rec["label"]})
            else:
                out.update({"final_source": "unresolved",
                            "reason": call.get("error") or "adjudicator format failure"})
        append_jsonl(out_path, out)
    print(f"[fix] reannotation -> {out_path}")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", choices=["c2ges", "ma", "both"], default=None,
                    help="pilot (v1.0) mode")
    ap.add_argument("--stage2", choices=["gate", "c2ges", "ma", "all", "retry"], default=None,
                    help="stage-2 mode: gate | c2ges full | ma full | all | retry (C-retry unresolved)")
    ap.add_argument("--stage3", choices=["fix", "c2ges", "ma", "all"], default=None,
                    help="stage-3 mode: fix reannotation | c2ges sealed | ma sealed | all")
    ap.add_argument("--limit", type=int, default=None,
                    help="only run first N sampled items per paper (smoke test)")
    args = ap.parse_args()
    if not args.paper and not args.stage2 and not args.stage3:
        ap.error("one of --paper / --stage2 / --stage3 is required")

    env = load_env()
    for k in ("DEEPSEEK_BASE_URL", "DEEPSEEK_API_KEY", "GEMINI_API_KEY",
              "CLOUBIC_BASE_URL", "CLOUBIC_API_KEY"):
        if not env.get(k):
            raise SystemExit(f"FATAL: missing env key {k} in .env / .env.cloubic")
    print("[ok] env keys present (values never logged)")

    if args.stage2:
        verify_protocols_v11()
        GATES.max_calls = STAGE2_MAX_CALLS
        # stage-2 budget covers all stage-2 ledgers (gate + full runs)
        for d in ("runs/c2ges_stage2", "runs/c2ges_stage2/validation_gate", "runs/ma_stage2"):
            GATES.total_calls += Ledger(PILOT_DIR / d).count_calls()
        print(f"[ok] prior stage-2 calls counted: {GATES.total_calls} / {GATES.max_calls}")

        if args.stage2 in ("gate", "all"):
            gate = run_c2ges_gate(env, args.limit)
            if args.stage2 == "all" and not args.limit and not gate["passed"]:
                print("[STOP] validation gate NOT passed (adjudication rate > 0.5 or "
                      "incomplete); full runs skipped per protocol. See "
                      "runs/c2ges_stage2/validation_gate/gate_result.json")
                return
        if args.stage2 in ("c2ges", "all"):
            run_c2ges_stage2(env, args.limit)
        if args.stage2 in ("ma", "all"):
            run_ma_stage2(env, args.limit)
        if args.stage2 == "retry":
            run_stage2_retry_unresolved(env)
        print(f"[done] stage-2 total llm calls: {GATES.total_calls} / {GATES.max_calls}; "
              f"halted: {GATES.halted or 'none'}")
        return

    if args.stage3:
        verify_protocols_stage3()
        GATES.max_calls = STAGE3_MAX_CALLS
        # stage-3 budget: independent count over stage-3 ledgers only
        GATES.total_calls += Ledger(SEALED_DIR).count_calls()
        GATES.total_calls += Ledger(PILOT_DIR / "runs/ma_stage2",
                                    filename="fix_reannotation.raw_ledger.jsonl").count_calls()
        GATES.total_calls += Ledger(PILOT_DIR / "runs/ma_stage3").count_calls()
        print(f"[ok] prior stage-3 calls counted: {GATES.total_calls} / {GATES.max_calls}")
        if args.stage3 in ("fix", "all"):
            run_fix_reannotation(env)
        if args.stage3 in ("c2ges", "all"):
            run_c2ges_stage3(env, args.limit)
        if args.stage3 in ("ma", "all"):
            run_ma_stage3(env, args.limit)
        print(f"[done] stage-3 total llm calls: {GATES.total_calls} / {GATES.max_calls}; "
              f"halted: {GATES.halted or 'none'}")
        return

    # ---- pilot (v1.0) mode ----
    verify_protocols()
    # initialize the global call counter from existing ledgers (append-only history,
    # including the archived smoke run — those calls count toward the 400-call cap)
    for d in ("runs/c2ges_pilot", "runs/ma_pilot",
              "runs/_smoke_archive_20260807/c2ges", "runs/_smoke_archive_20260807/ma"):
        GATES.total_calls += Ledger(PILOT_DIR / d).count_calls()
    print(f"[ok] prior ledger calls counted: {GATES.total_calls}")

    if args.paper in ("c2ges", "both"):
        run_c2ges(env, args.limit)
    if args.paper in ("ma", "both"):
        run_ma(env, args.limit)
    print(f"[done] total llm calls (incl. prior): {GATES.total_calls}; "
          f"halted: {GATES.halted or 'none'}")


if __name__ == "__main__":
    main()
