# Dataset card — frozen external incident-report corpus (C²GES, 2026-09)

## 1. What this asset is

A frozen, rights-aware evaluation set of **24 public incident / disruption reports** used as the
external layer of C²GES:

| Family | n | Candidate units per report | Reference words | Typical source |
|---|---:|---|---|---|
| ENTSO-E grid incidents | 7 | 589–2,000 | 1,190–10,935 | ENTSO-E factual / final incident reports (2024 SE Europe, 2025 Iberia, 2025 Czechia, 2025 MEPSO, …) |
| ENTSO-E market-coupling incidents | 9 | 21–84 | 108–779 | SDAC / SIDC partial-decoupling reports (2019–2025) |
| NERC event reports | 6 | 37–334 | 102–1,431 | NERC disturbance / incident reviews |
| ENTSO-E frequency-deviation reports | 2 | 271–336 | 401–800 | joint ENTSO-E / Eurelectric deterministic frequency-deviation reports (2012, 2013) |

Each document contributes: the report, its official summary section (used as the abstractive
reference), the post-summary candidate units, and per-arm selections and ROUGE-L scores.

The 19-document subset was frozen **before** its scores were computed (pre-registered external
evaluation); the five-document extension (Czechia, MEPSO-final, three SDAC reports, two
frequency-deviation reports — 24 in total after de-duplication) is reported as a **sensitivity**.
The GovReport transfer layer reuses the same frozen arm set out of domain and is documented
separately (`../govreport_transfer_v1/PROTOCOL_govreport_transfer_v1.md`).

## 2. What ships, and what does not

| Shipped (release scope) | Not shipped |
|---|---|
| the frozen protocol and its revision log | the source PDFs |
| per-document derived records (ROUGE-L, selected-unit counts, realised words) | the Markdown conversions |
| contrast records with sign counts, p-values and bounds | the extracted reference-summary text |
| this card, the inventory and the file hashes | any passage quoted from a report |

Third-party redistribution permission has not been established for the source documents, so the
release carries **only derived, non-verbatim numbers**. The verifier enforces this: no shipped data
record may contain a natural-language run of ≥300 characters with ≥40 words.

## 3. How to rebuild it

1. Retrieve the sources with the recorded channels (Wayback CDX enumeration of the publisher
   paths, direct ENTSO-E blob downloads, snapshot fallback for hosts that block direct access);
   the acquisition report lists every attempted host and every failure.
2. Convert each PDF to Markdown (`convert_to_markdown.py`, PyMuPDF-based, deterministic).
3. Apply the gate: a detectable official summary section of **≥100 words** inside the first
   25 pages, **≥20** post-summary candidate units, and event-date de-duplication keeping the
   most final version (final > interim > note).
4. Run `run_external_prospective_v2.py` (paired word-budget contrasts) and
   `run_external_arms_v3.py` (role / path / baseline arms), then the budget-curve and
   equivalence-bound analyses.

Scripts and the protocol live beside this card and in `../../Code/`; every shipped record carries
the hash of its input.

## 4. Intended use, and misuse

**Intended.** Paired, within-document diagnostics of extractive selectors on long technical
reports: budget-type sensitivity (equal words vs equal units), role/path component attribution,
and bounded negative results (one-sided limits rather than significance stars).

**Misuse.** Do not report a single accuracy across families; family sizes are 2–9 and are meant to
be read separately. Do not treat the official summaries as human extractive references — they are
human *abstractive* summaries, which caps attainable ROUGE and is why positional baselines do
well. Do not read "no significant difference" as "no effect" without the printed bound and the
power ceiling.

## 5. Known limitations

1. **Reference type.** Abstractive official summaries; extractive systems can only approximate
   their wording.
2. **Family sizes.** 2–9 documents per family; only pooled across families with an explicit
   warning, never into one accuracy.
3. **Unit cap.** The longest report is truncated at 2,000 candidate units by protocol.
4. **Layout noise.** Multi-column pages, tables and caption blocks produce some fused or split
   units; the layout audit quantifies this rather than fixing it.
5. **Visibility history.** The pilot corpus was accessed before its rules were frozen; only the
   19-document external subset has a freeze-before-scoring record.

## 6. Citation

Cite the paper's Data Availability statement and this card. If you reuse the derived records,
report the protocol version and the revision log entries that applied when they were produced.
