from pathlib import Path
import os, json, csv, hashlib, collections, zipfile, xml.etree.ElementTree as ET

ROOT = Path(r'D:/aicoding/powergrid_benchmark')
OUT = ROOT / 'deliverables/capabilities_20260920/internal'
SKIP = {'.git', '__pycache__', '.pytest_cache', 'node_modules'}

def walk(root):
    if not root.exists():
        return
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP and not Path(base, d).is_symlink() and not Path(base, d).is_junction()]
        for name in files:
            p = Path(base, name)
            if not p.is_symlink():
                yield p

def stats(root):
    paths = list(walk(root)) if root.is_dir() else ([root] if root.exists() else [])
    ext = collections.Counter(p.suffix.lower() or '(none)' for p in paths)
    return {'exists': root.exists(), 'files':len(paths), 'bytes':sum(p.stat().st_size for p in paths),
            'extensions':dict(ext), 'examples':[str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p) for p in paths[:4]]}

manifest = list(csv.DictReader((ROOT/'data/public_datasets/manifests/public_dataset_manifest.csv').open(encoding='utf-8-sig')))
datasets=[]
for row in manifest:
    p=Path(row['local_path'])
    if not p.is_absolute(): p=ROOT/p
    datasets.append({**row, 'physical_inventory':stats(p)})
tracking = ROOT/'data/public_datasets/grid_tracking/datasets'
tracking_stats = {p.name:stats(p) for p in tracking.iterdir() if p.is_dir() and not p.is_junction()}
literature={}
unique={}
for folder in (ROOT/'papers/literature').iterdir():
    if not folder.is_dir() or folder.is_junction(): continue
    pdfs=[p for p in walk(folder) if p.suffix.lower()=='.pdf']
    valid=0
    for p in pdfs:
        with p.open('rb') as f:
            if f.read(5)!=b'%PDF-': continue
            f.seek(0); sha=hashlib.file_digest(f,'sha256').hexdigest()
        valid+=1; unique.setdefault(sha,[]).append(str(p.relative_to(ROOT)))
    literature[folder.name]={'pdf_files':len(pdfs),'pdf_signature_valid':valid}
summary={'date':'2026-09-20','scope':'Filesystem inventory; no semantic or license completeness certification; skips directory links and .git; archive and unpacked bytes both counted.',
         'manifest_rows':len(manifest),'datasets':datasets,'tracking':tracking_stats,'literature':literature,
         'unique_pdf_sha256':len(unique),'pdf_duplicate_groups':sum(len(v)>1 for v in unique.values()),'pdf_hash_index':unique}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'local_inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'manifest_rows':len(manifest),'manifest_status':dict(collections.Counter(r['status'] for r in manifest)),
    'literature':literature,'unique_pdf_sha256':len(unique),
    'datasets':[{ 'id':r['dataset_id'],'status':r['status'],'files':r['physical_inventory']['files'],'GiB':round(r['physical_inventory']['bytes']/2**30,3)} for r in datasets],
    'tracking':{k:{'files':v['files'],'GiB':round(v['bytes']/2**30,3),'extensions':v['extensions']} for k,v in tracking_stats.items()}},ensure_ascii=False,indent=2))
