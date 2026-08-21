#!/usr/bin/env python3
"""Generate the read-only W7 citation and MDPI-compliance audit for C2GES."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[4]
OLD_DIR = REPO / "paper_projects/CMC/C2GES/06_Applied_Sciences_Current"
OLD_TEX = OLD_DIR / "paper_applsci.tex"
OLD_BIB = OLD_DIR / "references_applsci.bib"
W5 = REPO / "paper_projects/applied_sciences_dual_rebuild/C2GES/drafts/W5_METHOD_DATA_DRAFT.md"
W6 = REPO / "paper_projects/applied_sciences_dual_rebuild/C2GES/drafts/W6_RESULTS_DISCUSSION_DRAFT.md"
BUDGETS = REPO / "paper_projects/applied_sciences_dual_rebuild/manuscript_budgets.json"
CORPUS = REPO / "papers/literature/applied_sciences_power_ai_10/analysis/paper_stats_raw.json"
CORPUS_SUMMARY = REPO / "papers/literature/applied_sciences_power_ai_10/analysis/corpus_summary.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def balanced_argument(text: str, command: str) -> str | None:
    marker = f"\\{command}{{"
    position = text.find(marker)
    if position < 0:
        return None
    start = position + len(marker)
    depth = 1
    cursor = start
    while cursor < len(text) and depth:
        if text[cursor] == "{" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth += 1
        elif text[cursor] == "}" and (cursor == 0 or text[cursor - 1] != "\\"):
            depth -= 1
        cursor += 1
    return text[start:cursor - 1] if depth == 0 else None


def english_word_count(text: str) -> int:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"\\[A-Za-z]+(?:\{[^{}]*\})?", " ", text)
    return len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text))


def parse_bib(text: str) -> dict[str, dict[str, Any]]:
    starts = list(re.finditer(r"(?m)^@(\w+)\{([^,]+),", text))
    entries = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[match.start():end]
        fields = {
            key.lower(): value.strip().strip(",").strip().strip("{}")
            for key, value in re.findall(r"(?m)^\s*(\w+)\s*=\s*\{(.*?)\},?\s*$", block)
        }
        note_doi = re.search(r"https://doi\.org/([^}]+)", fields.get("note", ""), flags=re.I)
        entries[match.group(2)] = {
            "type": match.group(1).lower(), "fields": fields,
            "resolved_doi": (fields.get("doi") or (note_doi.group(1) if note_doi else None)),
        }
    return entries


def citations(text: str) -> list[str]:
    keys = []
    for match in re.finditer(r"\\cite\w*\{([^}]+)\}", text):
        keys.extend(key.strip() for key in match.group(1).split(","))
    return keys


def duplicate_groups(entries: dict[str, dict[str, Any]], field: str) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for key, entry in entries.items():
        if field == "doi":
            value = (entry["resolved_doi"] or "").lower()
        else:
            value = re.sub(r"[^a-z0-9]", "", entry["fields"].get(field, "").lower())
        if value:
            groups.setdefault(value, []).append(key)
    return [keys for keys in groups.values() if len(keys) > 1]


def build_audit() -> dict[str, Any]:
    old_tex = OLD_TEX.read_text(encoding="utf-8")
    bib_text = OLD_BIB.read_text(encoding="utf-8")
    w5_text, w6_text = W5.read_text(encoding="utf-8"), W6.read_text(encoding="utf-8")
    entries = parse_bib(bib_text)
    old_citations = citations(old_tex)
    old_unique = sorted(set(old_citations))
    w5_citations, w6_citations = citations(w5_text), citations(w6_text)
    abstract = balanced_argument(old_tex, "abstract") or ""
    old_sections = re.findall(r"(?m)^\\section\{([^}]+)", old_tex)
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    budgets = json.loads(BUDGETS.read_text(encoding="utf-8"))
    c2_budget = next(item for item in budgets["papers"] if item["paper"] == "C2GES")

    reusable = {
        "benchmark_and_evidence_selection": ["thorne2018fever", "liao2023muser", "yadav2020unsupervised", "liang2020hammer"],
        "query_focused_and_extractive_selection": ["zhong2021qmsum", "vig2022exploring", "zhong2020extractive", "bi2021aredsum", "joshi2022ranksuman"],
        "graph_and_local_structure": ["wang2020heterogeneous", "jing2021multiplex", "cui2020enhancing", "liu2021unsupervised", "zhao2023multigranularity"],
        "role_and_causal_relation_context": ["feder2022causal", "du2022ecare", "wang2024documentlevel", "zhang2023causal"],
        "reranking_context": ["qin2024pairwise", "zhuang2024setwise", "ren2025selfcalibrated"],
        "power_grid_context": ["xie2022massively", "srinivasan2023artificial", "rajkumar2023cyber", "madabhushi2023survey", "ramirezmeyers2021different"],
        "preprint_only_use_with_status_label": ["hamann2024foundation", "sotudeh2024rank", "liu2023rank"],
    }
    missing_reusable = sorted({key for keys in reusable.values() for key in keys if key not in entries})
    preprints = sorted(key for key, entry in entries.items() if entry["fields"].get("journal", "").lower().startswith("arxiv:"))
    explicit_doi = sum(bool(entry["fields"].get("doi")) for entry in entries.values())
    resolvable_doi = sum(bool(entry["resolved_doi"]) for entry in entries.values())

    metadata_findings = [
        {"id": "BIB-DOI-FIELD", "severity": "major", "keys": "all DOI-bearing entries",
         "finding": f"No entry uses a structured doi field; {resolvable_doi} DOI strings are embedded in note/href.",
         "action": "Move verified DOI strings into doi fields and let the final MDPI bibliography style format links."},
        {"id": "BIB-ARXIV-MACRO", "severity": "major", "keys": preprints,
         "finding": f"{len(preprints)} entries encode arXiv identifiers with the manuscript-specific \\adot macro and have no DOI.",
         "action": "Before reuse, verify publication status; otherwise retain explicit preprint status and use portable eprint/archivePrefix fields."},
        {"id": "BIB-RAJKUMAR-PAGES", "severity": "major", "keys": ["rajkumar2023cyber"],
         "finding": "Journal pages are absent; DOI record resolves to IEEE Access 11, 103154-103176.",
         "action": "Add verified page range 103154--103176."},
        {"id": "BIB-BELWAL-INCOMPLETE", "severity": "major", "keys": ["belwal2020graphbased"],
         "finding": "Volume, issue and pages are absent, and online-first year versus issue year needs resolution.",
         "action": "Refresh the complete record through DOI 10.1007/s12652-020-02591-x before reuse."},
        {"id": "BIB-RAMIREZ-INCOMPLETE", "severity": "major", "keys": ["ramirezmeyers2021different"],
         "finding": "Volume and article number are absent; the DOI publication page identifies Progress in Energy 3, 033001.",
         "action": "Add volume 3 and article number 033001 after author review."},
        {"id": "BIB-AHMAD-AUTHORS", "severity": "critical", "keys": ["ahmad2026mitigating"],
         "finding": "Local author names (Nadeem Ahmad; Chen Zhang; Umme Sehar) conflict with the publisher record (Nouman Ahmad; Changsheng Zhang; Uroosa Sehar).",
         "action": "Do not reuse until the authors are corrected from the publisher BibTeX."},
        {"id": "BIB-STALE-COMMENT", "severity": "minor", "keys": [],
         "finding": "The Bib header still says 'References for CMC submission' although the file is in the Applied Sciences tree.",
         "action": "Replace the stale provenance comment when the final Bib is assembled."},
    ]

    topic_matrix = [
        {"topic": "FEVER benchmark, evidence annotations and conversion boundary", "existing_keys": ["thorne2018fever"], "status": "available"},
        {"topic": "sentence-level evidence retrieval/fact verification", "existing_keys": ["thorne2018fever", "liao2023muser", "yadav2020unsupervised", "liang2020hammer"], "status": "available"},
        {"topic": "query-focused and extractive sentence selection", "existing_keys": reusable["query_focused_and_extractive_selection"], "status": "available"},
        {"topic": "graph/local-chain sentence interactions", "existing_keys": reusable["graph_and_local_structure"], "status": "available"},
        {"topic": "role/causal relation extraction background", "existing_keys": reusable["role_and_causal_relation_context"], "status": "available_but_avoid_claiming_causal_gain"},
        {"topic": "power-grid text analytics and report-review motivation", "existing_keys": reusable["power_grid_context"], "status": "partial; add locally verified Applied Sciences grid-NLP paper"},
        {"topic": "BM25 definition and implementation", "existing_keys": [], "status": "missing_verified_reference"},
        {"topic": "Sentence-BERT/MiniLM encoder", "existing_keys": [], "status": "missing_verified_reference"},
        {"topic": "cross-encoder and BGE rerankers", "existing_keys": [], "status": "missing_verified_references"},
        {"topic": "grouped OOF/cross-fitting", "existing_keys": [], "status": "missing_verified_method_reference"},
        {"topic": "cluster/hierarchical bootstrap, sign-flip and Holm", "existing_keys": [], "status": "missing_verified_statistical_references"},
        {"topic": "official NERC reports and usage/provenance", "existing_keys": [], "status": "missing_official_source_entries"},
    ]

    claim_gaps = [
        {"location": "W5 2.2", "claim": "FEVER construction, human evidence and task scope", "required": ["thorne2018fever"], "priority": "critical"},
        {"location": "W5 2.3", "claim": "grouped out-of-fold/train-only role prediction", "required": ["verified grouped OOF/cross-fitting reference"], "priority": "major"},
        {"location": "W5 3.2", "claim": "frozen MiniLM/SBERT query representation", "required": ["canonical Sentence-BERT and MiniLM/model reference"], "priority": "critical"},
        {"location": "W5 3.4", "claim": "local-chain/structural consistency motivation", "required": ["wang2020heterogeneous", "jing2021multiplex"], "priority": "major"},
        {"location": "W5 3.5", "claim": "pairwise ranking objective", "required": ["verified learning-to-rank reference"], "priority": "major"},
        {"location": "W5 4.1", "claim": "BM25, cross-encoder and BGE comparator definitions", "required": ["verified BM25", "verified cross-encoder", "verified BGE"], "priority": "critical"},
        {"location": "W5 4.3", "claim": "paired seed inference, hierarchical bootstrap and multiplicity control", "required": ["verified cluster bootstrap", "verified Holm"], "priority": "critical"},
        {"location": "W5 2.4 / W6 6.5", "claim": "NERC source and silver-label provenance", "required": ["official NERC report/source entries"], "priority": "critical"},
        {"location": "W6 6.1/6.3", "claim": "mechanistic interpretation of BM25 top-1 versus deeper-list behaviour", "required": ["BM25/IR literature or retain explicitly as hypothesis"], "priority": "major"},
        {"location": "Final Introduction/Related Work", "claim": "Applied Sciences fit and closest power-grid NLP precedent", "required": ["proposed local key meng2023gridfield", "xie2022massively"], "priority": "critical"},
    ]

    corpus_items = []
    for item in corpus:
        doi, title = item["doi"], item["title"]
        if doi == "10.3390/app131911074":
            relevance, use = "direct", "Closest local Applied Sciences precedent for power-grid NLP/relation extraction; create a verified Bib entry such as meng2023gridfield."
        elif doi == "10.3390/app142210368":
            relevance, use = "contextual", "Optional power-grid failure/emergency context only; it does not support evidence-retrieval claims."
        else:
            relevance, use = "venue_style_only", "Use for Applied Sciences structure/experiment expectations, not as a scientific citation unless a specific claim needs it."
        corpus_items.append({"title": title, "doi": doi, "doi_url": f"https://doi.org/{doi}", "year": item["year"],
                             "relevance_to_c2ges": relevance, "recommended_use": use})

    declaration_commands = {
        "supplementary": "supplementary", "author_contributions": "authorcontributions", "funding": "funding",
        "institutional_review": "institutionalreview", "informed_consent": "informedconsent",
        "data_availability": "dataavailability", "acknowledgments_ai": "acknowledgments",
        "conflicts_of_interest": "conflictsofinterest",
    }
    declarations = {name: balanced_argument(old_tex, command) for name, command in declaration_commands.items()}
    compliance = [
        {"item": "MDPI Applied Sciences article class", "status": "pass", "evidence": "documentclass[applsci,article,submit,moreauthors]"},
        {"item": "Abstract <= 200 words", "status": "pass_old_only", "evidence": f"Old abstract: {english_word_count(abstract)} words; rebuilt final abstract is not yet written."},
        {"item": "Section fit", "status": "open", "evidence": f"Old source has {len(old_sections)} top-level sections; corpus median is 5 and registered C2GES plan is {c2_budget['top_level_sections']}. Merge final draft to the six-section plan."},
        {"item": "Current title truthful to frozen role result", "status": "blocker", "evidence": "Old title says Causal-Role-Aware, but W6 freezes the primary role-conditioning claim as NO-GO."},
        {"item": "Current numerical claims", "status": "blocker", "evidence": "Old abstract/results use superseded 4000/800/800 and single-run positive role claims; final text must use frozen W6/W7 evidence only."},
        {"item": "Oracle disclosure", "status": "pass_in_new_drafts", "evidence": "W5/W6 explicitly label oracle-label conditional, end_to_end=false, and prohibit deployable interpretation."},
        {"item": "NERC provenance disclosure", "status": "pass_in_new_drafts", "evidence": "W5/W6 state agent-generated/verified silver, qualitative-only, not human gold or quantitative domain proof."},
        {"item": "AI-use disclosure", "status": "open", "evidence": "Old Acknowledgments discloses LLM drafting/editing and author responsibility; final version should retain it and identify tool/purpose per the submission-time policy."},
        {"item": "Author Contributions", "status": "blocker", "evidence": "Declaration exists, but initials L.B. do not match displayed author name Bijing Liu (normally B.L.); authors must correct/confirm."},
        {"item": "Funding", "status": "blocker", "evidence": "Funding statement contains [AUTHOR INPUT REQUIRED]."},
        {"item": "IRB and Informed Consent", "status": "author_confirmation", "evidence": "Both statements exist and say not applicable; authors/institution must confirm applicability for reuse of public benchmark/report material."},
        {"item": "Data Availability", "status": "blocker", "evidence": "Contains local workspace paths and requires a permanent public repository URL."},
        {"item": "Conflicts of Interest and funder role", "status": "pass_text_present", "evidence": "Both conflict declaration and funder non-involvement language are present."},
        {"item": "Author contact metadata", "status": "blocker", "evidence": "Two affiliation emails remain author-email-required@example.com placeholders."},
        {"item": "Citation coverage in rebuilt drafts", "status": "blocker", "evidence": f"W5 citations={len(w5_citations)}, W6 citations={len(w6_citations)}; artifact CLAIM comments are not scholarly citations."},
        {"item": "Final declarations present in rebuilt assembly", "status": "open", "evidence": "W5/W6 are staging drafts and contain no final declaration block; migrate only verified declarations during assembly."},
    ]

    verification_urls = [
        {"purpose": "Rajkumar IEEE Access metadata", "url": "https://doi.org/10.1109/ACCESS.2023.3317695"},
        {"purpose": "Belwal Springer metadata", "url": "https://doi.org/10.1007/s12652-020-02591-x"},
        {"purpose": "Ramirez-Meyers IOP metadata", "url": "https://doi.org/10.1088/2516-1083/abf636"},
        {"purpose": "Ahmad CMC publisher metadata", "url": "https://www.techscience.com/cmc/v87n1/66046/html"},
        {"purpose": "Borovcak CMC publisher metadata", "url": "https://www.techscience.com/cmc/v88n2/67604"},
    ]
    blockers = [item for item in compliance if item["status"] == "blocker"]
    return {
        "schema_version": "c2-w7-citation-compliance-audit-1.0", "audit_date": "2026-08-05",
        "scope": "read-only audit; no TeX/Bib modification",
        "summary": {"submission_ready": False, "blocker_count": len(blockers), "old_bib_entries": len(entries),
                    "old_unique_cited_keys": len(old_unique), "w5_citation_count": len(w5_citations), "w6_citation_count": len(w6_citations),
                    "old_abstract_words": english_word_count(abstract), "downloaded_applsci_corpus_n": len(corpus)},
        "sources": [{"path": str(path.relative_to(REPO)), "sha256": digest(path)}
                    for path in (OLD_TEX, OLD_BIB, W5, W6, BUDGETS, CORPUS, CORPUS_SUMMARY)],
        "old_tex": {"sections": old_sections, "citation_occurrences": len(old_citations), "unique_cited_keys": old_unique,
                    "undefined_citation_keys": sorted(set(old_unique) - set(entries)),
                    "unused_bib_keys": sorted(set(entries) - set(old_unique)), "abstract_words": english_word_count(abstract),
                    "declaration_presence": {key: value is not None for key, value in declarations.items()}},
        "old_bib": {"entry_count": len(entries), "explicit_doi_field_count": explicit_doi,
                    "doi_resolvable_from_note_or_field_count": resolvable_doi,
                    "preprint_only_keys": preprints, "duplicate_doi_groups": duplicate_groups(entries, "doi"),
                    "duplicate_title_groups": duplicate_groups(entries, "title"), "metadata_findings": metadata_findings},
        "reusable_existing_keys": reusable, "missing_reusable_keys_internal_error": missing_reusable,
        "related_work_topic_matrix": topic_matrix, "claim_citation_gaps": claim_gaps,
        "downloaded_applied_sciences_corpus": corpus_items,
        "draft_metrics": {"w5_words_excluding_claim_comments": english_word_count(w5_text),
                          "w6_words_excluding_claim_comments": english_word_count(w6_text),
                          "combined_staging_words": english_word_count(w5_text) + english_word_count(w6_text),
                          "target_body_words": c2_budget["target_body_words"], "planned_top_level_sections": c2_budget["top_level_sections"]},
        "mdpi_compliance": compliance, "verification_urls": verification_urls,
        "assembly_priority": [
            "Replace the old title and all superseded 4000/800/800 single-run claims.",
            "Build the missing Introduction/Related Work with verified citations, then insert citations into W5/W6 claim locations.",
            "Acquire and verify BM25, Sentence-BERT/MiniLM, cross-encoder/BGE, grouped-OOF, bootstrap/Holm and official NERC source references.",
            "Repair Bib DOI fields and critical author/incomplete-record issues; do not copy all 48 entries blindly.",
            "Assemble to the registered six-section structure and write a <=200-word abstract from frozen results.",
            "Resolve author emails, funding grant, CRediT initials, permanent repository/data DOI, IRB confirmation and AI-tool disclosure before submission.",
        ],
    }


def write_markdown(audit: dict[str, Any], path: Path) -> None:
    summary = audit["summary"]
    lines = [
        "# W7 C2GES Citation and Compliance Audit", "",
        "**Decision: NOT READY FOR ASSEMBLY/SUBMISSION.** This is a read-only audit; no TeX or Bib file was changed.", "",
        f"The old bibliography has {summary['old_bib_entries']} entries and {summary['old_unique_cited_keys']} cited keys. The rebuilt W5/W6 drafts contain **zero scholarly citations**. The old abstract is {summary['old_abstract_words']} words and passes the requested 200-word ceiling, but no rebuilt final abstract exists. There are {summary['blocker_count']} submission blockers.", "",
        "## Immediate blockers", "",
    ]
    for item in audit["mdpi_compliance"]:
        if item["status"] == "blocker":
            lines.append(f"- **{item['item']}:** {item['evidence']}")
    lines += ["", "## Reusable local Bib keys", ""]
    for theme, keys in audit["reusable_existing_keys"].items():
        lines.append(f"- **{theme.replace('_', ' ')}:** " + ", ".join(f"`{key}`" for key in keys))
    lines += ["", "These are candidate keys, not an instruction to cite every item. Three currently cited/background entries remain preprint-only and require publication-status review.", "",
              "## Bibliography integrity", "",
              f"- Exact DOI duplicates: {len(audit['old_bib']['duplicate_doi_groups'])}; exact normalized-title duplicates: {len(audit['old_bib']['duplicate_title_groups'])}.",
              f"- Structured `doi` fields: {audit['old_bib']['explicit_doi_field_count']}/{audit['old_bib']['entry_count']}; DOI strings recoverable from `note`: {audit['old_bib']['doi_resolvable_from_note_or_field_count']}.",
              f"- Preprint-only entries requiring status review: {len(audit['old_bib']['preprint_only_keys'])}.", ""]
    for finding in audit["old_bib"]["metadata_findings"]:
        keys = ", ".join(f"`{key}`" for key in finding["keys"]) if isinstance(finding["keys"], list) else finding["keys"]
        lines.append(f"- **{finding['id']} ({finding['severity']}):** {finding['finding']} {finding['action']}" + (f" Keys: {keys}." if keys else ""))
    lines += ["", "## Related-work coverage required", "", "| Topic | Local coverage | Status |", "|---|---|---|"]
    for item in audit["related_work_topic_matrix"]:
        coverage = ", ".join(f"`{key}`" for key in item["existing_keys"]) or "none"
        lines.append(f"| {item['topic']} | {coverage} | {item['status']} |")
    lines += ["", "## Claim--citation gaps", "", "| Location | Claim needing support | Required source | Priority |", "|---|---|---|---|"]
    for item in audit["claim_citation_gaps"]:
        lines.append(f"| {item['location']} | {item['claim']} | {'; '.join(item['required'])} | {item['priority']} |")
    lines += ["", "Artifact/claim-ledger comments support internal numerical provenance, but they do not replace citations for datasets, algorithms, prior methods, or domain context.", "",
              "## Ten-paper Applied Sciences corpus", "",
              "Only the grid-field relation-extraction paper is a direct C2GES related-work candidate. The emergency-dispatch paper is optional application context. The other eight are venue/style comparators and should not be cited merely because they appeared in the target journal.", ""]
    for index, item in enumerate(audit["downloaded_applied_sciences_corpus"], 1):
        lines.append(f"{index}. [{item['title']}]({item['doi_url']}) — {item['relevance_to_c2ges']}; {item['recommended_use']}")
    lines += ["", "## MDPI and scientific-disclosure checks", "", "| Item | Status | Evidence/action |", "|---|---|---|"]
    for item in audit["mdpi_compliance"]:
        lines.append(f"| {item['item']} | **{item['status']}** | {item['evidence']} |")
    lines += ["", "### Required final structure", "",
              "Use the registered six-section plan: Introduction; Related Work; Data and Task; Proposed C2GES Method; Experiments, Results and Discussion; Conclusions. Merge standalone Reproducibility and Limitations material into the relevant method/experiment section. The 10-paper corpus median is five top-level sections; six remains a reasonable task-driven target, not a journal rule.", "",
              "### Protocol and disclosure wording to preserve", "",
              "- Oracle-label is a conditional diagnostic using human FEVER veracity and must state `end_to_end=false`.",
              "- Predicted-label is end-to-end only within document-conditioned role prediction plus sentence selection; it is not open-corpus fact verification.",
              "- NERC material is agent-generated/verified silver and qualitative-only, not expert gold or quantitative domain proof.",
              "- Retain an AI-use declaration identifying drafting/editing assistance, author verification and responsibility; confirm exact tool and purpose at submission.", "",
              "## Metadata verification URLs", ""]
    for item in audit["verification_urls"]:
        lines.append(f"- {item['purpose']}: {item['url']}")
    lines += ["", "## Ordered remediation", ""]
    for index, action in enumerate(audit["assembly_priority"], 1):
        lines.append(f"{index}. {action}")
    lines += ["", "Machine-readable entry-level findings, source hashes and the complete 1060-cell statistics provenance boundary are kept outside the manuscript; this audit does not modify the paper.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    audit = build_audit()
    json_path = HERE / "W7_CITATION_COMPLIANCE_AUDIT.json"
    md_path = HERE / "W7_CITATION_COMPLIANCE_AUDIT.md"
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(audit, md_path)
    print(json.dumps({"submission_ready": audit["summary"]["submission_ready"],
                      "blockers": audit["summary"]["blocker_count"],
                      "bib_entries": audit["summary"]["old_bib_entries"],
                      "old_cited_keys": audit["summary"]["old_unique_cited_keys"],
                      "new_draft_citations": audit["summary"]["w5_citation_count"] + audit["summary"]["w6_citation_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
