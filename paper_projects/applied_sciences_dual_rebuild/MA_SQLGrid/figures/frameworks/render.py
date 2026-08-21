#!/usr/bin/env python3
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SHARED = HERE.parents[2] / "shared"
sys.path.insert(0, str(SHARED))
from framework_renderer import render_config

if __name__ == "__main__":
    manifest = render_config(HERE / "framework_config.json", HERE, Path(__file__).resolve())
    print(f"rendered={len(manifest['outputs'])} files")
