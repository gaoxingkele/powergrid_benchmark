#!/usr/bin/env python3
"""Render a PDF page (or all pages) to PNG for ARA evidence capture.

Usage:
  py -3 render_pdf_page.py <pdf> <page_1indexed> <out.png> [scale]
  py -3 render_pdf_page.py <pdf> --info                # print page count
  py -3 render_pdf_page.py <pdf> --all <out_dir> [scale]   # dump every page

Uses pypdfium2 (no external binaries needed).
"""
import sys, os
import pypdfium2 as pdfium


def _save(bitmap, out_png):
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    try:
        pil = bitmap.to_pil()
        pil.save(out_png)
        return pil.size
    except Exception:
        # No Pillow: use pypdfium2's numpy buffer -> write PNG via zlib (stdlib only)
        import numpy as np  # pypdfium2 dep may pull numpy; else fall through
        arr = bitmap.to_numpy()  # H x W x C (BGRA or RGB)
        _write_png(arr, out_png)
        return (arr.shape[1], arr.shape[0])


def _write_png(arr, out_png):
    import struct, zlib
    h, w = arr.shape[0], arr.shape[1]
    if arr.shape[2] == 4:  # BGRA -> RGB
        rgb = arr[:, :, [2, 1, 0]]
    else:
        rgb = arr[:, :, :3]
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rgb[y].tobytes())
    def chunk(typ, data):
        c = typ + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    png += chunk(b"IEND", b"")
    with open(out_png, "wb") as f:
        f.write(png)


def render(pdf_path, page_idx0, out_png, scale=2.0):
    doc = pdfium.PdfDocument(pdf_path)
    page = doc[page_idx0]
    bitmap = page.render(scale=scale)
    return _save(bitmap, out_png)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    pdf = sys.argv[1]
    if sys.argv[2] == "--info":
        doc = pdfium.PdfDocument(pdf)
        print(f"pages={len(doc)}")
        return
    if sys.argv[2] == "--all":
        out_dir = sys.argv[3]
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
        doc = pdfium.PdfDocument(pdf)
        os.makedirs(out_dir, exist_ok=True)
        for i in range(len(doc)):
            out = os.path.join(out_dir, f"page_{i+1:03d}.png")
            _save(doc[i].render(scale=scale), out)
        print(f"rendered {len(doc)} pages -> {out_dir}")
        return
    page1 = int(sys.argv[2])
    out = sys.argv[3]
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
    size = render(pdf, page1 - 1, out, scale)
    print(f"ok {out} {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
