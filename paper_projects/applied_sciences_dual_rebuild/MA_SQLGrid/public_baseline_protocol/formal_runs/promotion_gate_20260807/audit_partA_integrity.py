"""Promotion-gate audit part A: integrity verification (hashing/parsing only, no SQL).

Writes _partA_results.json next to this script. Read-only w.r.t. all frozen/ledger files.
"""
import gzip
import hashlib
import json
import os
from pathlib import Path

P = Path(r"D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\public_baseline_protocol")
OUT = P / "formal_runs" / "promotion_gate_20260807"
EXPECTED_FREEZE_SHA = "c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b"
EXPECTED_EVALUATOR_SHA = "da1bbcd4530be83692d7c650c814ea9704bb710d0c953eb75d02ccb38233cf89"
MODELS = ("qwen", "granite")
METHODS = ("B0_DIRECT", "B1_DECOMP", "B2_SCHEMA_SELECT", "B3_EXEC_REPAIR")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


checks = {}
details = {}
discrepancies = []


def check(name, ok, detail=None):
    checks[name] = bool(ok)
    if detail is not None:
        details[name] = detail
    if not ok:
        discrepancies.append({"check": name, "detail": detail})


# ---- freeze + evaluator + audit + approval ----
freeze_path = P / "BASELINE_PROTOCOL_FREEZE.json"
freeze_hash = sha256(freeze_path)
freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
check("freeze_sha256_matches_expected", freeze_hash == EXPECTED_FREEZE_SHA, freeze_hash)

eval_path = P / "official_evaluator_b3d4bcb" / "evaluation_ex.py"
eval_hash = sha256(eval_path)
check("evaluator_ex_sha256_matches", eval_hash == EXPECTED_EVALUATOR_SHA, eval_hash)
eval_utils_hash = sha256(P / "official_evaluator_b3d4bcb" / "evaluation_utils.py")
check("evaluator_utils_sha256_matches",
      eval_utils_hash == freeze["execution"]["evaluator"]["evaluation_utils"]["sha256"], eval_utils_hash)

audit = json.loads((P / "INDEPENDENT_TECHNICAL_FREEZE_AUDIT.json").read_text(encoding="utf-8"))
check("independent_audit_binds_freeze_and_pass",
      audit.get("decision") == "PASS"
      and audit.get("protocol_id") == freeze["protocol_id"]
      and audit.get("freeze_sha256") == freeze_hash,
      {"decision": audit.get("decision"), "protocol_id": audit.get("protocol_id"),
       "freeze_sha256": audit.get("freeze_sha256")})
for key in ("summary", "totals", "checks_summary", "results"):
    if key in audit:
        details.setdefault("independent_audit_extra", {})[key] = audit[key]

approval_path = P.parent / "human_launch_approval_bird_20260807.json"
approval = json.loads(approval_path.read_text(encoding="utf-8"))
check("approval_binds_freeze",
      bool(approval.get("approved_by_human"))
      and approval.get("acknowledge_5000_generation_calls") is True
      and approval.get("protocol_id") == freeze["protocol_id"]
      and approval.get("freeze_sha256") == freeze_hash,
      approval)

# ---- dataset metadata + databases + model files ----
meta = freeze["dataset"]["metadata"]
check("bird_metadata_sha256", sha256(Path(meta["path"])) == meta["sha256"])
db_ok = True
db_detail = {}
for db_id, item in freeze["dataset"]["database_manifest"].items():
    h = sha256(Path(item["path"]))
    db_detail[db_id] = h
    if h != item["sha256"]:
        db_ok = False
check("database_sha256_all_11", db_ok and len(db_detail) == 11, db_detail)

for model in MODELS:
    info = freeze["models"][model]
    h = sha256(Path(info["path"]))
    check(f"model_file_sha256_{model}", h == info["sha256"], {"path": info["path"], "sha256": h})

# ---- materialized prompts + call order frozen hashes ----
mat = freeze["prompt_materialization"]
order_path = P / "DETERMINISTIC_CALL_ORDER.jsonl"
check("call_order_sha256", sha256(order_path) == mat["call_order"]["sha256"])
order = [json.loads(line) for line in order_path.read_text(encoding="utf-8").splitlines()]
check("call_order_rows_2500", len(order) == 2500, len(order))

prompts = {}
for model in MODELS:
    gz_path = P / "materialized_prompts" / f"{model}_prompts.jsonl.gz"
    man_path = P / "materialized_prompts" / f"{model}_prompt_manifest.jsonl"
    check(f"prompts_gz_sha256_{model}", sha256(gz_path) == mat["prompt_manifests"][gz_path.name]["sha256"])
    check(f"prompt_manifest_sha256_{model}", sha256(man_path) == mat["prompt_manifests"][man_path.name]["sha256"])
    with gzip.open(gz_path, "rt", encoding="utf-8") as handle:
        prompts[model] = [json.loads(line) for line in handle]
    check(f"prompts_rows_2500_{model}", len(prompts[model]) == 2500, len(prompts[model]))

# ---- incident separation (fact record) ----
formal_runs = P / "formal_runs"
details["formal_runs_directories"] = sorted(
    d.name for d in formal_runs.iterdir() if d.is_dir()
)
old_dirs = [d for d in formal_runs.iterdir() if d.is_dir() and "_v101_" not in d.name]
separation = []
for d in old_dirs:
    man = d / "RUN_MANIFEST.json"
    separation.append({
        "dir": d.name,
        "has_run_manifest": man.is_file(),
        "manifest_freeze_sha256": (json.loads(man.read_text(encoding="utf-8")).get("freeze_sha256") if man.is_file() else None),
        "files": sorted(f.name for f in d.iterdir()),
    })
details["legacy_attempt_dirs"] = separation
check("legacy_attempt_dirs_separate_from_v101",
      all("_v101_" not in s["dir"] for s in separation)
      and all(s["manifest_freeze_sha256"] != EXPECTED_FREEZE_SHA for s in separation),
      separation)

# ---- per-model ledgers ----
stats_store = {}
for model in MODELS:
    d = formal_runs / f"MA_PUBLIC_BIRD_v101_{model}"
    manifest = json.loads((d / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
    prefix = f"manifest_{model}"
    check(f"{prefix}_fields",
          manifest.get("calls") == 2500 and manifest.get("retries") == 0
          and manifest.get("expected_final_rows") == 2000 and manifest.get("formal_run_complete") is True
          and manifest.get("protocol_id") == freeze["protocol_id"],
          manifest)
    check(f"{prefix}_freeze_sha256", manifest.get("freeze_sha256") == freeze_hash)
    check(f"{prefix}_model_sha256", manifest.get("model_sha256") == freeze["models"][model]["sha256"])
    cl_path, fs_path = d / "call_ledger.jsonl", d / "final_scores.jsonl"
    check(f"{prefix}_call_ledger_sha256", sha256(cl_path) == manifest.get("call_ledger_sha256"))
    check(f"{prefix}_final_scores_sha256", sha256(fs_path) == manifest.get("final_scores_sha256"))

    ledger = [json.loads(line) for line in cl_path.read_text(encoding="utf-8").splitlines()]
    check(f"ledger_rows_2500_{model}", len(ledger) == 2500, len(ledger))

    idx_ok = sorted(e["call_index"] for e in ledger) == list(range(2500))
    check(f"ledger_call_index_0_2499_{model}", idx_ok)
    fcn_ok = sorted(e["formal_call_number"] for e in ledger) == list(range(1, 2501))
    check(f"ledger_formal_call_number_1_2500_{model}", fcn_ok)
    check(f"ledger_retry_count_all_zero_{model}", all(e["retry_count"] == 0 for e in ledger))

    # identity vs DETERMINISTIC_CALL_ORDER, same sequence position
    mism = []
    for e in ledger:
        o = order[e["call_index"]]
        if (e["question_id"], e["method"], e["call"]) != (o["question_id"], o["method"], o["call"]) or e["db_id"] != o["db_id"]:
            mism.append(e["call_index"])
    check(f"ledger_matches_call_order_{model}", not mism, mism[:20])

    # prompt binding: re-render and compare hash
    first_call = {}  # question_id -> (extracted_sql, validator_feedback)
    for e in ledger:
        if e["method"] == "B3_EXEC_REPAIR" and e["call"] == 1:
            first_call[e["question_id"]] = (e["extracted_sql"], e.get("validator_feedback"))
    check(f"ledger_b3_call1_feedback_present_{model}",
          len(first_call) == 500 and all(v[1] in mat["feedback_vocabulary"] for v in first_call.values()),
          len(first_call))
    hash_mism = []
    ident_mism = []
    for e in ledger:
        rec = prompts[model][e["call_index"]]
        if (rec["question_id"], rec["db_id"], rec["method"], rec["call"]) != (e["question_id"], e["db_id"], e["method"], e["call"]):
            ident_mism.append(e["call_index"])
            continue
        rendered = rec["rendered_prompt"]
        if e["method"] == "B3_EXEC_REPAIR" and e["call"] == 2:
            cand, fb = first_call[e["question_id"]]
            rendered = rendered.replace("{{FIRST_CANDIDATE_RUNTIME_MAX_400_TOKENS}}", cand)
            rendered = rendered.replace("{{ONE_OF_FROZEN_FEEDBACK_VOCABULARY}}", fb)
        if text_sha(rendered) != e["rendered_prompt_sha256"]:
            hash_mism.append({"call_index": e["call_index"], "question_id": e["question_id"],
                              "method": e["method"], "call": e["call"]})
    check(f"prompt_record_identity_{model}", not ident_mism, ident_mism[:20])
    check(f"prompt_hash_binding_{model}", not hash_mism, {"mismatch_count": len(hash_mism), "first": hash_mism[:10]})

    # raw_output_sha256 self-consistency + extract_sql reproduction
    raw_mism = []
    for e in ledger:
        if text_sha(e["raw_output"]) != e["raw_output_sha256"]:
            raw_mism.append(e["call_index"])
    check(f"raw_output_sha256_consistent_{model}", not raw_mism, raw_mism[:20])

    # final scores
    scores = [json.loads(line) for line in fs_path.read_text(encoding="utf-8").splitlines()]
    check(f"final_rows_2000_{model}", len(scores) == 2000, len(scores))
    pairs = {(s["question_id"], s["method"]) for s in scores}
    qids = {s["question_id"] for s in scores}
    check(f"final_coverage_500x4_{model}", len(pairs) == 2000 and len(qids) == 500 and all(
        (q, m) in pairs for q in qids for m in METHODS))
    check(f"final_all_attempt_denominator_{model}", all(s["all_attempt_denominator"] is True for s in scores))
    check(f"final_model_field_{model}", all(s["model"] == model for s in scores))
    # cross-bind final rows to ledger final calls
    final_calls = {(e["question_id"], e["method"]): e for e in ledger
                   if e["method"] != "B3_EXEC_REPAIR" or e["call"] == 2}
    bind_mism = []
    for s in scores:
        e = final_calls.get((s["question_id"], s["method"]))
        if e is None or e["extracted_sql"] != s["final_sql"] or e["db_id"] != s["db_id"]:
            bind_mism.append((s["question_id"], s["method"]))
    check(f"final_sql_binds_ledger_{model}", not bind_mism, bind_mism[:20])
    stats_store[model] = {
        "ledger_scores": [{"question_id": s["question_id"], "db_id": s["db_id"], "method": s["method"],
                           "prediction_status": s["prediction_status"], "official_ex": s["official_ex"]}
                          for s in scores]
    }

result = {"checks": checks, "details": details, "discrepancies": discrepancies,
          "n_checks": len(checks), "n_pass": sum(1 for v in checks.values() if v)}
(OUT / "_partA_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(OUT / "_ledger_scores.json").write_text(json.dumps(stats_store, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"n_checks": result["n_checks"], "n_pass": result["n_pass"],
                  "failed": [k for k, v in checks.items() if not v]}, ensure_ascii=False))
