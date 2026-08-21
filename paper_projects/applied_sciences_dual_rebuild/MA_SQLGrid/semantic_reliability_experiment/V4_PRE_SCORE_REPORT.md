# v4 pre-score report

Status: `READY_AWAITING_V4_REAUDIT`.

Repair scope is limited to the executable freeze-key contract and a zero-SQL,
zero-output end-to-end preflight. The state databases, gold coverage,
adjudication, comparator, denominators, inference family, and release design are
unchanged from v3.

The preserved incident record proves v3 failed with missing
`prediction_bindings` before SQL execution and before output creation. v4 binds
both `prediction_bindings` and `pre_score`, refreshes every changed code hash,
and freezes tests that enumerate every Stage-B key.

