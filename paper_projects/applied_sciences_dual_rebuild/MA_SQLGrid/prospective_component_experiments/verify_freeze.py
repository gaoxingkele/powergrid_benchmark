#!/usr/bin/env python3
"""Fail closed if the prospective component freeze has drifted."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(parent for parent in HERE.parents if (parent / "paper_projects").is_dir())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    freeze = json.loads((HERE / "PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
    assert freeze["schema_version"] == "ma-sqlgrid-prospective-components-freeze-v1.1"
    assert freeze["status"] == "protocol_and_prompts_frozen_not_executed"
    assert freeze["formal_model_execution_started"] is False
    for relative, expected in freeze["input_hashes"].items():
        path = REPO / relative
        assert path.is_file(), f"missing frozen input: {relative}"
        assert path.stat().st_size == expected["bytes"], f"size drift: {relative}"
        assert sha256_file(path) == expected["sha256"], f"hash drift: {relative}"
    assert sha256_file(HERE / "frozen_prompts.jsonl") == freeze["prompt_ledger_sha256"]
    assert sha256_file(HERE / "warmup_prompts.jsonl") == freeze["warmup_ledger_sha256"]
    prompts = jsonl(HERE / "frozen_prompts.jsonl")
    assert len(prompts) == 360
    assert len({(row["question_id"], row["condition"]) for row in prompts}) == 360
    assert len({row["question_id"] for row in prompts}) == 180
    for row in prompts:
        assert hashlib.sha256(row["prompt"].encode()).hexdigest() == row["prompt_sha256"]
        assert hashlib.sha256(row["context"].encode()).hexdigest() == row["context_sha256"]
        assert "gold_sql" not in row["prompt"].lower()
        if row["condition"] == "V0_NoValueEvidence":
            assert "Exact database values matched from the question:" not in row["context"]
            assert "Power-grid domain normalization hints" not in row["context"]
    for model in ("qwen", "granite"):
        order_path = HERE / f"call_order_{model}.jsonl"
        assert sha256_file(order_path) == freeze["call_order_sha256"][model]
        order = jsonl(order_path)
        assert len(order) == freeze["formal_calls_per_model"][model]
        assert [row["call_index"] for row in order] == list(range(len(order)))
        assert len({(row["question_id"], row["condition"]) for row in order}) == len(order)
    audit = json.loads((HERE / "STATISTICAL_IMPLEMENTATION_AUDIT.json").read_text(encoding="utf-8"))
    assert audit["status"] == "pass_before_any_formal_output"
    assert audit["tests_run"] == audit["tests_passed"] == 8 and audit["tests_failed"] == 0
    for relative, expected in audit["artifacts"].items():
        path = HERE / relative
        assert path.stat().st_size == expected["bytes"]
        assert sha256_file(path) == expected["sha256"]
    print("PASS: frozen prompt, intervention, and call-order ledgers are internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
