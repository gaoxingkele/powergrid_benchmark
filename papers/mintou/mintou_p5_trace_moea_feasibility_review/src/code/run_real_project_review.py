from __future__ import annotations

from powergrid_benchmark.mintou_real_project_review import P5_EXPERIMENTS, P5_METHODS, P5_ROOT, run_paper


if __name__ == "__main__":
    run_paper("p5", P5_ROOT, P5_METHODS, P5_EXPERIMENTS)
