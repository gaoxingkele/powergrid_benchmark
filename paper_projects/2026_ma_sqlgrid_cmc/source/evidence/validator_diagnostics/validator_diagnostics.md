# MA-SQLGrid Validator Diagnostics

## C5 Selection Behavior

- C5 traces: 180
- Selected a non-first candidate: 22/180
- Nonempty repair response accepted: 15/180
- Selected SQL executable: 175/180
- Selected SQL shape-compatible: 175/180
- Selected SQL order-compatible: 180/180
- Selected execution-error taxonomy: {'no such column: wo.schedule_date': 4, 'no such column: wo.schedule': 1}

## Offline Ranker-Weight Sensitivity

| variant | changed selections | correct | execution accuracy |
|---|---:|---:|---:|
| default_recomputed | 3/180 | 132/180 | 0.7333 |
| no_shape_term | 3/180 | 132/180 | 0.7333 |
| no_value_terms | 11/180 | 136/180 | 0.7556 |
| no_order_empty_terms | 1/180 | 131/180 | 0.7278 |
| exec_only | 11/180 | 136/180 | 0.7556 |

## Residual Execution Errors

| condition | execution errors | taxonomy |
|---|---:|---|
| C4_MASQLGrid_DomainContext | 20 | {'no such column: schedule_date': 1, 'no such column: wo.schedule': 14, 'ambiguous column name: status': 2, 'no such column: wo.schedule_date': 3} |
| C5_MASQLGrid_DomainContext_Validated | 5 | {'no such column: wo.schedule_date': 4, 'no such column: wo.schedule': 1} |
