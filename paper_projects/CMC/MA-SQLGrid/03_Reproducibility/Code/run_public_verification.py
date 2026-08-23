#!/usr/bin/env python3
"""Convenience entry point for the MA-SQLGrid portable package verifier."""

from __future__ import annotations

import runpy
from pathlib import Path


VERIFIER = Path(__file__).resolve().parents[1] / "Package_Metadata" / "verify_package.py"
runpy.run_path(str(VERIFIER), run_name="__main__")
