# Applied Sciences Live-Requirements Check

**Checked:** 2026-09-06  
**Article type:** Article  
**Recommended section:** Computing and Artificial Intelligence  
**Current fit:** Medium; potentially high after E1/E2/E3  
**Current decision:** `DO_NOT_SUBMIT_YET`

## Official-source findings

1. The journal's current aims cover applied natural sciences and engineering and require enough experimental detail for reproduction. It states that papers have no maximum length. Source: <https://www.mdpi.com/journal/applsci/about>.
2. The Computing and Artificial Intelligence Section explicitly includes applied information processing, information retrieval, knowledge engineering, data mining, decision-support systems, and AI applications. C²GES fits this section more directly than a hardware-oriented electrical-engineering section. Source: <https://www.mdpi.com/journal/applsci/sections/computing_artificial_intelligence>.
3. MDPI's current style guide limits the abstract to about 200 words, requires a self-contained single paragraph, and expects background, methods, results, and conclusion without headings. Source: <https://res.mdpi.com/data/mdpi-author-layout-style-guide.pdf>.
4. MDPI requires a Data Availability Statement and asks authors to explain legal or licensing restrictions rather than redistribute restricted material. Source: <https://www.mdpi.com/ethics>.
5. MDPI currently requires disclosure when generative AI assists text, code, study design, analysis, or interpretation; superficial grammar editing alone need not be declared. Product details belong in Acknowledgments and substantive use in Materials and Methods. Source: <https://www.mdpi.com/ethics>.
6. The current listed APC for Applied Sciences is CHF 2400, payable after acceptance and subject to institutional or other discounts. Source: <https://www.mdpi.com/about/apc>.

## Current manuscript compliance

| Requirement | Status | Evidence / action |
|---|---|---|
| In-scope applied computing contribution | PASS, conditional | Long-report information processing and source-linked extraction fit the Computing and Artificial Intelligence Section; E1/E2/E3 must supply the completed application evidence. |
| MDPI LaTeX article structure | PASS | MDPI `applsci` class; Introduction, Materials and Methods, Results, Discussion, and Conclusions are present. |
| Abstract | PASS mechanically | One paragraph, no citation, within the 200-word verifier gate, with historical numerical findings and explicit claim boundaries. |
| Keywords | PASS | Six keywords, within the usual three-to-ten range. |
| Length | PASS | Twenty-four A4 pages; the journal states no maximum article length. |
| Figures and tables | PASS | Six vector PDF figures and nine tables; 6/6 lineage records and manuscript-copy hashes pass. |
| References | PASS | Thirty-five cited and verified entries; no dangling or orphan entry. |
| Data Availability | PASS for protocol snapshot | Rights-safe files are linked to `c2ges-2026-09-06-protocol-ready-v1`; a new final tag is required after E1--E3. |
| GenAI transparency | PASS for protocol snapshot | Materials and Methods and Acknowledgments identify OpenAI Codex use and explicitly exclude AI as author, expert annotator, or data source. Authors must reconfirm the wording before submission. |
| Funding and funder role | PASS from recorded author approval | State Grid Fujian project 521300250006 and no-role statement are present. |
| CRediT, consent, conflicts | PRESENT; author attestation required | All required back-matter fields exist. Author contributions and conflict wording remain the authors' responsibility at submission. |
| Human-research ethics | BLOCKED | E2 has not recruited participants. Applicable ethics approval or exemption must be documented before recruitment and inserted after execution. |
| Completed reproducible validation | BLOCKED | E1, blinded E2, and confirmatory E3 have not been run on the frozen external evidence. |

## Section and issue recommendation

Submit to the regular **Computing and Artificial Intelligence** Section unless the authors independently identify and vet a genuinely aligned Special Issue. Do not choose a Special Issue solely for a nearby keyword: the paper's primary object is source-linked technical-document summarization, not grid control, protection hardware, or predictive maintenance performance.

## Submission conversion rule

The protocol-ready tag must remain immutable. After E1--E3, create a new submission-final tag and replace every occurrence of “protocol-ready”, “remain unexecuted”, and future-tense experiment language with result-conditioned text. The current version satisfies format and transparency requirements but not the journal's applied-validation evidence bar.
