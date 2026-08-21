# W1 Scientific-Blocker Baseline

Captured before W1 code edits on 2026-08-05 (Asia/Shanghai). The working tree was already dirty; no cleanup, reset, checkout, or commit was performed.

## MA-SQLGrid SHA-256

| Artifact | SHA-256 |
|---|---|
| `source/code/experiment_final/applsci_factorial.py` | `CEB8BB100568904FAC2A17D4147C2400E1A3AEB1AA2927A43B1207EE79D8C28D` |
| `source/code/experiment_final/main.py` | `2D5BC317C25DFB903E261D1B7CE5A0362F13C4D9F022133A169AB55E1952F7E6` |
| `source/data/griddb_maintenance_v2_v0_1/database.sqlite` | `BA74E84F30C15ECF04BF2B1FFB5D1CCBB978A9E210B69F4676B9BDE64E5BBC46` |
| `source/data/griddb_maintenance_v2_v0_1/questions.jsonl` | `A08F302AFB47BC2E7C352D20CA69EFA0068B74D9AD296C988BC7B27160593A82` |
| `source/data/griddb_maintenance_v2_v0_1/splits.json` | `0F30A2CF73AA39F1E3E28AF82F4DFBE36360A1B18C7411C6336B179D27A65A95` |

Pre-W1 factorial state: four cells × 180 held-out questions = 720 frozen prompts; `prediction_count=0`; execution path called the unavailable proprietary `formal.llm_client()` path.

## C2GES SHA-256

| Artifact | SHA-256 |
|---|---|
| `source/code/prepare_fever_benchmark.py` | `AF5CE2A279291ABBA99AE61D55373435F21087DFD3E427D3E433AD344DB2F1F0` |
| `source/code/c2ges_learnable.py` | `957C63362D7470B89DD16A75148DD088BDB88220FAA4838506B650E20297B729` |
| `source/code/run_applsci_seed_sweep.py` | `5040CC2446F392519E368560DDCDDE8F94EC1A5F006C295A227AE4DF57FF0DCA` |

Pre-W1 protocol state: FEVER records preserved `title`, but constructed per-claim `doc_id`; the learning experiment supplied human-gold SUPPORTS/REFUTES as the role; the reported cluster bootstrap therefore did not establish a bottom-document-clustered end-to-end result.

## W1 exit conditions

- MA dry-run remains zero-cost and produces exactly 720 stable prompt/context hashes.
- MA execution requires an explicit OpenAI-compatible endpoint/model/key and never replaces failures with fake SQL.
- C2 records expose a stable bottom-document cluster key and audit split overlap.
- C2 explicitly distinguishes `oracle-label`, `predicted-label`, and `label-blind` protocols.
- C2 paired bootstrap uses the bottom-document key.
- Both runners emit per-instance artifacts, config/data/code hashes, and failure counts.
- Independent tests cover Cartesian completeness, duplicate IDs, missing clusters, leakage, and hash fields.
