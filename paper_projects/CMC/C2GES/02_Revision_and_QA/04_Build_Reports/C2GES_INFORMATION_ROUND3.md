# Pre-Submission Review — Round 3

**Manuscript:** `paper_information.tex` (C²GES, Information-format revision)
**Path:** `F:/aicoding/powergrid_benchmark/paper_projects/CMC/C2GES/01_Manuscript/LaTeX/paper_information.tex`
**Reviewed:** 2026-09-19 · 667 lines · 95,391 bytes · SHA-256 `98434fdb110a159c4150d48db5880539bdc1e45232c52702d02125f5b8087f25`
**Target venue:** MDPI *Information*
**Artifact:** `paper_information.pdf`, 29 pages (matches the brief)
**Procedure:** `pre-submission-reviewer` SKILL.md, Steps 0–9, with `references/forbidden-patterns.md`, `grammar-rules.md`, `latex-rules.md`, `logic-and-structure.md`, `section-guides.md`

> **Baseline note.** `00_Status_and_Index/CURRENT_BASELINE.md` records SHA `251c6f5d…` at 28 pages. Disk is `98434fdb…` at 29 pages. As instructed, the baseline note is treated as stale and was not reconciled. `paper_information.tex` is untracked in git, so no history diff was available; the review was performed against the file as read in full.

---

## Step 0 — Paradigm and venue calibration

| Item | Assessment |
|---|---|
| Paradigm | Empirical / diagnostic. Not a methods-novelty paper. The claim structure is explicitly *negative component diagnosis*: a structural feature was built, evaluated, and found not to add measured information. |
| Venue fit | MDPI *Information* publishes information-theoretic and information-extraction framing. The revision leans into that framing deliberately (L41, L49, L635). Fit is good. |
| Length | *Information* sets no article length limit. 29 pages with a 207-word Conclusions and a 195-word abstract is acceptable. |
| Required statements | CRediT present (L638), Data Availability present (L642), Abbreviations present (L646), Funding/Conflicts/IRB present. No human-subjects claim is made, correctly (L302). |
| Integrity gate | **Pass.** No fabricated citation detected; no claim of human validation; every machine-audit result is labelled non-human; every post-access result is labelled exploratory or held-out-for-this-revision. |

**Step-0 verdict:** the paper is submitted to the right venue in the right genre. Nothing in Step 0 blocks.

---

## Summary

| Severity | Count |
|---|---|
| **CRITICAL** | **0** |
| **MAJOR** | **3** |
| **MINOR** | **10** |

**Submission-readiness score: 7 / 10**
**Recommendation: Needs 1–2 days more work** (no new experiments; all three MAJORs are writing/records fixes)

### Top three fixes

1. **Report the development evidence behind the freeze.** §3.9 (L298) and §4.3 (L371–L373) present the frozen redesign as a choice made on development but never state the development outcome that drove it. The shipped `FREEZE.json` shows the frozen variant *won both development budgets* (0.08541/0.12532 vs no-path 0.08265/0.12197). Withholding that number while §3.11/§4.7 report that a 147-configuration development search on the *same 12 reports* selected zero path weight in 12/12 folds leaves an unexplained contradiction a referee will find immediately.
2. **Integrate the two new result layers into the navigational apparatus.** RQ1 (L41) still describes a two-layer study; the contributions paragraph (L43) still claims an evaluation that "separates the 15-report retained test from a seven-series post-access pilot"; §4.2 (L308) says "three explicitly separated layers" while §4.4 presents a fourth with its own table; §5.1 (L586) and §5.2 (L588) were not touched at all. The new content is described but not routed.
3. **Refresh the shipped release metadata.** L642 (Data Availability) now promises "the freeze-before-eval path-utility protocol and held-out matched-budget scores" as part of the release, and L580 (Implementation Reliability) claims the packaged records contain "file identities". The shipped `RELEASE_MANIFEST.json` (`file_count: 479`, `generated_at: 2026-09-12T01:24:56Z`) and `FILE_SHA256SUMS.txt` (2026-09-12) contain **zero** entries for `rsi_path_v1`, `synthetic_stress_v1/run_20260918_heldout_v8`, or the 20260917/20260918 protocol dates.

None of the three requires a new experiment, a new table, or re-running anything. All three are documentation repairs.

---

## Direct answer to the two-part question

**Did it improve? Yes — clearly, and in the places that mattered most.**

Round-2 MAJOR-1 is genuinely closed, not papered over. L609 now reads "the exploratory comparison did not establish that role typing contributes discriminative information beyond the untyped graph: the typed-minus-untyped effects did not agree in sign across the two budgets and both intervals crossed zero. That is a failure to demonstrate added information, not a demonstration of redundancy; no equivalence test was run". That is the correct epistemic shape and it is carried into L635 ("a failure to demonstrate an advantage, not a demonstration of equivalence"). Round-2 MINOR-2 is closed (abstract 212 → 195 words). The abstract was not merely shortened; it now carries the held-out/confirmatory distinction and the fictional-fixture disclaimer inside the abstract itself, which is the strongest possible place to put them.

The two new result layers are reported with unusual discipline. I audited every headline number against the shipped artifacts and every one reproduces (below). I also probed the specific risk named in the brief — whether the redesigned path reads as a success anywhere — and it does not, in any of the eight places it appears.

**Is anything blocking? No. Nothing blocks submission. Three things will draw first-round reviewer comments, and all three are fixable in an afternoon.** I found **0 CRITICAL**. The paper's claim structure is sound and honest; the defects are integration and records, not substance. My honest read is that the substance is at *Information* acceptance level and the packaging is one revision behind it.

On the score: round 1 was 7/10 with 4 MAJOR, round 2 was 8/10 with 1 MAJOR. This round is 7/10 with 3 MAJOR. The score did not go up because the revision, while fixing the old MAJOR, introduced three new ones by adding content faster than it updated the surrounding text. That is a normal third-round pattern and worth stating plainly: **the revision is substantively better than round 2 even though the number is lower.** The 8/10 in round 2 was a 1-MAJOR paper; this is a 3-MAJOR paper whose MAJORs are all cheaper to fix than round 2's was.

---

## Does the new experiment's reporting hold its stated discipline?

**Yes.** This was the primary scrutiny target and it survives. Detail follows, because the brief asked for it specifically.

### 1. Does the redesigned-path result read as a success anywhere?

**No.** I checked every location where the redesign or its numbers appear.

| Location | Text | Verdict |
|---|---|---|
| L22 (abstract) | "this is held-out for this revision, not unseen confirmatory, and is not a win on both budgets" | Disclaimed |
| L298 (§3.9) | "The 15-test run is held-out for this revision. It is not an unseen confirmatory corpus: those reports were already used in the historical evaluation, and the seen-exclusion registry contained no unused lawful public series." | Disclaimed |
| L308 (§4.2) | "that layer is held-out for this revision, not unseen confirmatory" | Disclaimed |
| L373 (§4.3) | "The redesigned path did not meet the pre-specified bounded win of a mean at least as large as no-path \cges{} at both budgets. It was 0.0002 below no-path at 110 words (0.0652 versus 0.0654) and 0.0023 above at 260 words (0.1044 versus 0.1020)." | Disclaimed, with the loss stated first |
| Table `tab:rsi-heldout` caption | "Held-out-for-this-revision mean ROUGE-L F1 on $n=15$ retained-test reports at matched word budgets. The redesigned path was frozen on the 12-report development split. This table is not an unseen confirmatory evaluation." | Disclaimed |
| L623 (Limitations) | "The freeze-before-eval path revision uses the same 15 retained-test reports as a held-out split for this revision; it is not an unseen confirmatory corpus." | Disclaimed |
| L635 (Conclusions) | "it did not win both budgets and is not unseen confirmatory" | Disclaimed |
| L373 (framing) | "do not replace the seven-series Full-minus-no-path diagnosis" | Subordinated to the negative result |

The sentence at L373 explicitly leads with the failure and reports the 110-word loss before the 260-word gain. The 260-word gain (+0.0023) is never narrated as a partial victory, never hedged into "trending positive", and never promoted to the abstract as anything but a budget-specific number. **This is honest reporting.** I looked specifically for the failure mode of reporting a mixed result as "competitive" or "on par" — it is not present.

### 2. Is "held-out for this revision" distinguished from "unseen confirmatory"?

**Yes, and consistently.** The exact label `held-out for this revision` and the exact negation `not unseen confirmatory` appear together at L4 (source comment), L22, L298, L308, L376, L623, and L635 — seven locations spanning header comment, abstract, methods, results overview, results body, limitations, and conclusions. The reason is also given, not just the label: L298 states *why* it is not confirmatory ("those reports were already used in the historical evaluation, and the seen-exclusion registry contained no unused lawful public series"). A referee cannot mistake this for a fresh confirmatory test.

The paper also correctly declines to treat the *development* split as independent — L298 says the utilities were redesigned "without reading 15-test or seven-series scores for the new utilities", which is the right boundary and matches `PROTOCOL.json`'s `forbidden_inputs` list (test JSONL, e1/e3 scores, 15-report outcomes).

### 3. Are the fictional fixtures clearly marked, and does anything compare against them as real-incident evidence?

**Yes, marked everywhere; no, nothing treats them as real.** The word "fictional" or an equivalent disclaimer appears at every single appearance of the fixtures:

- L22 (abstract): "On eight fictional role-chain fixtures … those fixtures are not real incident data."
- L391 (§4.4): "A four-series fictional stress set (8 reports…)"
- Table `tab:synthetic-stress` caption: "on $n=8$ fictional reports ($4$ series) … References are extractive reconstructions of the planted role chain. This table is not confirmatory and is not real incident data."
- L623 (Limitations): "The eight-report synthetic factorial uses fictional fixtures and planted extractive references; it is a software stress check, not real incident evidence."
- L635 (Conclusions): "On fictional stress fixtures whose gold summaries were built from the same role chain, Full exceeded no-path in mean ROUGE-L but Holm-adjusted path contrasts remained 1.0; that alignment does not transfer to real Executive Summaries."

Two further disciplines are observed that were not required: L391 states the *reason* the fixtures cannot support a validity claim ("The extractive references were assembled from the same typed role chain that the selector can recover, so this layer tests software and endpoint alignment rather than unseen real-report validity"), and L635 explicitly limits transfer ("that alignment does not transfer to real Executive Summaries"). The synthetic table also does not sit anywhere near the real-report table without a separator: it is its own subsection, its own table, its own disclaimers.

Note the fixture result is a **positive** result (Full > no-path at both budgets) reported inside a paper whose thesis is a negative component result. That is the highest-risk arrangement in the manuscript — a reader could lift the fixture numbers as vindication. The paper forecloses this in the abstract itself. I consider this handled.

### 4. Do the new numbers cohere with the old ones? (re-derivation audit)

Every headline number was re-derived from the shipped artifacts under `03_Reproducibility/`.

| Manuscript value | Artifact | Match |
|---|---|---|
| Table 10: no-path 0.0654/0.1020; redesign 0.0652/0.1044; TextRank 0.0675/0.1031 | `Data/rsi_path_v1/run/SUMMARY.json` → `no_path_c2ges {110: 0.065374728…, 260: 0.102023929…}`, `redesigned_path {110: 0.065181621…, 260: 0.104367211…}`, `textrank {110: 0.067525286…, 260: 0.103123701…}` | 6/6 exact |
| Table 11: Full 0.3886/0.3481; no-path 0.3750/0.3269; G-T 0.3750/0.3269; G-U 0.3002/0.2346 | `Data/synthetic_stress_v1/run_20260918_heldout_v8/` | 4/4 exact |
| Synthetic Full−no-path +0.0136 / +0.0212; Holm 1.0 | `SYNTHETIC_V8_STATUS.md`: "+0.0136 (110), +0.0212 (260); Holm-adjusted exact values 1.0" | exact |
| Typed−untyped Holm 0.25 | `e3_factorial_pilot/factorial_inference.json`: `holm_adjusted_p 0.25`, `holm_family_size 2` | exact |
| "the historical equal-unit $K=5/10$ means (Full 0.1060/0.1276; unrenormalized removal 0.1094/0.1310)" (L373) | historical retained-test artifacts | exact |
| Development freeze: historical utility @ 0.10 | `Data/rsi_path_v1/evolution/FREEZE.json`: `path_weight: 0.1`, `utility: "historical"`, `protocol_seed: 20260917` | exact (but see MAJOR-1) |
| "12-report development split", "15-report retained test", "$n=15$" | `PROTOCOL.json` + `score_eval.py` hard-asserts 15 test reports | exact |
| `wins_both_vs_nopath: false` | `SUMMARY.json` | matches the prose "did not win both budgets" |

The 5-utility × 3-weight grid, the `{0.05, 0.10, 0.15}` weights, and the renormalization rule all match `PROTOCOL.json`. I specifically checked one potential confound: the redesigned arm adds a nonzero path weight while the no-path arm has `path: 0.0`, which would reintroduce the scale-coupling problem §5.2 criticizes. `Code/rsi_path_v1/rsi_common.py::channel_weights()` renormalizes **both** arms to sum 1:

```python
def channel_weights(path_weight: float) -> dict[str, float]:
    weights = dict(NO_PATH_BASE)
    weights["path"] = float(path_weight)
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must be positive in total")
    return {name: value / total for name, value in weights.items()}
```

No scale-coupling confound was reintroduced. **The new numbers cohere with the old ones, and the estimands are explicitly separated** — L373 states that the complete-ranking word-budget means "are a different estimand from the historical equal-unit $K=5/10$ means … and do not replace the seven-series Full-minus-no-path diagnosis". Three result families with three different estimands are kept apart rather than blended. This is the single most credit-worthy writing decision in the revision.

### 5. Did adding ~2 pages introduce inconsistencies with untouched sections?

**This is where the three MAJORs live.** Yes, it did. The new content was added correctly but the sections around it were not revised to match: RQ1, the contributions, the Results roadmap, the Discussion lead, and the shipped release metadata all still describe the round-2 paper. See MAJOR-2 and MAJOR-3.

### Discipline verdict

**The new experiment's reporting holds its stated discipline on all five scrutiny points.** The honesty requirements are met; the consistency requirement is not, and that is what the MAJORs record. The distinction matters: this is not a paper overclaiming a weak result. It is a paper under-integrating a well-reported one.

---

## Findings

### CRITICAL — none

No claim in the manuscript is unsupported by its artifacts, no integrity gate is tripped, and no defect exists that would cause desk rejection.

---

### MAJOR-1 — The development evidence behind the freeze is never reported, and it appears to contradict §3.11

**Locations:** L298 (§3.9), L373 (§4.3), vs L294 (§3.11) and L570–L576 (§4.7)

§3.9 reports the *selection rule* ("The protocol maximized the development mean of the two budgets, with documented tie-breakers") and the *selection outcome* ("The frozen choice was the historical utility at weight 0.10") but never the *development scores*. The reader is asked to accept the frozen configuration on faith.

The problem is not merely incompleteness. §3.11 (L294) states that a separate exploratory program evaluated 147 configurations on the same 12 development reports and that "Twelve leave-one-report-out folds selected a zero-weight configuration in 12/12 folds. The best nonzero candidate used weight 0.025, won no fold, and remained below strict zero at both budgets." §4.7 and L635 repeat this. A referee will therefore read: *development selects zero path weight 12/12* in one section, and *development selected nonzero path weight 0.10* in the next — with no reconciliation.

The reconciliation exists in the artifacts and is entirely legitimate. `FREEZE.json` shows the frozen variant **won both development budgets**:

- frozen: `dev_mean_110: 0.08540744722049835`, `dev_mean_260: 0.12531917462935444`
- no-path: `no_path_dev_mean_110: 0.082653414832692`, `no_path_dev_mean_260: 0.12196649670129482`
- `wins_both_dev_budgets: true`

and the freeze rule records a defensible reason the two searches diverge: `"No-path is a development reference, not a freeze candidate."` The 147-configuration search was optimizing a *coefficient within the existing pipeline* (where zero wins); the freeze grid was selecting among *five redesigned utilities* under a different criterion (maximize the development mean of two budgets), and no-path was not in that candidate set.

**None of this is in the manuscript.** Three consequences:

1. A referee sees an apparent self-contradiction between L294 and L298 and will flag it.
2. The redesigned path looks arbitrary, when in fact it was chosen because it won both development budgets — a materially different and more favourable framing.
3. Most importantly for a diagnostic paper: the fact that the configuration *won both development budgets* and *then failed to win both test budgets* is the winner's-curse story. **Suppressing the development win makes the negative test result look like a cleaner refutation than it is.** The paper's own convention — "every headline number should reproduce from a shipped artifact" — is met by the artifacts but not by the text, because the development numbers never reach the text.

**Fix:** add two sentences to §3.9 giving the development means for the frozen configuration and no-path, stating that the frozen variant won both development budgets, and one sentence explaining why the freeze grid's candidate set excluded no-path while the 147-configuration search's did not. This strengthens the paper rather than weakening it, and it costs no new computation.

---

### MAJOR-2 — The two new result layers are described but not integrated; the navigational apparatus still describes the round-2 paper

**Locations:** L41 (RQ1), L43 (contributions), L308 (§4.2), L586 (§5.1), L588 (§5.2)

The new content was inserted into Methods and Results. Everything that *routes* a reader through the paper was left at round 2.

**(a) RQ1, L41.** The question "asks whether the apparent retained-test advantage persists after output length and report-series dependence are examined and whether the same ordering appears in a separately identified post-access pilot with matched 110- and 260-word budgets." This is a two-layer research question. The paper now has four result layers. A referee reading only the Introduction would not know that a freeze-before-eval redesign or a synthetic factorial exists. The Introduction was updated one sentence earlier (a new information-framing paragraph was added to the RQ paragraph), so this is an oversight of omission rather than design.

**(b) Contributions, L43.** The second contribution claims "a layered evaluation that separates the 15-report retained test from a seven-series post-access pilot and explicitly diagnoses length, clustering, layout, embedding, and multiplicity effects" — an explicit two-layer claim, now false as a description of the paper. The third contribution lists the negative component result as "path deletion did not improve the predefined retained-test endpoint, was negative relative to no-path in the exploratory word-budget pilot, and typed edge information showed no stable exploratory advantage over an untyped graph" — three items, none of which is the freeze-before-eval result or the synthetic result. (The paragraph does gain a closing sentence at L43 about role typing not being established, but that sentence addresses the *conclusion*, not the *scope*.)

**(c) §4.2, L308.** "The evidence is presented in three explicitly separated layers." The paragraph then enumerates retained-test, post-access exploratory, and freeze-before-eval. §4.4 presents a fourth layer — the synthetic stress-test factorial — with its own numbered table, and §5.5 and the Conclusions both treat it as a distinct layer. The roadmap undercounts its own section. A referee scanning the Results will notice that the map does not cover the territory between §4.3 and §4.6.

**(d) §5.1, L586.** Unchanged. It ends: "Taken together, these results do not establish a system-level advantage and instead favor no-path \cges{} as the simpler provisional configuration **pending a prospectively frozen study on genuinely unseen report series**." The paper now contains a prospectively frozen study. It is on held-out-for-this-revision rather than unseen reports, so the sentence is not *false* — but it reads as stale and, worse, it implies the frozen study does not exist. §5.1 is the Discussion's lead paragraph and the first thing a referee reads after the Results.

**(e) §5.2, L588.** Unchanged. "Why the Path-Deletion Term Did Not Improve ROUGE-L" reasons entirely from the historical factorial and the seven-series pilot. It does not mention that the redesigned path also failed to meet its bounded win, which is direct supporting evidence for the section's own thesis and the strongest single piece of evidence in the paper for it.

**Fix:** one clause in RQ1; one clause in contribution 2 and one in contribution 3; change "three" to "four" in L308 and add the synthetic layer to the enumeration; one sentence in §5.1 acknowledging the frozen study and stating that it did not change the default; one sentence in §5.2 noting the redesigned path's failure to meet the bounded win as corroboration. Six edits, no new numbers.

---

### MAJOR-3 — The shipped release metadata does not cover the artifacts the paper now cites

**Locations:** L642 (Data Availability), L580 (§4.10)

L642 was updated to promise the new material: "The diagnostic-submission release adds the post-access exploratory v3 code, **the freeze-before-eval path-utility protocol and held-out matched-budget scores**, non-verbatim inventory, layout audits, aggregate results, series-level statistics, selected identifiers, and machine-audit diagnostics."

The shipped release metadata was not regenerated. In `03_Reproducibility/Package_Metadata/`:

- `RELEASE_MANIFEST.json`: `file_count: 479`, `release_baseline: "2026-09-12 diagnostic submission v2"`, `generated_at: 2026-09-12T01:24:56Z`
- `FILE_SHA256SUMS.txt`: dated 2026-09-12

and per-term searches of the checksum list return **zero** hits for `rsi_path_v1`, `synthetic_stress_v1/run_20260918_heldout_v8`, `path_utilities`, `score_eval`, and `SEALED_CHOICES`, with **zero** occurrences of the dates `20260917` or `20260918`. (A naive combined grep shows ~94 hits, but these are substring false positives — e.g. `CURRENT_EXPLORATORY_VERSION` contains "rsi" across the `VERSI`/`rsi` boundary; per-term verification confirms zero.)

This matters on three counts. First, it is the exact check a data-availability or reproducibility referee runs — the manifest is a one-file lookup and this takes seconds to find. Second, it contradicts L580's own claim that "The packaged reproducibility records contain the complete matrix, **file identities**, and corrective history": the file identities that exist do not identity the two new layers. Third, MDPI treats the Data Availability statement as an integrity commitment; the statement currently describes a release that is not the release on disk.

Note that the *artifacts themselves are present and correct* — I audited them and every number reproduces. The defect is that the identity manifest was not regenerated after they were added. `Package_Metadata/generate_release_manifest.py` exists in the tree and is the natural instrument.

**Fix:** re-run the manifest generator, confirm the new directories are listed with checksums, and update `release_baseline`/`generated_at`. If the intention is instead to ship the protocol separately, then L642 should say so explicitly rather than describing it as part of the release.

---

### MINOR findings

| # | Location | Finding |
|---|---|---|
| 1 | L306 heading | §4.2 is titled "Overview of **Historical** Empirical Findings", but its paragraph now leads with and mainly describes the two new non-historical layers (§4.3 held-out revision, §4.4 synthetic). Retitle, e.g. "Overview of the Four Evidence Layers". |
| 2 | L296 vs L371 | Heading drift between Methods and Results for the same experiment: "Held-Out Matched-Budget Path-**Utility** Revision" (§3.9) versus "Held-Out Matched-Budget Path Revision" (§4.3). The frozen utility is also named "historical deletion loss" at L298 and "historical path-deletion loss" at L373 and in the Table 10 caption. Pick one form of each. |
| 3 | L373 | "It was 0.0002 below no-path at 110 words (0.0652 versus 0.0654) and 0.0023 above at 260 words (0.1044 versus 0.1020)." **This is not an error** — the unrounded 260-word delta is 0.00234328, so 0.0023 is correct and it is the table's 4-decimal rounding that makes a reader's subtraction give 0.0024. Worth a "(unrounded)" tag so the arithmetic does not look wrong at a glance. Verified: the manuscript is right, the displayed values are what disagree. |
| 4 | L298 | "with documented tie-breakers" — the tie-breakers are documented in `PROTOCOL.json` but never stated in the manuscript. Either state them in one clause or drop the phrase; as written it invites a referee to ask for a document they cannot see. |
| 5 | L373 | "the pre-specified bounded win of a mean at least as large as no-path \cges{} at both budgets" — the success criterion is stated here in Results but never in §3.9 where the protocol is defined. Move or repeat the criterion into Methods so it reads as pre-specification rather than post-hoc narration. This is a small point but it is the one that makes the "did not meet" claim credible. |
| 6 | L391 | "unused themes relative to the earlier network-calibrated fixtures" — the earlier network-calibrated fixtures (v6) are not described anywhere in the manuscript. A reader cannot resolve the reference. Either one clause of description or drop "earlier network-calibrated". |
| 7 | L43 | The newly added closing sentence ("Taken together, these results do not establish that role typing contributes extractable information beyond the untyped graph; on the evidence collected, the simpler representation is the defensible default.") is good, but it now sits directly after a contribution list that claims the paper reports a *negative component result*. Consider placing it before the third contribution so the list ends on the negative result rather than on a caveat. Presentational only. |
| 8 | L49 | The round-2 wording fix is only partly complete: "Extractive summarization is itself an information-extraction process, and the question this study measures is which of those signals contribute independently to the measured endpoint." — "the question this study measures" doubles a verb (one *asks* a question, *measures* an endpoint). Carried from round 2 MINOR-1 as a partial fix. Suggested: "the question this study asks is which of those signals contribute independently to the measured endpoint." |
| 9 | L308 | "None of the three layers supports confirmatory superiority or semantic-validity claims" — the synthetic layer is also a non-confirmatory layer and is excluded from the count. Folds into MAJOR-2(c) but is listed separately because it is a distinct sentence from the "three explicitly separated layers" one. |
| 10 | L22 | The abstract is 195 words (verified against `FORMAT_CHECK.md`'s independently confirmed 195) across 8 sentences covering four result layers. Compliant with the ~200-word MDPI guidance, and the compression is well done. Flagging only that it is at the density limit: if any MAJOR fix adds abstract text, something must come out. |

---

## Dimension-by-dimension assessment

### Dimension 1 — Macro logic and structure

| Check | Result |
|---|---|
| IMRaD compliance | Pass |
| Claim structure match to evidence | Pass — the negative diagnosis is supported at every level |
| RQ → method → result → conclusion traceability | **Partial** — MAJOR-2: RQ1 does not cover §4.3/§4.4 |
| Results roadmap matches Results content | **Fail** — MAJOR-2(c) |
| Contribution claims match delivered content | **Partial** — MAJOR-2(b) |
| Discussion addresses all result layers | **Partial** — MAJOR-2(d),(e) |
| Limitations cover all new layers | Pass — L623 covers both new layers explicitly |
| Conclusions match the evidence | Pass — L635 is a model of restrained conclusion-writing |
| No conclusion exceeds its evidence | Pass |

**Verdict:** the argument is sound and the paper never claims more than it has. What fails is coverage — the skeleton was built for a two-layer paper and now carries four.

### Dimension 2 — Writing details

| Check | Result |
|---|---|
| Terminology consistency | **Partial** — MINOR-2 (heading and utility-name drift) |
| Estimand separation | Pass (exemplary — L373) |
| Numbers reported with denominators | Pass ($n=15$, $n=8$/4 series, 12-report development, seven series all stated) |
| Hedging calibrated to evidence | Pass |
| Undefined references to prior work | **Partial** — MINOR-6 ("earlier network-calibrated fixtures") |
| Pre-specification language used correctly | **Partial** — MINOR-5 ("pre-specified" asserted in Results, not in Methods) |
| Paragraph length | Pass — no body paragraph exceeds a readable length |

### Dimension 3 — English grammar

| Check | Result |
|---|---|
| Grammar G1–G8 | Pass |
| Doubled words | Pass — 0 found |
| Subject–verb agreement | Pass |
| Verb doubling | **1 instance** — MINOR-8 (L49) |
| Article/tense consistency | Pass |
| Sentence-level clarity | Pass — L635's 207-word Conclusions paragraph is long but well-formed |

### Dimension 4 — LaTeX format

| Check | Result |
|---|---|
| Document class and options | Pass — `\documentclass[information,article,submit,moreauthors]{Definitions/mdpi}` |
| `\featuredapplication` removal | Pass — correctly removed for *Information*, with a source comment explaining why (moved to L28–L30) |
| Required MDPI blocks | Pass — CRediT (L638), Data Availability (L642), Abbreviations (L646), plus Funding/Conflicts/IRB |
| Undefined references / citations | **0** |
| Overfull / underfull boxes | **0 / 0** |
| Tilde-protected `\ref` | Pass — every `\ref` and `\eqref` uses `~` |
| Bibliography integrity | Pass — 38 entries, 38 cited keys, no orphans in either direction |
| Tables | Pass — 3-line `booktabs` style, captions above, labels present |
| Equation cross-referencing | **Loose** — six equations carry `\label` (`eq:edge-weight`, `eq:path-strength`, `eq:deletion`, `eq:full-score`, `eq:redundancy`, `eq:tboot`) but only one `\eqref` exists in the whole file (L181). The revision corrected one hard-coded `Equation~(1)` to `Equation~\eqref{eq:path-strength}`, which suggests a partial pass. Not a defect — the other equations are not cross-referenced from the text — but see the note below. |
| Page count | 29, matching the brief |

**Note (QA documentation, not a manuscript defect):** `01_Manuscript/LaTeX/FORMAT_CHECK.md` claims "Display equations numbered (1)–(6) with `\label`/`\eqref`". The `\label`s exist; the `\eqref`s do not (1 of 6). The claim is loosely worded rather than wrong. Worth tightening if the QA file is shipped.

### Dimension 5 — Figures and tables

| Check | Result |
|---|---|
| Table numbering and captions | Pass |
| Captions self-contained | Pass — the two new tables state the corpus, the split, and the non-confirmatory status in the caption itself |
| Table values reproduce from artifacts | Pass — Tables 5, 10, 11 all re-derived exactly |
| Table 11 internal coherence | Pass — Full > no-path > G-U ordering, G-T equals no-path as expected for a typed graph without path |
| Figures | None in this manuscript (correct for a diagnostic paper of this type) |
| Table 10/11 placement | Pass — each sits inside its own subsection, adjacent to its own prose |

---

## Forbidden-vocabulary and em-dash scan

**Em-dash scan:** 0 em dashes (U+2014), 0 en dashes (U+2013), 0 smart quotes, 0 straight double quotes, 0 non-breaking spaces, 0 ellipsis characters, 0 minus-sign characters in the source. The only `---` tokens are the two MDPI-required separators inside `\authorcontributions`. **Clean.**

**Forbidden-vocabulary scan:** scanned for the full forbidden list from `references/forbidden-patterns.md` including *innovative, pioneering, revolutionary, transformative, superior, surpass, excel, exceed, remarkable, unprecedented, state-of-the-art, breakthrough, novel, comprehensive, leverage, outperform, advantage, significantly, prove, guarantee, robust, notably, reveal, underscore, exhibit, pave the way*. Findings:

- **`superiority` — 4 occurrences, all negated.** All four are disclaimers ("not system superiority", "confirmatory superiority"). Compliant.
- **`exceed`/`exceeds`/`exceeded` — used only as arithmetic comparators** ("Full \cges{} exceeded no-path at both budgets"), never as evaluative praise. Compliant.
- **`advantage` — used only in negated or diagnostic frames** ("the apparent retained-test advantage", "no stable advantage", "a failure to demonstrate an advantage"). Compliant.
- **`significantly` — absent.** The paper correctly writes "Holm-adjusted exact values" and "intervals crossed zero" instead.

**Clean.** No banned vocabulary is used to make a positive claim.

---

## Fix verification against prior rounds

| Prior finding | Status | Evidence |
|---|---|---|
| **Round 2 MAJOR-1** — overclaim that typing contributes discriminative information | **FIXED** | L609: "the exploratory comparison did not establish that role typing contributes discriminative information beyond the untyped graph: the typed-minus-untyped effects did not agree in sign across the two budgets and both intervals crossed zero. That is a failure to demonstrate added information, not a demonstration of redundancy; no equivalence test was run". Carried into L635: "a failure to demonstrate an advantage, not a demonstration of equivalence". This is now the correct epistemic shape and it is stated twice, in the two places it matters most. |
| **Round 2 MINOR-2** — abstract 212 words | **FIXED** | Abstract is 195 words, independently confirmed by both my count and `FORMAT_CHECK.md`. |
| **Round 2 MINOR-1** — object-of-measurement wording | **PARTIALLY FIXED** | L49 corrected to "Extractive summarization is itself an information-extraction process", but the same sentence retains "the question this study measures" (verb doubling). See MINOR-8. |
| Round 1 (4 MAJOR) | Not re-litigated | All four were closed in round 2 and remain closed. No regression detected. |

**No regressions.** No previously fixed item has become wrong. No carried MINOR was re-litigated except MINOR-8, which is listed only because it remains a partial fix rather than a new observation.

---

## Final score

| Criterion | Value |
|---|---|
| CRITICAL | 0 |
| MAJOR | 3 |
| MINOR | 10 |
| **Score** | **7 / 10** |

Per the skill's scoring rule, 9–10 requires 0 CRITICAL and ≤2 MAJOR. With 3 MAJOR the ceiling is 7. The score reflects fixable integration and records defects, not substantive weakness: on the underlying claim structure and honesty of reporting this manuscript performs at 8–9 level, and the new experiment's discipline audit passed on all five points the review targeted.

## Submission recommendation

**Needs 1–2 days more work.** No new experiments, no re-running, no new claims. The three MAJORs are:

1. Report the development freeze scores and reconcile them with §3.11 (~15 lines in §3.9).
2. Update RQ1, the contributions, the §4.2 layer count, §5.1, and §5.2 for the two new layers (~25 lines across five locations).
3. Regenerate `RELEASE_MANIFEST.json` and `FILE_SHA256SUMS.txt` (one script run).

All three are documentation repairs to a paper whose substance, honesty, and reproducibility are already in order. If the three are addressed, I would score this 9/10 and recommend submission to MDPI *Information* without reservation.
