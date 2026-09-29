# Information cover letter — C2GES diagnostic submission

Bound to the current paper_information.tex. Not approved for sending.

Suggested section: Information Applications (or Artificial Intelligence).

## Draft

Dear Editors of *Information*,

Please consider our manuscript, “C²GES: A Diagnostic Evaluation of
Role-Conditioned Extractive Summarization for Long Power-System Technical
Reports,” by Bijing Liu and Yong Yang.

The information-science question is whether typed structural additions
supply discriminative information that lexical relevance and dense
similarity do not already carry. C²GES is a deterministic, source-linked
extractive selector. Role heuristics, a typed textual proxy graph, and a
path-deletion term are added incrementally and then removed under
controlled configurations.

The study is diagnostic, not confirmatory. The main diagnosis is that
the length-controlled, normalized path term did not show a stable gain:
on a post-access seven-series pilot at matched 110- and 260-word
budgets, Full-minus-no-path was −0.00799/−0.00718, TextRank ranked first
at 110 words (0.1690), and no-path C²GES ranked first at 260 words
(0.1844). That is not an equal-unit ROUGE win. On 15 retained NERC
reports at equal unit counts, Full C²GES recovered more
Executive-Summary wording than Semantic-MMR and TextRank, but the
extracts were 54–63% longer and no matched-word contrast survived Holm
adjustment; the unrenormalized coefficient-removal comparison is a
scale-coupled historical diagnostic. Typed-minus-untyped graph effects
did not agree in sign and both intervals crossed zero. A two-model
machine audit is not human or expert validation.

The paper is positioned inside this journal's own literature rather than
only against general-domain systems: four same-journal studies anchor the
comparison, covering graph-based extractive sentence scoring, long-document
summarization evaluation on domain corpora, summarization evaluation
methodology, and a structured-summarization evaluation that pairs automatic
measures with a human assessment survey. That last work is the reason the
present manuscript separates automatic reference overlap from construct
validity and states, in a dedicated table, which claims stay closed until an
independently annotated study is completed.

The manuscript does not claim system superiority, semantic validity of
the structural proxies, or operational benefit. No-path C²GES is the
simpler provisional default. Tool assistance used in manuscript
preparation and in the machine audit is disclosed in Materials and
Methods and in the Acknowledgments.

The manuscript is original to this submission, is not under consideration
elsewhere, and will be uploaded only after all authors have approved this
version. The authors declare no conflicts of interest. Funding, CRediT
roles, and data access are stated in the manuscript. Source PDFs and
verbatim derived text subject to third-party restrictions are excluded
from the public package.

Thank you for your consideration.

Sincerely,

Yong Yang
Corresponding author
yangyong1@sgepri.sgcc.com.cn
NARI Group Corporation (State Grid Electric Power Research Institute)

## Author must still confirm

- Suggested section on SuSy: Information Applications (or Artificial
  Intelligence).
- If SuSy asks about prior submission history, answer it there.
- That yangyong1@sgepri.sgcc.com.cn is the portal email for this paper.
- Originality, exclusive submission, and all-author approval for THIS file.
- SuSy generative-AI checkbox: match Materials and Methods (tools were used).
