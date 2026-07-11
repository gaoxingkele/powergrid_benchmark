from pathlib import Path

from powergrid_benchmark.mintou_experiments import MINTOU_ROOT, paper_by_id, run_paper


if __name__ == "__main__":
    paper = paper_by_id("mintou_p1")
    run_paper(paper, MINTOU_ROOT / paper.directory)
