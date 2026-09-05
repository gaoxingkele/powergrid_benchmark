# Human-validation execution entry point

Status: `SCAFFOLD_READY / NO HUMAN LABELS COLLECTED`

The repository contains no synthetic or AI-generated scientific annotations. Two eligible humans, an institutionally appropriate ethics/exemption determination, a frozen sample, and securely prepared context packets are still required.

Run commands from `03_Reproducibility/Code/prospective_v1` after completing the administrator-only sampling manifest:

```powershell
python human_validation.py prepare --schema ..\..\Data\human_structure_validation_v1\annotation_schema.json --manifest <frozen-sampling.csv> --output-dir <secure-packet-dir> --annotator-a <pseudonym-A> --annotator-b <pseudonym-B>

python human_validation.py pre --schema ..\..\Data\human_structure_validation_v1\annotation_schema.json --manifest <frozen-sampling.csv> --annotator-a <completed-A.csv> --annotator-b <completed-B.csv> --output <pre_adjudication_agreement.json>

python human_validation.py final --schema ..\..\Data\human_structure_validation_v1\annotation_schema.json --manifest <frozen-sampling.csv> --annotator-a <completed-A.csv> --annotator-b <completed-B.csv> --pre <pre_adjudication_agreement.json> --adjudication <completed-adjudication.csv> --output-dir <analysis-output-dir>
```

The final stage writes `human_structure_results.csv`, `confusion_matrix_roles.csv`, `edge_path_error_taxonomy.csv`, and `claim_gate_decisions.json`. A failed gate requires claim downgrading; passing the internal gate is necessary but is not by itself a universal validity guarantee.
