"""Generate a non-destructive, portable paper ownership catalog (no source edits).

Only directory names with explicit paper identities are auto-classified. Shared
packages remain intact. Junction installation is separate and Windows-only.
"""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/migration/paper_organization_20260912'
IDS = dict(zip(range(1, 7), ['GRU-LSR','CSA-LoadNet','CARS-MODE','SHIELD-MOEA','TRACE-MOEA','BiLo-NSGA']))
PAPERS = [*IDS.values(), 'C2GES', 'MA-SQLGrid']
registry = {p: {'project': f'paper_projects/{p}', 'history': [], 'shared': [], 'worktrees': []} for p in PAPERS}
skipped = []
links = []

def owner(name):
    n = name.lower()
    if n == 'c2ges_supplement_incoming':
        return None  # Incoming bundle contains BOTH CMC papers.
    match = re.search(r'mintou[_-]p([1-6])(?:[_-]|$)', n)
    if match:
        return IDS[int(match[1])]
    if re.search(r'ma[-_]?sql[-_]?grid', n):
        return 'MA-SQLGrid'
    if 'c2ges' in n:
        return 'C2GES'
    for p in PAPERS:
        if p.lower() in n:
            return p
    return None

def add_link(paper, target, category):
    relative = target.relative_to(ROOT).as_posix()
    bucket = registry[paper][category]
    if relative in bucket:
        return
    bucket.append(relative)
    if target.is_dir():
        num = len(bucket)
        label = re.sub(r'[^a-zA-Z0-9_.-]', '_', target.name)[:85]
        links.append({'link': f'paper_projects/{paper}/90_History_Links/{num:03d}_{label}', 'target': relative})

def scan(path):
    if path.is_symlink() or path.is_junction():
        skipped.append(str(path.relative_to(ROOT)))
        return
    p = owner(path.name)
    if p:
        add_link(p, path, 'history')
        return
    if path.is_dir():
        if path.name in {'.git','__pycache__','.pytest_cache','.venv','node_modules'}:
            return
        for child in sorted(path.iterdir()):
            scan(child)

roots = [
 'paper_projects/2026_c2ges_engineeringletters','paper_projects/2026_ma_sqlgrid_cmc',
 'paper_projects/applied_sciences_dual_rebuild','paper_projects/c2ges_supplement_incoming',
 'paper_projects/cmc_delivery_2026-07-24','paper_projects/CMC/90_Workspace_History',
 'ara_artifacts','deliverables','deliveries','delivery_20260809',
 'delivery_20260809_compressed_final','delivery_20260809_corrected_full_assets',
 'reviews','upload','MA_SQLGrid','configs','scripts/mintou',
 'data/processed','data/interim','data/metadata','papers/mintou/submission_assets',
 'research_wiki/paper_ideas',
]
for name in roots:
    path = ROOT / name
    if path.exists():
        scan(path)

# Every mixed collection is explicitly shared, not silently assigned to one paper.
mintou_shared = ['papers/mintou/harness','papers/mintou/submission_assets','reviews',
 'deliverables','scripts/mintou','src/powergrid_benchmark','configs',
 'data/public_datasets','papers/planning']
cmc_shared = ['paper_projects/applied_sciences_dual_rebuild',
 'paper_projects/cmc_delivery_2026-07-24','paper_projects/c2ges_supplement_incoming',
 'paper_projects/CMC/90_Workspace_History','deliveries']
for p in PAPERS:
    registry[p]['shared'] = mintou_shared if p in IDS.values() else cmc_shared
worktrees = subprocess.check_output(['git','worktree','list','--porcelain'], cwd=ROOT, text=True)
for block in worktrees.strip().split('\n\n'):
    lines = block.splitlines()
    identity = owner(block)
    if identity:
        registry[identity]['worktrees'].append(lines)

for p in PAPERS:
    base = ROOT / registry[p]['project']
    if p in IDS.values():
        current = 'manuscript/journal_submission/paper.tex'
        pdf = 'manuscript/journal_submission/paper.pdf'
        entry = 'manuscript/MANUSCRIPT.md'
        code = 'ARA/src'
        data = 'ARA/evidence'
        warning = 'journal_submission 是现有构建入口，不因本次归类自动成为已签核投稿版本；以 checkpoints 与证据合同为准。'
    else:
        main = 'paper_information.tex' if p == 'MA-SQLGrid' else 'paper_applsci.tex'
        current = f'Workspace/01_Manuscript/LaTeX/{main}'
        pdf = ('Workspace/01_Manuscript/LaTeX/paper_information.pdf' if p == 'MA-SQLGrid' else
               'Workspace/01_Manuscript/PDF/C2GES_Applied_Sciences_2026-09-12_diagnostic_submission.pdf')
        entry = 'Workspace/00_Status_and_Index/CURRENT_BASELINE.md'
        code = 'Workspace/03_Reproducibility'
        data = code
        warning = '当前稿身份以 CURRENT_BASELINE 为准；历史 ZIP 内的旧稿不得覆盖当前稿。'
    registry[p].update(current_tex=current, pdf=pdf, status=entry)
    text = [f'# {p} 论文项目总入口', '', '归类日期：2026-09-12。目录名称是论文缩写，不改论文标题、作者或科学结论。', '',
      f'- [当前状态/正文说明]({entry})', f'- [现有 LaTeX 主稿]({current})', f'- [现有 PDF]({pdf})',
      f'- [代码与环境]({code})', f'- [数据与实验记录]({data})',
      '- [历史版本目录入口](90_History_Links/)', '', warning, '',
      '## 存储规则', '',
      '当前工作区及闽投 ARA 证据已实体归入本项目。其他历史目录通过永久联接归类，联接不是副本；修改入口文件即修改原文件。',
      '历史材料只读使用，不因创建入口改变其证据等级。共享包不拆包，公共数据与公共实现不复制成私有版本。',
      '旧路径联接必须保留。勿递归清理或打包联接目录；独立投稿 ZIP 应使用论文已有发布脚本。跨机器重建入口须先验证 catalog.json 的目标。', '',
      '## 本篇历史材料（明确归属）', '']
    for rel in registry[p]['history']:
        text.append(f'- [{rel}]({(ROOT / rel).as_posix()})')
    text += ['', '## 跨论文共享材料（保留原始结构）', '']
    for rel in registry[p]['shared']:
        text.append(f'- [{rel}]({(ROOT / rel).as_posix()})')
    text += ['', '## Git 历史工作树', '', '这些工作树保留原址和分支，不移动、不合并、不删除。']
    for lines in registry[p]['worktrees']:
        text += ['', '```text', *lines, '```']
    (base / 'PROJECT_INDEX.md').write_text('\n'.join(text)+'\n', encoding='utf-8')
    (base / '90_History_Links').mkdir(exist_ok=True)

result = {'date':'2026-09-12','root':str(ROOT),'papers':registry,
 'history_links':links,'scan_roots':roots,'skipped_reparse':skipped,
 'other_projects':{'IIA_benchmark':'Research benchmark and literature reproductions found; no additional authored standalone manuscript confirmed in inspected locations.'},
 'scope_limit':'Not a whole-disk search. Downloaded literature, third-party reproductions, templates and unconfirmed ideas are not authored papers.'}
(OUT / 'catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'papers':len(registry),'history_links':len(links),'classified_items':sum(len(x['history']) for x in registry.values()),'per_paper':{p:len(r['history']) for p,r in registry.items()}},indent=2))
