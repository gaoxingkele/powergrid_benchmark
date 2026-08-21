from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parent
STEMS = [
    "ma_r1_f01_executed_pipeline",
    "ma_r1_f02_factorial_design",
    "ma_r1_f03_external_evidence_gate",
]


def test_exports_complete():
    for stem in STEMS:
        for suffix in (".svg", ".pdf", ".png"):
            path = ROOT / "figures" / f"{stem}{suffix}"
            assert path.is_file() and path.stat().st_size > 5000


def test_png_resolution():
    for stem in STEMS:
        data = (ROOT / "figures" / f"{stem}.png").read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert min(width, height) >= 1100
        offset, ppm = 8, None
        while offset + 12 <= len(data):
            length = struct.unpack(">I", data[offset:offset+4])[0]
            kind = data[offset+4:offset+8]
            payload = data[offset+8:offset+8+length]
            if kind == b"pHYs":
                xppm, yppm, unit = struct.unpack(">IIB", payload)
                ppm = (xppm, yppm, unit)
                break
            offset += 12 + length
        assert ppm and ppm[2] == 1
        assert min(ppm[:2]) / 39.3701 >= 449


def test_svg_text_and_workflow_boundary():
    joined = "\n".join((ROOT / "figures" / f"{stem}.svg").read_text(encoding="utf-8") for stem in STEMS)
    assert len(re.findall(r"<text", joined)) >= 30
    assert "models × repetitions" not in joined.lower()
    assert "repair pass" not in joined.lower()
    assert "no repair loop" in joined.lower()


def test_document_assets_present():
    for name in (
        "README.md", "METHOD_AND_PROMPT_ASSETS.md", "GRIDDB_DATA_CARD.md",
        "DKASQL_COMPARATOR.md", "ROUND1_BLOCKERS_AND_EXPERIMENT_SPECS.md",
        "FACT_PROVENANCE.md", "VISUAL_QA.md",
    ):
        assert (ROOT / name).is_file()
    assert (ROOT / "qa" / "page_scale_preview.pdf").is_file()
