from __future__ import annotations

import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import fitz


ROOT = Path(r"D:\aicoding\powergrid_benchmark")
PROJECTS = ROOT / "paper_projects"
OUT = ROOT / "reviews" / "mintou_2026-08-09_journal_fit_audit"
MANIFEST = ROOT / "ara_collections" / "target_journal_related" / "collection_manifest.csv"

PAPERS = {
    "mintou_p1_dstar_gru_dispatch": ("IEEE Access", "p1_twin_gru_dispatch"),
    "mintou_p2_hygraph_load_forecasting": ("Electronics", "p2_hyperbolic_gcn_smart_dispatch"),
    "mintou_p3_samode_distribution_planning": ("Energies", "p3_self_adaptive_mode_distribution_planning"),
    "mintou_p4_shield_resilience_planning": ("Energies", "p4_resilience_distribution_planning"),
    "mintou_p5_trace_moea_feasibility_review": ("Energies", "p5_hybrid_moea_feasibility_review"),
    "mintou_p6_bilonsga_project_review": ("Applied Sciences", "p6_nsga_bls_feasibility_review"),
}


def words(text: str) -> list[str]:
    return re.findall(r"\b[A-Za-z][A-Za-z'\-]*\b", text)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    # Protect common abbreviations and decimal points before sentence splitting.
    protected = text
    replacements = {
        "e.g.": "e§g§", "i.e.": "i§e§", "et al.": "et al§",
        "Fig.": "Fig§", "Eq.": "Eq§", "Sec.": "Sec§", "Dr.": "Dr§",
    }
    for old, new in replacements.items():
        protected = protected.replace(old, new)
    chunks = re.split(r"(?<=[.!?])\s+(?=(?:[A-Z\[]|\*\*))", protected)
    out = []
    for chunk in chunks:
        for old, new in replacements.items():
            chunk = chunk.replace(new, old)
        if words(chunk):
            out.append(chunk.strip())
    return out


def is_prose(block: str) -> bool:
    s = block.strip()
    if not s or s.startswith(("#", "|", "$$", "```", "![", "<!--")):
        return False
    if re.match(r"^(?:[-*]\s|\d+\.\s)", s):
        return False
    return len(words(s)) >= 5


def sentence_findings(sentence: str, target: str, section: str) -> tuple[str, list[str], str]:
    low = sentence.lower()
    issues: list[str] = []
    suggestions: list[str] = []

    if re.search(r"author input required|\btodo\b|\btbd\b|placeholder", low):
        issues.append("P0_PLACEHOLDER")
        suggestions.append("投稿前填入经作者确认的信息，删除占位标记")
    if re.search(r"we target|target venues?|accepted-paper corpus|during template conversion|before submission|at submission time|pre-submission checklist", low):
        issues.append("P0_INTERNAL_EDITORIAL")
        suggestions.append("删除面向内部流程或审稿人的元话语，改为客观学术陈述")
    if re.search(r"companion (?:study|paper|manuscript).*(?:in preparation|submitted)|currently in preparation", low):
        issues.append("P0_COMPANION_STATUS")
        suggestions.append("按投稿时真实状态和期刊政策处理姊妹稿引用，并在投稿信中完整披露")
    if len(words(sentence)) > 60:
        issues.append("P1_VERY_LONG_SENTENCE")
        suggestions.append("拆成2–3句，每句只承担一个主张或证据关系")
    elif len(words(sentence)) > 45:
        issues.append("P1_LONG_SENTENCE")
        suggestions.append("拆句并前置主语与结论，降低从句和插入语密度")
    if re.search(r"\bwe believe\b|worth (?:a subsection|documenting)|honest negative|red flag by reviewers|what the evidence chain taught us", low):
        issues.append("P1_RHETORICAL_META")
        suggestions.append("改为可验证的结果陈述，避免辩护式、编辑式或价值评判式措辞")
    if re.search(r"\b(first|novel|proves?|establishes?|confirms?)\b", low):
        if not re.search(r"\[[0-9,\- ]+\]|\b(?:table|fig(?:ure)?|section)\s+\d|\b(?:p|r)\s*[=<]", low):
            issues.append("P1_STRONG_CLAIM_CHECK")
            suggestions.append("核验独创性/因果/证明性措辞，并补直接证据或降格为观察性表述")
    if "future work" in low or "remains future" in low or "deferred" in low:
        issues.append("P2_FUTURE_WORK")
        suggestions.append("仅保留与当前证据边界直接相关的一句，避免用未来工作替代当前验证")
    if "reviewer" in low and "review" not in section.lower():
        issues.append("P1_REVIEWER_DIRECTED")
        suggestions.append("删除对审稿人反应的揣测，直接说明方法学风险或解释边界")

    if any(i.startswith("P0_") for i in issues):
        status = "BLOCK"
    elif any(i.startswith("P1_") for i in issues):
        status = "REVISE"
    elif issues:
        status = "CHECK"
    else:
        status = "PASS"
    return status, issues, "；".join(dict.fromkeys(suggestions))


def parse_manuscript(path: Path, target: str) -> tuple[list[dict], list[dict], dict]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    section = "Front matter"
    paragraph_rows: list[dict] = []
    sentence_rows: list[dict] = []
    buffer: list[tuple[int, str]] = []
    paragraph_id = 0
    sentence_id = 0

    def flush() -> None:
        nonlocal paragraph_id, sentence_id, buffer
        if not buffer:
            return
        text = " ".join(x[1].strip() for x in buffer).strip()
        start, end = buffer[0][0], buffer[-1][0]
        buffer = []
        if not is_prose(text):
            return
        paragraph_id += 1
        sents = split_sentences(text)
        p_issues: list[str] = []
        if len(words(text)) > 180:
            p_issues.append("P1_LONG_PARAGRAPH")
        if len(sents) == 1 and len(words(text)) > 65:
            p_issues.append("P1_DENSE_SINGLE_SENTENCE_PARAGRAPH")
        statuses = []
        for sentence in sents:
            sentence_id += 1
            status, issues, suggestion = sentence_findings(sentence, target, section)
            statuses.append(status)
            p_issues.extend(issues)
            sentence_rows.append({
                "target_journal": target,
                "section": section,
                "paragraph_id": paragraph_id,
                "sentence_id": sentence_id,
                "line_start": start,
                "word_count": len(words(sentence)),
                "status": status,
                "issue_codes": ";".join(issues),
                "suggestion_zh": suggestion,
                "sentence": sentence,
            })
        p_status = "BLOCK" if "BLOCK" in statuses else "REVISE" if ("REVISE" in statuses or any(i.startswith("P1_") for i in p_issues)) else "CHECK" if statuses and "CHECK" in statuses else "PASS"
        paragraph_rows.append({
            "target_journal": target,
            "section": section,
            "paragraph_id": paragraph_id,
            "line_start": start,
            "line_end": end,
            "word_count": len(words(text)),
            "sentence_count": len(sents),
            "status": p_status,
            "issue_codes": ";".join(dict.fromkeys(p_issues)),
            "paragraph_preview": text[:240],
        })

    in_comment = False
    in_fence = False
    for idx, line in enumerate(lines, 1):
        if "<!--" in line:
            flush(); in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.strip().startswith("```"):
            flush(); in_fence = not in_fence; continue
        if in_fence:
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush(); section = heading.group(2).strip(); continue
        if not line.strip():
            flush()
        else:
            buffer.append((idx, line))
    flush()

    counts = Counter(row["status"] for row in sentence_rows)
    pcounts = Counter(row["status"] for row in paragraph_rows)
    ref_parts = re.split(r"(?m)^##\s+References\s*$", raw, maxsplit=1)
    ref_block = re.split(r"(?m)^##\s+", ref_parts[1], maxsplit=1)[0] if len(ref_parts) == 2 else ""
    ref_matches = re.findall(r"^(?:\[[0-9]+\]|[0-9]+\.)\s", ref_block, re.M)
    summary = {
        "words": sum(row["word_count"] for row in paragraph_rows),
        "paragraphs": len(paragraph_rows),
        "sentences": len(sentence_rows),
        "sentence_status": dict(counts),
        "paragraph_status": dict(pcounts),
        "mean_sentence_words": round(statistics.mean(row["word_count"] for row in sentence_rows), 1),
        "median_paragraph_words": statistics.median(row["word_count"] for row in paragraph_rows),
        "references": len(ref_matches),
        "figures_cited": len(set(re.findall(r"(?i)\bFig(?:ure)?\.?\s*(\d+)", raw))),
        "tables_cited": len(set(re.findall(r"(?i)\bTable\s+(\d+)", raw))),
        "display_equations": len(re.findall(r"\$\$.*?\$\$", raw, re.S)),
        "placeholder_hits": len(re.findall(r"AUTHOR INPUT REQUIRED|\bTODO\b|\bTBD\b|PLACEHOLDER", raw, re.I)),
    }
    return paragraph_rows, sentence_rows, summary


def pdf_stats(path: Path) -> dict | None:
    try:
        doc = fitz.open(path)
        text = "\n".join(page.get_text("text") for page in doc)
        # Keep body-like prose; remove references tail when detectable.
        body = re.split(r"\n(?:References|REFERENCES)\s*\n", text, maxsplit=1)[0]
        blocks = [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n\s*\n", body)]
        blocks = [b for b in blocks if len(words(b)) >= 12]
        sents = [s for b in blocks for s in split_sentences(b)]
        return {
            "pages": len(doc),
            "words": len(words(body)),
            "mean_sentence_words": round(statistics.mean(len(words(s)) for s in sents), 1) if sents else 0,
            "median_block_words": statistics.median(len(words(b)) for b in blocks) if blocks else 0,
        }
    except Exception:
        return None


def comparator_summary() -> tuple[dict, list[dict]]:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    detailed: list[dict] = []
    for row in rows:
        pdf = ROOT / row["pdf_path"]
        if not pdf.exists():
            continue
        stats = pdf_stats(pdf)
        if stats:
            detailed.append({**row, **stats})
    by_journal: dict[str, list[dict]] = defaultdict(list)
    for row in detailed:
        by_journal[row["journal"]].append(row)
    summary = {}
    for journal, items in by_journal.items():
        summary[journal] = {
            "n": len(items),
            "pages_median": statistics.median(x["pages"] for x in items),
            "words_median": round(statistics.median(x["words"] for x in items)),
            "sentence_words_median_of_means": round(statistics.median(x["mean_sentence_words"] for x in items), 1),
            "block_words_median_of_medians": round(statistics.median(x["median_block_words"] for x in items), 1),
        }
    return summary, detailed


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    comparator, comparator_rows = comparator_summary()
    write_csv(OUT / "comparator_pdf_statistics.csv", comparator_rows)
    all_summary = {}
    for paper, (target, topic) in PAPERS.items():
        path = PROJECTS / paper / "manuscript" / "MANUSCRIPT.md"
        paragraphs, sentences, summary = parse_manuscript(path, target)
        for row in paragraphs:
            row["paper"] = paper
        for row in sentences:
            row["paper"] = paper
        # Move paper to first column for readability.
        paragraphs = [{"paper": r.pop("paper"), **r} for r in paragraphs]
        sentences = [{"paper": r.pop("paper"), **r} for r in sentences]
        write_csv(OUT / f"{paper}_paragraph_audit.csv", paragraphs)
        write_csv(OUT / f"{paper}_sentence_audit.csv", sentences)
        all_summary[paper] = {"target": target, "topic": topic, **summary}
    (OUT / "audit_summary.json").write_text(
        json.dumps({"generated": "2026-08-09", "comparator": comparator, "papers": all_summary}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"out": str(OUT), "comparator": comparator, "papers": all_summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
