# P2 s4 Experiment Protocol

**Status:** `METHOD_TASK_CONTRACT_IMPLEMENTED / INPUT_REGISTRIES_NO-GO / NO_RESULTS`
**Purpose:** Applied Sciences grid-investment evaluation with NDS-only, forward-only, backward-only, and bidirectional arms over two independent task families.  
**Protected predecessor:** `../p6_s3_matched_effort/` is read-only.

Before any formal run, freeze task-family provenance, action/cost semantics, repair behavior, unique-evaluation accounting, seed list, baseline budgets, HV/IGD+ reference rules, comparison family, multiplicity correction, failure policy, and output schema. Pilot outputs must be separated from formal outputs. The existing negative comparison with NSGA-II remains reportable context regardless of new outcomes.

No cybersecurity semantics and no numeric result are introduced by this scaffold.

The prospective implementation contract is frozen in `method_task_contract.json`,
with executable invariants in `../../scripts/p2_s03_method_task_contract.py` and
the reader-facing specification in
`../../manuscript/reconstruction_v2/METHOD_TASK_IMPLEMENTATION_CONTRACT.md`.
It defines separate RTS-GMLC branch-reinforcement and SimBench
line-reinforcement task generators. Formal runs remain prohibited until their
independent source/action registries and traceable cost-model inputs pass the
documented gates. `backward_only` denotes standalone deletion; atomic
delete--insert substitution is a separately gated control. Evaluation budgets
count cache-miss phenotypes once, retain all requests and cache hits, and use a
request cap as the duplicate-loop backstop. Records and counters are diagnostic
bookkeeping, not an audit mechanism.
