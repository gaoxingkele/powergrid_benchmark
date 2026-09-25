# paperreview.ai 评审原文（第二次提交：15 页 A3 评审副本）

| 项 | 内容 |
|---|---|
| Token | sjA3oxGSe0bRDX3iam9A5ab4pqL7YlynFmNWozfo3FM |
| 提交时间 | 2026-09-24T16:25:55Z（本机 09-25 00:25） |
| 评审完成 | 2026-09-25T10:41:26Z |
| 上传件 | 06_External_Review/C2GES_reviewcopy_15p_A3.pdf（A3 横向两页并排，覆盖 p1–30，省略参考文献） |
| 取回方式 | GET /api/review/{token}（2026-09-26 取回；评审全文先前由作者粘贴，此处为 API 原文存档） |

二元评分：Claims_Support +1 / Experimental_Soundness 0 / Writing_Clarity 0 / Prior_Work_Context +1 / Question_Importance 0 / Originality 0 / Value_to_Community 0

---

1. Summary
The paper proposes C²GES, a deterministic, role-conditioned extractive summarizer for long power-system technical reports that integrates five score channels: lexical relevance, role evidence, typed graph salience, a typed path-deletion term, and position, along with role-group reservation and redundancy-aware selection. The core scientific question is diagnostic: does the typed structural path-deletion channel add discriminative information beyond untyped graph salience and lexical/semantic relevance? Across a carefully stratified set of analyses (historical equal-unit tests, post-access seven-series factorial with matched word budgets, a freeze-before-eval path revision on held-out test reports, and a prospective external corpus), the authors find that role evidence and reservation contribute measurable effects, while the typed path-deletion channel does not consistently improve ROUGE-L and is detectably inferior to the no-path variant on the external corpus at the larger budget.

2. Strengths
- Technical novelty and innovation
  - A transparent, deterministic pipeline that cleanly decomposes five interpretable channels (Q, R, G, C, P) plus role-group reservation and redundancy control, enabling component-level inspection and ablation.
  - A typed path-deletion functional that is mathematically well-defined and unit-tested (consistency between direct deletion and membership-sum formulations) and distinct from degree-based salience.
  - A disciplined “diagnostic evaluation” framing focused on whether typed structural information carries independent value beyond standard signals.
- Experimental rigor and validation
  - Multiple evidence layers with clear claim bounds: historical equal-unit comparison, a post-access seven-series factorial with matched word budgets, a freeze-before-eval path revision scored on held-out reports, and a prospective external corpus; plus sensitivity analyses (series cluster bootstrap, exact sign-flips, LOSO).
  - Length-controlled evaluation and explicit post-hoc length diagnostics that reveal and correct the unequal-information problem in equal-unit comparisons.
  - Strong reproducibility posture: report-level unit of analysis, deterministic selection and tie-breaking, path/expansion work limits, artifact hashes, and packaged checks.
- Clarity of presentation
  - Careful separation between diagnostic vs. confirmatory claims; explicit discussion of estimands, multiplicity adjustment, and the limits of each evidence layer.
  - Transparent articulation of assumptions and failure modes (e.g., stage-monotone edges, 12-position horizon, abstentions on ambiguous roles).
- Significance of contributions
  - A well-executed negative result on typed structural path deletion under this design, with evidence pointing to the simpler no-path or untyped graph baselines as the defensible default.
  - A methodological template for component-level evaluation in long-document extractive summarization that others can adapt, especially in safety/engineering documentation contexts.

3. Weaknesses
- Technical limitations or concerns
  - Typed edges rely on surface lexical cues without discourse/coreference grounding; direction can contradict chronology, and the 12-position horizon likely excludes many real structural dependencies in long reports.
  - The path-deletion term competes additively with other channels; its utility may be masked by role reservation or by the choice of linear integration and min–max scaling within reports.
  - Very low recall for role cues in adjacent-corpus audits (≈6%) suggests the role layer may miss substantial amounts of relevant content unless expanded or learned.
- Experimental gaps or methodological issues
  - No human evaluation of extract validity, role correctness, edge/path support, or task utility, despite the domain-specific nature of the reports and the acknowledged limitations of ROUGE for this task.
  - Baseline tuning asymmetry in the historical layer (Full had a larger configuration search vs. default TextRank and an untuned MMR coefficient) makes system-level conclusions less compelling until addressed by matched tuning on unseen data.
  - The “prospective” external corpus is still not unseen in the formal sense; a complete freeze-before-access with series-level allocation and pre-registered analysis would strengthen claims.
- Clarity or presentation issues
  - The manuscript is dense; a few repeated sentences (e.g., Section 3.9 duplication) and long footnote-like asides could be streamlined to improve readability.
  - Some figures/tables are described textually rather than shown; cross-references are many, increasing cognitive load.
- Missing related work or comparisons
  - Although related work is broad and includes negative results (e.g., StrucSum structure combinations), stronger discussion of modern extractive systems that explicitly model redundancy/history or long contexts (e.g., MemSum, AREDSUM-CTX) would help position C²GES’s redundancy strategy and integration choices.
  - A clearer contrast to heterogeneous graph approaches that integrate typed structure with learned message passing (e.g., GraphLSS) would frame why a deterministic, typed approach is preferred here and how it might be hybridized.

4. Detailed Comments
- Technical soundness evaluation
  - The formalization of the path-deletion functional and the software validation (cache equivalence, deterministic scaling, membership-sum equality) are sound. The definition ensures non-negativity and additivity over qualified paths.
  - However, crucial modeling decisions likely constrain effectiveness: (i) an absolute 12-position horizon, (ii) edges permitted irrespective of chronological order, (iii) abstention on positive-tie roles (losing potentially informative sentences), and (iv) reliance on lexical overlap for edge weights, which privileges local surface similarity over discourse-level cohesion.
  - The linear score integration with per-report min–max scaling may encourage overfitting to report-specific distributions and complicate comparability across reports; alternative normalization or rank-based fusion could be probed.
- Experimental evaluation assessment
  - The factorial ablation (AB-0…AB-6, RP-00/10/01/11, G-U vs G-T) is valuable and well-documented; the finding that path-deletion materially changes selections (low Jaccard overlap) yet harms the endpoint strengthens the causal interpretation that the channel is actively misaligned with ROUGE-L.
  - The length diagnostics candidly reveal the equal-unit mismatch; the matched-budget pilot and re-run are the right corrective, though still exploratory in some layers.
  - The external corpus result—in which TextRank significantly exceeds no-path at 260 words while Full falls below no-path—provides the only familywise-corrected system contrast and should be centered more in the conclusions.
  - Absence of human evaluation remains a major gap, especially because the motivation is operational (engineers reviewing event analyses). Even a small, stratified expert study focused on source faithfulness, omission, and role/path validity would substantially increase impact.
- Comparison with related work (using the summaries provided)
  - MemSum and AREDSUM-CTX both emphasize adaptive redundancy and history-aware selection, often yielding compact, less-redundant extracts with strong ROUGE; C²GES uses a fixed -0.5 Jaccard penalty and coarse role reservation. A discussion of why a fixed penalty (vs. learned or state-conditioned) is appropriate for this domain—and ablations over redundancy coefficients—would help situate design choices relative to these works.
  - GraphLSS leverages learned heterogeneous graphs atop deterministic construction and shows typed edges help when coupled with message passing. Given C²GES’s typed edges but negative path result, it would be instructive to test whether typed signals help when used via learning (e.g., R-GCN/GAT) rather than via the current path-deletion utility.
  - Bi-GAE demonstrates improved sentence embeddings for graph ranking; swapping sentence encoders or testing whether Bi-GAE embeddings enhance C²GES’s untyped graph baseline could probe whether embedding quality, not typing, underlies some performance gaps.
  - StrucSum’s negative prompt-combination result in long documents provides converging evidence that “more structure” does not necessarily help; highlighting alignment between that negative finding and yours strengthens the broader-lesson narrative.
  - Sem-nCG with redundancy penalties (2310.03414) could augment evaluation given the emphasis on redundancy control and coverage; ROUGE alone may under-represent redundancy/importance tradeoffs that your selector is designed to manage.
- Discussion of broader impact and significance
  - The work provides a model of transparent negative-result reporting, careful ablations, and reproducibility practices that the community should emulate—especially for long-document, domain-specific summarization where construct validity is tricky.
  - Practically, the conclusion that a simpler, untyped representation may be preferable (under these constraints) can save future engineering effort.
  - The explicit freeze-before-eval protocol draft is valuable community infrastructure; executing it end-to-end on a genuinely unseen, series-disjoint corpus with expert outcomes would make this a strong benchmark paper for the domain.

5. Questions for Authors
1. Can you provide a systematic error analysis of cases where the path-deletion channel changed selections but reduced ROUGE-L? Are these primarily long-distance dependencies beyond the 12-position horizon, chronology violations, or cue-misattributions?
2. How sensitive are findings to the 12-position edge horizon and to enforcing chronological direction (i before j) on edges? Have you run ablations increasing horizon (e.g., 24/48) or adding a hard chronology constraint?
3. Your adjacent-corpus role audit shows ≈6% recall. Have you considered expanding the cue lexicon (morphology/synonyms/domain terms), shallow negation/hedge detection, or weakly supervised role classifiers to raise recall while retaining precision?
4. The redundancy penalty is fixed (-0.50 max Jaccard). Did you explore data-driven calibration (e.g., cross-validated sweeps) or adaptive penalties conditioned on already-selected roles/positions, akin to MemSum/AREDSUM history-aware strategies?
5. Given GraphLSS’s success with learned message passing over heuristically constructed typed graphs, did you attempt a hybrid where C²GES uses its deterministic typed edges but delegates scoring to a lightweight R-GCN/GAT trained on pseudo labels (e.g., greedy-ROUGE or executive-summary alignments)?
6. Could you report per-role coverage/benefit analyses under matched word budgets (e.g., precision of “mitigation” extractions against reference sentences mentioning corrective action) to corroborate the claim that the role layer carries measurable information?
7. For fairness, will you run a fully frozen, series-disjoint, matched-budget comparison where baselines (TextRank parameters, MMR coefficient, PacSum thresholds) receive symmetric tuning budgets and selection is pre-committed?
8. Have you considered alternative evaluation metrics (e.g., Sem-nCG with redundancy penalty, entity/event coverage, or NERC-guided attribute checklists) that may better reflect the intended engineering-review utility than ROUGE-L overlap to Executive Summaries?
9. In your freeze-before-eval redesign, why retain the same deletion utility after development indicated weight 0.0 was often preferred? Would a two-stage design—use reservation for coverage, apply path-only as a tiebreaker—better isolate its contribution?
10. Can you share more about the segmentation audit’s block-preserving candidates (e.g., distribution of remaining long blocks, examples where long units inflated ROUGE) and whether adopting that segmentation changes the relative ordering at matched budgets?

6. Overall Assessment
This is a careful, transparent diagnostic study that delivers a credible negative result: under the proposed deterministic role-conditioned framework for long power-system reports, the typed path-deletion channel does not improve ROUGE-L and can underperform simpler alternatives, while the role-evidence/reservation layers show measurable effects. The methodological strengths—length-controlled analyses, factorial ablations, series-level sensitivities, and reproducibility—are commendable. However, for a top-tier venue, the absence of human evaluation, incomplete symmetry in baseline tuning (in the historical layer), reliance on ROUGE-only endpoints, and the lack of a definitive, unseen confirmatory experiment reduce the impact. The work’s value is real, especially as a model for negative-result reporting and component-level diagnosis; to elevate it, I recommend (i) executing the freeze-before-eval protocol on a genuinely unseen, series-disjoint corpus, (ii) adding a targeted expert evaluation focused on role/path validity and operational utility, (iii) exploring stronger or hybrid structural models (learned message passing over typed edges; chronology and longer horizons), and (iv) adding redundancy- and coverage-aware metrics. With these additions, the paper could serve as a reference for principled evaluation of structure in long-document extraction.

TRIPLE_SCORES:
- Claims_Support: [+1]  # Are the central claims adequately supported with evidence?
- Experimental_Soundness: [0]  # Are the experimental setup and research methodology sound?
- Writing_Clarity: [0]  # Is the writing clear and well-organized?
- Prior_Work_Context: [+1]  # Is the work properly contextualized relative to prior work?
- Question_Importance: [0]  # Are the research questions being asked important?
- Originality: [0]  # Does the paper bring significant originality of ideas and/or execution?
- Value_to_Community: [0]  # Are the results valuable to share with the broader research community?