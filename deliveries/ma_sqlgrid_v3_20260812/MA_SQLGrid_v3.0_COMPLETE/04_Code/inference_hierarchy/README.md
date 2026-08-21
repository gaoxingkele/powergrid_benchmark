# MA-SQLGrid canonical v3 inference hierarchy

This is an additive Round-2 evidence package. It does not edit the frozen v2 release or manuscript and performs no model inference.

Run from the repository root:

```powershell
python paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/canonical_v3_inference_hierarchy/verify_inputs.py
python paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/canonical_v3_inference_hierarchy/build_v3_inference.py
python -m unittest discover -s paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/canonical_v3_inference_hierarchy/tests -v
```

The build stops before analysis if any of the 13 v2-accepted upstream inputs or five consumed v2 products differs from `EXPECTED_INPUT_HASHES.json`.

Interpretation rules:

- Point estimates are exact, equally weighted contrasts for the finite frozen 180-question set.
- `primary_execution_nine_core_factorial_tests` is the sole family for promoted execution-equality factorial claims; none survives its nine-test Holm correction.
- `secondary_structural_adherence_nine_core_factorial_tests` is a direct manipulation diagnostic. The Qwen and Granite hint main effects survive Holm, but they are not independent evidence of semantic correctness.
- Bootstrap limits in `composition_sensitivity.csv` are composition-sensitivity intervals, not population confidence intervals.
- The 39 difficulty-by-feature groups are deliberately labeled non-authoring groups.
- `MANUAL_VISUAL_QA.json` is inspected and edited independently; the generator never self-certifies it.
