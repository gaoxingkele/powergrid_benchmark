"""Local experiment harness used by the MA-SQLGrid runner."""

from __future__ import annotations

import json
import math
import sys
import time


class ExperimentHarness:
    def __init__(self, time_budget: int = 120):
        self._start = time.time()
        self._time_budget = max(1, int(time_budget))
        self._metrics: dict[str, float] = {}
        self._partial_results: list[dict[str, object]] = []
        self._step_count = 0
        self._nan_count = 0

    @property
    def elapsed(self) -> float:
        return time.time() - self._start

    def should_stop(self) -> bool:
        return self.elapsed >= self._time_budget * 0.8

    def check_value(self, value: float, name: str = "metric") -> bool:
        if math.isnan(value) or math.isinf(value):
            self._nan_count += 1
            print(f"WARNING: {name} = {value} (non-finite, skipped)", file=sys.stderr)
            if self._nan_count >= 5:
                print("FAIL: Too many NaN/Inf values detected.", file=sys.stderr)
                self.finalize()
                sys.exit(1)
            return False
        return True

    def report_metric(self, name: str, value: float) -> None:
        if not isinstance(value, (int, float)):
            try:
                value = float(value)
            except (TypeError, ValueError):
                print(f"WARNING: Cannot convert {name}={value!r} to float", file=sys.stderr)
                return
        if not self.check_value(float(value), name):
            return
        self._metrics[name] = float(value)
        print(f"{name}: {float(value)}")

    def log_result(self, result_dict: dict[str, object]) -> None:
        self._partial_results.append(result_dict)

    def step(self) -> None:
        self._step_count += 1

    def finalize(self) -> None:
        output: dict[str, object] = {
            "metrics": self._metrics,
            "elapsed_sec": round(self.elapsed, 2),
            "time_budget_sec": self._time_budget,
            "steps_completed": self._step_count,
            "nan_count": self._nan_count,
        }
        if self._partial_results:
            output["results"] = self._partial_results
        try:
            with open("results.json", "w", encoding="utf-8") as handle:
                json.dump(output, handle, indent=2, default=str)
        except OSError as exc:
            print(f"WARNING: Could not write results.json: {exc}", file=sys.stderr)
