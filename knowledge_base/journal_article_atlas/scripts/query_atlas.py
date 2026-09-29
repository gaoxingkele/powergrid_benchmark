"""Small skill-facing read-only query; unverified measurements are opt-in."""
import argparse
import json
import sqlite3
from pathlib import Path

def query(journal, allow_candidates=False):
    path=Path(__file__).resolve().parents[1]/'outputs/atlas.sqlite'
    db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    db.row_factory=sqlite3.Row
    statuses=['verified','automatic_candidate'] if allow_candidates else ['verified']
    placeholders=','.join('?' for _ in statuses)
    rows=db.execute(f'''SELECT p.paper_id,p.journal,p.title,o.field_id,o.value_json,o.status,o.evidence_json
      FROM paper p JOIN observation o ON o.entity_id=p.paper_id
      WHERE p.journal=? AND o.status IN ({placeholders}) ORDER BY p.paper_id,o.field_id''',[journal,*statuses]).fetchall()
    total=db.execute('SELECT count(*) FROM paper WHERE journal=?',(journal,)).fetchone()[0]
    db.close()
    records=[]
    for row in rows:
        item=dict(row); item['value']=json.loads(item.pop('value_json')); item['evidence']=json.loads(item.pop('evidence_json')); records.append(item)
    return {'journal':journal,'paper_candidates':total,'observation_records':len(records),
      'mode':'candidate_discovery_only' if allow_candidates else 'verified_only',
      'calibration_status':'NOT_CALIBRATED','acceptance_threshold':None,'difficulty_profile':None,
      'message':'Candidate counts are not journal standards. Current corpus has not passed semantic calibration.',
      'observations':records}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--journal',required=True); p.add_argument('--allow-candidates',action='store_true')
    args=p.parse_args(); print(json.dumps(query(args.journal,args.allow_candidates),ensure_ascii=False,indent=2))
