# Reference-type sensitivity layer — protocol v1 (frozen 2026-09-26, before any outcome)

Purpose: the paper's standing caveat is that **every** reference used so far is a human
*abstractive* summary, capped by the wording mismatch that extractive systems cannot close. This
layer asks whether the path-layer result is an artefact of that reference type by re-running the
frozen arm set against **human-written highlights** that are largely verbatim spans of the source
article.

## 0. What this layer cannot show (fixed before running)

1. The corpus is news, not power-system or government technical reports: this is a
   **reference-type** contrast, not domain evidence.
2. CNN/DailyMail highlights are human-written bullet points that copy article wording heavily;
   they are *close to* extractive but are not a sampled extractive oracle, and the articles are
   much shorter than the paper's target reports.
3. Any result here is reported as a sensitivity of the reference definition; it does not change
   any domain claim.

## 1. Corpus

| Item | Value |
|---|---|
| Source | `abisee/cnn_dailymail` (HuggingFace), configuration `3.0.0`, split `test` |
| Reference | the human-written `highlights` field, joined in order |
| Document | the `article` field with `(CNN)`/`(Daily Mail)` by-lines and `@highlight` markers removed |
| Local raw copy | `05_External_Prospective_20260922/cnndm/` (**outside the release scope**) |
| Shipped | derived numbers only |

## 2. Sampling (fixed now)

Test split, five strata by article character length, 80 rows per stratum,
`random.Random(20260926)` → **n = 400**. Strata are formed on the fetched slice of 2,000 rows
(twenty pages of 100) drawn from the beginning of the test split, which is the documented
procedure below; the slice is recorded in the acquisition log.

## 3. Units

Deterministic sentence segmentation of the cleaned article, dropping units shorter than three
words; `sid = u%05d`; `unit_type = body`. Reference = the cleaned highlights text, untruncated.

## 4. Arms and budgets

Identical to the frozen external arm set: AB0, AB1, AB2, no_path, Full (path weight 0.10),
TextRank, Lead, at word 110/260 and unit K = 5/10. No tuning.

## 5. Endpoints and criteria (fixed now)

* **H2** (primary): Full − no_path mean ≤ 0 and positive share of discordant documents ≤ 50 %.
* **H3** (primary): one-sided 95 % bootstrap upper limit on Full − no_path < +0.005.
* **Reference-type contrast**: compare the path-layer mean and upper limit here with the
  abstractive-reference layers (external prospective, transfer). State explicitly whether the
  bound is reference-type dependent.
* **H1** (exploratory, role layer): reported with the same sign-share and bound treatment; the
  cue lexicon is still the power-domain one, so a negative result here means cue mismatch, not a
  property of the role construct.
* Statistics: exact sign flip for n ≤ 20, otherwise 10⁵ randomised sign flips; Holm inside the
  contrast family; zero mass and discordant split reported for every contrast.

## 6. Red lines

No tuning on outcomes, no pooling with the power-domain or transfer layers, no verbatim news
text inside the release scope, and no claim that this replaces an expert-judged extraction
quality study (that is the E2 layer).
