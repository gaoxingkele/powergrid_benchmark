#!/usr/bin/env python3
"""No-op setup for the MA-SQLGrid local experiment package.

The experiment uses the checked-in GridDB-Maintenance-v2 v0.1 SQLite dataset
and local evaluator. No downloads or package installation are required.
"""

from __future__ import annotations

from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    print(f"SETUP_OK: using local assets from {here}")


if __name__ == "__main__":
    main()
