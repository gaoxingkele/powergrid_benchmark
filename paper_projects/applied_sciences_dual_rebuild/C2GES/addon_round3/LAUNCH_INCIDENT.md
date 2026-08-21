# Add-on launch incident record

- Initial command: `python run_addon.py`
- Start: approximately `2026-08-05T16:58:10+08:00`.
- Incident: the orchestration shell call used a short yield/timeout and returned timeout status after about five seconds. The Windows Python launcher and its five first-wave child processes survived the shell timeout.
- Verification: PID-level inspection found launcher PID 16744 and child PIDs 1276, 18440, 26368, 27640, and 28136, all with the same start time and increasing CPU time. Direct logs showed active document loading, encoder loading, and train-example encoding.
- Safety response: no relaunch was performed. Partial run directories are not classified as successful until each contains a success `resource_usage.json` plus the complete frozen artifact set. The exact surviving process set is monitored to completion before any new execution.
- Scientific impact: none; no outcomes were inspected or aggregated, no configuration changed, and the protocol freeze predates the launch.

## Cross-encoder wrapper incident

After all ten learned runs succeeded, the orphaned launcher exited before cross-encoder execution. An isolated attempt then failed before model loading because the resource wrapper created `runs/cross_encoder`, while the frozen cross-encoder runner requires its output directory not to exist. The failed directory and status record are preserved. No candidate was scored. The scoring run uses the unchanged frozen command in fresh `runs/cross_encoder_prospective`, with process logs stored separately so the runner can own its output directory.
