# C2GES Applied Sciences Experiment Plan

## Evidence policy

The main quantitative benchmark is the filtered FEVER sentence-selection set
with public human annotations. Public NERC reliability reports are application
material only until two independent human/domain experts annotate a frozen
domain test set and a third expert adjudicates disagreements. AI-simulated
labels must never be described as human, expert, or gold labels.

## Research questions and registered matrix

1. **RQ1---ranking quality:** compare C2GES with Lead-K, TF--IDF, BM25, SBERT,
   a lexical-role baseline, query-only, no-role, and no-chain ablations on the
   frozen FEVER test split.
2. **RQ2---training robustness:** train seeds 2026--2030; report mean, sample
   standard deviation, minimum, and maximum evidence F1. Keep dataset splits,
   encoder, epochs, and tuning rules fixed.
3. **RQ3---budget sensitivity:** evaluate K in {1, 3, 5, 10} from each frozen
   checkpoint. K=3 remains the registered primary endpoint.
4. **RQ4---encoder robustness:** repeat the five-seed matrix with MiniLM and one
   stronger frozen sentence encoder selected before viewing test results.
5. **RQ5---engineering transfer:** freeze at least 200 NERC role-conditioned
   questions spanning at least 20 reports. Two power-system experts annotate
   sentence IDs independently; report exact agreement, sentence-level Cohen's
   kappa, adjudication rate, and role-stratified results.
6. **RQ6---operational cost:** report parameter count, training time, inference
   latency, peak memory, and sentences processed per second on a named machine.

## Statistical protocol

- Primary metric: macro mean per-question evidence F1 at K=3.
- Secondary metrics: evidence precision, recall, exact evidence-set match, and
  role-stratified F1.
- Use paired document-cluster bootstrap confidence intervals because multiple
  questions can share a document. Use 10,000 resamples for the final paper.
- Correct the family of primary C2GES-versus-baseline comparisons with Holm's
  procedure. Report effect sizes and confidence intervals, not p-values alone.
- Do not tune on the test split. The development split selects the checkpoint;
  K sensitivity is descriptive and does not replace the registered K=3 result.

## Execution

```powershell
python source/code/c2ges_learnable.py --eval-k 1,3,5,10 --bootstrap-samples 10000
python source/code/run_applsci_seed_sweep.py --seeds 2026,2027,2028,2029,2030 --eval-k 1,3,5,10 --bootstrap-samples 10000
```

The NERC human study is a blocking experiment for domain-level superiority
claims; it cannot be completed from the current workspace without real expert
annotations.
