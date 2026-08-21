# Dual-Backbone Canonical Figure Captions

**Scope:** Two quantized instruction backbones (Qwen2.5-Coder-7B Q4_K_M and Granite-3.3-8B Q4_K_M), one GridDB; bounded sensitivity, not general model-family robustness.

## fig01_dual_cell_accuracy

Execution and answer-shape accuracy for the four aligned factorial cells and both audited backbones; each backbone/cell contains the same 180 questions. **Scope: two audited backbones, one GridDB; no general family-robustness claim.**

## fig02_backbone_factorial_effects

Per-backbone paired factorial effects with 95% bootstrap intervals over 70 normalized-gold-SQL template clusters (20,000 draws). **Scope: two audited backbones, one GridDB; no general family-robustness claim.**

## fig03_backbone_effect_modifiers

Granite-minus-Qwen differences in context, shape-hint, and context-by-shape effects. The execution three-way interaction excludes zero; this is backbone sensitivity, not model-family robustness. **Scope: two audited backbones, one GridDB; no general family-robustness claim.**

## fig04_shape_effect_replication

Shape-hint main effects are positive for both backbones and both metrics. Granite's execution interval crosses zero, and the execution effect is smaller than Qwen under the paired backbone-modifier interval. **Scope: two audited backbones, one GridDB; no general family-robustness claim.**

## fig05_cross_backbone_cells

Paired Granite-minus-Qwen cell differences with template-cluster intervals. Filled markers denote exact McNemar decisions surviving Holm correction across eight cell/metric tests. **Scope: two audited backbones, one GridDB; no general family-robustness claim.**
