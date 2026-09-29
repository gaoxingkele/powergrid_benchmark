"""Read-only access to the scope overlay, not calibrated journal standards."""
import argparse
import json
from pathlib import Path

def query(journal=None, decision='core_ai', keyword=None):
    path=Path(__file__).resolve().parents[1]/'calibration/2026-09-13_power_ai_scope/scope_records.json'
    records=json.loads(path.read_text(encoding='utf8'))
    records=[r for r in records if (not journal or r['manifest_venue']==journal)
             and (decision=='all' or r['decision']==decision)
             and (not keyword or keyword.casefold() in ' '.join(str(r.get(k,'')) for k in ['title','task','method_family','scope_notes']).casefold())]
    return {'status':'SCOPE_SCREENED_NOT_FULLY_CALIBRATED','n':len(records),
            'journal_average':None,'difficulty_profile':None,'records':records}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--journal')
    p.add_argument('--decision',default='core_ai',choices=['all','core_ai','computational_support','review_background','adjacent','out_of_scope','uncertain'])
    p.add_argument('--keyword')
    args=p.parse_args()
    print(json.dumps(query(**vars(args)),ensure_ascii=False,indent=2))
