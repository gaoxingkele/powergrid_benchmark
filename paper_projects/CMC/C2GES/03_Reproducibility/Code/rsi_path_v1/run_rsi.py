"""Orchestrate RSI: seen check, evolve on 12-dev, freeze, then score 15-test."""
from __future__ import annotations

import json

import evolve_dev
import score_eval
import seen_check
from rsi_common import PROTOCOL_PATH, RUN_DIR, assert_run_dir_writable, sha256


def main() -> dict:
    assert_run_dir_writable(RUN_DIR)
    seen = seen_check.main()
    freeze = evolve_dev.main()
    summary = score_eval.main()
    return {
        "protocol_sha256": sha256(PROTOCOL_PATH),
        "seen": seen,
        "freeze": freeze,
        "summary": summary,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
