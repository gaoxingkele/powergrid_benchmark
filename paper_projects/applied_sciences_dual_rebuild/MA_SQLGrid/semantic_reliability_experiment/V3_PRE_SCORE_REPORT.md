# v3 pre-score repair report

Status: `READY_AWAITING_V3_REAUDIT`.

No Stage-B candidate execution or multi-state model outcome was produced or
opened during this repair. The 18 v2 state databases and traces are unchanged.

Repairs implement all five v2 re-audit blocks:

1. protocol denominator is exactly 18 = 15 semantic + 3 physical diagnostics;
2. reviewer A, reviewer B, and adjudication are byte/hash bound and their chain
   is live-verified;
3. Stage B requires `PASS_AUTHORIZE_FORMAL_SCORE`, exact freeze identity, all
   ten gates PASS, and a launch companion binding audit SHA/bytes;
4. canonical-v2 freeze and canonical row files are physically verified live;
5. frozen analysis/release programs enforce 25,920/7,920/16,416 denominators,
   15-state AND, T0 consistency, fixed clustered/Holm inference, and complete
   atomic-to-CSV/TeX/SVG lineage.

All tests are pre-score and use gold-only artifacts or synthetic atomic rows.

