#!/usr/bin/env python3
"""Build every paper-facing P1 figure from the sealed v2 evidence.

The script fails closed on the execution-manifest outputs and the Stage-3
paper-table hashes before drawing anything.  It never reads the legacy v1
tables.  PNG is the exact raster consumed by the IEEE Access source; a PDF
counterpart is emitted for inspection and reuse.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RUN = PROJECT / "experiments" / "p1_ieee_access_upgrade_v2"
RESULTS = RUN / "results"
DERIVED = PROJECT / "manuscript" / "derived_tables"
MANIFEST_PATH = RUN / "run_manifest.json"
CONTRACT_PATH = RUN / "upgrade_contract.json"
PROVENANCE_PATH = RUN / "statistics_provenance.json"

WIDTH, HEIGHT = 2200, 1200
BG = "#F7F9FC"
INK = "#172033"
MUTED = "#596579"
GRID = "#D7DEE9"
BLUE = "#2367C9"
TEAL = "#00897B"
ORANGE = "#D97706"
RED = "#C43D3D"
GREEN = "#2E7D32"
PURPLE = "#7655B5"
WHITE = "#FFFFFF"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_lf_record(path: Path) -> tuple[int, str]:
    """Return length/hash after normalizing a Windows checkout to canonical LF."""
    payload = path.read_bytes().replace(b"\r\n", b"\n")
    return len(payload), hashlib.sha256(payload).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        Path(r"C:/Windows/Fonts/arialbd.ttf" if bold else r"C:/Windows/Fonts/arial.ttf"),
        Path(r"C:/Windows/Fonts/calibrib.ttf" if bold else r"C:/Windows/Fonts/calibri.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


F20 = find_font(20)
F24 = find_font(24)
F28 = find_font(28)
F28B = find_font(28, True)
F34 = find_font(34)
F34B = find_font(34, True)
F46B = find_font(46, True)


def validate_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    if manifest.get("run_namespace") != "p1_ieee_access_upgrade_v2":
        raise RuntimeError("unexpected execution namespace")
    if manifest.get("status") != "completed" or manifest.get("protocol_valid") is not True:
        raise RuntimeError("execution manifest is not completed and protocol-valid")
    for filename, record in manifest["outputs"].items():
        path = RESULTS / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.stat().st_size != int(record["bytes"]) or sha256(path) != record["sha256"]:
            raise RuntimeError(f"sealed execution output mismatch: {filename}")
    if provenance.get("run_namespace") != manifest["run_namespace"]:
        raise RuntimeError("statistics provenance namespace mismatch")
    for relative, record in provenance["paper_tables"].items():
        path = PROJECT / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        canonical_bytes, canonical_hash = canonical_lf_record(path)
        if canonical_bytes != int(record["bytes"]) or canonical_hash != record["sha256"]:
            raise RuntimeError(f"Stage-3 paper table mismatch: {relative}")
    return manifest, contract


def canvas(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 42), title, fill=INK, font=F46B)
    draw.text((72, 102), subtitle, fill=MUTED, font=F24)
    draw.line((70, 146, WIDTH - 70, 146), fill=GRID, width=3)
    return image, draw


def rounded(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], *, fill: str = WHITE, outline: str = GRID, radius: int = 20, width: int = 3) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, *, font: ImageFont.FreeTypeFont = F28, fill: str = INK) -> None:
    left, top, right, bottom = xy
    box = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=7)
    x = left + (right - left - (box[2] - box[0])) / 2
    y = top + (bottom - top - (box[3] - box[1])) / 2
    draw.multiline_text((x, y), text, font=font, fill=fill, align="center", spacing=7)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], *, fill: str = MUTED, width: int = 6) -> None:
    draw.line((start, end), fill=fill, width=width)
    x, y = end
    draw.polygon([(x, y), (x - 18, y - 10), (x - 18, y + 10)], fill=fill)


def save(image: Image.Image, stem: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    png = HERE / f"{stem}.png"
    pdf = HERE / f"{stem}.pdf"
    image.save(png, dpi=(220, 220), optimize=True)
    image.save(pdf, "PDF", resolution=220.0)
    for path in (png, pdf):
        records.append({"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size})
    return records


def draw_overview(contract: dict[str, Any]) -> Image.Image:
    image, draw = canvas(
        "Benchmark gate, analysis units, and onset support",
        "All counts and rules are frozen in p1_ieee_access_upgrade_v2; delivery targets are not independent replicates.",
    )
    temporal = contract["temporal_protocol"]["per_horizon"]
    panel = (70, 190, 2130, 650)
    rounded(draw, panel)
    draw.text((105, 220), "A  |  Horizon-offset temporal gate", fill=INK, font=F34B)
    colors = {"fit": BLUE, "selection": PURPLE, "calibration": ORANGE, "test": TEAL}
    x0, x1, y0, h = 120, 2080, 320, 92
    total = 8760
    boundaries = [("fit", 4380), ("selection", 5256), ("calibration", 6132), ("test", 8760)]
    previous = 0
    for name, end in boundaries:
        left = x0 + int((x1 - x0) * previous / total)
        right = x0 + int((x1 - x0) * end / total)
        draw.rectangle((left, y0, right, y0 + h), fill=colors[name])
        center_text(draw, (left, y0, right, y0 + h), name.title(), font=F24, fill=WHITE)
        draw.text((right - 35, y0 + h + 14), str(end), fill=MUTED, font=F20)
        previous = end
    draw.text((120, 474), "Target embargoes have length h at 4380, 5256, and 6132; each downstream query endpoint s=t-h has crossed its boundary.", fill=INK, font=F24)
    draw.text((120, 520), "Fit: normalization, model parameters, and retrieval bank  |  Selection: checkpoint/hyperparameters  |  Calibration: threshold  |  Test: score once", fill=MUTED, font=F20)

    rounded(draw, (70, 690, 1050, 1120))
    rounded(draw, (1090, 690, 2130, 1120))
    draw.text((105, 720), "B  |  Target counts", fill=INK, font=F34B)
    draw.text((1125, 720), "C  |  Positive onset support", fill=INK, font=F34B)
    headers = ["Lag", "Fit", "Select", "Calibrate", "Test"]
    for j, header in enumerate(headers):
        draw.text((115 + j * 180, 795), header, fill=MUTED, font=F24)
    for i, horizon in enumerate(("1", "24")):
        counts = temporal[horizon]["counts"]
        values = [f"{horizon} h", str(counts["fit"]), str(counts["selection"]), str(counts["calibration"]), str(counts["test"])]
        for j, value in enumerate(values):
            draw.text((115 + j * 180, 860 + i * 90), value, fill=INK, font=F28B if j == 0 else F28)
    support = [("1 h", "0", "0", "57"), ("24 h", "0", "0", "172")]
    headers2 = ["Lag", "Selection", "Calibration", "Test"]
    for j, header in enumerate(headers2):
        draw.text((1130 + j * 235, 795), header, fill=MUTED, font=F24)
    for i, values in enumerate(support):
        for j, value in enumerate(values):
            color = RED if j in (1, 2) else INK
            draw.text((1130 + j * 235, 860 + i * 90), value, fill=color, font=F28B if j == 0 else F28)
    draw.text((1128, 1045), "Onset-targeted selection is inapplicable; test metrics remain diagnostic.", fill=RED, font=F20)
    return image


def draw_architecture() -> Image.Image:
    image, draw = canvas(
        "GRU learned-space retrieval as the matched benchmark use case",
        "The target is method independent; raw and randomized spaces are attribution controls, and the target-hour transform is privileged.",
    )
    boxes = [
        ((80, 270, 390, 485), "48 x 7 window\nfit-only standardization", BLUE),
        ((485, 270, 805, 485), "GRU encoder\nhead-selected checkpoint", PURPLE),
        ((900, 190, 1250, 365), "Direct head\nalpha = 1", ORANGE),
        ((900, 430, 1250, 605), "Fit-bank kNN\nk = 8", TEAL),
        ((1350, 270, 1700, 485), "Selected / fixed blend\nalpha in {0, 0.5, 1}", BLUE),
        ((1800, 270, 2120, 485), "Held-out score\npaired by seed", GREEN),
    ]
    for xy, label, color in boxes:
        rounded(draw, xy, fill=WHITE, outline=color, width=5)
        center_text(draw, xy, label, font=F28B if "Held" in label else F28)
    arrow(draw, (390, 378), (485, 378))
    arrow(draw, (805, 345), (900, 278), fill=ORANGE)
    arrow(draw, (805, 410), (900, 515), fill=TEAL)
    arrow(draw, (1250, 278), (1350, 340), fill=ORANGE)
    arrow(draw, (1250, 515), (1350, 415), fill=TEAL)
    arrow(draw, (1700, 378), (1800, 378), fill=GREEN)

    rounded(draw, (80, 700, 2120, 1100))
    draw.text((115, 730), "Matched retrieval spaces and external references", fill=INK, font=F34B)
    controls = [
        ("Learned", "48-d forecasting-trained GRU embedding", TEAL),
        ("Raw", "336-d flattened standardized input", BLUE),
        ("Randomized", "48-d untrained GRU; same seed; zero updates", PURPLE),
        ("External", "Persistence, Seasonal-24h, Ridge", ORANGE),
    ]
    for i, (name, description, color) in enumerate(controls):
        left = 115 + i * 495
        rounded(draw, (left, 815, left + 455, 1018), outline=color, width=4)
        draw.text((left + 25, 845), name, fill=color, font=F28B)
        draw.multiline_text((left + 25, 900), description, fill=INK, font=F20, spacing=5)
    draw.text((115, 1050), "Target-hour direct transform: construction/visibility audit only; never rank eligible.", fill=RED, font=F20)
    return image


def effect_rows() -> list[dict[str, str]]:
    wanted = {
        "selected_learned_vs_gru_head": "Selected vs head",
        "learned_retrieval_vs_raw": "Learned vs raw",
        "learned_retrieval_vs_randomized": "Learned vs randomized",
    }
    result = []
    for row in rows(DERIVED / "v2_paired_seed_effects.csv"):
        if row["family_id"] == "primary_mae_mechanism_attribution" and row["contrast_id"] in wanted:
            result.append({**row, "label": wanted[row["contrast_id"]]})
    return sorted(result, key=lambda r: (int(r["horizon_hours"]), list(wanted).index(r["contrast_id"])))


def draw_effects() -> Image.Image:
    data = effect_rows()
    image, draw = canvas(
        "Primary cap: paired MAE effects across ten frozen seeds",
        "Points are treatment-minus-control means; whiskers are predeclared 95% seed-conditional t intervals. Negative favors treatment.",
    )
    panels = [(80, 215, 1070, 1090, 1), (1130, 215, 2120, 1090, 24)]
    xmin, xmax = -0.0075, 0.0020
    for left, top, right, bottom, horizon in panels:
        rounded(draw, (left, top, right, bottom))
        draw.text((left + 35, top + 25), f"{horizon} h retrospective lag", fill=INK, font=F34B)
        plot_left, plot_right = left + 330, right - 55
        plot_top, plot_bottom = top + 165, bottom - 100
        zero = plot_left + (0 - xmin) / (xmax - xmin) * (plot_right - plot_left)
        draw.line((zero, plot_top - 25, zero, plot_bottom + 20), fill=RED, width=4)
        for tick in (-0.006, -0.004, -0.002, 0.0):
            x = plot_left + (tick - xmin) / (xmax - xmin) * (plot_right - plot_left)
            draw.line((x, plot_top - 25, x, plot_bottom + 20), fill=GRID, width=2)
            draw.text((x - 45, plot_bottom + 35), f"{tick:+.3f}", fill=MUTED, font=F20)
        subset = [row for row in data if int(row["horizon_hours"]) == horizon]
        for i, row in enumerate(subset):
            y = plot_top + i * 205
            draw.multiline_text((left + 35, y - 25), row["label"], fill=INK, font=F24, spacing=4)
            mean = float(row["mean_treatment_minus_control"])
            low = float(row["seed_interval_low"])
            high = float(row["seed_interval_high"])
            xmean = plot_left + (mean - xmin) / (xmax - xmin) * (plot_right - plot_left)
            xlow = plot_left + (low - xmin) / (xmax - xmin) * (plot_right - plot_left)
            xhigh = plot_left + (high - xmin) / (xmax - xmin) * (plot_right - plot_left)
            color = GREEN if mean < 0 and row["holm_significant_005"] == "true" else RED if mean > 0 else ORANGE
            draw.line((xlow, y, xhigh, y), fill=color, width=8)
            draw.line((xlow, y - 14, xlow, y + 14), fill=color, width=5)
            draw.line((xhigh, y - 14, xhigh, y + 14), fill=color, width=5)
            draw.ellipse((xmean - 12, y - 12, xmean + 12, y + 12), fill=color)
            draw.text((left + 35, y + 42), f"mean {mean:+.6f}  |  Holm p={float(row['p_holm_within_family_horizon']):.6g}", fill=MUTED, font=F20)
        draw.text((left + 35, bottom - 50), "Seed-conditional only; not uncertainty over hours, years, or systems.", fill=MUTED, font=F20)
    return image


def draw_caps() -> Image.Image:
    data = rows(DERIVED / "v2_cross_cap_descriptive.csv")
    image, draw = canvas(
        "Selected learned retrieval minus Persistence across caps",
        "Same-sequence descriptive comparison. Persistence is deterministic and receives no seed-based p-value.",
    )
    panels = [(90, 230, 1070, 1080, "1"), (1130, 230, 2110, 1080, "24")]
    ymin, ymax = -0.0003, 0.0010
    for left, top, right, bottom, horizon in panels:
        rounded(draw, (left, top, right, bottom))
        draw.text((left + 35, top + 28), f"{horizon} h lag", fill=INK, font=F34B)
        plot_left, plot_right = left + 125, right - 70
        plot_top, plot_bottom = top + 150, bottom - 130
        zero = plot_bottom - (0 - ymin) / (ymax - ymin) * (plot_bottom - plot_top)
        draw.line((plot_left, zero, plot_right, zero), fill=INK, width=4)
        subset = sorted([r for r in data if r["horizon_hours"] == horizon], key=lambda r: float(r["cap"]))
        for i, row in enumerate(subset):
            x = plot_left + i * (plot_right - plot_left) / 2
            value = float(row["selected_minus_persistence_mae"])
            y = plot_bottom - (value - ymin) / (ymax - ymin) * (plot_bottom - plot_top)
            color = TEAL if value < 0 else ORANGE
            draw.line((x, zero, x, y), fill=color, width=60)
            draw.text((x - 38, plot_bottom + 35), f"c={float(row['cap']):.2f}", fill=INK, font=F24)
            draw.text((x - 78, y - 45 if value >= 0 else y + 18), f"{value:+.6f}", fill=color, font=F24)
        draw.text((left + 35, bottom - 55), "Below zero: selected learned retrieval lower  |  Above zero: Persistence lower", fill=MUTED, font=F20)
    return image


def main() -> None:
    manifest, contract = validate_sources()
    figures: Iterable[tuple[str, Image.Image]] = (
        ("fig_benchmark_overview", draw_overview(contract)),
        ("fig_architecture", draw_architecture()),
        ("fig_primary_effects", draw_effects()),
        ("fig_cap_profile", draw_caps()),
    )
    generated: list[dict[str, Any]] = []
    names: list[str] = []
    for stem, image in figures:
        names.append(stem)
        generated.extend(save(image, stem))
    artifact_manifest = {
        "schema": "p1_manuscript_figure_manifest",
        "schema_version": 2,
        "generator": "manuscript/figures/make_figures.py",
        "generator_sha256": sha256(Path(__file__)),
        "source_run_namespace": manifest["run_namespace"],
        "source_run_manifest": str(MANIFEST_PATH.relative_to(PROJECT)).replace("\\", "/"),
        "source_run_manifest_sha256": sha256(MANIFEST_PATH),
        "statistics_provenance": str(PROVENANCE_PATH.relative_to(PROJECT)).replace("\\", "/"),
        "statistics_provenance_sha256": sha256(PROVENANCE_PATH),
        "validated_execution_outputs": manifest["outputs"],
        "validated_paper_tables": json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))["paper_tables"],
        "paper_facing_stems": names,
        "generated_figures": generated,
        "scope": "All paper-facing figure values derive from the sealed p1_ieee_access_upgrade_v2 execution and Stage-3 paper tables; no legacy v1 values are plotted.",
    }
    (HERE / "artifact_manifest.json").write_text(json.dumps(artifact_manifest, indent=2) + "\n", encoding="utf-8")
    print(f"validated {len(manifest['outputs'])} sealed outputs; generated {len(names)} paper-facing figures")


if __name__ == "__main__":
    main()
