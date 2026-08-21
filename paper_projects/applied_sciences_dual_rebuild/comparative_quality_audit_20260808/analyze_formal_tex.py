from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"D:\aicoding\powergrid_benchmark")
FORMAL = ROOT / "paper_projects" / "applied_sciences_dual_rebuild" / "formal_submission_preview_20260808"
OUT = Path(__file__).resolve().parent

PAPERS = {
    "C2GES": FORMAL / "C2GES" / "paper_applsci.tex",
    "MA_SQLGrid": FORMAL / "MA_SQLGrid" / "paper_applsci.tex",
}

ENVIRONMENTS = (
    "figure", "figure*", "table", "table*", "equation", "equation*", "align",
    "align*", "gather", "gather*", "algorithm", "algorithmic", "verbatim",
)


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def strip_envs(text: str) -> str:
    for env in ENVIRONMENTS:
        text = re.sub(
            rf"\\begin\{{{re.escape(env)}\}}.*?\\end\{{{re.escape(env)}\}}",
            "\n\n", text, flags=re.S,
        )
    return text


def tex_to_plain(text: str) -> str:
    text = strip_comments(text)
    text = re.sub(r"\$.*?\$", " ", text, flags=re.S)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"\\(?:cite|citep|citet|ref|eqref|autoref|label|url|href)\*?(?:\[[^]]*\])?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\(?:textbf|textit|emph|mathrm|mathbf|operatorname|texttt)\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", text)
    text = text.replace("~", " ")
    text = re.sub(r"[{}_^&#]", " ", text)
    text = re.sub(r"\\[%$]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", tex_to_plain(text))


def classify(text: str, wc: int) -> tuple[str, str]:
    low = text.lower()
    evidence = bool(re.search(r"\\(?:cite|ref|eqref)|\b(?:table|figure|fig\.|p\s*[<=>]|ci|accuracy|result|observed|measured|dataset|benchmark)\b|\d", low))
    if any(k in low for k in ("limitation", "cannot", "does not establish", "boundary", "future work")):
        role = "boundary/limitation"
    elif any(k in low for k in ("we propose", "this study", "our contribution", "contribution")):
        role = "claim/contribution"
    elif any(k in low for k in ("results", "accuracy", "confidence interval", "bootstrap", "p-value", "effect")):
        role = "result/interpretation"
    elif any(k in low for k in ("we define", "we construct", "procedure", "protocol", "algorithm", "implementation")):
        role = "method/protocol"
    elif re.search(r"\\cite", text):
        role = "literature/context"
    else:
        role = "exposition/transition"
    flags = []
    if wc < 35:
        flags.append("short")
    if wc > 180:
        flags.append("long")
    if role in {"claim/contribution", "result/interpretation"} and not evidence:
        flags.append("support-check")
    return role, ";".join(flags) if flags else "ok"


def analyze(name: str, path: Path) -> dict:
    raw = strip_comments(path.read_text(encoding="utf-8"))
    body_match = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, flags=re.S)
    body = body_match.group(1) if body_match else raw
    abstract_match = re.search(r"\\abstract\{(.*?)\}\s*\\keyword", raw, flags=re.S)
    abstract_wc = len(words(abstract_match.group(1))) if abstract_match else 0

    start = re.search(r"\\section\{Introduction\}", body)
    end = re.search(r"\\(?:authorcontributions|funding|institutionalreview|informedconsent|dataavailability|conflictsofinterest|acknowledgments)\b", body, flags=re.I)
    article = body[start.start() if start else 0:end.start() if end else len(body)]

    heading_re = re.compile(r"\\(section|subsection|subsubsection)\{([^{}]+)\}")
    matches = list(heading_re.finditer(article))
    rows = []
    current_section = ""
    current_subsection = ""
    paragraph_no = defaultdict(int)
    for i, match in enumerate(matches):
        level, title = match.group(1), tex_to_plain(match.group(2))
        if level == "section":
            current_section, current_subsection = title, ""
        elif level == "subsection":
            current_subsection = title
        chunk_end = matches[i + 1].start() if i + 1 < len(matches) else len(article)
        chunk = strip_envs(article[match.end():chunk_end])
        for para in re.split(r"\n\s*\n", chunk):
            para = para.strip()
            if not para or para.startswith("\\") and len(words(para)) < 8:
                continue
            wc = len(words(para))
            if wc < 8:
                continue
            paragraph_no[current_section] += 1
            role, flag = classify(para, wc)
            rows.append({
                "paper": name,
                "section": current_section,
                "subsection": current_subsection,
                "paragraph": paragraph_no[current_section],
                "words": wc,
                "citations": len(re.findall(r"\\cite", para)),
                "crossrefs": len(re.findall(r"\\(?:ref|eqref|autoref)", para)),
                "numeric_tokens": len(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", para)),
                "role": role,
                "mechanical_flag": flag,
                "opening": tex_to_plain(para)[:220],
            })

    with (OUT / f"{name}_paragraph_audit.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

    sec = defaultdict(lambda: {"paragraphs": 0, "words": 0, "citations": 0, "short": 0, "long": 0})
    for row in rows:
        d = sec[row["section"]]
        d["paragraphs"] += 1; d["words"] += row["words"]; d["citations"] += row["citations"]
        d["short"] += "short" in row["mechanical_flag"]
        d["long"] += "long" in row["mechanical_flag"]

    pdf_candidates = list(path.parent.glob("build*/paper_applsci.pdf"))
    pdf = pdf_candidates[0] if pdf_candidates else path.with_suffix(".pdf")
    bib_candidates = list(path.parent.glob("*.bib"))
    bib = bib_candidates[0] if bib_candidates else path.parent / "references.bib"
    summary = {
        "paper": name,
        "tex": str(path),
        "pdf": str(pdf),
        "abstract_words": abstract_wc,
        "body_words_estimate": sum(r["words"] for r in rows),
        "body_paragraphs": len(rows),
        "mean_words_per_paragraph": round(sum(r["words"] for r in rows) / len(rows), 1),
        "top_level_sections": len(re.findall(r"\\section\{", article)),
        "subsections": len(re.findall(r"\\subsection\{", article)),
        "figures": len(re.findall(r"\\begin\{figure\*?\}", article)),
        "tables": len(re.findall(r"\\begin\{table\*?\}", article)),
        "display_math_environments": len(re.findall(r"\\begin\{(?:equation\*?|align\*?|gather\*?)\}", article)),
        "bib_entries": len(re.findall(r"^@", bib.read_text(encoding="utf-8"), flags=re.M)) if bib.exists() else None,
        "sections": dict(sec),
        "flag_counts": Counter(r["mechanical_flag"] for r in rows),
    }
    return summary


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = [analyze(name, path) for name, path in PAPERS.items()]
    (OUT / "formal_manuscript_stats.json").write_text(json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
