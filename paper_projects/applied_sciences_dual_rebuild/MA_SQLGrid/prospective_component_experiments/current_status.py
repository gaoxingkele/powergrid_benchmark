#!/usr/bin/env python3
"""Report whether the immutable freeze has any adjacent formal outputs."""

from __future__ import annotations

import json
from pathlib import Path

import verify_freeze


HERE = Path(__file__).resolve().parent


def main() -> int:
    verify_freeze.main()
    run_files = sorted(str(path.relative_to(HERE)).replace("\\", "/") for path in (HERE / "runs").glob("**/*") if path.is_file()) if (HERE / "runs").exists() else []
    analysis_files = sorted(str(path.relative_to(HERE)).replace("\\", "/") for path in (HERE / "analysis").glob("**/*") if path.is_file()) if (HERE / "analysis").exists() else []
    status = "FROZEN_NOT_RUN" if not run_files and not analysis_files else "FROZEN_WITH_FORMAL_OUTPUTS"
    print(json.dumps({"status": status, "formal_run_file_count": len(run_files),
                      "formal_analysis_file_count": len(analysis_files)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
