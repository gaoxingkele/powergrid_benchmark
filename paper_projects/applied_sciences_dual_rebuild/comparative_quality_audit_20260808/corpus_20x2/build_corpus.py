from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.request
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent
CANDIDATES = json.loads((ROOT / "crossref_candidates.json").read_text(encoding="utf-8"))
BY_DOI = {x["doi"].lower(): x for x in CANDIDATES}

C2 = [
    ("10.3390/app131911074", "direct-grid-text", "grid-field relation extraction"),
    ("10.3390/app12146993", "direct-grid-kg", "power-fault knowledge graph"),
    ("10.3390/app14209462", "direct-grid-kg", "line-loss knowledge-graph system"),
    ("10.3390/app15158188", "direct-grid-kg", "power-monitor alarm tracing with KG/GCNN"),
    ("10.3390/app14146189", "direct-grid-graph", "power cyber-physical attack-path graph"),
    ("10.3390/app16041985", "maintenance-kg-recent", "maintenance knowledge-graph construction"),
    ("10.3390/app14072946", "maintenance-llm", "maintenance multi-source text and LLM"),
    ("10.3390/app122412736", "maintenance-kg", "domain-specific maintenance knowledge graph"),
    ("10.3390/app15074034", "fault-text-llm", "LLM fault-information retrieval"),
    ("10.3390/app15126395", "extractive-graph-recent", "graph/LLM extractive summarization"),
    ("10.3390/app14114671", "extractive-hypergraph", "contextual hypergraph extractive summarization"),
    ("10.3390/app12094479", "extractive-semantic", "semantic extractive summarization"),
    ("10.3390/app13031458", "extractive-attention", "attentional extractive summarization"),
    ("10.3390/app122010382", "extractive-graph", "sentence-graph attention summarization"),
    ("10.3390/app12125854", "technical-report-summary", "bug-report extractive summarization"),
    ("10.3390/app14177548", "summarization-recent", "framing-aware text summarization"),
    ("10.3390/app13137753", "kg-summarization", "knowledge-graph-enhanced summarization"),
    ("10.3390/app14051880", "multi-document-summary", "topic-oriented multi-document summarization"),
    ("10.3390/app15042119", "relation-extraction-recent", "entity-relation extraction with MoE/dependency"),
    ("10.3390/app15137435", "cross-document-recent", "cross-document relation extraction"),
]

MA = [
    ("10.3390/app152011121", "direct-text-to-sql", "domain-specific Text-to-SQL"),
    ("10.3390/app142210359", "direct-text-to-sql", "relational-GNN Text-to-SQL"),
    ("10.3390/app15105306", "direct-text-to-sql", "zero-shot LLM Text-to-SQL prompting"),
    ("10.3390/app13042262", "direct-text-to-sql", "conversational Text-to-SQL dataset"),
    ("10.3390/app16020586", "direct-text-to-sql-recent", "schema retrieval and LLM SQL generation"),
    ("10.3390/app152111399", "sql-multi-model", "team of language models with SQL memory"),
    ("10.3390/app14177995", "database-qa", "RAG question answering over personalized databases"),
    ("10.3390/app15147647", "natural-language-retrieval", "LLM natural-language structured information retrieval"),
    ("10.3390/app122211830", "natural-language-interface", "natural-language data interface"),
    ("10.3390/app13085055", "structured-qa", "complex question answering over knowledge graphs"),
    ("10.3390/app16041896", "multi-agent-energy-recent", "multi-agent energy management with LLM reasoning"),
    ("10.3390/app15116079", "multi-agent-framework", "AI-driven multi-agent orchestration"),
    ("10.3390/app16136715", "llm-multi-agent-recent", "LLM multi-agent decision experiment"),
    ("10.3390/app16115453", "llm-multi-agent-recent", "generative-AI multi-agent architecture"),
    ("10.3390/app152312547", "agentic-rag", "knowledge graph and agentic RAG"),
    ("10.3390/app16136787", "multi-agent-framework-recent", "source-aware multi-agent framework"),
    ("10.3390/app16073122", "multi-agent-validation", "hybrid multi-agent detection system"),
    ("10.3390/app151910358", "power-multi-agent", "smart-microgrid multi-agent with real-time validation"),
    ("10.3390/app13052865", "power-multi-agent", "multi-microgrid multi-agent experimental study"),
    ("10.3390/app15020968", "industrial-multi-agent", "multi-agent industrial decision system"),
]


def slug_from_doi(doi: str) -> str:
    m = re.fullmatch(r"10\.3390/app(\d{2})(\d{2})(\d+)", doi)
    if not m:
        raise ValueError(doi)
    volume, _issue, article = m.groups()
    return f"applsci-{int(volume)}-{int(article):05d}"


def landing_url_from_doi(doi: str) -> str:
    m = re.fullmatch(r"10\.3390/app(\d{2})(\d{2})(\d+)", doi)
    if not m:
        raise ValueError(doi)
    volume, issue, article = m.groups()
    return f"https://www.mdpi.com/2076-3417/{int(volume)}/{int(issue)}/{int(article)}"


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size > 100:
        return
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 CodexResearch/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
    path.write_bytes(data)
    time.sleep(0.1)


def main() -> None:
    records = []
    seen = set()
    for corpus, selected in (("C2GES", C2), ("MA_SQLGrid", MA)):
        (ROOT / corpus / "xml").mkdir(parents=True, exist_ok=True)
        (ROOT / corpus / "pdf").mkdir(parents=True, exist_ok=True)
        for doi, category, reason in selected:
            if doi in seen:
                raise RuntimeError(f"duplicate across corpora: {doi}")
            seen.add(doi)
            meta = BY_DOI.get(doi)
            if not meta:
                raise RuntimeError(f"missing Crossref candidate: {doi}")
            slug = slug_from_doi(doi)
            base = f"https://mdpi-res.com/d_attachment/applsci/{slug}/article_deploy/{slug}"
            xml_path = ROOT / corpus / "xml" / f"{slug}.xml"
            pdf_path = ROOT / corpus / "pdf" / f"{slug}.pdf"
            download(base + ".xml", xml_path)
            download(base + ".pdf", pdf_path)
            tree = etree.parse(str(xml_path))
            root = tree.getroot()
            article_type = root.get("article-type", "")
            journal = " ".join(root.xpath(".//*[local-name()='journal-title'][1]//text()"))
            xml_doi = "".join(root.xpath(".//*[local-name()='article-id'][@pub-id-type='doi'][1]//text()")).strip().lower()
            if xml_doi != doi:
                raise RuntimeError(f"DOI mismatch {doi} != {xml_doi}")
            if "Applied Sciences" not in journal:
                raise RuntimeError(f"journal mismatch: {doi} {journal}")
            records.append({
                "corpus": corpus,
                "doi": doi,
                "slug": slug,
                "year": meta["year"],
                "title": meta["title"],
                "category": category,
                "selection_reason": reason,
                "article_type": article_type,
                "official_url": landing_url_from_doi(doi),
                "official_pdf_url": base + ".pdf",
                "official_xml_url": base + ".xml",
                "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest().upper(),
                "xml_sha256": hashlib.sha256(xml_path.read_bytes()).hexdigest().upper(),
                "pdf_bytes": pdf_path.stat().st_size,
                "xml_bytes": xml_path.stat().st_size,
            })
            print(corpus, doi, article_type, meta["title"])
    (ROOT / "corpus_manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"downloaded/verified={len(records)} unique={len(seen)}")


if __name__ == "__main__":
    main()
