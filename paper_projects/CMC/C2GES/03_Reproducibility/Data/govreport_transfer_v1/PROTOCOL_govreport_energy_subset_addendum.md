# Addendum — GovReport energy subset (frozen 2026-09-26, before any subset outcome)

Parent protocol: `PROTOCOL_govreport_transfer_v1.md`. This addendum changes **only the document
selection**; the arms, budgets, endpoint, statistics and decision rules are unchanged.

## Selection rule (fixed now)

A report belongs to the energy subset when its text matches **at least three distinct** entries of
the fixed keyword list below. Matching is case-insensitive on the report body only (the reference
summary is not used for selection).

```
department of energy, doe, electric grid, electrical grid, power grid, transmission,
distribution system, power plant, power system, electricity, electric utility, utility
grid, renewable, solar, wind power, nuclear, natural gas, hydropower, coal, energy
storage, battery storage, grid reliability, energy efficiency, crude oil, pipeline
```

The list is deliberately broad and mechanical; it selects reports *about* energy topics, not
power-system incidents. Nothing here is tuned on outcomes: the rule was written before the subset
was formed.

## What this subset can and cannot show

* It can show whether the out-of-domain path-layer bound of the parent layer also holds on the
  energy-related part of GovReport, which is the closest public analogue of the paper's target
  domain.
* It cannot show domain construct validity: these are policy, audit and programme reports, not
  incident reports, and the cue lexicon is still the power-domain one.
* Selection is by topic words, so the subset is a convenience stratum, not a random sample of
  energy-domain documents.

## Reporting rule (fixed now)

Report the subset size, the same four budgets, the path-layer mean with its discordant split and
one-sided 95 % bootstrap upper limit, and the role-layer mean. No new significance claim is made
unless the parent criteria H2 (mean ≤ 0 and positive share ≤ 50 %) and H3 (upper limit < +0.005)
hold **inside the subset**; otherwise the subset is reported as descriptive only.

## Runner

The subset reuses the parent runner with a filtered corpus file:

```
python -B run_govreport_transfer.py --corpus <energy_subset.jsonl> --documents <n> --json <out.json>
```

where `<energy_subset.jsonl>` is produced by `select_energy_subset.py` from the fetched test split.
