# Independent rerun verification

The `p1_s3_fair_v1` script was copied without modification into this separate
verification parent and rerun on 2026-08-13 with the same frozen configuration,
hashed RTS-GMLC inputs, seed list, and RTX 3090. The script directory retains
the required namespace name, while the parent directory separates the rerun
from the primary artifact.

## Identity checks

- Configuration SHA-256: `bb0a920069490b6c4fcbc015849358a653a3c3710c0c51a19bb8e782e74e2c69`
  in both runs.
- Script SHA-256: `4f209a5faf1071aa2b7da78a7556aa331026f4581df8e759f17d8e568b7958fe`
  in both runs.
- Source-file SHA-256 values and row counts match the primary manifest.
- Both runs contain 510 method--seed result rows.

## Result comparison

All non-timing fields in the 510 rows are identical. The following scientific
outputs are byte-identical to the primary run:

| File | SHA-256 |
|---|---|
| `leaderboard.csv` | `6A84DBB2974C3964A63D396D01BEAB8049BA0AF6742055B57DD06CC20E5D4A85` |
| `paired_primary.csv` | `303D14A7FE9243815768D3FFB382BCD477687C3FD5337B71775630E5016C5B0D` |
| `cap_sensitivity.csv` | `6320C5B70CDD904B15D5D4EFBAF6FF109D061D4B72F7986206B0505B3463E210` |
| `policy_transform_audit.csv` | `3C658C3E9773DDF1FCD0FE60C9E4B0BC209D3A6FB52C9F7ED1B904190C1D9208` |

The raw result CSVs are not byte-identical because `runtime_s` differs for all
510 rows. This field is a wall-clock measurement, not a model output or an
analysis input. The original run used Python 3.12.13 with NumPy 2.3.5; the
independent rerun used Python 3.12.10 with NumPy 2.4.6. Both used PyTorch
2.13.0+cu130 on the same RTX 3090. No claim of byte-for-byte replay is made for
the timing-bearing raw table.

## Verification status

The scientific outputs and all derived statistical conclusions reproduced.
This record does not broaden the data-vintage or operational-forecasting scope
declared in the primary evidence boundary.
