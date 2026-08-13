"""Comprehensive latest-manuscript comparison against ten target-journal papers.

The comparator membership is frozen by
``reviews/mintou_2026-08-10_comparative_benchmark/selected_comparators.csv``.
Counts are reproducible descriptive proxies, not journal acceptance thresholds.
"""

from __future__ import annotations

import csv
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "reviews" / "mintou_2026-08-10_comparative_benchmark"
OUT = ROOT / "reviews" / "mintou_2026-08-10_comprehensive_latest_vs_10"
SELECTED = BASE / "selected_comparators.csv"

PAPERS = {
    "P1": ("mintou_p1_dstar_gru_dispatch", "IEEE Access", 2, 5, 8, 5, 208),
    "P2": ("mintou_p2_hygraph_load_forecasting", "Electronics", 3, 5, 5, 5, 860),
    "P3": ("mintou_p3_samode_distribution_planning", "Energies", 1, 7, 9, 4, 2940),
    "P4": ("mintou_p4_shield_resilience_planning", "Energies", 3, 8, 5, 7, 3120),
    "P5": ("mintou_p5_trace_moea_feasibility_review", "Energies", 4, 10, 7, 8, 3360),
    "P6": ("mintou_p6_bilonsga_project_review", "Applied Sciences", 4, 10, 7, 10, 4320),
}

CATEGORIES = ["abstract", "introduction", "related_work", "problem_data", "method", "experimental_setup", "results", "discussion", "limitations", "conclusion"]

TERMS = [
    "non-dominated sorting", "constraint dominance", "crowding distance", "pareto front", "hypervolume",
    "objective function", "budget constraint", "feasibility repair", "sensitivity analysis", "ablation study",
    "mann-whitney", "holm correction", "confidence interval", "effect size", "standard deviation",
    "training set", "validation set", "test set", "temporal split", "data leakage", "baseline",
    "attention weights", "embedding", "encoder", "loss function", "computational complexity",
    "power flow", "ac feasibility", "distribution network", "load forecasting", "scenario screening",
    "external validity", "statistical significance", "random seed", "reproducibility",
]

STYLE_PHRASES = [
    "results show that", "results indicate that", "as shown in figure", "as presented in table",
    "compared with", "compared to", "under the same", "statistically significant",
    "no significant difference", "it should be noted that", "in order to", "can be expressed as",
    "is defined as", "is calculated as", "the objective function", "constraint condition",
    "experimental results", "sensitivity analysis", "ablation study", "confidence interval",
    "standard deviation", "random seed", "training set", "validation set", "test set",
    "future work", "limitations of this study", "in this paper", "this paper proposes",
    "we propose", "we evaluate", "does not establish", "under the evaluated protocol",
]

CONNECTORS = {
    "contrast": ["however", "whereas", "although", "nevertheless", "in contrast", "by contrast"],
    "cause": ["because", "therefore", "thus", "consequently", "hence"],
    "qualification": ["may", "might", "suggests", "indicates", "within", "under the evaluated", "does not establish"],
    "evidence": ["table ", "figure ", "fig. ", "p =", "p <", "confidence interval", "evidence:"],
}


def words(text: str) -> list[str]:
    return re.findall(r"\b[A-Za-z][A-Za-z0-9'’-]*\b", text)


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    for a, b in {"e.g.": "e§g§", "i.e.": "i§e§", "et al.": "et al§", "Fig.": "Fig§", "Eq.": "Eq§"}.items():
        text = text.replace(a, b)
    chunks = re.split(r"(?<=[.!?])\s+(?=[A-Z\[])" , text)
    return [x.replace("§", ".").strip() for x in chunks if len(words(x)) >= 3]


def category(title: str) -> str:
    t = title.lower().strip()
    if "abstract" in t: return "abstract"
    if "introduction" in t: return "introduction"
    if any(x in t for x in ("related work", "literature", "background")): return "related_work"
    if any(x in t for x in ("problem formulation", "benchmark", "dataset", "data set", "system model")): return "problem_data"
    if any(x in t for x in ("method", "framework", "algorithm", "model", "network", "moea", "loadnet", "cars", "shield", "trace", "bilo")): return "method"
    if any(x in t for x in ("experimental setup", "experiment setup", "methodology", "simulation setup", "case study setup")): return "experimental_setup"
    if any(x in t for x in ("result", "validation", "case stud", "simulation", "analysis", "ablation", "sensitivity")): return "results"
    if "limitation" in t: return "limitations"
    if any(x in t for x in ("discussion", "implication")): return "discussion"
    if "conclusion" in t: return "conclusion"
    return "other"


def sentence_metrics(text: str) -> dict[str, float]:
    ss = sentences(text)
    lens = [len(words(s)) for s in ss] or [0]
    low = [s.lower() for s in ss]
    out = {
        "sentences": len(ss), "mean_sentence_words": statistics.mean(lens),
        "median_sentence_words": statistics.median(lens),
        "p90_sentence_words": sorted(lens)[max(0, math.ceil(.9 * len(lens)) - 1)],
        "short_sentence_share_le15": sum(n <= 15 for n in lens) / len(lens),
        "long_sentence_share_gt40": sum(n > 40 for n in lens) / len(lens),
        "first_person_share": sum(bool(re.search(r"\b(we|our)\b", s)) for s in low) / len(low),
        "passive_proxy_share": sum(bool(re.search(r"\b(is|are|was|were|be|been)\s+\w+(ed|en)\b", s)) for s in low) / len(low),
    }
    for name, toks in CONNECTORS.items():
        out[f"{name}_connector_share"] = sum(any(x in s for x in toks) for s in low) / len(low)
    return out


def theory_scores(text: str, eq: int, kind: str) -> dict[str, float]:
    low = text.lower()
    logic_items = ["gap", "contribution", "research question", "organized as", "related work", "limitations", "conclusion", "ablation", "discussion"]
    math_items = ["objective", "constraint", "normalization", "distance", "loss", "dominance", "hypervolume", "complexity", "argmin", "argmax"]
    stat_items = ["seed", "standard deviation", "mann", "holm", "p-value", "p =", "confidence interval", "effect size", "significant", "non-significant"]
    if kind == "ml":
        foundation = ["encoder", "embedding", "loss", "training", "validation", "test", "attention", "baseline", "ablation", "complexity"]
    else:
        foundation = ["pareto", "dominance", "crowding", "hypervolume", "constraint", "repair", "selection", "mutation", "crossover", "complexity"]
    def score(items, bonus=0):
        return min(5.0, round(5 * sum(x in low for x in items) / len(items) + bonus, 2))
    return {
        "logic_spine_score_5": score(logic_items),
        "math_foundation_score_5": score(math_items, min(1.0, eq / 12)),
        "statistics_score_5": score(stat_items),
        "ml_or_optimization_foundation_score_5": score(foundation),
    }


def markdown(path: Path, paper: str) -> tuple[dict, list[dict], dict, Counter]:
    raw = path.read_text(encoding="utf-8")
    body = re.split(r"(?m)^##\s+References\s*$", raw)[0]
    section = "other"
    section_name = "Front matter"
    section_rows = defaultdict(lambda: {"words": 0, "paragraphs": 0, "sections": set()})
    paras, prose = [], []
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b or b.startswith(("<!--", "|", "![", "```", "$$")): continue
        h = re.match(r"^(#{1,6})\s+(.+)", b)
        if h:
            section_name = h.group(2).strip()
            # Compare journal-like top-level chapters.  A subsection named
            # "Methods Compared" inside Experimental Setup must not move its
            # prose back into the Method chapter.
            c = category(section_name)
            if len(h.group(1)) <= 2 and c != "other": section = c
            continue
        # Count substantive numbered/bulleted contribution and limitation
        # items as prose units; tables, figures, code and equations remain
        # excluded above.
        clean = re.sub(r"^(?:[-*]\s|\d+\.\s)", "", b)
        clean = re.sub(r"\$.*?\$", " ", clean, flags=re.S)
        n = len(words(clean))
        if n >= 10:
            paras.append(n); prose.append(clean)
            section_rows[section]["words"] += n
            section_rows[section]["paragraphs"] += 1
            section_rows[section]["sections"].add(section_name)
    text = " ".join(prose)
    figs = set(re.findall(r"(?i)\bFig(?:ure)?\.?\s*(\d+)", body))
    tables = set(re.findall(r"(?i)\bTable\s+(\d+)", body))
    eq = len(re.findall(r"\$\$.*?\$\$", body, re.S))
    metric = {
        "paper": paper, "words": len(words(body)), "paragraphs": len(paras),
        "mean_paragraph_words": statistics.mean(paras), "median_paragraph_words": statistics.median(paras),
        "display_equations": eq, "figures": len(figs), "tables": len(tables),
        **sentence_metrics(text), **theory_scores(body, eq, "ml" if paper in {"P1", "P2"} else "opt"),
    }
    srows=[]
    for c in CATEGORIES:
        d=section_rows[c]
        srows.append({"paper":paper,"source":"manuscript","category":c,"words":d["words"],"paragraphs":d["paragraphs"],"mean_paragraph_words":d["words"]/d["paragraphs"] if d["paragraphs"] else 0,"subsections":len(d["sections"])})
    term=Counter({x: body.lower().count(x) for x in TERMS})
    return metric,srows,{"raw":body,"prose":text},term


def pdf(path: Path, paper: str) -> tuple[dict, list[dict], str, Counter]:
    doc=fitz.open(path); section="other"; rows=defaultdict(lambda:{"words":0,"paragraphs":0,"sections":set()}); prose=[]; all_text=[]
    stopped=False
    for page in doc:
        all_text.append(page.get_text("text",sort=True))
        for block in page.get_text("blocks",sort=True):
            b=re.sub(r"\s+"," ",block[4]).strip()
            if not b: continue
            if re.match(r"(?i)^(references|bibliography)\b",b): stopped=True
            if stopped: continue
            # IEEE/MDPI PDFs often merge the section heading and its first
            # paragraph into one text block (for example, "I. INTRODUCTION
            # Contingency analysis ...").  Classify the leading window rather
            # than discarding everything after the first full stop.
            first=b[:180]
            c=category(first)
            main_heading = bool(re.match(r"^\s*(?:[IVX]+\.|\d+\.)\s+", b)) and not bool(re.match(r"^\s*\d+\.\d+", b))
            if c!="other" and (main_heading or section=="other"):
                section=c
            if c!="other" and len(words(first))<=22:
                rows[section]["sections"].add(first)
            if re.match(r"(?i)^(fig(?:ure)?\.?|table)\s*\d+",b): continue
            n=len(words(b))
            if n>=20:
                rows[section]["words"]+=n; rows[section]["paragraphs"]+=1; prose.append(b)
    full="\n".join(all_text); body=re.split(r"(?im)^\s*(references|bibliography)\s*$",full)[0]
    text=" ".join(prose); paras=[len(words(x)) for x in prose] or [0]
    eq=len(set(re.findall(r"(?m)\((\d{1,3})\)\s*$",body)))
    figs=len(set(re.findall(r"(?im)^\s*(?:fig(?:ure)?\.?)\s*(\d+)",body)))
    tables=len(set(re.findall(r"(?im)^\s*table\s*(\d+)",body)))
    metric={"paper":paper,"words":len(words(body)),"paragraphs":len(prose),"mean_paragraph_words":statistics.mean(paras),"median_paragraph_words":statistics.median(paras),"display_equations":eq,"figures":figs,"tables":tables,**sentence_metrics(text),**theory_scores(body,eq,"ml" if paper in {"P1","P2"} else "opt")}
    srows=[]
    for c in CATEGORIES:
        d=rows[c]; srows.append({"paper":paper,"source":"comparator","category":c,"words":d["words"],"paragraphs":d["paragraphs"],"mean_paragraph_words":d["words"]/d["paragraphs"] if d["paragraphs"] else 0,"subsections":len(d["sections"])})
    term=Counter({x:body.lower().count(x) for x in TERMS})
    return metric,srows,body,term


def write_csv(path: Path, rows: list[dict]):
    if not rows:return
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def common_ngrams(text: str, n: int) -> Counter:
    stop = {"the","and","for","with","that","this","from","are","was","were","has","have","had","into","using","used","its","their","which","than","then","also","can","may","not","our","between","under","over","each","all","these","those","such","both","one","two","three","based","paper","study","where","same","more","shown","figure","number","data","model","output","current","overall","following","represents"}
    metadata = {"doi","https","org","creativecommons","licensed","license","editor","manuscript","appl","sci","authors","author","article","received","accepted","publication","volume"}
    toks=[x.lower() for x in words(text) if len(x)>=3]
    out=Counter()
    for i in range(len(toks)-n+1):
        gram=toks[i:i+n]
        if any(x in metadata for x in gram) or any(x in stop for x in gram): continue
        out[" ".join(gram)]+=1
    return out


def mean_rows(rows: list[dict], keys: list[str]) -> dict:
    return {k:statistics.mean(float(r[k]) for r in rows) for k in keys}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    selected=list(csv.DictReader(SELECTED.open(encoding="utf-8-sig")))
    latest=[]; comp=defaultdict(list); sec_latest=[]; sec_comp=defaultdict(list); term_latest={}; term_comp=defaultdict(list); latest_text={}; comp_text=defaultdict(list)
    for p,(slug,target,datasets,experiments,baselines,ablations,runs) in PAPERS.items():
        m,s,texts,terms=markdown(ROOT/"paper_projects"/slug/"manuscript"/"MANUSCRIPT.md",p)
        m.update(target=target,datasets=datasets,experiment_settings=experiments,baselines=baselines,ablations_or_controls=ablations,seeded_runs=runs)
        latest.append(m);sec_latest.extend(s);term_latest[p]=terms;latest_text[p]=texts["raw"]
    for row in selected:
        p=row["paper"]; path=ROOT/row["pdf"]
        m,s,body,terms=pdf(path,p);m.update(title=row["title"],target=row["target"]);comp[p].append(m);sec_comp[p].extend(s);term_comp[p].append(terms);comp_text[p].append(body)
    metric_keys=[k for k,v in latest[0].items() if isinstance(v,(int,float)) and k not in {"datasets","experiment_settings","baselines","ablations_or_controls","seeded_runs"}]
    comparisons=[]
    for m in latest:
        p=m["paper"]; avg=mean_rows(comp[p],metric_keys)
        row={"paper":p,"target":m["target"]}
        for k in metric_keys:
            row[f"manuscript_{k}"]=round(float(m[k]),4);row[f"comparator_mean_{k}"]=round(avg[k],4);row[f"ratio_{k}"]=round(float(m[k])/avg[k],4) if avg[k] else ""
        row.update({k:m[k] for k in ("datasets","experiment_settings","baselines","ablations_or_controls","seeded_runs")})
        comparisons.append(row)
    section_compare=[]
    for p in PAPERS:
        lm={r["category"]:r for r in sec_latest if r["paper"]==p}
        for cat in CATEGORIES:
            rs=[r for r in sec_comp[p] if r["category"]==cat]
            x=lm[cat]
            for key in ("words","paragraphs","mean_paragraph_words","subsections"):
                vals=[float(r[key]) for r in rs]; avg=statistics.mean(vals) if vals else 0
                x[f"comparator_mean_{key}"]=round(avg,3);x[f"ratio_{key}"]=round(float(x[key])/avg,3) if avg else ""
            section_compare.append(x)
    terminology=[]
    for p in PAPERS:
        for term in TERMS:
            vals=[c[term] for c in term_comp[p]]
            terminology.append({"paper":p,"term":term,"manuscript_count":term_latest[p][term],"comparator_mean_count":round(statistics.mean(vals),2),"comparator_document_frequency":sum(v>0 for v in vals),"n_comparators":len(vals)})
    style_phrases=[]
    for p in PAPERS:
        mlow=latest_text[p].lower()
        for phrase in STYLE_PHRASES:
            vals=[t.lower().count(phrase) for t in comp_text[p]]
            style_phrases.append({"paper":p,"phrase":phrase,"manuscript_count":mlow.count(phrase),"comparator_mean_count":round(statistics.mean(vals),2),"comparator_document_frequency":sum(v>0 for v in vals),"n_comparators":len(vals)})
    phrase_rows=[]
    for p in PAPERS:
        manuscript_grams={n:common_ngrams(latest_text[p],n) for n in (2,3)}
        comparator_grams={n:[common_ngrams(t,n) for t in comp_text[p]] for n in (2,3)}
        candidates=[]
        for n in (2,3):
            universe=set().union(*(set(c) for c in comparator_grams[n]))
            for phrase in universe:
                vals=[c[phrase] for c in comparator_grams[n]]; df=sum(v>0 for v in vals)
                if df>=5:
                    candidates.append((df,statistics.mean(vals),n,phrase,manuscript_grams[n][phrase]))
        for df,avg,n,phrase,mcount in sorted(candidates,reverse=True)[:40]:
            phrase_rows.append({"paper":p,"ngram_n":n,"phrase":phrase,"manuscript_count":mcount,"comparator_mean_count":round(avg,2),"comparator_document_frequency":df,"n_comparators":len(comp_text[p])})
    write_csv(OUT/"latest_manuscript_metrics.csv",latest)
    write_csv(OUT/"comparator_metrics_recomputed.csv",[r for rs in comp.values() for r in rs])
    write_csv(OUT/"paper_vs_10_average.csv",comparisons)
    write_csv(OUT/"section_comparison.csv",section_compare)
    write_csv(OUT/"terminology_comparison.csv",terminology)
    write_csv(OUT/"style_phrase_comparison.csv",style_phrases)
    write_csv(OUT/"common_phrase_comparison.csv",phrase_rows)
    (OUT/"methodology.json").write_text(json.dumps({"comparators_per_paper":{p:len(comp[p]) for p in PAPERS},"categories":CATEGORIES,"theory_score":"0-5 transparent token-coverage rubric plus equation-density bonus for mathematics; descriptive, not an acceptance probability","sentence_split":"rule-based English sentence segmentation","limitations":["PDF block segmentation differs from author paragraphs","equation count uses numbered PDF equations","dataset tokens undercount unnamed/proprietary datasets"]},indent=2),encoding="utf-8")
    print(OUT)


if __name__=="__main__":main()
