"""Compatibility entry point for the canonical P3 S4 artifact generator.

The single source of configuration and artifact truth is
``evidence/runs/p3_s4_results_narrative_20260813/manifest.json``.
"""

from pathlib import Path
import runpy


if __name__ == "__main__":
    for ancestor in Path(__file__).resolve().parents:
        generator = ancestor / "scripts" / "generate_p3_s4_artifacts.py"
        if generator.is_file():
            runpy.run_path(str(generator), run_name="__main__")
            break
    else:
        raise FileNotFoundError("canonical P3 S4 artifact generator not found")
