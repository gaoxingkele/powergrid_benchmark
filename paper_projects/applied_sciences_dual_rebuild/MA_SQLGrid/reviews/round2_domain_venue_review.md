# MA-SQLGrid independent Round-2 domain, venue, and visual review

**Target:** MDPI *Applied Sciences*  
**Best-fit Section:** Computing and Artificial Intelligence  
**Review role:** independent power-grid application, venue-fit, closest-work, and figure/table reviewer  
**Decision:** **Major revision**  
**Current fit:** **Medium**. The manuscript is now an unusually candid and reproducible controlled Text-to-SQL case study, but the application claim is still supported quantitatively by only one development-visible synthetic 8-table/98-row database.  
**Submission ready:** **No**

## Material reviewed and build identity

I reviewed the latest `manuscript_applsci/paper_applsci.tex`, rebuilt PDF, six manuscript figures, four tables, the qualitative DKASQL comparator, the public-baseline feasibility/freeze files, the BIRD 499/500 blocker, the license checklist, and the Round-1 response. I did not modify the manuscript.

- PDF: `manuscript_applsci/build/paper_applsci.pdf`
- Pages: 19
- Bytes: 482,206
- SHA-256: `90A887C1FD5675D348A48DC3CE563DE7E72C12D3EB8760E4509E2ADD72261E96`
- Build: 0 overfull boxes; 0 undefined references/citations; current evidence verifier passes.
- Abstract: approximately 218 words.
- Main structure: six numbered sections, with Materials and Methods, Results, Discussion, Conclusions, mandatory MDPI declarations, six figures, and four tables.

## Overall assessment

The Round-1 revision has materially improved scientific honesty. The singular title accurately says this is a controlled study over a power-grid maintenance database. The abstract discloses the two bundled interventions, reports the corrected Granite upper interval endpoint of 0.3689, states that GridDB is synthetic/development-visible/small, and avoids operational-generalization claims. The paper no longer claims to be the first grid Text-to-SQL system, no longer presents a condition-dependent shape endpoint as comparable across cells, and no longer depicts an unexecuted repair loop. These are substantive corrections.

The qualitative comparison with DKASQL is defensible. It identifies the same-journal predecessor, separates the research questions and data/evaluator boundaries, and makes neither a reproduction nor a numerical superiority claim. The manuscript's most credible novelty is consequently methodological: paired factorial decomposition, corrected common-target diagnostics, cluster-aware uncertainty, complete execution ledgers, backbone sensitivity, and retention of a negative context-package result.

Nevertheless, the present evidence does not yet clear the application-validation bar I would apply to a regular *Applied Sciences* article. The primary quantitative result is based on 180 questions over one exposed synthetic database with only 98 rows. The two larger engineering resources are plumbing pilots whose question--SQL pairs have not been independently reviewed; the BIRD comparison has not run; and single-state execution equality has not been checked against expert semantic judgments or discriminating database states. These limitations are stated honestly, but disclosure does not substitute for the missing evidence. In its current form, the paper is stronger as a reproducibility-rich pilot/methodology case study than as a validated applied system.

## Major issues

### R2-DV-M01 — Applied power-grid validity remains below the journal threshold

The title and abstract no longer exaggerate the current evidence, and the Featured Application is appropriately caveated. Even so, the only canonical accuracy/effect estimates come from a synthetic, development-visible 8-table/98-row GridDB snapshot. RTS-GMLC and SimBench add realistic schema scale but not expert-certified Text-to-SQL accuracy. Thus the beneficiary and engineering use case are plausible, but demonstrated application validity is still weak.

**Required action:** complete the prepared dual independent domain review and adjudication of the 91 visible candidates, then evaluate a genuinely new, family-isolated sealed grid-domain confirmatory set produced after the prompt/selector rules are frozen. Report the visible reviewed set and sealed set separately. At minimum, the confirmatory analysis should retain all attempts, both backbones, execution equality, failure taxonomy, and uncertainty at a question-family unit. If this cannot be completed, retain the narrow title but acknowledge that venue fit remains only medium and consider positioning the article explicitly as a synthetic benchmark/methodology paper.

### R2-DV-M02 — No executed public or literature-level comparator yet supports the contribution

The DKASQL table is a good comparability boundary, not an empirical comparator. F00--F11 answer a useful internal factorial question but do not show how the tested snapshots compare with direct, decomposition/CoT, schema-selection, or execution-feedback pipelines on a fixed public benchmark. The BIRD archive and draft are valuable preparation, but the 499/500 gold-SQL preflight correctly blocks all model calls because question 701 exceeds the registered ceiling. An unfinished future experiment cannot carry the current paper's comparative evidence.

**Required action:** independently resolve and sign the BIRD evaluator boundary without dropping or silently rewriting question 701, freeze the protocol, and run the registered direct, decomposition, schema-selection, and bounded execution-feedback arms for both backbones. If BIRD will not be completed for this submission, move the detailed Q701 protocol narrative out of Materials and Methods into a short limitation/supplement note and add at least transparent same-data literature-level baselines on GridDB. Do not label an independent implementation as DKASQL reproduction.

### R2-DV-M03 — Semantic reliability is not validated beyond one database state

The manuscript correctly calls the primary endpoint execution equality and warns that accidental agreement is possible. However, line 181 still introduces it as “strict execution correctness,” and the applied reliability discussion depends on a metric that can accept nonequivalent SQL on an insufficiently discriminating state. The projected-column endpoint is explicitly diagnostic and does not repair this gap.

**Required action:** add either blinded expert semantic review of a prospectively sampled, stratified set of predictions or a frozen test-suite/perturbed-database evaluation that distinguishes accidental execution agreement. Report the false-agreement rate of the current metric. Independently, change “strict execution correctness” to “strict execution equality on the frozen database state.”

### R2-DV-M04 — Public reproducibility and mandatory submission metadata remain unresolved

The central reproducibility claim currently points to a local artifact tree, while GridDB redistribution permission is unresolved and no permanent public repository URL/DOI exists. The title page and all author-controlled declarations still contain visible `W10_FRONT_MATTER` placeholders. These are hard submission blockers, not copyediting niceties.

**Required action:** obtain GridDB redistribution permission or provide a licensed deterministic regeneration route; review source-specific obligations for RTS-GMLC, SimBench, and any BIRD derivatives; deposit the permitted code/data/ledgers with a permanent DOI; and replace every author, affiliation, CRediT, funding, conflict, acknowledgment, ethics-confirmation, and AI-use placeholder with author-approved text. If raw GridDB cannot be released, specify exactly which artifacts and regeneration inputs can be shared and why the remainder is restricted.

## Minor issues

### R2-DV-m01 — Keep the title; tighten one abstract phrase

The revised title is accurate and should be retained. The 218-word abstract is acceptable, but “backbone-specific validation” can be read more strongly than the one-run two-snapshot sensitivity design permits. Replace it with “two-snapshot sensitivity evidence” or equivalent, and quantify GridDB as 8 tables/98 rows in the abstract so the evidence scale is immediately visible.

### R2-DV-m02 — Separate completed methods from unexecuted prospective work

Section 3.9 combines a future BIRD protocol with the closest-work boundary, and Section 4.5 reports an unreviewed external diagnostic. The boundary language is responsible, but the amount of unfinished-study detail makes the submitted study appear incomplete. Keep the DKASQL comparison in Related Work, keep only a concise BIRD status sentence in Limitations/Future Work, and place protocol/blocker details in supplementary material unless the baseline is completed.

### R2-DV-m03 — Synchronize the BIRD support documents

`GOLD_PREFLIGHT_BLOCKER.md`, the manuscript, and the Round-1 response say the database archive was safely expanded, whereas `DOWNLOAD_LICENSE_CHECKLIST.md` still labels the archive “not extracted or used for model execution.” Model execution is indeed zero, but extraction status is inconsistent. Update the checklist and bind all extracted-tree/protocol statuses to one authoritative manifest.

### R2-DV-m04 — Improve result-figure information density

All six figures are readable at final page scale, use high contrast, and have no clipping. The three framework diagrams now accurately show one generation, no repair/ranking, one 180-by-4 run per backbone, and the sealed-evidence gate. Figure 4, however, shows cell bars without uncertainty even though Table 3 contains intervals; add interval marks or explicitly label the plot as point estimates. In Figure 6, annotate the 155/180 all-column and 115/116 join-path counts directly, or add a small companion panel, because the current histogram makes the operational selector failure modes less visible than the prose.

### R2-DV-m05 — Repair reference formatting

Several conference references render “In Proceedings of the Proceedings of ...” (e.g., Spider, PICARD, RAT-SQL). Normalize BibTeX `booktitle` fields so the MDPI bibliography introduces each proceedings title only once. Also verify page ranges and conference-title capitalization in the final bibliography audit.

### R2-DV-m06 — Preserve the present claim discipline

The Discussion appropriately states that the compact package has no independently supported positive execution effect, that Granite's interval crosses zero, and that the external 15 matches are not accuracy. Preserve these NO-GO boundaries during revision. In particular, do not convert token reduction into efficiency, the 115/116 offline join-path audit into an online selector score, or the nonzero three-way modifier into a general backbone ranking.

## Title, abstract, and section-level verdict

| Component | Verdict | Comment |
|---|---|---|
| Title | Pass | Singular, controlled-study wording matches the actual canonical evidence and is not materially different from the project title. |
| Featured Application | Pass with evidence gate | It names the intended beneficiary and explicitly withholds operational accuracy. |
| Abstract | Pass with minor edit | Numerically synchronized, including Granite CI upper 0.3689; should quantify GridDB size and soften “validation.” |
| Introduction/Related Work | Pass | Clear gap, bounded contributions, and direct acknowledgment of DKASQL. |
| Materials and Methods | Pass for executed GridDB study | Algorithm, factor bundles, data card, endpoints, and statistics are substantially complete; prospective BIRD material should be relocated unless executed. |
| Results | Pass for internal factorial evidence | Complete 1440-row accounting and corrected endpoints; external diagnostic is correctly noncanonical. |
| Discussion/Conclusions | Pass with major evidence caveat | Claims are disciplined, but application validity still depends on future human/sealed evidence. |
| Figures/tables | Pass with minor revisions | Readable and scientifically aligned; Figure 4/6 can communicate uncertainty and selector failures more directly. |
| Data/mandatory statements | Fail for submission | License, DOI, authorship, disclosures, and author confirmations remain open. |

## Applied Sciences fit statement

**[Target]** MDPI *Applied Sciences*  
**[Fit]** Medium — a concrete applied Text-to-SQL workflow and sound internal validation are present, but the power-grid application is not yet externally or semantically validated.  
**[Contribution type]** applied-method / controlled experimental case study  
**[Main evidence gap]** expert-reviewed sealed grid-domain validation plus an executed public/comparative baseline  
**[Best-fit Section]** Computing and Artificial Intelligence  
**[Top rejection risk]** validation restricted to a small exposed synthetic database  
**[Recommendation]** major revision before submission; fit could become high after the external, comparative, license, and metadata gates close.

## Priority order for the next revision

1. Close human-reviewed and genuinely sealed grid-domain validation.
2. Resolve the BIRD Q701 evaluator boundary and execute the frozen comparison, or remove the unfinished protocol from the main study and provide a defensible comparator alternative.
3. Add semantic/test-suite validation of execution equality.
4. Close GridDB/source licenses, public DOI, and every mandatory author declaration.
5. Relocate prospective material, improve Figures 4/6, and normalize the bibliography.

