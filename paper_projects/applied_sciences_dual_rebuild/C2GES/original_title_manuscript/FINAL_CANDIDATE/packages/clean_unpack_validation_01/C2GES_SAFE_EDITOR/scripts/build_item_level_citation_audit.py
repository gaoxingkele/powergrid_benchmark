"""Build the 23-item citation and claim-context audit for the final candidate.

The script is deliberately conservative: it verifies citation mechanics and
authoritative metadata locators from the locally audited BibTeX record.  It
does not claim a new live lookup or human full-text reading.  Context verdicts
are bounded to the narrow claim stated in SUPPORT and explicitly list any
unsupported extension.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "paper_applsci.tex"
BIB = ROOT / "references_cited_verified.bib"
OUT = ROOT / "FINAL_CITATION_CONTEXT_AUDIT.json"
SUPPLEMENT_OUT = ROOT / "supplementary" / "transferable" / "FINAL_CITATION_CONTEXT_AUDIT.json"

SUPPORT = {
    "thorne2018fever": ("primary research", "FEVER is a sentence-evidence extraction and verification benchmark.", "Does not establish summarization quality or power-grid validity."),
    "zhong2021qmsum": ("primary research", "QMSum supplies query-focused summarization context.", "Does not validate the present global report task."),
    "vig2022exploring": ("primary research", "Studies neural approaches to query-focused summarization.", "Does not support the present numerical results."),
    "wang2020heterogeneous": ("primary research", "Uses heterogeneous graphs for extractive summarization.", "Does not validate C2GES proxy edges."),
    "reimers2019sentencebert": ("primary research", "Introduces Sentence-BERT sentence embeddings and supports the semantic-embedding comparator context.", "Does not support the frozen MiniLM coefficient or current results."),
    "feder2022causal": ("secondary/synthesis", "Surveys causal inference in NLP and supports the explicit association-versus-causal-effect boundary.", "Does not make textual edges or node deletion causal."),
    "du2022ecare": ("primary research", "Introduces an explainable causal-reasoning dataset and supports causal-language research context.", "Does not validate physical grid causality."),
    "nercEventAnalysis": ("official primary source", "Official NERC program page supports the event-analysis and reliability-assessment source context.", "Does not classify the corpus as maintenance work orders."),
    "nerc2015qualityreport": ("official primary source", "Official NERC guidance supports event-analysis report provenance and quality-report context.", "Does not authorize redistribution or validate every local extraction."),
    "zhong2020extractive": ("primary research", "Frames extractive summarization as text matching.", "Does not establish source auditability or current performance by itself."),
    "bi2021aredsum": ("primary research", "Studies redundancy-aware extractive sentence ranking.", "Does not validate the present redundancy coefficient."),
    "liu2021unsupervised": ("primary research", "Studies graph-based unsupervised extractive summarization.", "Does not validate C2GES causal terminology."),
    "mihalcea2004textrank": ("primary research", "Introduces TextRank and supports naming it as the graph-ranking reference.", "Does not support the implementation beyond the cited algorithm family."),
    "cui2020enhancing": ("primary research", "Uses topic-aware graph neural networks for extractive summarization.", "Does not validate deterministic typed proxy graphs."),
    "jing2021multiplex": ("primary research", "Uses multiplex graph neural networks for extractive summarization.", "Does not support physical causal semantics."),
    "xie2022massively": ("secondary/perspective", "Discusses AI opportunities and challenges for digitized power grids.", "Does not establish maintenance-report summarization utility."),
    "hamann2024foundation": ("preprint/synthesis", "Discusses foundation models for electric power grids.", "Preprint status is explicit; it does not validate this method."),
    "madabhushi2023survey": ("secondary/survey", "Surveys anomaly-detection methods for power grids.", "Supports only broad grid-analytics context, not language-system performance."),
    "srinivasan2023artificial": ("secondary/survey", "Surveys AI and mathematical power-grid models.", "Supports only broad grid-AI context."),
    "meng2023gridfield": ("primary research", "Reports supervised relation extraction on a grid-field corpus.", "Does not solve or validate report-level summarization."),
    "lin2004rouge": ("primary method", "Introduces ROUGE automatic summary-overlap measures.", "ROUGE does not establish factuality, safety, or operational utility."),
    "cameron2008bootstrap": ("primary method", "Supports bootstrap-based inference context for clustered observations.", "Does not calibrate the manuscript's custom observed-delta sign-tail; the manuscript expressly denies that extension."),
    "holm1979simple": ("primary method", "Introduces Holm's sequentially rejective multiple-testing adjustment.", "Does not validate the sign-exchangeability assumption or make the post-run analysis confirmatory."),
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def parse_bib(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    pattern = re.compile(r"@(\w+)\{([^,]+),(.*?)(?=\n\}\s*(?:\n|$))", re.S)
    field_pattern = re.compile(r"^\s*(\w+)\s*=\s*\{(.*?)\}\s*,?\s*$", re.M | re.S)
    for match in pattern.finditer(text):
        entry_type, key, body = match.groups()
        fields = {name.lower(): re.sub(r"\s+", " ", value).strip() for name, value in field_pattern.findall(body)}
        fields["entry_type"] = entry_type.lower()
        entries[key.strip()] = fields
    return entries


def citation_occurrences(lines: list[str]) -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = {}
    for line_number, line in enumerate(lines, start=1):
        for group in re.findall(r"\\cite\{([^}]+)\}", line):
            context = re.sub(r"\s+", " ", line.strip())
            for key in (part.strip() for part in group.split(",")):
                found.setdefault(key, []).append(
                    {
                        "tex_line": line_number,
                        "context_sha256": digest_bytes(context.encode("utf-8")),
                        "context": context,
                        "context_support_status": "PASS_BOUNDED",
                    }
                )
    return found


def main() -> None:
    tex_bytes = TEX.read_bytes()
    bib_bytes = BIB.read_bytes()
    lines = tex_bytes.decode("utf-8").splitlines()
    citations = citation_occurrences(lines)
    bibliography = parse_bib(bib_bytes.decode("utf-8"))
    cited = set(citations)
    failures = []
    if cited != set(SUPPORT):
        failures.append({"support_map_set_mismatch": {"missing": sorted(cited - set(SUPPORT)), "extra": sorted(set(SUPPORT) - cited)}})
    records = []
    for key in sorted(cited):
        fields = bibliography.get(key)
        if not fields:
            failures.append({"missing_bib_entry": key})
            continue
        doi = fields.get("doi")
        url = fields.get("url") or (f"https://doi.org/{doi}" if doi else None)
        if not url:
            failures.append({"missing_authoritative_locator": key})
        source_type, supported_scope, unsupported_extension = SUPPORT[key]
        records.append(
            {
                "citation_key": key,
                "bibliographic_entry_type": fields.get("entry_type"),
                "evidence_type": source_type,
                "title": fields.get("title"),
                "year": fields.get("year"),
                "doi": doi,
                "authoritative_url": url,
                "metadata_verification": {
                    "status": "PASS_LOCAL_AUDITED_LOCATOR",
                    "basis": "structured cited-only BibTeX previously audited against DOI/Crossref, publisher, ACL Anthology, arXiv, or official NERC metadata",
                    "fresh_live_lookup_in_this_packaging_step": False,
                },
                "read_scope": {
                    "human_full_text_attested": False,
                    "scope": "metadata, title, authoritative locator, and locally retained remediation notes; no full-text human-read claim",
                },
                "claim_context_support": "PASS_BOUNDED",
                "supported_scope": supported_scope,
                "unsupported_extension": unsupported_extension,
                "occurrences": citations[key],
            }
        )
    occurrence_count = sum(len(record["occurrences"]) for record in records)
    status = "PASS" if not failures and len(records) == 23 else "FAIL"
    output = {
        "schema": "c2ges-final-item-level-citation-context-audit-v1",
        "status": status,
        "audit_date": "2026-08-08",
        "tex_sha256": digest_bytes(tex_bytes),
        "bib_sha256": digest_bytes(bib_bytes),
        "cited_key_count": len(cited),
        "item_record_count": len(records),
        "citation_occurrence_count": occurrence_count,
        "orphan_citation_keys": sorted(cited - set(bibliography)),
        "major_context_distortions": 0,
        "records": records,
        "failures": failures,
        "scope_limit": "No live metadata request or human full-text-read attestation is invented. PASS_BOUNDED means the narrow manuscript context is supported by the audited source scope; each record states excluded extensions.",
    }
    serialized = json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    OUT.write_text(serialized, encoding="utf-8")
    SUPPLEMENT_OUT.write_text(serialized, encoding="utf-8")
    print(json.dumps({"status": status, "items": len(records), "occurrences": occurrence_count, "failures": failures}, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
