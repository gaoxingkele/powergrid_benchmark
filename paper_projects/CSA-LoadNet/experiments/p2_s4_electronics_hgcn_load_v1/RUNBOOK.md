# P4 s04 Frozen Runbook

**State:** protocol only; no command below has been executed as a scientific run.

1. Materialize only the two sources named in `data_manifest.json`. Verify the
   inherited OPSD hash; record every Ausgrid raw-file hash. Attach source-specific
   licence evidence. Stop if identity, integrity, permitted use, or redistribution
   scope remains unresolved.
2. Run the frozen parsers without changing row rules. Persist processed files,
   rejection/empty-cell ledgers, node maps, timestamp maps, and SHA-256 hashes.
   Resolve every frozen development and formal anchor to a processed index. Stop
   if any anchor or complete 672-origin block is unavailable.
3. Verify the Stage-3 implementation bindings in `data_manifest.json`, then run
   `python verify_implementation.py`. This checks synthetic invariants only and
   is not a pilot or result.
4. Implement a runner that reads `config.json` without fallback defaults and
   emits every required field. Record its hash. Verify graph and normalization
   fits use only each block's training prefix and that future perturbation cannot
   alter them.
5. Lock the exact runtime described by `environment.json`. Run the two-seed,
   one-development-block Ausgrid pilot under `pilot/`. Check shape, graph,
   leakage, determinism, numerical events, schema, wall time, and peak memory.
   Pilot metrics remain `paper_use=false` and cannot select settings.
6. Obtain resource acceptance using pilot timing only. Rejection is a documented
   no-go; it does not authorize fewer models, seeds, origins, candidates, or
   epochs.
7. Execute all eight candidate configurations for the five trainable families
   on both datasets, three development blocks, and three development seeds: 720
   tuning runs. Release all rows and select by median block WAPE with the frozen
   lexicographic tie rule.
8. Lock the selected configurations and hashes. Generate identity/random graphs;
   ablation arms inherit the same-geometry real-graph selection and are not
   retuned.
9. Confirm zero overlap between development and formal anchors/seeds. Hide formal
   test targets from tuning and checkpoint selection. Execute nine trainable
   arms over two datasets, eight blocks, and five paired seeds (720 runs), plus
   one deterministic persistence output per dataset-block (16).
10. Preserve every failure. Do not add runs, substitute seeds, impute failures,
    change graphs, or inspect favorable subsets.
11. Average seeds within method--dataset--block, then evaluate the single
    14-contrast WAPE family by exact paired sign-flip tests and Holm correction.
    Emit all primary, secondary, efficiency, stability, null, adverse, and
    incomplete results. Update `planned_vs_executed.json` and hash every artifact
    before any manuscript result edit.

Formal execution is blocked while the source/licence manifest, processed hashes,
anchor map, runner, runtime pilot, or resource-acceptance gate is incomplete.
