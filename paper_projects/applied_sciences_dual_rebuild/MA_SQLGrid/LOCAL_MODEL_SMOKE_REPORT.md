# MA-SQLGrid Local Model Smoke Report

## Outcome

The independently resumed workflow completed one real development question in all four 2x2 factorial cells. All four provider calls succeeded and yielded safely executable read-only SQL. There were no provider or parse errors. This is diagnostic only: gold scoring was disabled, `correct` is null in every score, and `canonical_result_eligible=false`.

## Exact real outputs

| Cell | Raw response | Extracted SQL | Latency | Tokens in/out | Response SHA-256 |
|---|---|---|---:|---:|---|
| F00_Full_NoShape | `SELECT COUNT(*) FROM assets WHERE status = 'in_service';` | same | 610 ms | 2439/13 | `6ae5f528a7502ebe65e2ef517b41681849d293f344af2d25a8a66cf9382e8fed` |
| F01_Full_WithShape | `SELECT COUNT(*) FROM assets WHERE status = 'in_service';` | same | 625 ms | 2481/13 | `6ae5f528a7502ebe65e2ef517b41681849d293f344af2d25a8a66cf9382e8fed` |
| F10_Compact_NoShape | `SELECT COUNT(*) FROM assets WHERE status = 'in_service'` | normalized with semicolon | 250 ms | 413/13 | `f6fbc066b8246c38fe41ee03d55c415aa920685e5d36b8007c16f6b10f25ab78` |
| F11_Compact_WithShape | fenced SQL containing the same query | fence removed | 218 ms | 453/17 | `69d1916f00bfb3183a386be75e88fe337c30374ffe3db7a0e4d928d928c25b42` |

Each score has `status=diagnostic_only`, `exec_ok=true`, `shape_ok=true`, and `correct=null`. The loopback-only server was stopped by verified PID; neither process nor port-8080 listener remained. These records establish adapter, parsing, safety, SQLite execution, and GPU viability only—not accuracy or a factorial effect.
