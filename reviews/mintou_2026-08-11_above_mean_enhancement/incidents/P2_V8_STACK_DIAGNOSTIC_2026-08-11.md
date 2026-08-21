# P2 v8 Stack Diagnostic Record

- Invocation: explicit workspace source plus `faulthandler` samples every 10 seconds and a predeclared 35-second diagnostic exit
- Outcome: 12 model--seed units completed before the diagnostic timer exited the process (48 reconciliation rows plus header)
- Stack observations: active frames were in the expected Torch linear forward and autograd backward paths; no deadlock, I/O stall, or unintended code path was observed
- Preserved partial: `P2_V8_STACK_DIAGNOSTIC_PARTIAL_EXCLUDED.csv`
- Preserved SHA-256: `C1E8948AF8C553EC0C3BB255D7A3AFEABE61FCFA4869C2D778C50CFEBBF1500A`
- Manuscript status: excluded, because the diagnostic invocation was deliberately incomplete
- Resolution: delayed tool output, rather than a slow scientific unit, explained the apparent stall. A normal complete invocation may proceed under the frozen protocol.

