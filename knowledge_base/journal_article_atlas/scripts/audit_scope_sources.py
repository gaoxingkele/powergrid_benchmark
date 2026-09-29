"""Audit immutable sources for the full power/AI scope round (no semantic promotion)."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
import fitz
from finalize_calibration_round1 import corrected_labels

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'calibration/2026-09-13_power_ai_scope'
PREFLIGHT = Path('C:/Users/10175/.codex/skills/academic-research-suite/ars/scripts/pdf_read_preflight.py')

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sidecars = OUT / 'read_integrity'
    sidecars.mkdir(exist_ok=True)
    manifest = json.loads((ROOT/'outputs/corpus_manifest.json').read_text(encoding='utf8'))
    results = []
    for i, item in enumerate(manifest['articles'], 1):
        pdf = Path(item['source_path'])
        result = {'paper_id': item['paper_id'], 'source_sha256': item['source_sha256'],
                  'source_path': str(pdf), 'hash_match': False, 'status': 'pending'}
        try:
            actual = sha(pdf)
            result['actual_sha256'] = actual
            result['hash_match'] = actual == item['source_sha256']
            if not result['hash_match']:
                raise ValueError('source hash changed; refuse stale annotation')
            sidecar = sidecars/(item['paper_id']+'.json')
            subprocess.run(['py','-3.12',str(PREFLIGHT),str(pdf),'--output',str(sidecar)],
                           check=True, capture_output=True, timeout=45)
            check = json.loads(sidecar.read_text(encoding='utf8'))
            result['preflight_verdict'] = check['verdict']
            result['preflight_sidecar'] = str(sidecar.relative_to(OUT))
            with fitz.open(pdf) as doc:
                result['pages'] = len(doc)
                char_counts = [len(p.get_text().strip()) for p in doc]
                result['low_text_pages'] = [i+1 for i,c in enumerate(char_counts) if c < 80]
                result['page_counts_agree'] = len(doc) == check['reader_page_count']
            objects = corrected_labels(pdf)
            # Save only label and coordinates, not copied captions/full texts.
            result['objects'] = [{k:v for k,v in o.items() if k!='caption_candidate'} for o in objects]
            result['candidate_counts'] = {kind:len({o['label'] for o in objects if o['type']==kind})
                                           for kind in ('figure','table','equation')}
            result['sequence_gap_candidates'] = {}
            for kind in ('figure','table','equation'):
                labels = {int(o['label']) for o in objects if o['type']==kind and re.fullmatch(r'\d+',o['label'])}
                result['sequence_gap_candidates'][kind] = sorted(set(range(1,max(labels)+1))-labels) if labels else []
            result['status'] = 'source_integrity_pass' if check['verdict']=='PASS' and result['page_counts_agree'] else 'requires_source_review'
            result['object_status'] = 'automatic_candidate_NOT_visual_validation'
        except Exception as e:
            result['status'] = 'audit_failed'
            result['error'] = str(e)
        results.append(result)
        if i%20==0:
            print(f'{i}/{len(manifest["articles"])} sources audited', flush=True)
    payload = {'manifest_sha256': sha(ROOT/'outputs/corpus_manifest.json'),
               'script_sha256':sha(__file__), 'counts':dict(Counter(r['status'] for r in results)),
               'scope':'file integrity and automatic object candidates only', 'records':results}
    (OUT/'source_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(payload['counts']))

if __name__=='__main__':
    main()
