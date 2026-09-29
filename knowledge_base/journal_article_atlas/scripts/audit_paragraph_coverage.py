"""Exhaustive extracted-line accounting with explicit reviewed exclusion ranges.

Completeness refers only to this hash-bound PDF text extraction. Raster content,
semantic paragraph boundaries and scholarly field completeness remain separate.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'deconstruction/v1/papers'
RULES = ROOT / 'deconstruction/v1/information_coverage_rules.json'


def audit(paper_id, config):
    source = (BASE / config['source_path']).resolve()
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != config['source_sha256']:
        raise ValueError('PDF changed: '+paper_id)
    with fitz.open(source) as doc:
        blocks = {p+1: page.get_text('blocks') for p, page in enumerate(doc)}
        universe = {(p,b,i): line for p, bs in blocks.items()
                    for b, block in enumerate(bs) if block[6] == 0
                    for i, line in enumerate(block[4].splitlines())}
        assigned, duplicates = {}, []

        def assign(key, category, owner):
            if key not in universe:
                raise ValueError('Nonexistent text line '+str(key))
            if key in assigned:
                duplicates.append({'locator': key, 'old': assigned[key], 'new': [category,owner]})
            else:
                assigned[key] = (category, owner)

        map_path = BASE / (paper_id+'.paragraph_map.json')
        if map_path.exists():
            mapping = json.loads(map_path.read_text(encoding='utf8'))
            if mapping['source_sha256'] != digest:
                raise ValueError('Map source mismatch')
            for n,row in enumerate(mapping['paragraphs'],1):
                for spec in row[3]:
                    p,b = spec[:2]
                    a,z = spec[2:] if len(spec)==4 else (0,len(blocks[p][b][4].splitlines()))
                    for i in range(a,z):
                        assign((p,b,i), row[4] if len(row)>4 else 'prose', f'P{n:03}')
        for p, start, end, category, owner in config['block_rules']:
            if end == -1:
                end = len(blocks[p])-1
            for b in range(start,end+1):
                if blocks[p][b][6] != 0:
                    continue
                for i in range(len(blocks[p][b][4].splitlines())):
                    assign((p,b,i),category,owner)
        ledger = []
        for key,line in universe.items():
            p,b,i = key
            category,owner = assigned.get(key,('unassigned',None))
            ledger.append({'page':p,'block':b,'line':i,'category':category,'owner':owner,
                           'characters':len(line),'text_sha256':hashlib.sha256(line.encode()).hexdigest(),
                           'block_bbox':[round(x,3) for x in blocks[p][b][:4]]})
        counts = dict(Counter(row['category'] for row in ledger))
        return {'paper_id':paper_id,'source_sha256':digest,'parser':fitz.VersionBind,
                'rules_sha256':hashlib.sha256(RULES.read_bytes()).hexdigest(),
                'map_sha256':hashlib.sha256(map_path.read_bytes()).hexdigest() if map_path.exists() else None,
                'scope':'Every splitlines item in each PyMuPDF type0 block, including blank lines; no source text exported.',
                'text_partition_complete':not duplicates and counts.get('unassigned',0)==0,
                'semantic_distillation_complete':False,'raster_or_vector_content_completeness':'requires separate visual inventory',
                'counts':counts,'total_lines':len(universe),'duplicates':duplicates,'ledger':ledger}


if __name__ == '__main__':
    rules=json.loads(RULES.read_text(encoding='utf8'))
    for paper_id,config in rules['papers'].items():
        result=audit(paper_id,config)
        target=BASE/(paper_id+'.coverage_audit.json')
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(json.dumps({k:result[k] for k in ('paper_id','text_partition_complete','total_lines','counts')},ensure_ascii=False))
