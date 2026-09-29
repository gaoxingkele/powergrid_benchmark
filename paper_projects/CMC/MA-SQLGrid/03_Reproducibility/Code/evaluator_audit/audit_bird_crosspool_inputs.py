"""Inspect retained BIRD input identity/completeness without scoring a selector.

No SQL, questions, model responses or credentials are copied into the output.
Historical correctness labels are present in the input but not summarized here.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

REPRO = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or not args.output.parent.is_dir():
        parser.error("Output must be new with an existing parent")
    prior = json.loads((REPRO / "Data/BIRD_aggregates/POST_RUN_INDEPENDENT_AUDIT_v1_1.json").read_text(encoding="utf-8"))
    report = {"status": "INPUT_AUDIT_ONLY", "exposure": "historical outcomes already inspected; not unseen",
              "models": {}, "core_selector_replayed": False, "new_model_calls": 0}
    populations = []
    tracked = {}
    for model in ("qwen", "granite"):
        folder = args.protocol / "formal_runs" / ("MA_PUBLIC_BIRD_v1_1_" + model + "_clean1")
        files = {}
        for name in ("final_scores", "call_ledger"):
            path = folder / (name + ".jsonl")
            actual = sha(path)
            tracked[path] = actual
            expected = prior["artifact_hashes"][model][name + "_sha256"]
            if actual != expected:
                raise ValueError("Historical source hash mismatch: " + str(path))
            files[name] = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        finals, calls = files["final_scores"], files["call_ledger"]
        if len(finals) != 2000 or len(calls) != 2500:
            raise ValueError("Unexpected retained population")
        keys = [(r["question_id"], r["method"]) for r in finals]
        if len(set(keys)) != 2000:
            raise ValueError("Duplicate question/method key")
        population = {(r["question_id"], r["db_id"]) for r in finals}
        populations.append(population)
        per_question = Counter(r["question_id"] for r in finals)
        if len(population) != 500 or set(per_question.values()) != {4}:
            raise ValueError("Incomplete four-slot populations")
        report["models"][model] = {
            "final_rows": len(finals), "calls": len(calls), "questions": len(population),
            "databases": len({db for _, db in population}),
            "method_counts": dict(Counter(r["method"] for r in finals)),
            "nonempty_final_sql": sum(isinstance(r.get("final_sql"), str) and bool(r["final_sql"].strip()) for r in finals),
            "field_names": sorted(set().union(*(r.keys() for r in finals))),
            "historical_hashes_verified": True,
            "missing_replay_features": [k for k in ("shape_ok", "order_ok", "value_hits", "safe", "executable")
                                        if not all(k in r for r in finals)]}
    if populations[0] != populations[1]:
        raise ValueError("Backbone item populations differ")
    annotations = args.protocol / "official_metadata/bird_mini_dev_sqlite.json"
    report["annotations_present"] = annotations.is_file()
    report["annotations_sha256"] = sha(annotations) if annotations.is_file() else None
    databases = args.protocol / "official_downloads/bird_dev_databases_extracted/dev_databases"
    report["databases_present"] = {db: (databases / db / (db + ".sqlite")).is_file()
                                    for db in sorted({db for _, db in populations[0]})}
    report["source_hashes"] = {str(path): value for path, value in tracked.items()}
    if any(sha(path) != value for path, value in tracked.items()):
        raise ValueError("Source changed during input audit")
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
