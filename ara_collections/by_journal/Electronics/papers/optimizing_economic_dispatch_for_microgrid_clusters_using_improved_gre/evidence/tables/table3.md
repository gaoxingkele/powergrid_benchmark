# Table 3 - Expressions of several commonly used chaotic maps

**Source**: Table 3, Section 3.2.1 in "Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization" (Electronics 2024, 13, 3139)
**Caption**: "Expressions of several commonly used chaotic maps."
**Screenshot**: table3.png
**Location on page**: Page 9 (PDF page 9), middle of page.
**Extraction type**: raw_table

| Example | Expression |
| --- | --- |
| Tent | x_{i+1} = x_i/a  if x_i < a ;  (1 − x_i)/(1 − a)  if x_i ≥ a ;  a ∈ (0, 1) |
| Sine | x_{i+1} = (a/4)·sin(π x_i) ;  a = 4 |
| Chebyshev | x_{i+1} = cos(a · cos^{-1}(x_i)) ;  a = 4 |
| Logistic | x_{i+1} = a x_i (1 − x_i) ;  a ∈ (0, 4] |
