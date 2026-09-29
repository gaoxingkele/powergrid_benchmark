from __future__ import annotations

from powergrid_benchmark.mintou_real_project_review import P6_EXPERIMENTS, P6_METHODS, P6_ROOT, run_paper


if __name__ == "__main__":
    run_paper("p6", P6_ROOT, P6_METHODS, P6_EXPERIMENTS)
