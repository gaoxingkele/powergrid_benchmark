# P6 S3 matched-effort experiment

This stage-local package runs new comparisons of BiLo-NSGA, NSGA-II, and
Pareto Local Search on the eight registered P6 scenarios. It reads the shared
candidate builder and problem definition but does not modify the shared P5/P6
source or either paper's pre-existing evidence archive.

The frozen design is in `config.json`. There are two comparison protocols:

- `matched_evaluation`: exactly 3,200 evaluation units per run. One unit is
  charged for a newly scored population candidate or for an evaluated local
  proposal. Repair and ranking operations use already visible candidate
  attributes and do not consume an objective-evaluation unit.
- `matched_time`: the same algorithms, scenarios, and seed schedule run to a
  0.20-second search deadline. Hypervolume calculation is outside the search
  deadline and both target and realized search time are retained.

All methods see the same scenario pool, budget, objectives, fixed empirical
normalization bounds, and seed index. The stage-local NSGA-II is fully
specified in the config because the host's installed `pymoo==0.4.1` cannot run
the repository's recorded `pymoo==0.6.2` import paths. No different pymoo
release is silently substituted. The BiLo-NSGA and PLS implementations retain
the disclosed project representation and move semantics, with explicit
evaluation accounting added here.

The primary inferential family contains the 16 matched-evaluation contrasts
of BiLo-NSGA against two comparators in eight scenarios. It uses an exact
two-sided paired sign test across 30 common seed indices and one Holm
correction. The matched-time protocol has its own separately declared
16-contrast secondary family. Hypervolume normalization/reference sensitivity
and local-parameter sensitivity are descriptive and emit no p-values.

Run from the harness repository root:

```powershell
python paper_projects/mintou_p6_bilonsga_project_review/experiments/p6_s3_matched_effort/run_experiments.py `
  --config paper_projects/mintou_p6_bilonsga_project_review/experiments/p6_s3_matched_effort/config.json `
  --output-root paper_projects/mintou_p6_bilonsga_project_review/experiments/p6_s3_matched_effort/runs/new_run
```

Output roots are immutable: the runner refuses to write to an existing path.

## Scientific-closure scope notes

- The metered BiLo-NSGA runner is a stage-local implementation, not an exact semantic replay of the legacy broad-archive code. The legacy code freezes normalization bounds on parents plus pre-repair offspring and uses a `1e-9` denominator floor; this runner freezes bounds on parents plus the repaired child and uses `1e-12`. The retained results therefore apply to this metered implementation.
- The `depth_2`, registered-depth, and `depth_16` cells jointly set forward/backward proposal caps to `(2, 2)`, `(8, 4)`, and `(16, 8)`. They support only a joint-depth conclusion.
- The local sensitivity grid is one-factor-at-a-time. It does not identify interactions among depth, penalty, and group bonus.
- NSGA-II has no repair operator in this runner. Its reported final-feasibility rate is empirical rather than guaranteed by construction.

