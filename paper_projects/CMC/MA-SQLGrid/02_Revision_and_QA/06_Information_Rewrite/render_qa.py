"""Render every manuscript page; contact sheets are inspection aids, not proof."""
from pathlib import Path
import fitz
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / "01_Manuscript" / "LaTeX" / "paper_information.pdf"
OUT = ROOT / "qa_pages"
OUT.mkdir(exist_ok=True)
doc = fitz.open(SOURCE)
pages = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
    path = OUT / f"page_{i+1:02d}.png"
    pix.save(path)
    im = Image.open(path).convert("RGB")
    im = ImageOps.expand(im, border=(0, 26, 0, 0), fill="white")
    ImageDraw.Draw(im).text((8, 5), f"PAGE {i+1}", fill="black")
    pages.append(im)
for start in range(0, len(pages), 4):
    width, height = pages[0].size
    sheet = Image.new("RGB", (2*width, 2*height), "#cccccc")
    for j, im in enumerate(pages[start:start+4]):
        sheet.paste(im, ((j % 2)*width, (j//2)*height))
    sheet.save(OUT / f"sheet_{start//4+1:02d}.png")
print(f"Rendered {len(pages)} pages and {(len(pages)+3)//4} contact sheets to {OUT}")
