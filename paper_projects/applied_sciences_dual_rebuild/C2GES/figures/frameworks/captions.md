# Caption drafts

> Protocol/method diagrams only. No unfrozen experimental result is represented.

## c2_f01_three_protocols

Parallel C2GES evaluation protocols over the same claims, candidate sentences and frozen instances. Oracle-label exposes the human veracity role and is conditional rather than end-to-end. Predicted-label obtains a role from a leakage-controlled upstream classifier and is end-to-end. Label-blind exposes no role and is also end-to-end. Candidate pools and evidence metrics remain aligned across protocols.

Source evidence: MASTER_EXECUTION_PLAN.md Sections 4.3-4.6; experiment_registry.json C2-M01; W1_ACCEPTANCE_REPORT.md three-protocol contract; CLAIM_LEDGER.md C2-C02

## c2_f02_oof_document_split

Leakage-controlled document grouping and out-of-fold upstream-label generation. All claims sharing an underlying Wikipedia document are assigned atomically to train, development or test. Training documents alone are divided into grouped folds: each held-out fold receives predictions from a classifier fitted on the remaining folds. A final upstream classifier fitted on all training documents predicts roles for development and test. Claim-level pseudo-document identifiers are not used and test labels never enter training.

Source evidence: W1_ACCEPTANCE_REPORT.md grouped document split; W2_ACCEPTANCE_REPORT.md StratifiedGroupKFold OOF protocol; MASTER_EXECUTION_PLAN.md Sections 4.4 and 4.6; CLAIM_LEDGER.md C2-C02

## c2_f03_evidence_audit_bootstrap

Evidence artifact audit and document-clustered inference flow. Per-instance outputs retain source-document and evidence-sentence identifiers, configuration, seed and provenance hashes. The strict gate rejects missing fields, duplicates, incomplete method-by-item cells, inconsistent hashes and document coverage. Unique complete pairs are resampled by underlying document for paired bootstrap confidence intervals; registered paired tests and Holm adjustment feed E4 canonical evidence. No result values are shown.

Source evidence: shared/stat_audit.py; shared/README.md C2GES example; experiment_registry.json C2-M01-M03; MASTER_EXECUTION_PLAN.md Sections 4.6 and 9
