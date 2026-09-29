# MA-SQLGrid data-only delivery

Delivery date: 2026-09-07

This archive contains the two GridDB-Maintenance-v2 dataset variants distributed
with the official MA-SQLGrid GitHub release `v0.2.0`:

- `griddb_maintenance_v2_v0_1`: original 90-question benchmark database;
- `griddb_maintenance_v2_x10`: deterministic tenfold row-scale expansion with
  two distractor tables, using the same questions and split definitions.

Each directory contains its SQLite database, SQL schema, questions, split file,
and applicable protocol/verification metadata. The x10 expansion manifest reports
zero gold-validation errors.

Source release: <https://github.com/gaoxingkele/ma-sqlgrid/releases/tag/v0.2.0>

Source tag commit: `837b4fdaf9e39d5dd4ab7704a804144e2461bad4`

Verification performed before packaging:

- the official tag archive was downloaded from GitHub;
- `python -m pytest code/evaluator/tests/test_evaluator.py -q` passed 13/13;
- package contents were taken directly from that tag archive;
- `SHA256SUMS.txt` records every delivered file other than itself.

The SimBench and RTS-GMLC pilot artifacts from later exploratory work are not
included: they are automatic candidates rather than the released MA-SQLGrid
benchmark, and the locally preserved RTS source notice is incomplete. Model
outputs, API traces, manuscripts, and author information are also excluded.

License: see `REPOSITORY_LICENSE.txt`.
