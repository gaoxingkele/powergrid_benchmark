"""Post-run independent audit for MA-PUBLIC-BIRD-MINIDEV-v1.1."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import random
from collections import defaultdict
from pathlib import Path

import freeze_public_baseline_v1_1 as f

ROOT = Path(__file__).resolve().parent
RUNS = {
    "qwen": ROOT / "formal_runs" / "MA_PUBLIC_BIRD_v1_1_qwen_clean1",
    "granite": ROOT / "formal_runs" / "MA_PUBLIC_BIRD_v1_1_granite_clean1",
}
OUT = ROOT / "formal_runs" / "MA_PUBLIC_BIRD_v1_1_postrun_audit"


def rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def holm(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    adjusted = [0.0] * len(values)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(values) - rank) * values[index]))
        adjusted[index] = running
    return adjusted


def cluster_ci(records: list[dict], samples: int = 20000) -> tuple[float, float]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for record in records:
        grouped[record["db_id"]].append(record["official_ex"])
    names = sorted(grouped)
    rng = random.Random(20260808)
    draws = []
    for _ in range(samples):
        selected = [rng.choice(names) for _ in names]
        values = [score for name in selected for score in grouped[name]]
        draws.append(sum(values) / len(values))
    draws.sort()
    return draws[int(0.025 * samples)], draws[int(0.975 * samples)]


def exact_cluster_sign_p(differences: list[int]) -> float:
    observed = abs(sum(differences))
    extreme = 0
    total = 1 << len(differences)
    for mask in range(total):
        value = sum((1 if mask & (1 << i) else -1) * d for i, d in enumerate(differences))
        extreme += abs(value) >= observed
    return extreme / total


def main() -> int:
    if OUT.exists():
        raise SystemExit(f"Audit output already exists: {OUT}")
    freeze_path = ROOT / "BASELINE_PROTOCOL_FREEZE_v1_1.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    order = rows(ROOT / "DETERMINISTIC_CALL_ORDER.jsonl")
    question_rows = {r["question_id"]: r for r in f.load_rows()}
    checks: dict[str, bool] = {
        "freeze_hash": sha(freeze_path) == "0aba454650c569d51183d4a96248ff977a5dbdf3a82a77c62592162f28f9f640",
        "call_order_2500": len(order) == 2500,
        "runtime_python": __import__("platform").python_version() == "3.10.11",
        "runtime_sqlite": __import__("sqlite3").sqlite_version == "3.40.1",
    }
    all_finals: list[dict] = []
    artifact_hashes = {}
    expected_call_keys = [(r["question_id"], r["db_id"], r["method"], r["call"]) for r in order]
    expected_final_keys = {(r["question_id"], method) for r in question_rows.values() for method in f.METHODS}
    for model, directory in RUNS.items():
        manifest = json.loads((directory / "RUN_MANIFEST.json").read_text(encoding="utf-8"))
        calls = rows(directory / "call_ledger.jsonl")
        finals = rows(directory / "final_scores.jsonl")
        call_hash = sha(directory / "call_ledger.jsonl")
        final_hash = sha(directory / "final_scores.jsonl")
        keys = [(r["question_id"], r["db_id"], r["method"], r["call"]) for r in calls]
        final_keys = {(r["question_id"], r["method"]) for r in finals}
        checks[f"{model}_manifest"] = (
            manifest["protocol_id"] == freeze["protocol_id"]
            and manifest["freeze_sha256"] == sha(freeze_path)
            and manifest["model_sha256"] == freeze["models"][model]["sha256"]
            and manifest["calls"] == 2500 and manifest["retries"] == 0
            and manifest["formal_run_complete"] is True
            and manifest["call_ledger_sha256"] == call_hash
            and manifest["final_scores_sha256"] == final_hash
        )
        checks[f"{model}_call_population"] = (
            len(calls) == len(set(keys)) == 2500 and keys == expected_call_keys
            and [r["call_index"] for r in calls] == list(range(2500))
            and [r["formal_call_number"] for r in calls] == list(range(1, 2501))
            and all(r["retry_count"] == 0 and r["model"] == model for r in calls)
        )
        checks[f"{model}_final_population"] = len(finals) == len(final_keys) == 2000 and final_keys == expected_final_keys
        artifact_hashes[model] = {"call_ledger_sha256": call_hash, "final_scores_sha256": final_hash}
        all_finals.extend(finals)

    gold_cache = {}
    mismatches = []
    for qid, row in question_rows.items():
        gold_cache[qid] = f.safe_execute(row["SQL"], f.db_path(row["db_id"]), timeout_seconds=180.0)
    for index, record in enumerate(all_finals):
        status, predicted = f.safe_execute(record["final_sql"], f.db_path(record["db_id"]), timeout_seconds=180.0)
        gold_status, gold = gold_cache[record["question_id"]]
        score = f.official_ex(predicted or [], gold or []) if status == "SAFE_EXECUTED" and gold_status == "SAFE_EXECUTED" else 0
        if status != record["prediction_status"] or score != record["official_ex"]:
            mismatches.append({"index": index, "question_id": record["question_id"], "model": record["model"]})
    checks["direct_reexecution_4000"] = len(all_finals) == 4000 and not mismatches
    checks["all_gold_safe_500"] = len(gold_cache) == 500 and all(x[0] == "SAFE_EXECUTED" for x in gold_cache.values())
    checks["incident_exclusion"] = all("clean1" in str(path) for path in RUNS.values()) and freeze["excluded_incidents"]["physical_calls_completed"] == 2476

    summaries = []
    for model in RUNS:
        for method in f.METHODS:
            subset = [r for r in all_finals if r["model"] == model and r["method"] == method]
            low, high = cluster_ci(subset)
            summaries.append({"model": model, "method": method, "n": len(subset), "correct": sum(r["official_ex"] for r in subset), "accuracy": sum(r["official_ex"] for r in subset) / len(subset), "cluster_ci_low": low, "cluster_ci_high": high})
    contrasts = []
    for model in RUNS:
        indexed = {(r["question_id"], r["method"]): r for r in all_finals if r["model"] == model}
        for left, right in itertools.combinations(f.METHODS, 2):
            differences = []
            for db_id in sorted({r["db_id"] for r in question_rows.values()}):
                qids = [qid for qid, r in question_rows.items() if r["db_id"] == db_id]
                differences.append(sum(indexed[(q, right)]["official_ex"] - indexed[(q, left)]["official_ex"] for q in qids))
            contrasts.append({"model": model, "left": left, "right": right, "delta": sum(differences) / 500, "exact_cluster_sign_p": exact_cluster_sign_p(differences)})
    adjusted = holm([r["exact_cluster_sign_p"] for r in contrasts])
    for record, value in zip(contrasts, adjusted):
        record["holm_p_12"] = value

    OUT.mkdir(parents=True)
    for name, data in (("method_summary.csv", summaries), ("cluster_contrasts_holm.csv", contrasts)):
        with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader(); writer.writerows(data)
    report = {"protocol_id": freeze["protocol_id"], "freeze_sha256": sha(freeze_path), "decision": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "passed": sum(checks.values()), "total": len(checks), "formal_calls": 5000, "final_rows": 4000, "retries": 0, "direct_reexecution_mismatches": mismatches, "artifact_hashes": artifact_hashes, "statistical_family": "12 within-model pairwise method contrasts; exact database-cluster sign randomization; Holm adjustment", "method_summary": summaries, "contrasts": contrasts}
    (OUT / "POST_RUN_INDEPENDENT_AUDIT_v1_1.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decision": report["decision"], "passed": report["passed"], "total": report["total"], "output": str(OUT)}))
    return 0 if report["decision"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
