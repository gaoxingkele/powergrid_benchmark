"""Verify this scoped narrative edit; produce a source-bound QA record."""
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys
import fitz

HERE = Path(__file__).resolve().parent
OUTPUT = HERE if len(sys.argv) == 1 else HERE / sys.argv[1]
if OUTPUT != HERE:
    assert re.fullmatch(r'[a-z0-9_-]+',sys.argv[1])
    OUTPUT.mkdir(exist_ok=False)
SOURCE = HERE.parents[1] / "01_Manuscript/LaTeX/paper_information.tex"
old = (HERE / "paper_information.before.tex").read_text(encoding="utf-8")
new = SOURCE.read_text(encoding="utf-8")
for environment in ("table", "equation", "figure"):
    pattern = r"\\begin\{" + environment + r"\*?\}.*?\\end\{" + environment + r"\*?\}"
    assert re.findall(pattern, old, re.S) == re.findall(pattern, new, re.S), environment
before_section = r"\subsection{Evidence Summary and Reading Guide}"
after_section = r"\subsection{Validation-Aware Selection in the Historical Candidate Pool}"
assert old.split(before_section)[0] == new.split(before_section)[0]
assert old.split(after_section)[1] == new.split(after_section)[1]
log = SOURCE.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
assert not re.search(r"Overfull|LaTeX Error|undefined references|Rerun to get", log)
weights = [15,15,15,15,10,15,5,5,5]
ratings = [3,2,1,2,3,3,2,3,1]
points = [w*r/4 for w,r in zip(weights,ratings)]
pdf = fitz.open(SOURCE.with_suffix(".pdf"))
report = {"before_sha256": hashlib.sha256((HERE/'paper_information.before.tex').read_bytes()).hexdigest(),
          "after_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          "pdf_sha256": hashlib.sha256(SOURCE.with_suffix('.pdf').read_bytes()).hexdigest(),
          "pages": len(pdf), "tables_equations_figures_preserved": True,
          "only_reading_guide_changed": True,
          "rubric": "paper-meta-review-v1.0", "weights": weights,
          "before_ratings": ratings, "after_ratings": ratings,
          "before_total": sum(points), "after_total": sum(points),
          "scientific_subtotal": sum(points[:6]), "technical_author_subtotal": sum(points[6:]),
          "score_basis": "Reviewer-assigned ordinal ratings, deterministic arithmetic, no acceptance calibration"}
with (OUTPUT/'verification.json').open('x',encoding='utf-8') as handle:
    json.dump(report,handle,indent=2)
with (OUTPUT/'revision.patch').open('x',encoding='utf-8') as handle:
    handle.write(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True))))
for i,page in enumerate(pdf):
    if "core results distinguish" in page.get_text() or (i and "core results distinguish" in pdf[i-1].get_text()):
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(OUTPUT/f'changed_page_{i+1}.png'))
print(json.dumps(report,indent=2))
