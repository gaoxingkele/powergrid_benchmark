## Numerical reporting amendment

`primary_v3` completed and its hypervolume values remain valid. Its clipping
incidence counter used strict floating comparisons, however, and therefore
classified 28 analytic-bound coordinates with minimum normalized value
`-3.3545534947581475e-17` as clips. Those are floating roundoff rather than
mathematical bound violations.

The final run uses a declared `1e-12` incidence tolerance. This amendment does
not change any portfolio, objective value, hypervolume, method comparison, or
sensitivity factor. `primary_v3` is retained as supplementary run history but
is superseded for clipping-count reporting.
