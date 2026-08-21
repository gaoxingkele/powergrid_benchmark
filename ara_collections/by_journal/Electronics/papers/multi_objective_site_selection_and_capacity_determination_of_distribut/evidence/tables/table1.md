# Table 1 - A comparison of objective functions under the four scenarios

**Source**: Table 1, Section 5 (Case Analysis), page 9
**Caption**: "A comparison of objective functions under three scenarios." (verbatim caption; the table body actually reports four scenario columns — the caption's "three" appears to be a typo, so this file transcribes all four columns as printed)
**Screenshot**: table1.png (table located mid-page 9, directly under the scenario-comparison paragraph)
**Extraction type**: raw_table

Scenario definitions (from Section 5 text, page 8):
- scenario 1: DG is not connected.
- scenario 2: Access to DG without energy storage.
- scenario 3: Connect to DG and add EVS energy storage.
- scenario 4: Connect to DG and add normal energy storage.

Objective meanings (from Section 2): Target 1 = node voltage fluctuation objective f1; Target 2 = network loss objective f2; Target 3 = energy-storage capacity objective f3 (`/` = not applicable when no storage is present).

| Objective | scenario 1 | scenario 2 | scenario 3 | scenario 4 |
|-----------|-----------|-----------|-----------|-----------|
| Target 1 | 0.319736 | 0.369132 | 0.36345 | 0.36784 |
| Target 2 | 1.657225 | 0.947059 | 1.170143 | 1.268574 |
| Target 3 | / | / | 2.565299 | 2.325875 |

Notes:
- Target 1 (voltage fluctuation): scenario 3 (EVS storage, 0.36345) is lower than scenario 4 (normal storage, 0.36784).
- Target 2 (network loss): scenario 3 (1.170143) is lower than scenario 4 (1.268574); both exceed scenario 2 (0.947059).
- Target 3 (storage capacity): applies only to scenarios 3 and 4; scenario 4 (2.325875) is lower than scenario 3 (2.565299).
