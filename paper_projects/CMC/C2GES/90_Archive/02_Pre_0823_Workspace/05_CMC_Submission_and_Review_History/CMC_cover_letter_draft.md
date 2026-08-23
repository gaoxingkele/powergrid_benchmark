# CMC Cover Letter Draft — C2GES

To be pasted into the Tech Science Press submission system after the author-input fields have been completed and the final title has been confirmed.

---

Dear Editors of Computers, Materials & Continua,

We are pleased to submit our manuscript "Causal-Role-Aware Extractive Evidence Selection for Power Grid Reliability Reports" for consideration in Computers, Materials & Continua.

**Fit.** The manuscript formalizes a practical information-extraction task — selecting evidence sentences from official NERC power-grid reliability reports, conditioned on five causal roles (trigger, root cause, propagation/response, impact, mitigation) — and presents a transparent, fully auditable selection method evaluated with document-cluster bootstrap statistics. This applied NLP/information-extraction contribution with a self-built domain corpus matches the profile of recent CMC publications in text analytics and AI for the energy domain.

**What the paper contributes.**
1. A task formalization and benchmark over 40 public NERC reliability reports: 200 role-conditioned questions and 608 candidate evidence sentence identifiers, with the corpus manifest and acquisition script released.
2. A deterministic, cue-and-structure-based selection method that improves evidence F1 by approximately 41% over TF-IDF, 31% over BM25, and 51% over SBERT query retrieval (document-cluster bootstrap for the pre-specified primary comparison, p < 0.001), with role-stratified analysis of where the gains concentrate.
3. Protocol-matched learned and LLM baselines run under identical conditions (same 200 questions, same K=3 budget, same document-cluster bootstrap): two neural rerankers (BGE-reranker-base, 0.2604; ms-marco-MiniLM cross-encoder, 0.2787) land between BM25 and C2GES, with C2GES ahead on point estimates (one comparison borderline-significant, the other statistically indistinguishable), and a zero-shot LLM selector reaches 0.5887 evidence F1 — reported honestly as an upper reference subject to the label-provenance caveat, and used to quantify the tradeoff between accuracy and per-term decomposable, deterministic, auditable selection.
4. An unusually complete transparency package: paired bootstrap comparisons for all reported deltas, per-document dispersion analysis, an explicit label-provenance and cue-circularity discussion, and a released evidence supplement in which the vast majority of reported numbers can be independently recomputed (https://github.com/gaoxingkele/c2ges, release v0.2.0).

**Declarations.**
- The manuscript is original, has not been published previously, and is not under consideration elsewhere (no simultaneous submission).
- Generative AI use is disclosed in the Acknowledgement section per journal policy, covering both manuscript preparation assistance and — material to this work — the agent-generated-and-verified provenance of the candidate evidence labels, which the manuscript discusses openly with a planned human-gold verification path.
- The authors declare no conflicts of interest related to this submission.
- We commit to the article processing charge applicable upon acceptance, including page charges where applicable.
- All authors (Bijing Liu and Yong Yang) have read and approved the submission.
- Data availability: the source reports are official public NERC documents; the evidence supplement, analysis code, corpus manifest, dataset workspace, and the learned/LLM baseline harness and outputs are all public at the repository above (release v0.2.0).

Suggested reviewers: [OPTIONAL AUTHOR INPUT: researchers in information extraction, domain NLP, or power-system reliability analytics; exclude collaborators and other conflicts of interest]

Corresponding author: Yong Yang, NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China. Email: yangyong1@sgepri.sgcc.com.cn

Thank you for your consideration.

Sincerely,
Bijing Liu and Yong Yang
