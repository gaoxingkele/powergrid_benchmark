# Canonical C2GES Tables

All values are generated from the frozen five-seed artifacts. Oracle-label is conditional and must not be reported as end-to-end. The primary role-effect and blanket-superiority claims are NO-GO.

## Main results

| Protocol | K | Mean F1 | SD | Delta vs BM25 | Positive gate |
|---|---|---|---|---|---|
| oracle-label | 1 | 0.6705 | 0.0050 | -0.0289 | False |
| oracle-label | 3 | 0.4926 | 0.0015 | 0.0062 | True |
| oracle-label | 5 | 0.4160 | 0.0009 | 0.0051 | True |
| oracle-label | 10 | 0.3563 | 0.0001 | 0.0033 | True |
| predicted-label | 1 | 0.6688 | 0.0051 | -0.0306 | False |
| predicted-label | 3 | 0.4920 | 0.0021 | 0.0056 | True |
| predicted-label | 5 | 0.4150 | 0.0007 | 0.0041 | True |
| predicted-label | 10 | 0.3563 | 0.0002 | 0.0033 | True |
| label-blind | 1 | 0.6677 | 0.0021 | -0.0317 | False |
| label-blind | 3 | 0.4910 | 0.0021 | 0.0046 | False |
| label-blind | 5 | 0.4154 | 0.0006 | 0.0045 | True |
| label-blind | 10 | 0.3560 | 0.0003 | 0.0031 | True |
| bm25 | 1 | 0.6994 | 0.0000 | 0.0000 | True |
| bm25 | 3 | 0.4864 | 0.0000 | 0.0000 | True |
| bm25 | 5 | 0.4109 | 0.0000 | 0.0000 | True |
| bm25 | 10 | 0.3530 | 0.0000 | 0.0000 | True |

## Runtime and memory

| Protocol | Mean wall s | Wall SD | Mean RSS GiB | RSS SD |
|---|---|---|---|---|
| oracle-label | 200.4019 | 7.1542 | 1.2803 | 0.0184 |
| predicted-label | 204.9940 | 11.4081 | 1.2696 | 0.0329 |
| label-blind | 200.3984 | 4.9628 | 1.2738 | 0.0166 |
