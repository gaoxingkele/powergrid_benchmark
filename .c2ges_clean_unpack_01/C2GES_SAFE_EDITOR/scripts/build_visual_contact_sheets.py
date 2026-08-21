"""Build deterministic four-page contact sheets from rendered manuscript pages."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / "final_visual_qa"


def main() -> None:
    pages = sorted(QA.glob("page-*.png"))
    if len(pages) != 14:
        raise SystemExit(f"expected 14 rendered pages, found {len(pages)}")
    for sheet_index, start in enumerate(range(0, len(pages), 4), start=1):
        group = pages[start : start + 4]
        thumbs = []
        for page in group:
            image = Image.open(page).convert("RGB")
            image.thumbnail((650, 900))
            thumbs.append((page.name, image.copy()))
        canvas = Image.new("RGB", (1360, 1900), "white")
        draw = ImageDraw.Draw(canvas)
        for index, (name, image) in enumerate(thumbs):
            x = 20 + (index % 2) * 680
            y = 45 + (index // 2) * 930
            draw.text((x, y - 25), name, fill="black")
            canvas.paste(image, (x, y))
        canvas.save(QA / f"contact_{start + 1:02d}_{start + len(group):02d}.png", optimize=True)
    print(f"contact_sheets={(len(pages) + 3) // 4}")


if __name__ == "__main__":
    main()
