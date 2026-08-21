# Call Budget, Entry Points, and Go/No-Go

## Budget

Formal budget is 700 calls plus eight warm-ups: 350 + 4 for Qwen and 350 + 4 for Granite. Each formal call requests three candidates in one response, so E2 adds no model calls beyond E1. Existing direct-run medians were approximately 0.375 s/call for Qwen and 0.750 s/call for Granite, but three-candidate output is longer. A conservative normal planning window is 10–25 minutes of inference plus model-server startup/swap and artifact verification. The fail-closed timeout ceiling is much larger and is not a runtime estimate.

Expected new artifacts before analysis are roughly tens of megabytes, not a new dataset download. No network download is needed.

## Ready entry points

1. `python build_freeze.py` — deterministically rebuild prompt/call ledgers; use only before execution starts.
2. `python verify_freeze.py` — fail-closed preflight; currently PASS.
3. Start the frozen GGUF in the pinned llama.cpp backend with exclusive GPU access and retain the exact server command in a run incident note.
4. `python run_frozen.py --model qwen --base-url http://127.0.0.1:<port>/v1 --execute-frozen` (then Granite). The runner verifies the freeze, `/models`, manifest, actual GGUF size and SHA-256; records before/after `nvidia-smi` snapshots in `RUN_MANIFEST.json`; warms up; writes each response immediately; and stops on first failed call. `--resume` is explicit.
5. `python offline_replay.py select --model <model>` — gold-blind parse/rank and selection seal.
6. `python offline_replay.py score --model <model>` — refuses drift, then loads gold and scores.

7. `python aggregate_results.py` — validates every run/selection/scoring hash, executes the registered cluster-aware statistics, applies the frozen Holm families, and emits JSON/CSV/Markdown plus a manifest. It was implemented and tested on synthetic fixtures before any formal output existed.

## Go/no-go

- **E1: GO** for local execution. The intervention is non-degenerate for 170 questions/61 clusters, invariant fields are hashed, and the estimand is honestly named a bundled presented value-evidence effect.
- **E2: GO** for local execution. Candidate generation, a no-repair reference-free selector, and a selection-before-gold seal are specified and implemented. Formal claim promotion remains conditional on extraction completeness and the registered statistics, not effect direction.
- **E4: conditional GO**. Token telemetry is ready. Latency is formal only with exclusive GPU, identical server arguments within a backbone, incident logging, ≥95% zero-retry calls, and no provider failures/throttling; otherwise latency is diagnostic.
- **Broad framework/field efficacy: NO-GO from these experiments alone.** They cannot satisfy the outstanding human-reviewed external/sealed-set or public-baseline requirements.
- **Formal run now: NOT STARTED.** The protocol is ready, but this audit intentionally launched no time-consuming model inference.
