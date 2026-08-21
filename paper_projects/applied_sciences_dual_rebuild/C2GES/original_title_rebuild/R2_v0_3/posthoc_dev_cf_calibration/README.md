# C2GES post-unblinding development-only CF calibration

This directory is an exploratory sensitivity analysis created only after the
frozen v0.3.1 formal result had been revealed. It does not overwrite, rerun, or
reinterpret the v0.3.1 formal test. The executable accepts no command-line data
path and reads only the hash-pinned 12-report development JSONL and the audited
run04 development decision.

The held-out test JSONL and all formal predictions, aggregates, and contrasts
are forbidden inputs. Any configuration suggested here requires a newly
acquired, never-inspected external holdout and a new v0.4 freeze before it can
support a confirmatory claim.
