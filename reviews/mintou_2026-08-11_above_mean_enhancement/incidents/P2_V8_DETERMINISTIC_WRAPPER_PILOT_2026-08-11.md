# P2 v8 Deterministic-Wrapper Pilot Incident Record

- Start: 2026-08-11 21:27:11 Asia/Shanghai
- Stop: 2026-08-11 21:29:40 Asia/Shanghai
- Environment: Torch 2.13.0+cu130, RTX 3090; device-resident window indexing was active
- Observed state: the same model--seed function had completed a stand-alone 10-epoch smoke in 3.8 seconds, but the full wrapper did not finish its first unit in about 149 seconds. CUDA belonged to the active process, and no exception was raised.
- Action: terminated to isolate wrapper-level execution settings before another complete run.
- Evidence handling: no result, leaderboard, or partial result file was produced; this pilot is excluded from all manuscript results.
- Next diagnostic: benchmark the wrapper's global thread and deterministic-backend settings around the identical model--seed function. Scientific inputs remain unchanged.

