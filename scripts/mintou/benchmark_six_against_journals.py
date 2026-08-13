"""Quantitative structure/experiment audit for the six Mintou manuscripts.

The script uses cached full-text PDFs only.  Counts are operational metrics, not claims
about editorial policy: PDF paragraphs are text blocks with >=20 words; equations are
display equations carrying a numeric label; figures/tables are unique caption numbers.
"""

from __future__ import annotations

import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "reviews" / "mintou_2026-08-10_comparative_benchmark"
SOURCE_CSV = ROOT / "reviews" / "mintou_2026-08-09_journal_fit_audit" / "comparator_pdf_statistics.csv"

PAPERS = {
    "P1": {
        "slug": "mintou_p1_dstar_gru_dispatch",
        "target": "IEEE Access",
        "priority_topics": ["p1_twin_gru_dispatch", "p2_hyperbolic_gcn_smart_dispatch", "p3_self_adaptive_mode_distribution_planning"],
        "datasets": 1, "experiment_settings": 4, "baselines": 6, "ablations": 5, "seeded_runs": 160,
        "baseline_freshness": 2.5, "innovation": 3.0,
    },
    "P2": {
        "slug": "mintou_p2_hygraph_load_forecasting",
        "target": "Electronics",
        "priority_topics": ["p2_hyperbolic_gcn_smart_dispatch", "p1_twin_gru_dispatch", "p4_resilience_distribution_planning"],
        "datasets": 3, "experiment_settings": 5, "baselines": 5, "ablations": 5, "seeded_runs": 420,
        "baseline_freshness": 4.0, "innovation": 2.5,
    },
    "P3": {
        "slug": "mintou_p3_samode_distribution_planning",
        "target": "Energies",
        "priority_topics": ["p3_self_adaptive_mode_distribution_planning", "p4_resilience_distribution_planning"],
        "datasets": 1, "experiment_settings": 7, "baselines": 6, "ablations": 4, "seeded_runs": 2310,
        "baseline_freshness": 3.0, "innovation": 3.0,
    },
    "P4": {
        "slug": "mintou_p4_shield_resilience_planning",
        "target": "Energies",
        "priority_topics": ["p4_resilience_distribution_planning", "p3_self_adaptive_mode_distribution_planning"],
        "datasets": 1, "experiment_settings": 8, "baselines": 5, "ablations": 4, "seeded_runs": 2400,
        "baseline_freshness": 2.5, "innovation": 3.5,
    },
    "P5": {
        "slug": "mintou_p5_trace_moea_feasibility_review",
        "target": "Energies",
        "priority_topics": ["p5_hybrid_moea_feasibility_review", "p6_nsga_bls_feasibility_review", "p4_resilience_distribution_planning"],
        "datasets": 3, "experiment_settings": 10, "baselines": 6, "ablations": 8, "seeded_runs": 3600,
        "baseline_freshness": 2.5, "innovation": 3.0,
    },
    "P6": {
        "slug": "mintou_p6_bilonsga_project_review",
        "target": "Applied Sciences",
        "priority_topics": ["p6_nsga_bls_feasibility_review", "p5_hybrid_moea_feasibility_review", "p4_resilience_distribution_planning", "p1_twin_gru_dispatch", "p2_hyperbolic_gcn_smart_dispatch"],
        "datasets": 3, "experiment_settings": 10, "baselines": 6, "ablations": 9, "seeded_runs": 3840,
        "baseline_freshness": 3.0, "innovation": 3.0,
    },
}

IEEE_EXT = [
    ("Short-Term Power Load Forecasting Based on VMD-Pyraformer-Adan", "2023", "10.1109/access.2023.3273596", "ieee_access_2023_vmd_pyraformer_adan.pdf"),
    ("Short Term Power Load Combination Forecasting Method Based on Feature Extraction", "2024", "10.1109/access.2024.3384246", "ieee_access_2024_feature_extraction_combination.pdf"),
    ("Enhancing Short-Term Power Load Forecasting With a TimesNet-Crossformer-LSTM Approach", "2024", "10.1109/access.2024.3383912", "ieee_access_2024_timesnet_crossformer_lstm.pdf"),
    ("Short-Term Power Load Forecasting Based on DE-IHHO Optimized BiLSTM", "2024", "10.1109/access.2024.3437247", "ieee_access_2024_de_ihho_bilstm.pdf"),
    ("The Power Load Forecasting Model of Combined SaDE-ELM and FA-CAWOA-SVM Based on CSSA", "2024", "10.1109/access.2024.3377097", "ieee_access_2024_sade_elm_cawoa_svm.pdf"),
    ("Communication-Efficient Federated Learning for Power Load Forecasting in Electric IoTs", "2023", "10.1109/access.2023.3262171", "ieee_access_2023_federated_load_forecasting.pdf"),
    ("Short-Term Load Forecasting for Electrical Power Distribution Systems Using Enhanced Deep Neural Networks", "2024", "10.1109/access.2024.3432647", "ieee_access_2024_enhanced_dnn_distribution.pdf"),
]

METHOD_TOKENS = [
    "persistence", "ridge", "svm", "lssvm", "elm", "mlp", "cnn", "lstm", "bilstm", "gru", "bigru", "tcn",
    "transformer", "informer", "autoformer", "fedformer", "patchtst", "dlinear", "timesnet", "crossformer", "xgboost",
    "lightgbm", "random forest", "nsga-ii", "nsga-iii", "moea/d", "spea2", "differential evolution", "particle swarm",
    "genetic algorithm", "grey wolf", "whale optimization", "benders", "milp", "ahp", "topsis", "weighted sum",
]
RECENT_METHODS = ["patchtst", "timesnet", "crossformer", "dlinear", "fedformer", "autoformer", "nsga-iii"]
DATASETS = ["opsd", "simbench", "ausgrid", "rts-gmlc", "ieee 14", "ieee 30", "ieee 33", "ieee 39", "ieee 57", "ieee 118", "matpower", "miso", "nerc", "pjm", "entso-e"]


def words(text: str) -> list[str]:
    return re.findall(r"\b[A-Za-z][A-Za-z0-9'’-]*\b", text)


def category(title: str) -> str:
    value = title.lower()
    if any(x in value for x in ("reference", "author contribution", "funding", "data availability", "conflict")):
        return "back_matter"
    if "abstract" in value or "introduction" in value:
        return "introduction"
    if any(x in value for x in ("related", "literature", "background")):
        return "related_work"
    if any(x in value for x in ("data", "problem", "formulation", "model", "method", "framework", "algorithm")):
        return "method_data"
    if any(x in value for x in ("experiment", "case stud", "simulation", "setup", "scenario")):
        return "experimental_setup"
    if any(x in value for x in ("result", "validation", "ablation", "sensitivity", "analysis")):
        return "results"
    if any(x in value for x in ("discussion", "limitation", "implication")):
        return "discussion"
    if "conclusion" in value:
        return "conclusion"
    return "other"


def markdown_metrics(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body = re.split(r"(?m)^##\s+References\s*$", text)[0]
    blocks = re.split(r"\n\s*\n", body)
    paras, current = [], "other"
    cat_words = Counter()
    for block in blocks:
        clean = block.strip()
        if not clean or clean.startswith("<!--"):
            continue
        heading = re.match(r"^#{1,6}\s+(.+)", clean)
        if heading:
            new_category = category(heading.group(1))
            if new_category != "other":
                current = new_category
            continue
        if clean.startswith("|") or clean.startswith("![") or clean.startswith("```") or re.match(r"^[-*]\s", clean):
            continue
        n = len(words(re.sub(r"\$.*?\$", " ", clean)))
        if n >= 15:
            paras.append(n)
            cat_words[current] += n
    figure_nums = set(re.findall(r"(?i)(?:figure|fig\.)\s*(\d+)", body))
    table_nums = set(re.findall(r"(?i)table\s*(\d+)", body))
    display_eq = len(re.findall(r"(?s)\$\$.*?\$\$|\\\[.*?\\\]", body))
    inline_math = len(re.findall(r"(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)", body, re.S))
    fig_files = []
    evidence_root = ROOT / "papers" / "mintou" / path.parents[1].name
    if evidence_root.exists():
        fig_files = [p for p in evidence_root.rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".pdf"}]
    dimensions = []
    raster_sizes = []
    for fig in fig_files:
        if fig.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            try:
                with Image.open(fig) as im:
                    dimensions.append(f"{im.width}x{im.height}")
                    raster_sizes.append((im.width, im.height))
            except Exception:
                pass
    total_cat = sum(cat_words.values()) or 1
    has_script = (evidence_root / "manuscript" / "figures" / "make_figures.py").exists()
    coverage = len(fig_files) / max(1, len(figure_nums))
    figure_quality = 0
    figure_quality += 1 if fig_files else 0
    figure_quality += 1 if coverage >= 1 else 0
    figure_quality += 1 if raster_sizes and min(min(x) for x in raster_sizes) >= 800 else 0
    figure_quality += 1 if has_script else 0
    figure_quality += 1 if any(p.suffix.lower() in {".svg", ".pdf"} for p in fig_files) else 0
    out = {
        "words": len(words(body)), "paragraphs": len(paras), "median_paragraph_words": statistics.median(paras) if paras else 0,
        "display_equations": display_eq, "inline_math_spans": inline_math, "figures_cited": len(figure_nums),
        "figure_files": len(fig_files), "figure_dimensions": ";".join(dimensions), "figure_quality_proxy_5": figure_quality,
        "figure_file_coverage": round(coverage, 3), "tables": len(table_nums),
    }
    out.update({f"share_{k}": round(v / total_cat, 4) for k, v in cat_words.items()})
    return out


def pdf_metrics(path: Path) -> dict:
    doc = fitz.open(path)
    blocks, all_text, captions = [], [], []
    image_dpis, figure_pages_with_vector = [], 0
    current = "other"
    cat_words = Counter()
    stopped = False
    for page in doc:
        page_text = page.get_text("text", sort=True)
        all_text.append(page_text)
        if re.search(r"(?im)^\s*(references|bibliography)\s*$", page_text):
            before = re.split(r"(?im)^\s*(references|bibliography)\s*$", page_text)[0]
        else:
            before = page_text
        page_has_caption = bool(re.search(r"(?im)^\s*(?:fig(?:ure)?\.?|table)\s*\d+", before))
        if page_has_caption and len(page.get_drawings()) >= 8:
            figure_pages_with_vector += 1
        for info in page.get_image_info(xrefs=True):
            bbox = fitz.Rect(info["bbox"])
            if bbox.width > 20 and bbox.height > 20:
                dpi_x = info["width"] / (bbox.width / 72)
                dpi_y = info["height"] / (bbox.height / 72)
                image_dpis.append(min(dpi_x, dpi_y))
        for b in page.get_text("blocks", sort=True):
            raw_text = b[4].strip()
            first_line = raw_text.splitlines()[0].strip() if raw_text else ""
            first_category = category(first_line)
            if first_category != "other" and len(words(first_line)) <= 16:
                current = first_category
                raw_text = "\n".join(raw_text.splitlines()[1:])
            text = re.sub(r"\s+", " ", raw_text).strip()
            if not text:
                continue
            if re.match(r"(?i)^(references|bibliography)\b", text):
                stopped = True
            if stopped:
                continue
            if len(words(text)) <= 14 and (re.match(r"^(?:\d+(?:\.\d+)*\.?|[IVX]+\.)\s+", text) or category(text) != "other"):
                new_category = category(text)
                if new_category != "other":
                    current = new_category
                continue
            if re.match(r"(?i)^(fig(?:ure)?\.?|table)\s*\d+", text):
                captions.append(text)
                continue
            n = len(words(text))
            if n >= 20:
                blocks.append(n)
                cat_words[current] += n
    text = "\n".join(all_text)
    main = re.split(r"(?im)^\s*(references|bibliography)\s*$", text)[0]
    figures = set(re.findall(r"(?im)^\s*(?:fig(?:ure)?\.?)\s*(\d+)", main))
    tables = set(re.findall(r"(?im)^\s*table\s*(\d+)", main))
    equations = set(re.findall(r"(?m)\((\d{1,3})\)\s*$", main))
    lower = main.lower()
    methods = sorted({token for token in METHOD_TOKENS if token in lower})
    recent = sorted({token for token in RECENT_METHODS if token in lower})
    datasets = sorted({token for token in DATASETS if token in lower})
    exp_heads = len(re.findall(r"(?im)^\s*(?:\d+(?:\.\d+)*\.?|[IVX]+\.)?\s*(?:experimental|experiments|case stud|simulation|results|validation|sensitivity|ablation)\b", main))
    total_cat = sum(cat_words.values()) or 1
    med_dpi = statistics.median(image_dpis) if image_dpis else 0
    low_dpi = sum(1 for x in image_dpis if x < 120)
    quality = 0
    quality += 1 if len(figures) >= 3 else 0
    quality += 1 if med_dpi >= 180 else 0
    quality += 1 if image_dpis and low_dpi == 0 else 0
    quality += 1 if figure_pages_with_vector >= max(1, len(figures) // 3) else 0
    quality += 1 if len(captions) >= max(1, len(figures) // 2) else 0
    if len(methods) <= 1:
        freshness = 1.0
    elif len(methods) <= 3:
        freshness = 2.0
    elif len(methods) < 7:
        freshness = 3.0
    else:
        freshness = 3.5
    freshness += min(1.5, 0.75 * len(recent))
    freshness = min(5.0, freshness)
    title_text = doc.metadata.get("title", "").lower()
    if any(x in title_text for x in ("review", "overview", "survey")):
        innovation = 1.5
    elif any(x in title_text for x in ("framework", "federated", "benders", "wasserstein", "scenario", "two-stage", "multi-stage", "two-tier")):
        innovation = 3.5
    elif any(x in title_text for x in ("novel", "enhanced", "improved", "hybrid", "attention", "combination")):
        innovation = 3.0
    else:
        innovation = 2.5
    out = {
        "pages": len(doc), "words": len(words(main)), "paragraphs": len(blocks), "median_paragraph_words": statistics.median(blocks) if blocks else 0,
        "display_equations": len(equations), "figures": len(figures), "tables": len(tables), "embedded_images": len(image_dpis),
        "median_raster_dpi": round(med_dpi, 1), "low_dpi_images": low_dpi, "vector_figure_pages": figure_pages_with_vector,
        "figure_quality_proxy_5": quality, "experimental_subsections": exp_heads, "method_family_count": len(methods),
        "recent_method_count": len(recent), "dataset_token_count": len(datasets), "methods": ";".join(methods), "datasets": ";".join(datasets),
        "baseline_freshness_proxy_5": freshness, "innovation_title_proxy_5": innovation,
    }
    out.update({f"share_{k}": round(v / total_cat, 4) for k, v in cat_words.items()})
    return out


def load_pool() -> list[dict]:
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        row["path"] = ROOT / row.pop("pdf_path")
        row["key"] = (row.get("doi") or row["title"]).lower()
    ext_dir = ROOT / "papers" / "literature" / "target_journal_related" / "pdfs" / "p1_ieee_access_extension"
    for title, year, doi, name in IEEE_EXT:
        rows.append({"paper_id": name.removesuffix(".pdf"), "title": title, "topic_id": "p1_ieee_access_extension", "journal": "IEEE Access",
                     "publication_date": year, "doi": doi, "path": ext_dir / name, "key": doi.lower(), "pages": ""})
    return rows


def select_samples(pool: list[dict]) -> dict[str, list[dict]]:
    selected = {}
    for pid, cfg in PAPERS.items():
        candidates = [x for x in pool if x["journal"] == cfg["target"] and x["path"].exists()
                      and not re.search(r"(?i)\b(review|overview|survey)\b", x["title"])
                      and (not str(x.get("pages", "")).isdigit() or int(x["pages"]) >= 8)]
        topic_rank = {topic: i for i, topic in enumerate(cfg["priority_topics"])}
        candidates.sort(key=lambda x: (topic_rank.get(x.get("topic_id"), 99), -(int(str(x.get("publication_date", "0"))[:4] or 0))))
        chosen, keys = [], set()
        for row in candidates:
            title_key = re.sub(r"\W+", "", row["title"].lower())
            if row["key"] in keys or title_key in keys:
                continue
            chosen.append(row)
            keys.update((row["key"], title_key))
            if len(chosen) == 10:
                break
        if len(chosen) < 10:
            raise RuntimeError(f"{pid}: only {len(chosen)} unique cached PDFs for {cfg['target']}")
        selected[pid] = chosen
    return selected


def mean(rows: list[dict], field: str) -> float:
    vals = [float(r.get(field, 0) or 0) for r in rows]
    return sum(vals) / len(vals)


def write_csv(path: Path, rows: list[dict]) -> None:
    keys = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    pool = load_pool(); samples = select_samples(pool)
    comparator_rows, sample_rows, manuscript_rows, summary_rows = [], [], [], []
    cache = {}
    for pid, chosen in samples.items():
        for row in chosen:
            key = str(row["path"].resolve())
            if key not in cache:
                cache[key] = pdf_metrics(row["path"])
            metrics = cache[key]
            comparator_rows.append({"paper": pid, "target": PAPERS[pid]["target"], "title": row["title"], "date": row.get("publication_date", ""),
                                    "doi": row.get("doi", ""), "pdf": str(row["path"].relative_to(ROOT)), **metrics})
            sample_rows.append({"paper": pid, "target": PAPERS[pid]["target"], "title": row["title"], "date": row.get("publication_date", ""),
                                "doi": row.get("doi", ""), "pdf": str(row["path"].relative_to(ROOT))})
    by_paper = defaultdict(list)
    for row in comparator_rows:
        by_paper[row["paper"]].append(row)
    fields = ["words", "paragraphs", "median_paragraph_words", "display_equations", "figures", "tables", "figure_quality_proxy_5",
              "experimental_subsections", "method_family_count", "recent_method_count", "dataset_token_count",
              "baseline_freshness_proxy_5", "innovation_title_proxy_5",
              "share_introduction", "share_related_work", "share_method_data", "share_experimental_setup", "share_results", "share_discussion", "share_conclusion"]
    for pid, cfg in PAPERS.items():
        mpath = ROOT / "paper_projects" / cfg["slug"] / "manuscript" / "MANUSCRIPT.md"
        mm = markdown_metrics(mpath)
        manuscript = {"paper": pid, "slug": cfg["slug"], "target": cfg["target"], **mm,
                      "datasets": cfg["datasets"], "experiment_settings": cfg["experiment_settings"], "baselines": cfg["baselines"],
                      "ablations": cfg["ablations"], "seeded_runs": cfg["seeded_runs"], "baseline_freshness_5": cfg["baseline_freshness"],
                      "innovation_5": cfg["innovation"]}
        manuscript_rows.append(manuscript)
        summary = {"paper": pid, "target": cfg["target"], "comparator_n": len(by_paper[pid])}
        for field in fields:
            summary[f"manuscript_{field}"] = manuscript.get(field, 0)
            summary[f"comparator_mean_{field}"] = round(mean(by_paper[pid], field), 2)
        summary["manuscript_figures"] = manuscript["figures_cited"]
        summary["manuscript_actual_figure_files"] = manuscript["figure_files"]
        summary["manuscript_experimental_subsections"] = manuscript["experiment_settings"]
        summary["manuscript_method_family_count"] = manuscript["baselines"]
        summary["manuscript_dataset_token_count"] = manuscript["datasets"]
        summary["manuscript_baseline_freshness_proxy_5"] = manuscript["baseline_freshness_5"]
        summary["manuscript_innovation_title_proxy_5"] = manuscript["innovation_5"]
        summary_rows.append(summary)
    write_csv(AUDIT / "selected_comparators.csv", sample_rows)
    write_csv(AUDIT / "comparator_metrics.csv", comparator_rows)
    write_csv(AUDIT / "manuscript_metrics.csv", manuscript_rows)
    write_csv(AUDIT / "comparison_summary.csv", summary_rows)
    (AUDIT / "methodology.json").write_text(json.dumps({
        "sample_rule": "10 unique cached full-text papers per manuscript from its target journal; topic-priority ordering, then adjacent power-grid/method papers",
        "paragraph": "PDF text block with >=20 English-word tokens before References; manuscript prose block with >=15 tokens, excluding headings/tables/lists",
        "equation": "numbered display equation in PDFs; $$ or \\[ display blocks in Markdown",
        "figure_table": "unique numbered captions/references",
        "figure_quality_proxy": "0-5 production proxy based on caption count, raster DPI and vector content; not a semantic-aesthetic score",
        "caveat": "PDF extraction can merge or split paragraphs and can miss unnumbered equations or vector-only panels",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary_rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
