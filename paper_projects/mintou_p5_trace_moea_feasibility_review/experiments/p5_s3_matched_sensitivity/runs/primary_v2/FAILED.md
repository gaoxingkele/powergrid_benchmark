## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Verification Status: UNVERIFIED
- Version Label: p5_s3_primary_v2_terminated

## Terminated runtime attempt

This attempt was stopped before the first method-cell completion marker while
diagnosing the free-threaded, pure-Python pymoo runtime. No result CSV or
analysis artifact was written, and this directory is not used as evidence.

Single-run profiling subsequently confirmed that the shared TRACE engine and
the exact hypervolume helper were responsive; the slowdown occurred in the
uncompiled pymoo comparator path. The next attempt uses the normal-GIL host
interpreter with the explicitly documented distance-only SciPy compatibility
surface. Statistical calls remain disabled.
