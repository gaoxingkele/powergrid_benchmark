"""Render a hash-bound PDF into a new output folder; no visual pass inferred."""
import argparse
import hashlib
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--round', type=int, required=True)
ap.add_argument('--pass-name', default='')
a = ap.parse_args()
pdf = ROOT.parents[1] / '01_Manuscript/LaTeX/paper_information.pdf'
out = ROOT / f'round{a.round}' / 'qa_pages'
if a.pass_name:
    import re
    assert re.fullmatch(r'[a-z0-9_-]+', a.pass_name)
    out = ROOT / f'round{a.round}' / a.pass_name / 'qa_pages'
out.mkdir(exist_ok=False)
doc = fitz.open(pdf)
previews = []
for i, p in enumerate(doc):
    path = out / f'page_{i+1:02d}.png'
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False).save(path)
    im = Image.open(path).convert('RGB')
    im.thumbnail((460,650))
    cell = Image.new('RGB',(480,680),'white')
    cell.paste(im, (10,25))
    ImageDraw.Draw(cell).text((10,5),f'PAGE {i+1}',fill='black')
    previews.append(cell)
for start in range(0,len(previews),6):
    sheet=Image.new('RGB',(1440,1360),'#cccccc')
    for j,im in enumerate(previews[start:start+6]):
        sheet.paste(im,((j%3)*480,(j//3)*680))
    sheet.save(out/f'sheet_{start//6+1:02d}.png')
(out/'render_manifest.json').write_text(json.dumps(dict(pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
    pages=len(doc),visual_review='pending'),indent=2),encoding='utf-8')
print(out)
