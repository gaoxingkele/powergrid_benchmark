# Statistical reference suggestions for the MA-SQLGrid revision

These references support the method; they do not turn the fixed, development-visible 180-question corpus into a probability sample.

1. Efron, B. Bootstrap methods: Another look at the jackknife. *Annals of Statistics* **1979**, *7*, 1–26. https://doi.org/10.1214/aos/1176344552. Use for the bootstrap origin, while naming the reported intervals **composition-sensitivity intervals**.
2. Cameron, A.C.; Gelbach, J.B.; Miller, D.L. Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* **2008**, *90*, 414–427. https://doi.org/10.1162/rest.90.3.414. Use for keeping dependent observations together at a cluster unit.
3. Canay, I.A.; Romano, J.P.; Shaikh, A.M. Randomization tests under an approximate symmetry assumption. *Econometrica* **2017**, *85*, 1013–1030. https://doi.org/10.3982/ECTA13086. Use for the explicit symmetry boundary of cluster sign flips.
4. Phipson, B.; Smyth, G.K. Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn. *Statistical Applications in Genetics and Molecular Biology* **2010**, *9*, Article 39. https://doi.org/10.2202/1544-6115.1585. Use for the Monte Carlo plus-one correction `(extreme+1)/(B+1)`.
5. Holm, S. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* **1979**, *6*, 65–70. Stable JSTOR record: https://www.jstor.org/stable/4615733. Use for the two explicit nine-test families.
6. McNemar, Q. Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika* **1947**, *12*, 153–157. https://doi.org/10.1007/BF02295996. Cite only if the question-level McNemar diagnostic remains; keep it descriptive because it ignores clustered dependence.

Recommended wording: “All point estimates are exact, equally question-weighted contrasts on the finite frozen set. Cluster sign-flip p-values test a symmetry-based sharp-null model using normalized-gold-SQL groups as a dependence proxy. Cluster bootstrap limits describe sensitivity to the empirical mix of observed groups and are not confidence intervals for a claimed external question population.”
