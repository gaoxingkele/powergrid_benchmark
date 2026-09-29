"""Fetch one pre-registered open source using the workspace aria2 helper."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
import fitz
sys.path.insert(0, 'D:/aicoding/mylib')
from download_tools import download

ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--doi',required=True)
    args=parser.parse_args()
    sources=json.loads((ROOT/'deconstruction/v1/expansion_sources.json').read_text(encoding='utf8'))['records']
    matches=[r for r in sources if r.get('doi')==args.doi]
    if len(matches)!=1 or matches[0].get('full_text_status')!='open_pdf':
        raise ValueError('A unique registered open PDF is required')
    source=matches[0]
    dest=ROOT/'deconstruction/v1/sources'/(args.doi.replace('/','_')+'.pdf')
    if dest.exists():
        raise FileExistsError('Existing source preserved; audit it instead of downloading again')
    code=download(source['pdf_url'],dest,fallback=False,max_tries=2,connect_timeout=15,
                  aria2_extra_args=['--timeout=25','--allow-overwrite=false'])
    record={'doi':args.doi,'url':source['pdf_url'],'download_exit':code,'path':str(dest),'status':'failed'}
    if code==0:
        with fitz.open(dest) as doc:
            record.update(pages=len(doc),status='downloaded_pending_identity_review')
        record['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    log=dest.with_suffix('.download.json')
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(record,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
