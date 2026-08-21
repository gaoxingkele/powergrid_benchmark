#!/usr/bin/env python3
"""Render the two manuscript framework figures from auditable JSON configs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib as mpl


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
sys.path.insert(0, str(PROJECT / "shared"))

from framework_renderer import render_config  # noqa: E402


def main() -> None:
    mpl.rcParams["hatch.linewidth"] = 0.30
    manifests = {}
    for paper in ("C2GES", "MA_SQLGrid"):
        directory = HERE / paper
        config = directory / "framework_config.json"
        manifests[paper] = render_config(config, directory, Path(__file__).resolve())
    summary = {
        paper: {
            "config_sha256": manifest["config"]["sha256"],
            "outputs": manifest["outputs"],
        }
        for paper, manifest in manifests.items()
    }
    (HERE / "BUILD_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
