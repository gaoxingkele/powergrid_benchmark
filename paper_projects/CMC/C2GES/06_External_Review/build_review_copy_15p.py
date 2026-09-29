"""Build a 15-sheet review copy of the C2GES submission for paperreview.ai.

paperreview.ai analyses only the first 15 pages of an upload.  The submission is
33 pages, so this script imposes the body (pages 1-30: title through conclusions)
two-up on A3 landscape sheets.  A3 landscape is exactly two A4 portrait pages
side by side, so the text is placed at 1:1 scale and stays fully legible and
text-extractable.  30 pages / 2 = 15 sheets, i.e. the whole scientific body falls
inside the analysed window.  Declarations and the bibliography (pages 31-33) are
omitted from this review copy only; the submission PDF is unchanged.
"""

from __future__ import annotations

from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
SUBMISSION = HERE.parent / "01_Manuscript" / "LaTeX" / "paper_information.pdf"
OUT = HERE / "C2GES_reviewcopy_15p_A3.pdf"
BODY_PAGES = 30


def main() -> None:
    src = fitz.open(SUBMISSION)
    if len(src) < BODY_PAGES:
        raise SystemExit(f"unexpected source length {len(src)}")
    a4 = src[0].rect
    sheet = fitz.paper_rect("a3-l")  # 1190.55 x 841.89 pt = 2 x A4 portrait
    out = fitz.open()
    for start in range(0, BODY_PAGES, 2):
        page = out.new_page(width=sheet.width, height=sheet.height)
        for column, index in enumerate((start, start + 1)):
            if index >= BODY_PAGES:
                continue
            rect = fitz.Rect(
                column * a4.width, 0.0, (column + 1) * a4.width, a4.height
            )
            page.show_pdf_page(rect, src, index)
    out.set_metadata(
        {
            "title": "C2GES compressed review copy (original pages 1-30, two per sheet)",
            "subject": "Review copy for paperreview.ai; bibliography omitted; submission is 33 pages",
            "author": "Bijing Liu; Yong Yang",
        }
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, garbage=4, deflate=True)
    out.close()

    check = fitz.open(OUT)
    text = "\n".join(page.get_text() for page in check)
    print(f"written {OUT.name}: {len(check)} pages, {OUT.stat().st_size/1e6:.2f} MB")
    print("page size pt:", round(check[0].rect.width, 1), "x", round(check[0].rect.height, 1))
    for probe in ("Causal-Chain Graph Extractive Summarization", "the only corrected internal win",
                  "External Prospective Evaluation", "0.022940", "Adjacent-Corpus Construct Audit"):
        print(f"  text probe {probe[:44]!r}: {'OK' if probe in text else 'MISSING'}")
    check.close()


if __name__ == "__main__":
    main()
