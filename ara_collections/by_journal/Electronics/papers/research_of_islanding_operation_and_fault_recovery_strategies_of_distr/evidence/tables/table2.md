# Table 2 - Weight coefficient and located node of the three types of loads

**Source**: Table 2, Section 5.1 (Example System), page 12
**Location on page**: top of page 12, below the first paragraph
**Caption**: "Weight coefficient and located node of the three types of loads."
**Screenshot**: table2.png
**Extraction type**: raw_table

| Load Type | Weight Coefficient | Node |
|-----------|--------------------|------|
| Level 1 | 100 | 5, 6, 12, 13, 23, 24, 29, 31 |
| Level 2 | 10 | 7, 11, 15, 22, 26, 30, 32 |
| Level 3 | 1 | 1, 2, 3, 4, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 25, 27, 28 |

Notes: These weight coefficients are the `α_{i,k}` load weight values used in objective
functions Eq. (1) and Eq. (35), and form the first term of the fault-recovery weight
`β_{i,k}` in Eq. (36). Higher weight = more important load, prioritized for supply.
