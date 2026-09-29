from pathlib import Path
import shutil, hashlib, json
from PIL import Image, ImageChops
base=Path(__file__).resolve().parent.parent
internal=base/'internal'
old=internal/'render'
new=internal/'render_final'
pages=list(new.glob('page-*.png'))
assert len(pages)==21
changed=[]
for f in pages:
    if ImageChops.difference(Image.open(f).convert('RGB'),Image.open(old/f.name).convert('RGB')).getbbox():changed.append(f.name)
assert set(changed)=={'page-1.png','page-16.png','page-20.png'}
pdf=new/'电力人工智能科研能力说明_20260920.pdf'
assert pdf.read_bytes().startswith(b'%PDF-')
shutil.copy2(pdf,base/pdf.name)
attachments={}
for ext in ['docx','pdf']:
    f=base/f'电力人工智能科研能力说明_20260920.{ext}'
    attachments[ext]={'name':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
qa={'date':'2026-09-20','pages':21,'visual_review':'passed','review_method':'All 21 first-pass page images inspected; final changes on pages 1,16,20 re-inspected. Remaining 18 images pixel-identical. No clipping, overlap or unexpected blank pages observed.','final_changed_pages':changed,'resource_catalog_rows':65,'research_directions':9,'journal_rows':13,'caveats':['JCR, not CAS quartiles; years explicit','Information is ESCI, not SCIE','Joint project statistics attributed to joint material; reassessment presentation not treated as award decision','Inventory is not exhaustive semantic validation of every archive','Related publication ownership not assumed from local folder labels'],'attachments':attachments}
(internal/'QA_RECORD.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
