# CMC Cover Letter Draft — MA-SQLGrid

To be pasted into the Tech Science Press submission system after the author-input fields have been completed and the final title has been confirmed.

---

Dear Editors of Computers, Materials & Continua,

We are pleased to submit our manuscript "MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL over Power Grid Maintenance Databases" for consideration in Computers, Materials & Continua.

**Fit and precedent.** The manuscript applies large-language-model text-to-SQL techniques to a concrete industrial setting — natural-language querying of power-grid maintenance databases — which sits squarely within CMC's coverage of applied artificial intelligence and information systems. It complements recent CMC work on LLM-based SQL agents (CMC 2026, DOI 10.32604/cmc.2026.078330) with a domain-grounded framework and a fully released benchmark.

**What the paper contributes.**
1. A five-condition controlled comparison (schema-only, full schema+values, CHESS-style, compact domain context, compact context + reference-free validation) on a released power-grid maintenance benchmark of 200 question–SQL pairs, with paired sign tests.
2. Cross-generator validation: all headline findings replicate on a second, independent, open-weight-family generator (deepseek-chat) using byte-identical prompts — the compact-context gain is +36.1 percentage points strict execution accuracy on the second generator, and a 3-repeat consistency companion bounds run-to-run variation at 1.1 points with 98.3% per-question verdict agreement.
3. A scale-robustness stress test: the full three-condition comparison is repeated on a 10x-scale variant of the maintenance database (540 main plus 13 repair archived calls), where the compact-context advantage persists (+26.1 points strict) at flat token cost while the full-schema condition's prompts grow by 51%; the single observed degradation channel is traced, prompt-byte level, to a value-list truncation artifact affecting 31 questions, with a concrete fix path stated.
4. An evaluation-convention sensitivity analysis that reports order-insensitive and projection-tolerant scores alongside the strict metric, transparently separating answer-contract conformance from row-content retrieval.
5. A full reproducibility release: benchmark, evaluator with tests, all 3,073 raw API traces (2,520 from the original runs plus 540 main and 13 repair calls from the x10 run), and analysis code (https://github.com/gaoxingkele/ma-sqlgrid, release v0.2.0).

**Declarations.**
- The manuscript is original, has not been published previously, and is not under consideration elsewhere (no simultaneous submission).
- Generative AI use is disclosed in the Acknowledgement section per journal policy: LLMs are both the object of study and were used, under full author oversight, for drafting and editing assistance.
- The authors declare no conflicts of interest related to this submission.
- We commit to the article processing charge applicable upon acceptance, including page charges where applicable.
- All authors (Bijing Liu, Chenglong Sun, and Yong Yang) have read and approved the submission.
- Data availability: the complete benchmark and code are public at the repository above (release v0.2.0). The second-generation context-builder modules are included and reproduce the archived experiment prompts byte-for-byte (180/180); the only remaining unreleased components are the original researchclaw LLM client shim and the v0.1 dataset-generator script, neither of which affects reproduction of any reported number.

Suggested reviewers: [OPTIONAL AUTHOR INPUT: researchers in NL2SQL, LLM applications, or power-system informatics; exclude collaborators and other conflicts of interest]

Corresponding author: Yong Yang, NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China. Email: yangyong1@sgepri.sgcc.com.cn

Thank you for your consideration.

Sincerely,
Bijing Liu, Chenglong Sun, and Yong Yang
