"""Bounded round-one checks, not an acceptance gate."""
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
TEX = WORK / "01_Manuscript/LaTeX/paper_information.tex"
BEFORE = HERE / "paper_information.before.tex"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tables(s):
    return {re.search(r"\\label\{([^}]+)\}", b)[1]: b
            for b in re.findall(r"\\begin\{table\}.*?\\end\{table\}", s, re.S)}


old, new = BEFORE.read_text(encoding="utf-8"), TEX.read_text(encoding="utf-8")
ot, nt = tables(old), tables(new)
assert sha(BEFORE).upper() == "BCEE5E325D140DBF949D3012C12644E876B46F8F4A71C7EEB1B7B783735CF95B"
assert all(nt[k] == v for k, v in ot.items()), "Historical table changed"
assert set(nt) - set(ot) == {"tab:failure-partition"}
data = WORK / "03_Reproducibility/Data/selection_failure_decomposition/information_r1/selection_failure_decomposition.json"
d = json.loads(data.read_text(encoding="utf-8"))
categories = ["no_correct_candidate", "all_correct_candidates_gated_out",
              "correct_candidates_below_top_score", "correct_top_candidate_lost_by_tie_order",
              "selected_correct"]
expected = [[d['summaries'][s]['categories'].get(c, 0) for s in
             ['validation_only', 'complete_witness']] for c in categories]
printed = [[int(x) for x in pair] for pair in re.findall(r"& (\d+) & (\d+)\\\\", nt['tab:failure-partition'])]
assert printed == expected + [[180, 180]]
labels = re.findall(r"\\label\{([^}]+)\}", new)
assert len(labels) == len(set(labels))
assert set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", new)) <= set(labels)
log = TEX.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
assert not re.search(r"Overfull|LaTeX Error|undefined references|Rerun to get", log)
report = dict(scope="Source-table preservation, new table arithmetic, labels and build log only",
    before_sha256=sha(BEFORE), after_sha256=sha(TEX), pdf_sha256=sha(TEX.with_suffix('.pdf')),
    data_sha256=sha(data), historical_tables_preserved=len(ot), new_tables=1,
    scientific_acceptance_verified=False, visual_qa="pending", iteration="round1")
(HERE / 'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
(HERE / 'revision.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
    fromfile='paper_information.before.tex', tofile='paper_information.round1.tex')), encoding='utf-8')
print(json.dumps(report, indent=2))
