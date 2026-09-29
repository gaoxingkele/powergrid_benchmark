"""Prepare source-anchored same-task pilot cohorts; outputs are not human calibration."""
from pathlib import Path
import json, re, subprocess, hashlib
from collections import Counter
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'calibration/2026-09-13_round1'
SELECTION={
 'Applied Sciences': ['p_c8763eed4f1a695a','p_8685474523df0850','p_ba8e73559896f121'],
 'Electronics':['p_10518b844b194e90','p_e90a29790e1667db','p_9711769edf1bafa5'],
 'IEEE Access':['p_5908282d0c137859','p_5fd7d69670cfc8e8','p_9054a62c1e9b25b4'],
 'Energies':['p_e2822d4e02526031','p_d2e16e5d3f9b1b3f','p_320f77a542175910','p_e5502fa6e3ee1a5f'],
 'Sensors':['p_a1adf441aa349153']}
PREFLIGHT=Path('C:/Users/10175/.codex/skills/academic-research-suite/ars/scripts/pdf_read_preflight.py')

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 rows=json.loads((ROOT/'outputs/articles.json').read_text(encoding='utf-8'))
 records=[]
 for r in rows:
  if r['paper_id'] not in SELECTION.get(r['venue'],[]): continue
  pid=r['paper_id']; pdf=Path(r['source_path'])
  with pdf.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==r['source_sha256']
  sidecar=OUT/(pid+'_read_integrity.json')
  subprocess.run(['py','-3.12',str(PREFLIGHT),str(pdf),'--output',str(sidecar)],check=True,capture_output=True)
  with fitz.open(pdf) as doc:
   pages=[p.get_text(sort=True) for p in doc]
  texts=[]
  for i,t in enumerate(pages,1): texts.append(f'\n=== PHYSICAL PAGE {i} ===\n{t}')
  (OUT/(pid+'_text.txt')).write_text(''.join(texts),encoding='utf-8')
  poppler=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,check=True).stdout.decode('utf-8',errors='replace')
  captions=[]; eq=[]; headings=[]
  for pn,page in enumerate(poppler.split('\f'),1):
   lines=page.splitlines()
   for i,line in enumerate(lines):
    s=line.strip()
    # IEEE TABLE label may be uppercase Roman and caption may follow on another line.
    cap=re.match(r'^(Figure|Fig\.|TABLE|Table)\s+(\d+|[IVX]+)(?:[.:]|\s|$)',s)
    if cap:
     captions.append({'kind':'table' if cap[1].lower()=='table' else 'figure','label':cap[2], 'page':pn,'text':' '.join(x.strip() for x in lines[i:i+3])[:300]})
    # Right-aligned labels after an equation, not only label-only lines.
    match=re.search(r'\s{3,}\((\d+[a-z]?)\)\s*$',line)
    if match:
     eq.append({'label':match[1],'page':pn,'context':s[:160]})
    if re.match(r'^(?:\d+(?:\.\d+)*\.?|[IVX]+\.)\s+[A-Z]',s) and len(s)<115:
     headings.append({'page':pn,'text':s})
  unique={k:sorted(set(c['label'] for c in captions if c['kind']==k)) for k in ['figure','table']}
  metrics={'figure_label_candidates':len(unique['figure']),'table_label_candidates':len(unique['table']),
    'numbered_equation_label_candidates':len(set(x['label'] for x in eq))}
  task='distribution_planning' if pid in SELECTION['Energies'][1:] else 'load_forecasting'
  rec={'paper_id':pid,'journal':r['venue'],'title':r['title'],'doi':r['doi'],'source_sha256':r['source_sha256'],
    'source_path':str(pdf),'cohort':f"{r['venue']}|{task}|empirical_method",'task':task,
    'scope_status':'selected_for_source_review','read_integrity':json.loads(sidecar.read_text(encoding='utf8'))['verdict'],
    'v0_metrics':r['metrics'],'v1_metrics':metrics,'captions':captions,'equation_labels':eq,'headings':headings,
    'counts_status':'automatic_candidate_not_gold','semantic_review_status':'pending'}
  records.append(rec)
 (OUT/'pilot_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps([{'id':r['paper_id'],'journal':r['journal'],'task':r['task'],'preflight':r['read_integrity'],'v0':{k:r['v0_metrics'][k] for k in r['v1_metrics']},'v1':r['v1_metrics']} for r in records],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
