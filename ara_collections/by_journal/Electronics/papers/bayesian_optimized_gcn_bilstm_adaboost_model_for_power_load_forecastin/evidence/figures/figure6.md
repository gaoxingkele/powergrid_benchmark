# Figure 6: Adaboost structure

- **Source**: Figure 6, §2.4 (page 9, middle of page)
- **Caption**: "Adaboost structure."
- **Screenshot**: figure6.png (full-page render of p.9)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - *training data* (purple box, left).
  - Ten parallel chains: *Sample Weight k* (pink) → *Weak learner k* (blue) → *Weak learner
    weight k* (green), for k = 1, 2, …, 10 (rows 1, 2 and 10 drawn; vertical ellipses indicate
    3–9).
  - *Weighted combination* (green box) → *Strong learner* (yellow box, right).
- **Connections**: training data fans out to every sample-weight node; between consecutive rows a
  labeled arrow "Update the sample weight 2 based on the weak learner 1." (…, "Update the sample
  weight 10 based on the weak learner 9.") encodes the sequential boosting dependency; every weak
  learner weight feeds the weighted combination that yields the strong learner.
- **What it conveys**: the boosting loop of §2.4 — each of the 10 GCN-BiLSTM weak learners is
  trained under sample weights updated from the previous learner's errors (Eqs 11–16), and the
  final predictor is the weighted combination of all weak learners. Note the learner weights are
  NOT normalized at this stage; normalization is deferred to the Bayesian testing phase (Eqs
  18–19). Supports C04. Mirrored into `logic/solution/algorithm.md`.
