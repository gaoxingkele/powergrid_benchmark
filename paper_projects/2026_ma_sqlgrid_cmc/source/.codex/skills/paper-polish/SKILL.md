---
name: paper-polish
description: Polish an existing LaTeX paper (light wording changes, remove AI flavor). Inherits the general academic English writing rules and adds a latexq-based per-section polishing workflow. Use when asked to polish, refine prose, or remove AI-sounding expressions from an existing LaTeX manuscript.
license: Complete terms in LICENSE.txt
---

# Paper Polish (LaTeX, EN)

## Scope
Use this skill to *polish* an existing scientific paper in English LaTeX. The paper is already drafted; the task is light wording-level refinement: improve flow, tighten clarity, remove AI-flavored expressions. Not for first-draft writing or structural rewrites.

**Repo context**: This workspace has `paper.tex` and `references.bib` at the root for English paper drafting. Use `python tools/check_cites.py` to verify citation hygiene (compares cited keys vs .bib entries).

Non-goals:
- Do not change technical claims without evidence.
- Do not add citations you cannot justify; prefer asking for sources or marking TODOs.
- Do not over-rewrite: preserve the author's voice and intent.
- Do not restructure (move/merge/split sections, reorder).
- Do not change cite keys, equations, numbers, labels, or experimental conclusions.

## Default Working Mode (recommended)
1. **Clarify the target**: venue style (IEEE/ACM/Elsevier), section(s), word/page constraints.
2. **Outline-first**: propose bullet outline before writing full prose when structure is unclear.
3. **Evidence-first**: every nontrivial claim should have a citation, data, or qualification.
4. **LaTeX-native**: write as valid LaTeX, using semantic commands (`\section`, `\subsection`, `\label`, `\ref`, `\cite`).

## IMRAD Writing Heuristics
### Introduction (pattern)
- Context: what area + why it matters.
- Problem: what concrete limitation exists.
- Gap: what prior work misses (cite).
- Objective: what this paper does.
- Contributions: 2–4 bullet contributions.
- Paper organization: brief roadmap.

### Related Work
- Group by approach/theme (not by author).
- For each group: what it solves, what it assumes, and limitations.
- End with a *positioning paragraph*: what you do differently.

### Methodology
- Write for reproducibility.
- Include: data (source/splits), model/architecture, training details, baselines, evaluation metrics.
- Explicitly state assumptions and limitations.

### Results
- Report numbers with context (dataset, metric, split, N).
- Prefer tables/figures; reference them in text.
- Avoid "promising" language; be precise.

### Discussion
- Interpret results: *why* it worked/failed.
- Compare to baselines and related work.
- Discuss threats to validity.

### Conclusion
- Summarize contributions and key results.
- State limitations.
- Propose realistic future work.

## Citation & Cross-Reference Rules
- Place citations immediately after the claim: `... improves generalization \cite{key}.`
- For multiple sources: `\cite{key1,key2}` (or project-specific citation commands).
- Always `\label{sec:...}` sections you may reference later; reference with `\ref{sec:...}`.

## LaTeX Style Checklist
- Consistent terminology (same term for same concept).
- Acronyms: define on first use, then use acronym consistently.
- Use proper LaTeX quotes: ``like this''.
- Prefer `booktabs` in tables (`\toprule`, `\midrule`, `\bottomrule`) when available.

## Quality Checklist
- Objective and contributions are explicit.
- Claims are either cited, measured, or qualified.
- Method is reproducible.
- Results support conclusions.
- LaTeX compiles without errors.

## Citation Hygiene (repo-specific)
After writing/editing, run citation check:
```bash
python tools/check_cites.py
```
This reports:
- Missing .bib entries for cited keys.
- Unused .bib entries (optional cleanup).

If PDFs are in `papers/`, extract abstracts with:
```bash
python tools/extract_papers.py
python tools/review_papers.py
```

---

## Polish Workflow

When polishing an existing `paper.tex`, use the `latexq` CLI (`lq`) to slice the manuscript by section instead of reading the whole file. This avoids token waste and keeps changes contained.

Invoke via uvx (no install required):
```bash
uvx --python 3.12 --from latexq lq <subcommand> ...
```
First call is ~10s (one-time Python 3.12 fetch); subsequent calls <1s.

### Commands
```bash
# See the section tree
uvx --python 3.12 --from latexq lq graph --input-file paper.tex --format text --stdout

# Extract one section
uvx --python 3.12 --from latexq lq select --input-file paper.tex --query '@sec:introduction' --stdout

# Extract a section together with its subsections (list each explicitly, whitespace-separated)
uvx --python 3.12 --from latexq lq select --input-file paper.tex \
  --query '@sec:method @sec:<subsection-a> @sec:<subsection-b>' --stdout
```

Notes:
- A parent query (`@sec:method`) returns only the section header — list subsections explicitly to include them.
- Multi-selector uses **whitespace**, not comma or pipe.
- Selections include `\section{...}` and `\label{...}` — don't duplicate them when writing back.

### Loop
For each target section: `lq select` → polish in memory → show before/after diff → wait for user OK → Edit tool writes back into `paper.tex` (preserve `\section` / `\label`) → `git commit -m "polish(<section>): ..."` → ask whether to continue.

### Removing AI flavor
LLM-generated prose shares common tells. Treat these as flags to re-evaluate, not a ban list — keep them when genuinely correct.

Common word flags: `delve`, `furthermore`, `moreover` (stacked at paragraph starts), `leverage` (verb), `paradigm shift`, `at its core`, `it is worth noting that`, `in the realm of`, `cutting-edge`, `seamlessly`, `harnessing the power of`, `unlock the potential of`.

Structural flags:
- Uniform sentence length (most sentences 15–25 words). Mix in short ones.
- Transition word at every paragraph start. Vary with direct topic sentences.
- Triple lists (`X, Y, and Z`) everywhere. Break the rhythm with single or paired examples.
- Over-confident phrasing where claims depend on data. Restore `may`, `suggests`, `is consistent with`.
- Conclusion sentence merely restating the opening. Cut or replace with the actual implication.

## Prompt Patterns (polish)
- "帮我润色 Introduction，去 AI 味"
- "polish the Discussion section, keep all claims and numbers intact"
- "scan the whole paper for AI tells, then we'll go section by section"
