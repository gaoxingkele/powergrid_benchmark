"""Verify scoped manuscript invariants and retain a version-specific diff."""
import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def table_map(s):
    return {re.search(r"\\label\{([^}]+)\}", b)[1]: b
            for b in re.findall(r"\\begin\{table\}.*?\\end\{table\}", s, re.S)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', type=int, required=True)
    ap.add_argument('--pass-name', default='')
    args = ap.parse_args()
    folder = ROOT / f'round{args.round}'
    before = folder / 'paper_information.before.tex'
    if args.pass_name:
        assert re.fullmatch(r'[a-z0-9_-]+', args.pass_name)
        folder = folder / args.pass_name
        folder.mkdir(exist_ok=True)
    current = WORK / '01_Manuscript/LaTeX/paper_information.tex'
    old, new = before.read_text(encoding='utf-8'), current.read_text(encoding='utf-8')
    ot, nt = table_map(old), table_map(new)
    if args.round == 3:
        # The old main table survives verbatim at the data-row level in Appendix A.
        def rows(block):
            return [line.strip() for line in block.splitlines() if ' & ' in line and not line.startswith('Method &')]
        assert rows(ot['tab:offline']) == rows(nt['tab:historical-question-statistics'])
        assert all(nt[k] == v for k,v in ot.items() if k != 'tab:offline')
        original = rows(ot['tab:offline'])
        reduced = rows(nt['tab:offline'])
        assert len(original) == len(reduced) == 10
        for a,b in zip(original,reduced):
            fields = a.removesuffix('\\\\').split(' & ')
            assert b == ' & '.join(fields[:4] + [fields[5]]) + '\\\\'
        assert 'Holm' not in nt['tab:offline']
    else:
        assert ot == nt, 'This prose round must preserve every table'
    assert re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', old) == re.findall(
        r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', new)
    labels = re.findall(r'\\label\{([^}]+)\}', new)
    assert len(labels) == len(set(labels))
    assert set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', new)) <= set(labels)
    bib = ''.join((current.parent / name).read_text(encoding='utf-8') for name in
                  ['references_verified.bib', 'references_information.bib'])
    keys = set(re.findall(r'@\w+\s*\{\s*([^,]+),', bib))
    cited = {k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}', new) for k in group.split(',')}
    assert cited <= keys
    abstract = new.split(r'\abstract{')[1].split(r'\keyword{')[0].rstrip().removesuffix('}')
    log = current.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
    assert not re.search(r'Overfull|LaTeX Error|undefined references|Rerun to get', log)
    assert 'BIRD does not rerun the historical-pool selector' in new
    report = dict(round=args.round, before_sha256=sha(before), after_sha256=sha(current),
        pdf_sha256=sha(current.with_suffix('.pdf')), table_environments=len(nt),
        prior_table_rows_preserved=True,
        cited_keys=len(cited), abstract_whitespace_words=len(abstract.split()),
        missing_labels=[], missing_bibkeys=[], visual_qa='pending',
        scope='Tables, figure references, label/key completeness, build log, source diff; not citation truth or acceptance')
    (folder/'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    (folder/'revision.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),
        fromfile='before.tex',tofile='after.tex')),encoding='utf-8')
    snapshot = folder/'paper_information.after.tex'
    if snapshot.exists() and snapshot.read_bytes() != current.read_bytes():
        raise FileExistsError('Round snapshot differs; do not overwrite')
    snapshot.write_bytes(current.read_bytes())
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
