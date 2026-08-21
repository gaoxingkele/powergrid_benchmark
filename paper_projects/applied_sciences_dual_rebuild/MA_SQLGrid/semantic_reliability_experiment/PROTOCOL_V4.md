# Multi-state reliability protocol v4 — executable preflight freeze

v4 preserves the v3 scientific design unchanged: 18 total states partitioned
into 15 semantic-suite states and 3 physical-order diagnostics; 66 automatic
primary questions; 114 order holds; and frozen denominators 25,920, 7,920, and
16,416.

The v4 repair makes the executable freeze contract complete. It includes the
full canonical-v2-bound `prediction_bindings` and gold-only `pre_score` objects
used by Stage B. Every Stage-B freeze key is asserted by tests.

`--preflight-only` traverses authorization, exact canonical-v2 identity, both
720-key ledger loads, all 18 state identities/runtime locks, the 114-item order
checklist, and canonical-row identity. It then exits before opening a state for
SQL scoring and before creating the requested output directory. A test-only
synthetic PASS audit and launch companion exercise this path; they cannot start
formal scoring because the flag is mandatory in the preflight harness and the
temporary artifacts are destroyed immediately.

Before authorization or ledger trust, Stage B also recomputes SHA-256 and byte
counts for every `frozen_files` entry, immutable questions/database, the
Stage-A manifest, and the launch-approval policy artifact itself.

Invalid audit/companion inputs remain fail-closed. Formal scoring still requires
a real independent `PASS_AUTHORIZE_FORMAL_SCORE` re-audit of this exact v4 SHA
and a companion binding that audit's SHA-256 and bytes.

The v3 freeze and its preflight KeyError incident are retained verbatim. No
formal model suite outcome was written or accessed during v4 repair.
