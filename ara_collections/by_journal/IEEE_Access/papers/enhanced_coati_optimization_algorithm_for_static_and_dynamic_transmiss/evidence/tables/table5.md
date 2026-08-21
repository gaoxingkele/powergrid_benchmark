# Table 5 - CEC2020 Wilcoxon test results of the COA algorithm and its variations with FDB

**Source**: Table 5, §III-B (p.35079)
**Caption**: "CEC2020 Wilcoxon test results of the COA algorithm and its variations with FDB."
**Screenshot**: table5.png (middle of page)
**Extraction type**: raw_table

Each cell is `+/=/-` (wins / ties / losses) of the row algorithm **vs baseline COA**. "+" = victory over classical COA, "=" = draw, "-" = defeat.

## CEC2020, Pop-size = 30
| vs COA | Dim=5 | Dim=10 | Dim=15 | Dim=20 | Dim=30 | Dim=50 | Dim=100 |
|--------|-------|--------|--------|--------|--------|--------|---------|
| FDBCOA1 | 4/6/0 | 7/3/0 | 5/5/0 | 6/4/0 | 6/4/0 | 7/3/0 | 7/3/0 |
| FDBCOA2 | 3/7/0 | 4/6/0 | 6/4/0 | 7/3/0 | 7/3/0 | 7/3/0 | 8/2/0 |
| FDBCOA3 | 1/9/0 | 4/4/2 | 4/6/0 | 3/6/1 | 5/5/0 | 5/5/0 | 6/4/0 |

## CEC2020, Pop-size = 50
| vs COA | Dim=5 | Dim=10 | Dim=15 | Dim=20 | Dim=30 | Dim=50 | Dim=100 |
|--------|-------|--------|--------|--------|--------|--------|---------|
| FDBCOA1 | 5/5/0 | 6/4/0 | 5/5/0 | 7/3/0 | 6/4/0 | 7/3/0 | 7/3/0 |
| FDBCOA2 | 2/8/0 | 5/5/0 | 7/3/0 | 7/3/0 | 8/2/0 | 7/3/0 | 8/2/0 |
| FDBCOA3 | 3/7/0 | 3/7/0 | 5/5/0 | 5/5/0 | 5/5/0 | 4/6/0 | 6/4/0 |

## CEC2020, Pop-size = 100
| vs COA | Dim=5 | Dim=10 | Dim=15 | Dim=20 | Dim=30 | Dim=50 | Dim=100 |
|--------|-------|--------|--------|--------|--------|--------|---------|
| FDBCOA1 | 2/5/3 | 6/4/0 | 5/4/1 | 6/4/0 | 6/3/1 | 7/3/0 | 7/3/0 |
| FDBCOA2 | 3/6/1 | 4/6/0 | 6/4/0 | 7/3/0 | 6/4/0 | 8/2/0 | 8/2/0 |
| FDBCOA3 | 1/9/0 | 3/7/0 | 5/5/0 | 6/4/0 | 6/4/0 | 5/5/0 | 7/3/0 |

**Note (aggregate, §III-B)**: FDBCOA1 lost 6 out of 282 problems across population sizes 30/50/100, drew 110, won 166 — win rate 58.86%, draw 39.01%, loss 2.13%. Note the residual losses concentrate at P=100 Dim=5 (FDBCOA1 2/5/3).
