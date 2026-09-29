# Pre-Submission Re-Review — MDPI *Information* (confirmation round)

**Manuscript**: `paper_projects/CMC/C2GES/01_Manuscript/LaTeX/paper_information.tex` (598 lines, 89,320 bytes)
**Prior review**: `02_Revision_and_QA/04_Build_Reports/C2GES_INFORMATION_PREREVIEW.md` — CRITICAL 0 / MAJOR 4 / MINOR 15, score 7/10
**Scope of this round**: verify each fix is correct and complete; hunt for defects introduced by the fixes. Full `.tex` read; `diff paper_applsci.tex.ORIG paper_information.tex` re-run; `references_cited_verified.bib` read; Table 4 re-derived from `03_Reproducibility/Data/exploratory_external_v0/e1_system_comparison_exploratory_v3/external_aggregate_metrics.csv`; compiled `paper_information.pdf` (27 pages, built 07:03, same session as the `.tex`) text-searched to confirm the shipped PDF carries the corrected content.
**Review method**: `pre-submission-reviewer` skill, five dimensions, CRITICAL / MAJOR / MINOR taxonomy, Step 6 full banned-vocabulary and em-dash scan.
**Mandate**: review only. No edit was made to the manuscript.

---

## Fix verification

`diff` returns **11 hunks**, all accounted for by the four MAJORs and the numeric fix. Nothing else in the file differs.

### M1 — venue framing carried past the Introduction: **FIXED and complete**

All four sub-items of the prescribed fix are present.

| Sub-item | Location | Text now in the manuscript |
|---|---|---|
| (i) soften the opposition | L40 | "**Beyond its summarization framing**, the question this study turns on is an information one: …" — the phrase "rather than a summarization problem" is gone (grep: 0 occurrences) |
| (ii) abstract sentence | L21 | "Framed as an information question, the issue is whether added structure supplies discriminative information that lexical relevance and dense similarity do not already carry." |
| (iii) §2.1 bridge | L48 | "Extractive summarization is itself an information-extraction process, and the question this study measures is which of those signals actually carry the information a reader needs and which merely re-encode it." |
| (iv) §5.3 + Conclusions | L556, L582 | "Stated as an information result rather than an engineering one, …" and "Read as an information result, the typed structure re-encoded …" |

**Does it cohere with the summarization framing rather than fighting it?** Yes. The paper no longer denies its own framing: the title ("Role-Conditioned Extractive Summarization", L13), the abstract's opening ("Structural additions to an extractive selector", L21), the §2.1 heading, and the ROUGE endpoint are all left intact, and the new §2.1 sentence explicitly subordinates the information framing to them ("Extractive summarization **is itself** an information-extraction process"). The Introduction's added sentences complement rather than replace. The reframing is now a lens the paper declares and uses, not one it contradicts.

**One caveat, reported below as MAJOR-1** — the framing is now carried *too far* at L556 and L582, where the information lesson is stated as an established finding at a strength the Results do not support.

### M2 — journal-scoped positioning: **FIXED**

- L64 now reads "positions this formulation against **selected adjacent studies**"; L67's caption now reads "Positioning against **selected studies with related structural or power-domain objectives**". Grep for "Applied Sciences" in the manuscript body returns **0 hits** (the only two occurrences are LaTeX comments at L1 and L25, which do not render).
- Bibliography grew 35 → **38**, and all three added entries are from outside Applied Sciences: `carbonell1998mmr` (SIGIR 1998), `erkan2004lexrank` (JAIR 2004), `yuan2026strucsum` (Findings of EACL 2026). Applied Sciences share of the reference list fell from 14/35 (40%) to **14/38 (36.8%)**.
- The 14 Applied Sciences entries were retained, as prescribed.
- The comparison content of Table 1 is untouched and remains accurate.

### M3 — MMR attribution: **FIXED, and the LexRank citation does real work**

L243 now reads: "It greedily maximizes the **maximal-marginal-relevance objective** $0.5\cos(e_i,\bar e_D)-0.5\max_{j\in A}\cos(e_i,e_j)$~\cite{carbonell1998mmr}, **evaluated over the Sentence-Transformers representations**~\cite{reimers2019sentencebert}."

- The objective is now attributed to Carbonell & Goldstein, with Sentence-BERT named as the representation — the two roles are separated in one sentence, exactly as prescribed.
- The formula is MMR with λ = 0.5 (relevance to the document centroid as the query term, minus redundancy against the selected set). The attribution is correct.
- The bib entry is correct: SIGIR 1998, pages 335--336, doi 10.1145/290941.291025.
- `erkan2004lexrank` is placed at L48: "Lead and centroid methods remain useful controls, while **TextRank and LexRank** provide widely used graph-ranking references~\cite{mihalcea2004textrank,erkan2004lexrank}." **This is not padding.** §2.1's function is to establish the ranking principles the comparator set instantiates, and the paper's TextRank condition is the graph-centrality family's representative. Naming one canonical reference for a comparator family would under-cover it; naming the pair grounds the family the paper tests against. The word chosen is "references", not "comparators", so the sentence does not promise a LexRank condition. A reviewer could still ask why the family is represented by one member, but TextRank and LexRank are near-siblings (eigenvector centrality over a similarity graph) and the paper's own rationale at L245 ("TextRank tests an untyped similarity graph") covers the family. I do not record this as a finding.

### M4 — StrucSum coverage: **FIXED**

L56 adds: "StrucSum injects sentence-graph structure into prompts for zero-shot extractive summarization of long documents and reports that combining its structural prompting strategies does not clearly improve performance~\cite{yuan2026strucsum}. That null concerns prompt-level combinations on general-domain corpora rather than typed against untyped edges on a domain report family, but it is a negative structural result in the same problem setting, and we record it as the closest published analogue of the component question asked here."

- Both prescribed difference axes are present: mechanism (prompt-level injection versus typed-versus-untyped edges) and corpora (general-domain versus a domain report family). The mechanism axis is stated as a difference in *what was compared* rather than in *how the graph is built*; combined with the preceding sentence's "injects sentence-graph structure into prompts", the contrast is recoverable. Adequate.
- No numbers were imported, as the skill requires. The bib entry resolves to the same ACL Anthology record the prior review cited.
- The sentence is honest self-positioning and strengthens rather than weakens the paper's standing: it shows the authors know the closest analogue and can state the difference.

### Numeric fix — Table 4: **FIXED, and both cells are correct**

Re-derived every cell of `tab:external-exploratory` (L311--318) from `e1_system_comparison_exploratory_v3/external_aggregate_metrics.csv`. **16/16 exact**, including the two the brief asked about:

| Method | 110 words (artifact) | paper | 260 words (artifact) | paper |
|---|---|---|---|---|
| Lead | 0.16574259119989718 | 0.1657 | 0.16433763141791796 | 0.1643 |
| Centroid | 0.1560411262660693 | 0.1560 | 0.16782696625053967 | 0.1678 |
| TextRank | 0.1689679435960581 | **0.1690** | 0.1795713369787397 | 0.1796 |
| Semantic-MMR | 0.15899477117228228 | 0.1590 | 0.17506822397008306 | 0.1751 |
| **Role-only** | **0.15634716954114494** | **0.1563** | **0.16867109135556688** | **0.1687** |
| No-path C2GES | 0.1668303889286586 | 0.1668 | 0.18435333400674953 | **0.1844** |
| Full C2GES | 0.15884202458018784 | 0.1588 | 0.17717479224887933 | 0.1772 |
| PacSum-MiniLM | 0.16612959598911986 | 0.1661 | 0.17872481271884144 | 0.1787 |

- **0.1563 is correct.** The prior review's diagnosis was right: the artifact's `rougeL_f1` for `Role-only` at 110 words is 0.15634716954114494 and the 4th-decimal digit is 3.
- **0.1687 is also correct.** `Role-only` at 260 words is 0.16867109135556688 → 0.1687 at four decimals. Unchanged by the fix and verified independently.
- **The correction changes no ranking.** `Role-only` sits 7th of 8 at 110 words either way (0.1564 and 0.1563 both exceed Centroid's 0.1560), and no prose claim about its rank exists. (The prior review's aside that Role-only was "fifth" at 110 words was itself inaccurate; its substantive point — that nothing depends on the cell — holds.) Both bolded maxima in the table are still the true per-budget maxima.
- The corrected value is present in the compiled PDF (page 14), so the shipped artifact, the source, and the PDF agree.

### Fix-induced defects

**One.** The two information-framing sentences added to §5.3 (L556) and the Conclusions (L582) state the information lesson as an established finding, at a strength the Results do not support and that contradicts the paper's own hedged formulations elsewhere — including the sentence immediately preceding one of them. Reported as **MAJOR-1**. Everything else the fixes touched is clean: no new banned vocabulary, no new em-dash or typographic character, no new citation or label defect, no build regression (27 pages, 0 overfull boxes, 0 undefined references, 0 undefined citations), and the cross-reference counts are internally consistent (29 `\cite` commands resolving to all 38 bib keys with no orphan in either direction; 19 `\ref`; 17 labels).

---

## Summary

- **CRITICAL: 0**
- **MAJOR: 1**
- **MINOR: 4**

**Top three fixes first**:

1. **MAJOR-1 (MAJOR)** — bring the two information-result sentences (L556, L582) back to the strength the Results support, matching the paper's own L42 wording.
2. **MINOR-2** — trim the abstract back to MDPI's ~200-word maximum; the added sentence pushed it to 212 words.
3. **MINOR-1** — the new §2.1 sentence renders the measured endpoint as "the information a reader needs", which §3.1 and §6.5 disclaim.

MINOR-3 (near-verbatim repetition between §5.3 and the Conclusions) is subsumed by the MAJOR-1 edit, and MINOR-4 (paragraph length) is optional.

All four prior MAJORs are closed. The one new MAJOR is a two-clause edit confined to two sentences; nothing requires re-analysis, a new experiment, or a re-run.

**Carried MINOR tail (not re-litigated).** The 15 MINORs from the first review are untouched, as expected for a fix round. I re-checked only the ones the fixes interact with: **m7** ("The distinction has consequences beyond this corpus: if the typing is redundant…", L40) is unchanged and is now coupled to MAJOR-1 — the conditional reads as satisfied once §5.3 calls it "the finding", so fixing MAJOR-1 also restores m7's defensibility; and **m9** (abstract "why" sentence) is closed, because the abstract's new second sentence occupies that slot.

---

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| **MAJOR-1** | **The information result is asserted as established, but the evidence for it is two null effects of opposite sign.** At L582 the Conclusions say "**Read as an information result, the typed structure re-encoded what the untyped graph and the lexical channels already carried rather than extending them.**" The sentence immediately before it states the measured result at the correct strength: "…while **typed graph information showed no stable advantage over an untyped graph**." The escalation is one sentence wide and the two do not agree. L556 states it more strongly still: "**Stated as an information result rather than an engineering one, the finding is that role typing did not add discriminative information to the representation: the untyped graph and the lexical channels carried the same extractable signal, so the typing contributed representational cost without contributing information.**" Against this, the manuscript's own Results report "**Typed-minus-untyped graph effects were $+0.00139$ and $-0.00544$, with both intervals crossing zero**" (L323) and "**Typed graph information increased formal edge coverage relative to G-U but did not show a stable ROUGE-L benefit. … The 110-word graph contrast reversed direction in two of seven LOSO analyses**" (L357). Three things follow. (a) The effect is *positive* at 110 words, so "re-encoded … rather than extending" has the wrong sign in one of the two budgets. (b) No equivalence test is reported anywhere, so "carried the same extractable signal" is an affirmative no-difference claim that two zero-crossing intervals cannot license. (c) The claim sweeps in "the lexical channels", against which no typed-versus-lexical comparison was ever run. The paper is also internally graded on this point: the Introduction states it as an open question ("does a typed structural representation supply discriminative information … or does it merely re-encode what those signals already supply?", L40) and as a non-finding ("these results **do not establish** that role typing contributes extractable information…; **on the evidence collected**, the simpler representation is the defensible default", L42) — so the Introduction declines to establish exactly what §5.3 calls the finding and the Conclusions assert. Because the paper's disclaimers bound only "system superiority, structural-proxy validity, or operational benefit" (L21, L582), this new claim is not covered by them. | **MAJOR** | Reword both sentences to the strength of the abstract's own sentence ("typed graph information showed no stable advantage over an untyped graph"). At L556: "Read as an information question, the result is that typed structure did not show a stable advantage over the untyped graph or the lexical channels on the measured endpoint, so the typing carried representational cost without a demonstrated informational gain." At L582: "On the evidence collected, the typed structure did not extend the extractable signal beyond what the untyped graph and the lexical channels already carried." Two further points while editing this passage: the claim currently sits in §5.3, headed "Methodological Lessons for Structure-Aware Long-Document Extraction", while §5.1 "Main Findings and System-Level Comparison" (L534) carries no information-framed finding at all, so a reader who skips the lessons subsection never sees it — if it is kept as a finding, §5.1 is its home; and the §5.3 sentence now sits immediately after lesson three ("formal typed-edge coverage cannot be interpreted as semantic coherence when the types originate from lexical rules", L554), which reads oddly next to a claim about what the typing *did* contribute. |
| MINOR-1 | **The new §2.1 sentence renders the measured endpoint as reader need.** L48: "Extractive summarization is itself an information-extraction process, and the question this study measures is which of those signals actually carry **the information a reader needs** and which merely re-encode it." §3.1 states the endpoint's limits precisely: "These measures characterize **reference overlap and lexical repetition rather than expert-assessed completeness or operational usefulness**" (L89), and §6.5 repeats it ("ROUGE and redundancy cannot provide these judgments", L570). The framing sentence is right in intent; only the object of measurement is overstated. (Same sentence, smaller point: "the question this study **measures**" is an odd verb for a question; L40's "the question this study turns on" is the better construction.) | MINOR | Change the object of measurement to what was actually measured: "…and the question this study addresses is which of those signals carry information the reference summary does not already supply, and which merely re-encode it." |

---

## Dimension 2: Writing details

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| MINOR-2 | **The abstract is now 212 words against MDPI's "about 200 words maximum".** Counting the rendered abstract (L21) as whitespace-delimited words with macros resolved gives **212** (the pre-fix abstract in `paper_applsci.tex.ORIG` gives 188 by the same method). MDPI's instructions for authors state "The abstract should be a total of about 200 words maximum"; the prior review's m9 fix note estimated the added sentence "Leaves the abstract ~200 words", and it does not. This is a production-stage trim, not a rejection risk — *Information* sets no article length limit and the manuscript is 27 pages. | MINOR | Cut one result sentence from the abstract (S5 and S6, "A post-access pilot covered seven public report series from three organizations." / "Eight methods used identical layout-filtered candidates and 110/260-word budgets.", can be merged into S7) to bring it to ~195 words. |
| MINOR-3 | **The new information-result sentence is repeated almost verbatim 26 lines apart.** §5.3 (L556): "the untyped graph and the** lexical channels carried the same extractable signal**". Conclusions (L582): "the typed structure re-encoded what **the untyped graph and the lexical channels already carried** rather than extending them." Both are newly added and both open with the same meta-frame ("Stated as an information result…", "Read as an information result…"). Restating a Discussion conclusion in the Conclusions is normal; repeating its wording is not. | MINOR | Resolves with the MAJOR-1 reword if the Conclusions sentence is narrowed to the path mechanism, which the Conclusions paragraph is about. Otherwise vary the second phrasing. |
| MINOR-4 | **Two Introduction paragraphs now occupy 13 printed lines each, above the skill's 10-line guideline.** Measured against the MDPI line numbers in the compiled PDF: the framing/RQ paragraph (L40) spans printed lines **52--64**, and the contributions paragraph (L42) spans printed lines **65--77**. The same two paragraphs spanned **11 lines** in the previous build (`paper_applsci.pdf`, lines 54--64 and 62--72), so the condition predates this round — but the fixes added two printed lines to each (L40 is 157 words, L42 is 146). **This corrects the prior review**, which recorded that "no paragraph exceeds 153 words or ten lines"; the source-line word counts there were low. Several other paragraphs sit in the same band (L272, L481, L554 are 140--150 words), so this is a uniform property of the manuscript rather than a defect of the added sentences, and it is a guideline-level item. | MINOR | Optional. Split L40 at the natural boundary after "…a simpler untyped representation is the better instrument.", letting "This diagnostic study asks three bounded questions." open the next paragraph, which also separates the study's questions from the framing. L42 can split before "Stronger confirmatory and semantic-validity claims are reserved…". Neither change is required for submission. |

**Dimension 2 is otherwise clean.** Paragraph-level checks were re-run over the passages the fixes touched. Each of the added sentences is a single-sentence addition at the correct location, and both touched paragraphs still open with a topic sentence. L40's opening "Beyond its summarization framing" has its antecedent one paragraph back (L38, "The study uses…"); I checked it and did not record it — the referent is recoverable and the phrase is idiomatic. The Abstract still delivers what/why/how/results/bounded-conclusion, and the new second sentence correctly occupies the "why this question needed asking" slot that m9 identified as missing, so m9 is closed.

---

## Dimension 3: English grammar

No new grammar findings. The added sentences were checked against the rule set:

- **G1 (articles)**: "Extractive summarization is itself an information-extraction process" — abstract noun, no article required; "a typed structural representation", "a simpler untyped representation", "the graph machinery" all correct.
- **G2 (agreement)**: "which of those signals actually **carry** the information" — plural verb with plural "signals" (L48); "TextRank and LexRank **provide**" (L48); "these results **do not establish**" (L42). All correct.
- **G3 (tense)**: present throughout for the paper's claims, as §2.1 and the Introduction require.
- **G4 (complexity)**: the longest addition is 43 words (L40's first sentence, shown above) and is a single question with a coordinated alternative, not a multi-clause pile-up. The other two added framing sentences are 24 and 30 words.
- **G5 (which/that)**: no new `which`; the four pre-existing uses remain correctly non-restrictive or interrogative.
- **G7 (Chinglish)**: no new over-hedging, no idiom translation, no "very" inflation.
- **G8 (quotation punctuation)**: 0 straight and 0 smart quote characters in the file.

---

## Dimension 4: LaTeX format

The abstract-length item (MINOR-2) is the only format finding this round; it is recorded under Dimension 2 to keep it next to its fix.

Re-verified and clean:

- **Citations**: 29 `\cite` commands resolving to **all 38** bib keys, with **no orphan in either direction**; the three new entries were added correctly and are all cited.
- **References**: 19 `\ref`, all 19 written with the non-breaking tilde. All 17 labels resolve; no `\ref` points at a missing label.
- **Build**: 27 pages; **0 overfull boxes**; 0 undefined references; 0 undefined citations; the only log notices are tabularx underfull-hbox stretches, as before. All 15 float environments captioned; all 6 figures vector PDF; no raster.
- **Typography**: 0 × U+2014, 0 × U+2013, 0 × smart quotes, 0 × straight double quote, 0 × U+00A0, 0 × U+2026, 0 × U+2212; 0 doubled words; 0 double spaces. The only two `---` tokens are in `\authorcontributions` (L585, "writing---original draft preparation", "writing---review and editing"), the MDPI-required separator, exempt from the em-dash rule.
- Carried MINORs m2--m5 and m8 (thousands separators; ` \cite` versus `~\cite`; hyphenated labels; unreferenced numbered equations; Table 8's mixed-format column) are unchanged and were not re-litigated.

---

## Dimension 5: Figure quality

No figure file changed in this round (`figures/` contents all predate the revision; `fig:component-diagnostic` remains the most recent, 6 September). No figure is touched by any of the edits, so no figure finding arises from the fixes. The prior review's figure items (m10, Figure 2's "13 excluded reasons in Table S1" label; m11, default Matplotlib styling in Figures 3, 5 and 6) are carried, unchanged, and not re-litigated.

---

## Banned-vocabulary and em-dash scan

**Scan scope (attestation).** Run in full over the whole manuscript, not sampled: all 598 source lines, case-insensitive **word-boundary** match with inflectional suffixes allowed for every term on the skill's list, plus a Unicode codepoint scan for U+2014, U+2013, U+201C, U+201D, U+2018, U+2019, U+00A0, U+2026 and U+2212, and a doubled-word and double-space scan.

| Term | Occurrences | Reading | Severity |
|---|---|---|---|
| **"superiority"** | 4 (L21, L296, L556, L582) | Every occurrence is a disclaimer ("but not system superiority…", "…does not establish system superiority…"). **Unchanged by the fixes** — none of the new sentences introduced one. | Clean |
| **"exceeded" family** | 7 (L296, L361, L477, L479, L481 ×2, L487) | As the prior review recorded for the 5 "exceeded" instances: three are the paper's own bounded comparisons, each qualified in the same sentence; two are numeric thresholds. The two additional hits are "exceeding" (L477, L479), same class. **Unchanged by the fixes.** | MINOR (carried) |
| All other listed terms | 0 | Zero occurrences of innovative, pioneering, revolutionary, transformative, superior (adjective), surpass, excel, remarkable, unprecedented, state-of-the-art, SOTA, breakthrough, general-purpose, "is capable of", notably, yet, yielding, "at its essence", encompass, differentiate, reveal, underscore, exhibit, "pave the way", "highlight the potential", "profound challenge", "stems from", rigid, impede. | Clean |
| **Em-dash as sentence connector** | 0 | The only `---` tokens are the two MDPI-required separators in `\authorcontributions`. | Clean |

**The additions introduced no banned term.** The nine added sentences use "discriminative information", "re-encode", "representational cost", "extractable signal", "defensible default", "instrument", "analogue" and "null" — none on the list, and none of them hyperbole.

---

## Final score (1-10)

**8 / 10.**

Up from 7. The four venue-facing MAJORs that set the previous score are closed, and closed properly: the framing now runs through the abstract, §2.1, §5.3 and the Conclusions without fighting the paper's own summarization framing; the positioning criterion is topical with the journal scoping gone from the body; the MMR objective is attributed to Carbonell & Goldstein with Sentence-BERT separated out as the representation, and the LexRank addition grounds the comparator family rather than padding; StrucSum is covered with both difference axes and no imported numbers. The reproducibility record, which was already the paper's strongest feature, is now **16/16 exact** on Table 4, with both audited cells correct and no ranking affected.

What holds it below the near-ready band is one item, and it is the same class of defect the first review did not have to report: a conclusion stated more strongly than its evidence. "The untyped graph and the lexical channels carried the same extractable signal" and "re-encoded … rather than extending" are affirmative claims built on two zero-crossing intervals of opposite sign, with no equivalence test, in a paper whose entire standing rests on the precision of its hedges. It is confined to two sentences and is repairable by matching the abstract's own wording, which is why it costs one point rather than more.

---

## Submission recommendation

**Needs 1-2 days more work** — and materially less than that in elapsed effort: the MAJOR is a two-clause edit to two sentences (L556, L582), and the four MINORs are an abstract trim, one wording change at L48, a de-duplication that disappears with the MAJOR fix, and an optional paragraph split. Nothing in the manuscript is wrong in the sense of being unsupported data, arithmetic, or reference: the numeric audit is now exact, the build is clean, the boundary disclaimers hold everywhere except the two sentences identified, and no fix has broken a neighbouring passage.

The one item that matters most is **MAJOR-1**, because it is the only place where a reviewer with the Results section open can catch the paper claiming more than it measured, and because the correct wording already exists in the manuscript three times over (L21's "no stable advantage over an untyped graph", L42's "do not establish … on the evidence collected", L357's "did not show a stable ROUGE-L benefit") — the fix is to reuse it.

---
