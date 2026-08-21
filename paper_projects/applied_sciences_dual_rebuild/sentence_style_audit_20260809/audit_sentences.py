from __future__ import annotations

import csv
import json
import re
import statistics
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(r"D:\aicoding\powergrid_benchmark")
BASE = ROOT / "paper_projects" / "applied_sciences_dual_rebuild"
FINAL = BASE / "formal_submission_p60_revision_20260808" / "three_round_peer_review" / "final"
CORPUS = BASE / "comparative_quality_audit_20260808" / "corpus_20x2"
OUT = Path(__file__).resolve().parent

PAPERS = {
    "C2GES": FINAL / "C2GES" / "paper_applsci.tex",
    "MA_SQLGrid": FINAL / "MA_SQLGrid" / "paper_applsci.tex",
}

ABBREVIATIONS = {
    "e.g.": "e<prd>g<prd>", "i.e.": "i<prd>e<prd>", "et al.": "et al<prd>",
    "Fig.": "Fig<prd>", "Figs.": "Figs<prd>", "Eq.": "Eq<prd>",
    "Eqs.": "Eqs<prd>", "Dr.": "Dr<prd>", "Prof.": "Prof<prd>",
    "vs.": "vs<prd>", "No.": "No<prd>", "Sec.": "Sec<prd>",
}

ENVIRONMENTS = {
    "table", "table*", "equation", "equation*", "align", "align*", "gather",
    "gather*", "algorithm", "algorithmic", "verbatim", "adjustwidth",
}


def percentile(values: list[int], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    protected = text
    for src, dst in ABBREVIATIONS.items():
        protected = protected.replace(src, dst)
    protected = re.sub(r"(?<=\d)\.(?=\d)", "<prd>", protected)
    protected = re.sub(r"\b([A-Z])\.(?=\s*[A-Z]\.)", r"\1<prd>", protected)
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\\\"`(\[])", protected)
    return [p.replace("<prd>", ".").strip() for p in pieces if p.strip()]


def plain_tex(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(r"\\(?:cite|citep|citet)\*?(?:\[[^]]*\])?\{[^{}]*\}", "", text)
    text = re.sub(r"\\(?:ref|eqref|autoref|label)\*?\{[^{}]*\}", "[reference]", text)
    text = re.sub(r"\\url\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\href\{[^{}]*\}\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:textbf|textit|emph|mathrm|mathbf|mathit|operatorname|texttt|texorpdfstring)\{([^{}]*)\}", r"\1", text)
    text = text.replace(r"\cges{}", "C²GES").replace(r"\cges", "C²GES")
    text = re.sub(r"\$[^$]*\$", " [formula] ", text)
    text = re.sub(r"\\\([^)]*\\\)", " [formula] ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", text)
    text = re.sub(r"[{}_^&#]", " ", text)
    text = text.replace("~", " ").replace(r"\%", "%").replace(r"\&", "&")
    return re.sub(r"\s+", " ", text).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[²³]|[-'][A-Za-z0-9]+)*", text))


def xml_paragraphs(folder: Path) -> list[str]:
    paras: list[str] = []
    for path in sorted(folder.glob("*.xml")):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            continue
        for elem in root.findall(".//body//p"):
            txt = re.sub(r"\s+", " ", "".join(elem.itertext())).strip()
            if word_count(txt) >= 8:
                paras.append(txt)
    return paras


def balanced_macro(raw: str, name: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    token = "\\" + name + "{"
    pos = 0
    while True:
        start = raw.find(token, pos)
        if start < 0:
            break
        i, depth = start + len(token), 1
        while i < len(raw) and depth:
            if raw[i] == "{" and (i == 0 or raw[i - 1] != "\\"):
                depth += 1
            elif raw[i] == "}" and (i == 0 or raw[i - 1] != "\\"):
                depth -= 1
            i += 1
        if depth == 0:
            out.append((raw.count("\n", 0, start) + 1, raw[start + len(token):i - 1]))
        pos = i
    return out


def manuscript_units(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    units: list[dict] = []
    for macro, section in [
        ("abstract", "Abstract"), ("featuredapplication", "Featured Application"),
    ]:
        for line, txt in balanced_macro(raw, macro):
            units.append({"section": section, "subsection": "", "line": line, "text": plain_tex(txt), "kind": "prose"})

    start_m = re.search(r"\\section\{Introduction\}", raw)
    end_m = re.search(r"\\supplementary\{", raw)
    if not start_m:
        raise RuntimeError(f"Introduction not found in {path}")
    start = start_m.start()
    end = end_m.start() if end_m else len(raw)
    body = raw[start:end]
    base_line = raw.count("\n", 0, start) + 1
    section = "Introduction"
    subsection = ""
    para: list[str] = []
    para_line = base_line
    env_stack: list[str] = []

    def flush() -> None:
        nonlocal para
        txt = plain_tex(" ".join(para))
        if word_count(txt) >= 5:
            units.append({"section": section, "subsection": subsection, "line": para_line, "text": txt, "kind": "prose"})
        para = []

    for offset, line_text in enumerate(body.splitlines()):
        line_no = base_line + offset
        sec_m = re.match(r"\s*\\section\{([^{}]+)\}", line_text)
        sub_m = re.match(r"\s*\\subsection\{([^{}]+)\}", line_text)
        begin_m = re.search(r"\\begin\{([^{}]+)\}", line_text)
        end_env_m = re.search(r"\\end\{([^{}]+)\}", line_text)
        if sec_m:
            flush(); section, subsection = plain_tex(sec_m.group(1)), ""; continue
        if sub_m:
            flush(); subsection = plain_tex(sub_m.group(1)); continue
        if begin_m and begin_m.group(1) in ENVIRONMENTS:
            flush(); env_stack.append(begin_m.group(1)); continue
        if env_stack:
            if end_env_m and end_env_m.group(1) == env_stack[-1]:
                env_stack.pop()
            continue
        if not line_text.strip():
            flush(); continue
        if line_text.lstrip().startswith("%"):
            continue
        if not para:
            para_line = line_no
        para.append(line_text)
    flush()

    for macro, section in [
        ("supplementary", "Supplementary Materials"),
        ("authorcontributions", "Author Contributions"), ("funding", "Funding"),
        ("institutionalreview", "Institutional Review Board Statement"),
        ("informedconsent", "Informed Consent Statement"),
        ("dataavailability", "Data Availability Statement"),
        ("acknowledgments", "Acknowledgments"),
        ("conflictsofinterest", "Conflicts of Interest"),
    ]:
        for line, txt in balanced_macro(raw, macro):
            units.append({"section": section, "subsection": "", "line": line, "text": plain_tex(txt), "kind": "backmatter"})
    return sorted(units, key=lambda x: (x["line"], 0 if x["section"] == "Abstract" else 1))


def classify(name: str, section: str, sentence: str, benchmark: dict, previous: str | None, next_sentence: str | None) -> tuple[str, list[str], str]:
    low = sentence.lower()
    wc = word_count(sentence)
    flags: list[str] = []
    suggestions: list[str] = []
    p90 = benchmark["sentence_words_p90"]
    if wc > max(48, p90 + 8):
        flags.append("overlong")
        suggestions.append("拆为2句：首句只陈述主结果/步骤，次句保留限制、原因或适用边界")
    elif wc > max(38, p90):
        flags.append("long")
        suggestions.append("检查能否在转折词或分号处拆句，减少单句信息负荷")
    if sentence.count(";") >= 2 or sentence.count(":") >= 2:
        flags.append("punctuation_load")
        suggestions.append("减少分号/冒号串联，改为完整句或项目化列举")
    clause_markers = len(re.findall(r"\b(?:although|whereas|while|because|but|yet|which|that|therefore|however|so that|rather than)\b", low))
    if clause_markers >= 4 and wc > 40:
        flags.append("clause_stack")
        suggestions.append("保留一个主从关系，其余从句拆出并明确证据—解释顺序")
    negatives = len(re.findall(r"\b(?:not|no|neither|nor|cannot|without|untested|unresolved|unavailable|excluded|failed)\b", low))
    if negatives >= 3:
        flags.append("negation_density")
        suggestions.append("改为先正面说明证据支持什么，再用一句集中限定不支持的范围")
    if re.match(r"^(This|These|It)\b", sentence) and previous:
        flags.append("anaphora_check")
        suggestions.append("将句首代词替换为明确名词短语，避免跨句指代含混")
    if re.search(r"\b(?:aspirational|title-concordant|scientific claims|does not assert|must not be|cannot rehabilitate)\b", low):
        flags.append("reviewer_facing_meta")
        suggestions.append("若不属于方法定义，移至研究范围或局限性集中陈述，正文改为对象—方法—证据的直接表达")
    if len(re.findall(r"\b\d+(?:\.\d+)?(?:%|/[0-9.]+)?\b", sentence)) >= 5:
        flags.append("numeric_density")
        suggestions.append("将密集数值移入表格/括号，仅在句中保留主要估计、方向和不确定性")
    if re.search(r"(?<![A-Za-z])\d+(?:\.\d+)?/\d", sentence):
        flags.append("compressed_numeric_pair")
        suggestions.append("展开K=5与K=10或两个比较对象，避免斜线数值对造成歧义")
    if "counterfactual critic" in low and "metamorphic-state critic" not in low:
        flags.append("legacy_term")
        suggestions.append("统一为Metamorphic-State Critic；历史名称仅在首次定义处保留一次")
    if "sql synthesizer" in low and re.search(r"\b(generate|generates|generated)\b", low):
        flags.append("role_semantics")
        suggestions.append("明确该角色只封装外部候选，不在核心协调协议内生成SQL")
    if "causal" in low and not re.search(r"\b(?:not|proxy|textual|distinguish(?:es|ed|ing)?|rather than)\b", low) and re.search(r"\b(effect|identify|identification|inference)\b", low):
        flags.append("causal_scope")
        suggestions.append("明确是文本结构代理或计算扰动，避免读成物理因果识别")
    if name == "MA_SQLGrid" and re.search(r"\b(?:counterfactual evidence|counterfactual-required|no-counterfactual mode|empty counterfactual mapping)\b", low):
        flags.append("legacy_evidence_term")
        suggestions.append("统一为named-state或constructed-state evidence；若是代码中的历史参数名，仅在首次出现时注明")
    if previous and sentence[:60] == previous[:60]:
        flags.append("repeated_opening")
        suggestions.append("调整句首主语或合并重复命题")
    if next_sentence and negatives >= 2 and len(re.findall(r"\b(?:not|no|cannot|without|untested|unresolved)\b", next_sentence.lower())) >= 2:
        flags.append("consecutive_caveats")
        suggestions.append("与下一句合并为一个边界段尾句，避免连续否定削弱论证推进")

    severe = {"overlong", "clause_stack", "reviewer_facing_meta", "role_semantics", "causal_scope", "legacy_evidence_term"}
    if any(f in severe for f in flags):
        status = "REVISE"
    elif flags:
        status = "REVIEW"
    else:
        status = "KEEP"
        suggestions.append("句式、术语和承接未见明显问题，可保留")
    return status, flags, "；".join(dict.fromkeys(suggestions))


def benchmark(folder: Path) -> dict:
    paras = xml_paragraphs(folder)
    sentences = [s for p in paras for s in split_sentences(p) if word_count(s) >= 4]
    sw = [word_count(s) for s in sentences]
    ps = [len(split_sentences(p)) for p in paras]
    pw = [word_count(p) for p in paras]
    return {
        "reference_papers": len(list(folder.glob("*.xml"))),
        "paragraphs": len(paras), "sentences": len(sentences),
        "sentence_words_mean": round(statistics.mean(sw), 2),
        "sentence_words_median": round(statistics.median(sw), 2),
        "sentence_words_p75": round(percentile(sw, .75), 2),
        "sentence_words_p90": round(percentile(sw, .90), 2),
        "paragraph_words_median": round(statistics.median(pw), 2),
        "paragraph_sentences_median": round(statistics.median(ps), 2),
        "semicolon_rate_per_100_sentences": round(100 * sum(";" in s for s in sentences) / len(sentences), 2),
        "first_person_rate_per_100_sentences": round(100 * sum(bool(re.search(r"\b(?:we|our)\b", s.lower())) for s in sentences) / len(sentences), 2),
        "negation_rate_per_100_sentences": round(100 * sum(bool(re.search(r"\b(?:not|no|cannot|without)\b", s.lower())) for s in sentences) / len(sentences), 2),
    }


def audit(name: str, path: Path, bench: dict) -> dict:
    rows: list[dict] = []
    sentence_id = 0
    for unit_no, unit in enumerate(manuscript_units(path), 1):
        ss = split_sentences(unit["text"])
        for i, sentence in enumerate(ss):
            sentence_id += 1
            prev = ss[i - 1] if i else None
            nxt = ss[i + 1] if i + 1 < len(ss) else None
            status, flags, suggestion = classify(name, unit["section"], sentence, bench, prev, nxt)
            if unit["section"] in {"Author Contributions", "Funding", "Institutional Review Board Statement", "Informed Consent Statement", "Conflicts of Interest"}:
                status, flags, suggestion = "KEEP", [], "MDPI固定声明句式，当前格式可保留"
            rows.append({
                "sentence_id": f"{name}-S{sentence_id:04d}", "source_line": unit["line"],
                "section": unit["section"], "subsection": unit["subsection"],
                "unit_no": unit_no, "sentence_in_unit": i + 1, "words": word_count(sentence),
                "status": status, "flags": ";".join(flags) if flags else "none",
                "sentence": sentence, "modification_suggestion": suggestion,
            })
    out_csv = OUT / f"{name}_sentence_by_sentence_audit.csv"
    with out_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

    status_counts = Counter(r["status"] for r in rows)
    flag_counts = Counter(f for r in rows for f in r["flags"].split(";") if f != "none")
    section_counts = defaultdict(Counter)
    for r in rows:
        section_counts[r["section"]][r["status"]] += 1
    return {
        "paper": name, "tex": str(path), "sentences_audited": len(rows),
        "status_counts": dict(status_counts), "flag_counts": dict(flag_counts),
        "section_status_counts": {k: dict(v) for k, v in section_counts.items()},
        "sentence_words_mean": round(statistics.mean(r["words"] for r in rows), 2),
        "sentence_words_median": round(statistics.median(r["words"] for r in rows), 2),
        "sentence_words_p90": round(percentile([r["words"] for r in rows], .90), 2),
        "csv": str(out_csv),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    benches = {name: benchmark(CORPUS / name / "xml") for name in PAPERS}
    reports = [audit(name, path, benches[name]) for name, path in PAPERS.items()]
    result = {"benchmarks": benches, "manuscripts": reports}
    (OUT / "sentence_audit_summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
