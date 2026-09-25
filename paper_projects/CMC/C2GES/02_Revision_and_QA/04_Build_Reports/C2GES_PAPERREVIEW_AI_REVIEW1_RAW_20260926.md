# paperreview.ai 评审原文（第一次提交：33 页投稿版）

| 项 | 内容 |
|---|---|
| Token | Y1fgiQDAfNoMyfLfyNze3nBILeCuhZVc4qNKCHSxxGY |
| 提交时间 | 2026-09-24T16:22:51Z（本机 09-25 00:22） |
| 评审完成 | 2026-09-25T10:40:31Z |
| 上传件 | 01_Manuscript/LaTeX/paper_information.pdf（33 页，当时版本） |
| 名义限制 | 页面声明"只分析前 15 页"，但评审引用了仅 §4.11/Table S9 出现的 ~6% recall 与 19 报告外部语料等 p17+ 内容——**实际覆盖全文**，该限制未生效 |
| 取回方式 | GET /api/review/{token}（2026-09-26 取回） |

二元评分：Claims_Support 0 / Experimental_Soundness 0 / Writing_Clarity 0 / Prior_Work_Context +1 / Question_Importance +1 / Originality +1 / Value_to_Community +1

---

1. Summary
The paper presents C²GES, a deterministic, source-linked extractive summarizer for long power-system technical reports that integrates five transparent scoring channels: lexical relevance, role evidence, typed graph salience, a typed path-deletion score, and position, along with role-group reservation and a redundancy-aware selection rule. Through carefully designed ablations, length-controlled diagnostics, series-level resampling, and a freeze-before-evaluation protocol, the study finds that role evidence and reservation provide measurable benefits, whereas the typed path-deletion component fails to improve ROUGE-L and can underperform an otherwise identical no-path variant. The work is framed explicitly as a diagnostic evaluation that yields a negative result for typed paths on the present corpora and budgets, not as a claim of overall superiority.

2. Strengths
- Technical novelty and innovation
  - Introduces a transparent, deterministic role-conditioned framework with inspectable channels and source-linked outputs, enabling fine-grained component diagnostics.
  - Proposes a typed path-deletion functional distinct from degree-based graph salience, with clear mathematical properties and unit tests demonstrating non-identity.
  - Implements a role-group reservation mechanism that operationalizes discourse coverage (condition/trigger, propagation/impact, mitigation) in extractive selection.
  - Emphasizes reproducibility via fixed candidates, exact selection logging, tie-breaking rules, and immutable configuration registries.
- Experimental rigor and validation
  - Conducts a comprehensive ablation program (incremental AB-0..6 chain; RP 2×2 factorial; typed vs untyped graph salience) under matched candidates and budgets.
  - Addresses evaluation pitfalls through length-controlled budgets and post-hoc analyses clarifying earlier length confounds in equal-unit settings.
  - Uses series-level equal-weighting, bootstrapped composition intervals, and exact sign-flip enumeration to contextualize paired contrasts.
  - Includes a freeze-before-evaluation revision for the path component and a prospective external corpus, improving the credibility of the negative result.
- Clarity of presentation
  - States claims and non-claims explicitly (diagnostic scope, no human-gold validation, no superiority assertion), avoiding overreach.
  - Carefully documents implementation details (edge gating, scaling, complexity caps), enabling replication and critical audit.
  - Provides a transparent account of development vs test usage, including post-access analyses and their limitations.
- Significance of contributions
  - Offers a rare, well-controlled negative result about typed structural path signals in long-document extractive summarization, relevant to ongoing work (e.g., StrucSum’s structural findings).
  - Supplies methodology for disentangling structural from lexical effects under length-matched budgets—useful to practitioners evaluating graph-based additions.
  - Highlights domain-specific considerations for power-system reports and sets groundwork for future confirmatory studies with stronger construct validity.

3. Weaknesses
- Technical limitations or concerns
  - The typed path-deletion channel underperforms and its failure modes are not fully dissected (e.g., sensitivity to the 12-position horizon, directionality vs chronology, and abstention rates eroding path availability).
  - Strong dependence on lexical cue proxies for roles without modeling negation, scope, or coreference increases the risk of spurious edges and sparse/biased path structures.
  - The positional prior and absolute edge horizon may encode artifacts of document layout rather than discourse logic; sensitivity analyses are only partially reported.
  - O(n^2) edge scans and path enumeration with high caps raise scalability concerns for very large candidate sets; runtime and memory profiles are not reported quantitatively.
- Experimental gaps or methodological issues
  - Earlier retained-test “wins” occur under unequal realized lengths; while this is later analyzed, the primary historical comparison remains confounded.
  - Human expert validation is absent; adjacent-corpus audits (GUM, EBM-NLP) suggest role-cue precision but extremely low recall (~6%), limiting conclusions about role fidelity in-domain.
  - Baseline tuning opportunities are unbalanced (Full has 144-config search; Semantic-MMR and TextRank use defaults), complicating system-level comparisons.
  - The freeze-before-eval “held-out” test set is not unseen, so the revised path conclusions, while informative, stop short of confirmatory generalization.
- Clarity or presentation issues
  - The manuscript is dense, with repeated caveats and many condition labels; readers may benefit from a consolidated, earlier summary of the key ablation findings in a single figure/table.
  - Some details about series assignment, external corpus composition, and selection coverage metrics are scattered, making it harder to form a quick, global picture.
- Missing related work or comparisons
  - Although several adjacent methods are discussed, more direct head-to-heads under matched budgets with modern unsupervised graph and redundancy-aware methods (e.g., GraphFusion-style submodular ranking, PacSum variants, AREDSUM-CTX-style redundancy modeling) are not presented on the retained test.
  - Limited discussion of recent long-document extractive architectures (e.g., sparse/hierarchical encoders like SciBERTSUM or hybrid state-space approaches) in the context of component-level diagnostics.

4. Detailed Comments
- Technical soundness evaluation
  - The role taxonomy and edge-typing are executed deterministically with transparent lexicons and gating; this is appropriate for controlled diagnostics but fragile semantically (no negation/scope/coreference).
  - The path-deletion score is formally well-defined and software-verified (deletion loss, cache equivalence), but its utility depends on sufficient qualified paths; abstention and tight horizons can undermine signal.
  - The selection rule cleanly separates reservation (coverage) from redundancy control; however, the fixed coefficients (e.g., 0.40Q, 0.20R, 0.15G, 0.15C, 0.10P) may conceal interactions that a learned or cross-validated weighting could reveal.
  - The unrenormalized coefficient-removal diagnostic is rightly flagged as scale-coupled; the renormalized AB-5 vs AB-6 and RP factorial are the appropriate component estimands and strengthen the negative conclusion.
- Experimental evaluation assessment
  - The seven-series, length-controlled pilot and factorial ablations convincingly isolate that role evidence/reservation matter while typed paths do not, at least under these conditions.
  - The freeze-before-eval revision is a strong design step; however, the small development variant pool and reuse of the earlier test set constrain the strength of inference.
  - Reporting realized length differences and adding word budgets post hoc is responsible; future primary analyses should use word budgets end-to-end to avoid re-interpretation.
  - Absent quantitative runtime/memory statistics limit assessment of practical deployability on very long reports.
- Comparison with related work (using the summaries provided)
  - StrucSum shows that combining structural prompting strategies did not clearly improve zero-shot performance on general corpora; your typed-path negative result is a convergent structural null in a different setting, reinforcing the caution that not all structural signals add extractable information.
  - GraphLSS demonstrates gains from heterogeneous graphs when learned end-to-end; in contrast, your deterministic typed paths underperform, suggesting that either (i) learned fusion of heterogeneous edges or (ii) cross-granularity connections (word–sentence) may be necessary to realize structural benefits in long documents.
  - Bi-GAE shows that improving sentence embeddings can rescue graph rankers; your results may reflect that stronger semantic embeddings and untyped graphs (e.g., PacSum/Bi-GAE) could outperform brittle typed proxies, especially with sparse/cue-based roles.
  - AREDSUM-CTX’s explicit redundancy modeling helps on datasets with high redundancy potential; your fixed Jaccard-based penalty is simpler—future incorporation of semantic redundancy features might improve robustness without typed paths.
  - SciBERTSUM and MAMBA-BERT target long documents via sparse attention/hybrid state-space modeling; while supervised, they highlight alternatives to graph typing for capturing inter-sentence structure at scale.
- Discussion of broader impact and significance
  - The paper’s most useful community contribution is methodological: a careful blueprint for disentangling structural components under matched information budgets and documenting negative findings without overclaiming.
  - In the power-systems documentation ecosystem, a transparent extractive pipeline that preserves page links and role coverage could aid practitioners even if typed paths are ineffective; however, user-facing utility requires human validation and task-oriented metrics beyond ROUGE.
  - The negative result responsibly tempers enthusiasm for typed structural complexity in specialized domains; simpler untyped graphs or semantic rankers may suffice until stronger semantic grounding or human-labeled roles/edges are available.

5. Questions for Authors
1. Can you quantify how often qualified typed paths exist per report (distribution of path counts, abstention rates, and effective path coverage), and how this scarcity correlates with the negative path-deletion effect?
2. How sensitive are your findings to the 12-position edge horizon and to enforcing chronological direction (source position increasing) rather than role-order direction alone?
3. Could you report per-report runtime and memory usage (including edge construction and path enumeration) and how these scale with candidate counts (e.g., 50–1,900 sentences)?
4. What was the realized role-assignment distribution (including abstentions) and how did reservation change role coverage versus no-reservation? Do misassigned roles disproportionately affect mitigation coverage?
5. In the RP factorial, what are the precise main and interaction effects (with CIs) of reservation and path deletion on ROUGE-L and redundancy?
6. Would a learned channel-weighting (e.g., logistic regression or listwise learning-to-rank on development with freeze-before-eval) alter the relative contribution of C versus G/R/Q/P, and did you attempt cross-validated weight learning?
7. Beyond GUM and EBM-NLP, do you plan a small expert annotation to directly rate role correctness, edge/path validity, and extract faithfulness on a stratified subset to validate the diagnostic conclusions?
8. Could you extend the typed-vs-untyped comparison to more baselines (e.g., PacSum, GraphFusion-like submodular selection with semantic coverage/diversity) under matched word budgets to situate the no-path variant competitively?
9. How robust are conclusions across organizations in the 19-report external corpus (e.g., stratified by issuer, report genre), and did you observe domain-shift effects that differentially impact typed vs untyped edges?
10. Given the very low recall (~6%) of role cues in adjacent-corpus audits, have you considered augmenting cues with weak supervision or shallow parsing (negation, scope, coreference) to increase path availability without moving to fully learned edge labels?

6. Overall Assessment
This is a careful, transparent diagnostic study that convincingly shows—under matched, length-controlled conditions on power-system technical reports—that typed path-deletion signals, as currently instantiated, do not add measurable value over simpler channels, while role evidence and reservation do. The authors’ rigorous ablations, explicit acknowledgment of scale coupling, and freeze-before-evaluation step distinguish this work methodologically and make the negative result credible. The main limitations are the absence of in-domain human validation, residual confounds in the historical equal-unit comparisons, limited baseline tuning parity, and incomplete exploration of why typed paths fail (sparsity, horizon, directionality, positional priors). With added runtime/resource reporting, expanded head-to-heads under fair tuning and word budgets, and a modest expert annotation to validate role/edge/path correctness, this work would make a valuable contribution—especially as a well-executed negative structural result—appropriate for venues that recognize rigorous diagnostic evaluation and reproducibility.

```
TRIPLE_SCORES:
- Claims_Support: [0]  # Are the central claims adequately supported with evidence?
- Experimental_Soundness: [0]  # Are the experimental setup and research methodology sound?
- Writing_Clarity: [0]  # Is the writing clear and well-organized?
- Prior_Work_Context: [+1]  # Is the work properly contextualized relative to prior work?
- Question_Importance: [+1]  # Are the research questions being asked important?
- Originality: [+1]  # Does the paper bring significant originality of ideas and/or execution?
- Value_to_Community: [+1]  # Are the results valuable to share with the broader research community?
```