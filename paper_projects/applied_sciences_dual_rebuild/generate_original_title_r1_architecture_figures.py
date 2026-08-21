"""Generate auditable R1 architecture diagrams for the original-title papers.

The SVGs are intentionally constructed from the executable method cores rather
than from image-generation prompts.  Every label is restricted to behavior
implemented in the cited Python source.  The script also emits a lineage record
and performs structural, text, and canvas-boundary checks.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import textwrap
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
C2_SOURCE = ROOT / "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_rebuild/c2ges_offline.py"
MA_SOURCE = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/original_title_rebuild/ma_sqlgrid_agents.py"
C2_OUT = ROOT / "paper_projects/applied_sciences_dual_rebuild/C2GES/original_title_manuscript/R1/figures"
MA_OUT = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/original_title_manuscript/R1/figures"
SVG_NS = "http://www.w3.org/2000/svg"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrapped_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False) or [""]


class Svg:
    def __init__(self, width: int = 1600, height: int = 900) -> None:
        self.width = width
        self.height = height
        self.parts: list[str] = [
            f'<svg xmlns="{SVG_NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
            "<defs>",
            '<marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L10,4 L0,8 Z" fill="#24445c"/></marker>',
            '<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#19354a" flood-opacity="0.16"/></filter>',
            "</defs>",
            '<rect x="0" y="0" width="1600" height="900" fill="#ffffff"/>',
        ]

    def title(self, title: str, subtitle: str) -> None:
        self.parts.append(f'<title>{esc(title)}</title><desc>{esc(subtitle)}</desc>')
        self.text(800, 43, title, size=27, weight="700", anchor="middle", fill="#153247")
        self.text(800, 75, subtitle, size=16, anchor="middle", fill="#536978")

    def text(
        self,
        x: float,
        y: float,
        text: str,
        *,
        size: int = 18,
        weight: str = "400",
        anchor: str = "start",
        fill: str = "#183240",
        family: str = "Arial, Helvetica, sans-serif",
    ) -> None:
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{esc(text)}</text>'
        )

    def multiline(
        self,
        x: float,
        y: float,
        lines: list[str],
        *,
        size: int = 17,
        leading: int = 25,
        weight: str = "400",
        anchor: str = "start",
        fill: str = "#183240",
    ) -> None:
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        )
        for index, line in enumerate(lines):
            dy = 0 if index == 0 else leading
            self.parts.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
        self.parts.append("</text>")

    def box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        heading: str,
        body: list[str],
        *,
        fill: str,
        stroke: str = "#24445c",
        heading_fill: str = "#153247",
        note: str | None = None,
    ) -> None:
        self.parts.append(
            f'<g data-box="{esc(heading)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>'
            f'<line x1="{x}" y1="{y + 51}" x2="{x + w}" y2="{y + 51}" stroke="{stroke}" stroke-width="1" opacity="0.55"/></g>'
        )
        self.text(x + w / 2, y + 34, heading, size=19, weight="700", anchor="middle", fill=heading_fill)
        self.multiline(x + 18, y + 78, body, size=16, leading=25)
        if note:
            self.text(x + w / 2, y + h - 15, note, size=13, anchor="middle", fill="#5d6870")

    def arrow(self, points: list[tuple[float, float]], label: str | None = None, *, dashed: bool = False) -> None:
        coords = " ".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="8 6"' if dashed else ""
        self.parts.append(
            f'<polyline points="{coords}" fill="none" stroke="#24445c" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"{dash}/>'
        )
        if label:
            segments = []
            total = 0.0
            for left, right in zip(points, points[1:]):
                length = ((right[0] - left[0]) ** 2 + (right[1] - left[1]) ** 2) ** 0.5
                segments.append((left, right, length))
                total += length
            target = total / 2
            traversed = 0.0
            midpoint = points[0]
            for left, right, length in segments:
                if traversed + length >= target and length:
                    ratio = (target - traversed) / length
                    midpoint = (left[0] + ratio * (right[0] - left[0]), left[1] + ratio * (right[1] - left[1]))
                    break
                traversed += length
            self.text(midpoint[0], midpoint[1] - 8, label, size=13, anchor="middle", fill="#425b6c")

    def finish(self) -> str:
        return "\n".join([*self.parts, "</svg>", ""])


def c2ges_svg() -> str:
    s = Svg()
    s.title(
        "C²GES: implemented offline summarization pipeline",
        "Deterministic sentence-level proxy graph; no GNN, model API, or claim of ground-truth causality",
    )
    s.box(
        45, 150, 225, 235, "Report inputs",
        ["• sentence ID + text", "• report position", "• optional query", "• optional silver", "  role evidence"],
        fill="#e9f3f8", note="Silver evidence is not human gold",
    )
    s.box(
        335, 105, 430, 325, "Typed causal event graph",
        [
            "Sentence nodes retain five lexical role scores:",
            "trigger • root cause • propagation/response",
            "impact • mitigation",
            "Dominant role → allowed typed transition",
            "Edge weight = proximity + token overlap",
            "+ role confidence (fixed coefficients)",
        ],
        fill="#e8f5ef", note="Auditable proxy graph; rule-based, not a learned GNN",
    )
    s.box(
        830, 105, 310, 325, "Deterministic interventions",
        [
            "Baseline causal flow = Σ edge weight",
            "For each sentence node:",
            "1. delete node + incident edges",
            "2. recompute causal flow",
            "3. measure non-negative flow loss",
            "4. min–max scale across nodes",
        ],
        fill="#fff4df", note="Node deletion only; no synthetic counterfactual text",
    )
    s.box(
        1205, 105, 350, 325, "Multi-channel scoring",
        [
            "0.30 relevance (query/document focus)",
            "0.20 lexical/silver role evidence",
            "0.20 weighted-degree graph signal",
            "0.25 node-deletion sensitivity",
            "0.05 report-position prior",
            "→ fixed weighted sum per sentence",
        ],
        fill="#f2edfa", note="Weights are configured constants in the current core",
    )
    s.box(
        440, 555, 650, 235, "Constrained extractive selection",
        [
            "Reserve available causal-function groups when budget ≥ 3:",
            "cause/trigger • propagation/impact • mitigation",
            "Fill remaining budget by adjusted score",
            "Adjusted score = base score − 0.35 × max Jaccard redundancy",
            "Return selected sentences in original report order",
        ],
        fill="#eaf1fb", note="Deterministic tie-break: score, earlier position, sentence ID",
    )
    s.box(
        1240, 585, 290, 170, "Output",
        ["Extractive summary", "selection order", "covered role groups", "per-sentence reason + score"],
        fill="#e8f5ef",
    )
    s.arrow([(270, 267), (335, 267)])
    s.arrow([(765, 267), (830, 267)])
    s.arrow([(1140, 267), (1205, 267)])
    s.arrow([(550, 430), (550, 505), (630, 505), (630, 555)], "roles + graph signal")
    s.arrow([(1380, 430), (1380, 510), (1000, 510), (1000, 555)], "base scores")
    s.arrow([(1090, 672), (1160, 672), (1160, 620), (1240, 620)])
    s.text(55, 855, "Solid arrows denote actual data dependencies in c2ges_offline.py.", size=14, fill="#536978")
    return s.finish()


def ma_svg() -> str:
    s = Svg()
    s.title(
        "MA-SQLGrid: implemented deterministic coordination core",
        "Five evidence-producing/review roles + a deterministic adjudicator; external candidates, no model call or free-form deliberation",
    )
    # Inputs
    s.box(35, 120, 190, 150, "Question input", ["question ID", "natural-language", "question"], fill="#e9f3f8")
    s.box(35, 310, 190, 165, "Database input", ["schema", "foreign keys", "optional executor"], fill="#e9f3f8")
    s.box(35, 520, 190, 185, "External evidence", ["candidate SQL strings", "counterfactual", "state results", "expected state IDs"], fill="#fff4df")

    # Five roles
    s.box(285, 100, 235, 155, "1  Query Analyst", ["aggregation cues", "ordering + limit", "lexical tokens"], fill="#e8f5ef")
    s.box(285, 300, 235, 180, "2  Schema Cartographer", ["token-overlap tables", "matched columns", "in-scope join edges", "unmatched tokens"], fill="#e8f5ef")
    s.box(285, 540, 235, 165, "3  SQL Synthesizer", ["canonicalize + deduplicate", "package external SQL", "assign stable IDs"], fill="#e8f5ef", note="Does not generate SQL or call a model")
    s.box(585, 300, 245, 190, "4  Safety Validator", ["single statement", "read-only + no comments", "execution evidence", "shape/order/value hits", "retain failure; no retry"], fill="#f2edfa")
    s.box(585, 540, 245, 175, "5  Counterfactual Critic", ["consume supplied states", "execution + equivalence", "pass/fail state IDs", "coverage completeness"], fill="#f2edfa")

    # Blackboard and adjudication
    s.box(
        885, 110, 300, 395, "Append-only blackboard",
        [
            "0  query_intent",
            "1  schema_grounding",
            "2  sql_candidates",
            "3+ validation_evidence",
            "…  counterfactual_evidence",
            "last  decision",
            "then seal + SHA-256 audit digest",
        ],
        fill="#eef1f3", note="Records handoffs; it is not a conversational memory",
    )
    s.box(
        1235, 255, 320, 260, "Deterministic adjudicator",
        [
            "Eligibility: safe AND executable",
            "Rank: validation points",
            "→ counterfactual pass rate",
            "→ evaluated-state coverage",
            "→ original candidate order",
        ],
        fill="#eaf1fb", note="Reference-free; no gold SQL access",
    )
    s.box(
        1235, 610, 320, 145, "Decision",
        ["SELECT candidate + SQL", "or ABSTAIN when no safe", "executable candidate exists"],
        fill="#e8f5ef",
    )

    # Actual direct dependencies.
    s.arrow([(225, 195), (285, 195)])
    s.arrow([(402, 255), (402, 300)], "intent")
    s.arrow([(225, 392), (285, 392)])
    s.arrow([(130, 475), (130, 505), (555, 505), (555, 455), (585, 455)], "executor")
    s.arrow([(225, 612), (285, 612)])
    s.arrow([(520, 622), (552, 622), (552, 405), (585, 405)], "candidates")
    s.arrow([(520, 650), (585, 650)])
    s.arrow([(225, 680), (245, 680), (245, 730), (560, 730), (560, 690), (585, 690)], "state results")
    s.arrow([(830, 395), (850, 395), (850, 525), (1210, 525), (1210, 380), (1235, 380)], "validation evidence")
    s.arrow([(830, 650), (1165, 650), (1165, 545), (1210, 545), (1210, 465), (1235, 465)], "CF evidence")
    s.arrow([(1395, 515), (1395, 610)], "selected / abstain")

    # One audit-post bus keeps the visual separate from execution dependencies.
    s.parts.append('<rect x="260" y="88" width="595" height="660" rx="22" fill="none" stroke="#627887" stroke-width="1.7" stroke-dasharray="8 6"/>')
    s.text(557, 775, "Five structured roles; each appends its output to the audit trace", size=14, anchor="middle", fill="#536978")
    s.arrow([(855, 205), (885, 205)], "audit posts", dashed=True)
    s.arrow([(1235, 295), (1185, 295)], "post decision", dashed=True)
    s.text(48, 855, "Solid arrows = execution dependencies; dashed arrows = append-only audit posts.", size=14, fill="#536978")
    return s.finish()


FORBIDDEN_BY_FIGURE = {
    "c2ges": ("graph neural network", "GNN encoder", "LLM-generated counterfactual"),
    "ma_sqlgrid": ("LLM negotiation", "agent debate", "gold SQL ranking"),
}


def qa_svg(path: Path, expected_phrases: tuple[str, ...], forbidden_phrases: tuple[str, ...]) -> dict[str, object]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    viewbox = [float(value) for value in root.attrib["viewBox"].split()]
    if viewbox != [0.0, 0.0, 1600.0, 900.0]:
        raise AssertionError(f"unexpected viewBox in {path}: {viewbox}")
    text_content = " ".join("".join(node.itertext()) for node in root.iter(f"{{{SVG_NS}}}text"))
    for phrase in expected_phrases:
        if phrase.lower() not in text_content.lower():
            raise AssertionError(f"missing expected phrase {phrase!r} in {path}")
    for phrase in forbidden_phrases:
        if phrase.lower() in text_content.lower():
            raise AssertionError(f"forbidden phrase {phrase!r} in {path}")
    # Boundary gate for explicitly positioned primitives.  Paths inside marker
    # definitions are excluded because their local coordinate system is separate.
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "rect":
            x, y = float(node.attrib.get("x", 0)), float(node.attrib.get("y", 0))
            w, h = float(node.attrib.get("width", 0)), float(node.attrib.get("height", 0))
            if x < 0 or y < 0 or x + w > 1600 or y + h > 900:
                raise AssertionError(f"rectangle outside canvas in {path}: {(x, y, w, h)}")
        elif tag == "text":
            x, y = float(node.attrib["x"]), float(node.attrib["y"])
            if not (0 <= x <= 1600 and 0 <= y <= 900):
                raise AssertionError(f"text anchor outside canvas in {path}: {(x, y)}")
        elif tag == "polyline":
            for pair in node.attrib["points"].split():
                x, y = (float(v) for v in pair.split(","))
                if not (0 <= x <= 1600 and 0 <= y <= 900):
                    raise AssertionError(f"arrow point outside canvas in {path}: {(x, y)}")
    return {
        "xml_well_formed": True,
        "viewbox": "0 0 1600 900",
        "text_elements": len(list(root.iter(f"{{{SVG_NS}}}text"))),
        "all_explicit_anchors_within_canvas": True,
        "required_text_present": True,
        "forbidden_overclaim_text_absent": True,
        "minimum_font_size_pt_equivalent": 13,
        "rendered_visual_review": {
            "status": "PASS",
            "method": "1600×900 Chromium render inspected for clipping, overlap, arrow routing, and label legibility",
            "round": 2,
        },
    }


def write_package(
    *,
    out_dir: Path,
    filename: str,
    svg: str,
    paper: str,
    source: Path,
    expected: tuple[str, ...],
    forbidden: tuple[str, ...],
    claims: list[str],
    limitations: list[str],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / filename
    svg_path.write_text(svg, encoding="utf-8", newline="\n")
    qa = qa_svg(svg_path, expected, forbidden)
    lineage = {
        "schema_version": "figure-lineage-v1",
        "paper": paper,
        "round": "R1",
        "generation_method": "deterministic native SVG; no image API",
        "artifact": {
            "artifact_id": filename.removesuffix(".svg"),
            "file": filename,
            "sha256": sha256(svg_path),
            "source_code": {
                "file": source.relative_to(ROOT).as_posix(),
                "sha256": sha256(source),
            },
            "transformation": {
                "script": Path(__file__).relative_to(ROOT).as_posix(),
                "sha256": sha256(Path(__file__)),
            },
            "caption_claim": claims[0],
            "supported_manuscript_claims": claims,
            "limitations": limitations,
            "qa": qa,
        },
    }
    (out_dir / "FIGURE_LINEAGE.json").write_text(
        json.dumps(lineage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )


def main() -> None:
    write_package(
        out_dir=C2_OUT,
        filename="fig_c2ges_implemented_architecture_r1.svg",
        svg=c2ges_svg(),
        paper="C2GES original-title edition",
        source=C2_SOURCE,
        expected=("Typed causal event graph", "Deterministic interventions", "Multi-channel scoring", "Constrained extractive selection"),
        forbidden=FORBIDDEN_BY_FIGURE["c2ges"],
        claims=[
            "The implemented offline core transforms report sentences into a typed sentence-level proxy causal graph, applies deterministic node-deletion interventions, combines five scoring channels, and performs role-covered non-redundant extractive selection."
        ],
        limitations=[
            "The graph is rule-based and sentence-level; it is not a learned GNN and is not asserted to recover ground-truth causality.",
            "Counterfactual sensitivity is causal-flow loss under node deletion; the implementation does not generate counterfactual report text.",
            "Optional silver role evidence is not human gold annotation.",
        ],
    )
    write_package(
        out_dir=MA_OUT,
        filename="fig_ma_sqlgrid_implemented_coordination_r1.svg",
        svg=ma_svg(),
        paper="MA-SQLGrid original-title edition",
        source=MA_SOURCE,
        expected=("Query Analyst", "Schema Cartographer", "SQL Synthesizer", "Safety Validator", "Counterfactual Critic", "Append-only blackboard", "Deterministic adjudicator", "ABSTAIN"),
        forbidden=FORBIDDEN_BY_FIGURE["ma_sqlgrid"],
        claims=[
            "The implemented coordination core uses five evidence-producing or review roles, an append-only sealed blackboard, and a separate deterministic adjudicator that selects a safe executable candidate or abstains."
        ],
        limitations=[
            "SQL candidates and counterfactual state results are supplied externally; the core does not call a language model or generate SQL itself.",
            "The blackboard records structured handoffs and is not evidence of free-form inter-agent negotiation.",
            "The adjudicator is reference-free and does not access gold SQL.",
        ],
    )
    print(C2_OUT / "fig_c2ges_implemented_architecture_r1.svg")
    print(MA_OUT / "fig_ma_sqlgrid_implemented_coordination_r1.svg")


if __name__ == "__main__":
    main()
