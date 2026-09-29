"""Check migration integrity without walking junctions or rerunning experiments."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'docs/migration/paper_organization_20260912'
before = json.loads((AUDIT/'before.json').read_text(encoding='utf-8-sig'))
catalog = json.loads((AUDIT/'catalog.json').read_text(encoding='utf-8'))
failures = []
count = 0
for move in before:
    source, target = Path(move['source']), Path(move['target'])
    if not source.is_junction() or source.resolve() != target.resolve():
        failures.append(f'Compatibility link: {source}')
    for record in move['files']:
        p = target / record['path']
        if not p.is_file():
            failures.append(f'Missing: {p}')
        elif hashlib.file_digest(p.open('rb'), 'sha256').hexdigest().upper() != record['sha256']:
            failures.append(f'Changed: {p}')
        count += 1
for entry in catalog['history_links']:
    p, target = ROOT/entry['link'], ROOT/entry['target']
    if not p.is_junction() or p.resolve() != target.resolve():
        failures.append(f'History link: {p}')
entry_count = 0
for paper, row in catalog['papers'].items():
    project = ROOT / row['project']
    for key in ['current_tex', 'pdf', 'status']:
        p = project / row[key]
        entry_count += 1
        if not p.is_file():
            failures.append(f'Paper entry: {p}')
    for rel in row['history'] + row['shared']:
        if not (ROOT/rel).exists():
            failures.append(f'Catalog entry: {rel}')
worktrees = subprocess.check_output(['git','worktree','list','--porcelain'],cwd=ROOT,text=True)
wt = [line[9:] for line in worktrees.splitlines() if line.startswith('worktree ')]
for p in wt:
    if not (Path(p)/'.git').exists():
        failures.append(f'Worktree: {p}')
result = {'file_hashes_checked': count, 'compatibility_junctions':len(before),
 'history_junctions':len(catalog['history_links']), 'manuscript_entry_files':entry_count,
 'worktree_paths':len(wt),'failures':failures,
 'limitations':'No experimental reruns; original files checked, generated new navigation files excluded from pre-move hashes.'}
(AUDIT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(failures))
