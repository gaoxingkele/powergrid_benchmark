from __future__ import annotations

import csv
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

from lxml import etree
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / "corpus_manifest.json").read_text(encoding="utf-8"))
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")

ROLES = [
    "Introduction",
    "Related Work/Background",
    "Methods and Setup",
    "Results and Analysis",
    "Discussion and Limitations",
    "Conclusions",
]


def text(node) -> str:
    return re.sub(r"\s+", " ", " ".join(node.itertext())).strip() if node is not None else ""


def wc(value: str) -> int:
    return len(WORD_RE.findall(value or ""))


def quantile(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return float(values[lo])
    return values[lo] * (hi - pos) + values[hi] * (pos - lo)


def role_for(title: str) -> str:
    t = re.sub(r"^\s*\d+(?:\.\d+)*\.?\s*", "", title).lower().replace("\xa0", " ")
    if "conclusion" in t or "future recommendation" in t:
        return "Conclusions"
    if "limitation" in t or t.startswith("discussion") or "discussion and conclusion" in t:
        return "Discussion and Limitations"
    if (
        "related" in t or "literature review" in t or "state of the art" in t
        or "state of knowledge" in t or t.startswith("background")
        or "theoretical background" in t or "current trends" in t
    ):
        return "Related Work/Background"
    if "introduction" in t:
        return "Introduction"
    result_terms = (
        "result", "evaluation", "experiments and", "experimental result",
        "experimental simulation", "experimental section", "analysis",
    )
    if any(term in t for term in result_terms) and not any(term in t for term in ("requirements analysis", "data analysis")):
        return "Results and Analysis"
    if t == "experiment" or t == "experiments" or t.startswith("evaluation"):
        return "Results and Analysis"
    return "Methods and Setup"


def aggregate_paper(record: dict) -> tuple[dict, list[dict]]:
    corpus = record["corpus"]
    slug = record["slug"]
    xml_path = ROOT / corpus / "xml" / f"{slug}.xml"
    pdf_path = ROOT / corpus / "pdf" / f"{slug}.pdf"
    root = etree.parse(str(xml_path)).getroot()
    body = root.xpath(".//*[local-name()='body'][1]")[0]
    role_words = defaultdict(int)
    role_paras = defaultdict(int)
    section_rows = []
    top_sections = [x for x in body if etree.QName(x).localname == "sec"]
    for idx, sec in enumerate(top_sections, start=1):
        title_nodes = sec.xpath("./*[local-name()='title'][1]")
        title = text(title_nodes[0]) if title_nodes else f"Section {idx}"
        role = role_for(title)
        paras = sec.xpath(".//*[local-name()='p']")
        lengths = [wc(text(p)) for p in paras if wc(text(p))]
        role_words[role] += sum(lengths)
        role_paras[role] += len(lengths)
        section_rows.append({
            "corpus": corpus,
            "slug": slug,
            "doi": record["doi"],
            "year": record["year"],
            "category": record["category"],
            "section_index": idx,
            "section_title": title,
            "normalized_role": role,
            "paragraphs": len(lengths),
            "words": sum(lengths),
        })
    body_paras = body.xpath(".//*[local-name()='p']")
    body_lengths = [wc(text(p)) for p in body_paras if wc(text(p))]
    abstract_nodes = root.xpath(".//*[local-name()='abstract'][1]")
    figures = root.xpath(".//*[local-name()='fig']")
    tables = root.xpath(".//*[local-name()='table-wrap']")
    formulas = body.xpath(".//*[local-name()='disp-formula']")
    refs = root.xpath(".//*[local-name()='ref-list']//*[local-name()='ref']")
    row = {
        **record,
        "pages": len(PdfReader(str(pdf_path)).pages),
        "abstract_words": wc(text(abstract_nodes[0])) if abstract_nodes else 0,
        "body_words": sum(body_lengths),
        "body_paragraphs": len(body_lengths),
        "figures": len(figures),
        "tables": len(tables),
        "display_formulas": len(formulas),
        "references": len(refs),
    }
    for role in ROLES:
        key = re.sub(r"[^a-z]+", "_", role.lower()).strip("_")
        row[f"{key}_words"] = role_words[role]
        row[f"{key}_paragraphs"] = role_paras[role]
    row["foundation_words"] = role_words["Introduction"] + role_words["Related Work/Background"]
    row["evidence_words"] = role_words["Results and Analysis"] + role_words["Discussion and Limitations"]
    return row, section_rows


def subgroup(record: dict) -> str:
    category = record["category"]
    direct_terms = ("direct", "grid", "power", "maintenance", "fault", "industrial", "database", "sql")
    return "domain/direct" if any(x in category for x in direct_terms) else "method/framework"


def stats(values: list[float]) -> dict:
    return {
        "n": len(values),
        "p25": round(quantile(values, 0.25), 1),
        "p50": round(quantile(values, 0.50), 1),
        "p60": round(quantile(values, 0.60), 1),
        "p75": round(quantile(values, 0.75), 1),
        "min": round(min(values), 1) if values else 0,
        "max": round(max(values), 1) if values else 0,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    paper_rows, section_rows = [], []
    for record in MANIFEST:
        row, sections = aggregate_paper(record)
        row["subgroup"] = subgroup(record)
        row["recent_2024_2026"] = int(row["year"] >= 2024)
        paper_rows.append(row); section_rows.extend(sections)
    write_csv(ROOT / "paper_level_stats.csv", paper_rows)
    write_csv(ROOT / "top_level_section_stats.csv", section_rows)

    metrics = [
        "pages", "abstract_words", "body_words", "body_paragraphs", "figures", "tables",
        "display_formulas", "references", "foundation_words", "evidence_words",
    ]
    for role in ROLES:
        key = re.sub(r"[^a-z]+", "_", role.lower()).strip("_")
        metrics += [f"{key}_words", f"{key}_paragraphs"]

    summary = {}
    for corpus in ("C2GES", "MA_SQLGrid"):
        crows = [r for r in paper_rows if r["corpus"] == corpus]
        summary[corpus] = {}
        groups = {
            "all_20": crows,
            "domain_direct": [r for r in crows if r["subgroup"] == "domain/direct"],
            "method_framework": [r for r in crows if r["subgroup"] == "method/framework"],
            "recent_2024_2026": [r for r in crows if r["recent_2024_2026"]],
        }
        for group_name, grows in groups.items():
            summary[corpus][group_name] = {}
            for metric in metrics:
                # Section-specific distributions are present-only; zero means the role is integrated elsewhere.
                present_only = metric.endswith("_words") or metric.endswith("_paragraphs")
                vals = [float(r[metric]) for r in grows if not present_only or float(r[metric]) > 0]
                summary[corpus][group_name][metric] = stats(vals)
            summary[corpus][group_name]["papers"] = [r["doi"] for r in grows]
    (ROOT / "corpus_20x2_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    target_rows = []
    for corpus in ("C2GES", "MA_SQLGrid"):
        for role in ROLES:
            key = re.sub(r"[^a-z]+", "_", role.lower()).strip("_")
            full = summary[corpus]["all_20"][f"{key}_words"]
            direct = summary[corpus]["domain_direct"][f"{key}_words"]
            method = summary[corpus]["method_framework"][f"{key}_words"]
            recent = summary[corpus]["recent_2024_2026"][f"{key}_words"]
            target_rows.append({
                "corpus": corpus,
                "role": role,
                "papers_with_explicit_role": full["n"],
                "all_p50_words": full["p50"],
                "all_p60_words_target": full["p60"],
                "all_p75_words_ceiling": full["p75"],
                "domain_direct_p50": direct["p50"],
                "method_framework_p50": method["p50"],
                "recent_2024_2026_p50": recent["p50"],
                "all_p60_paragraphs": summary[corpus]["all_20"][f"{key}_paragraphs"]["p60"],
            })
    write_csv(ROOT / "section_targets_p60.csv", target_rows)
    print(json.dumps({c: summary[c]["all_20"] for c in summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
