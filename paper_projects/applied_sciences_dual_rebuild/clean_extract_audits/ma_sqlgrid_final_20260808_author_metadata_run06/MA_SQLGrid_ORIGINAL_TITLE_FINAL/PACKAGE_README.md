# MA-SQLGrid FINAL Candidate Package

This is a local editor/reviewer inspection package for the exact original-title
candidate. It is not a claim that the public GitHub repository is synchronized,
that all third-party sharing permissions are complete, or that the paper is
portal-ready.

## Scientific boundary

- Historical v3 results are deterministic descriptive re-execution results;
  the FINAL executor correction was not used to obtain or reinterpret them.
- No reported experiment estimates a five-role or autonomous-agent benefit.
- No machine or author-assisted label is represented as qualified independent
  power-grid expert gold.
- Q039 remains a constructed, outcome-exposed, semantically ambiguous trace.

## Contents and verification

`PACKAGE_MANIFEST.json` lists every archive member, byte count, SHA-256, and
rights class. `RIGHTS_INVENTORY.csv` defines the rights basis and remaining
manual condition for each class. A clean-extraction audit distributed beside
the ZIP records the archive hash, compile, tests, text-content comparison, and
prohibited-content check; it is external because embedding an audit of an
archive inside that same archive would be circular. The final PDF is
`build/paper_applsci.pdf`.

From the extracted package root, run the executor tests with:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) 'code')
python -m unittest discover -s tests -p 'test_*.py' -q
```

Then run `./build.ps1`. The clean build is required to reproduce the same
20-page text content; PDF container bytes can differ because pdfTeX embeds
build-time metadata, which is recorded explicitly in the clean-extraction
audit.

## Open gates

The authors have confirmed the correspondence field, author order,
affiliations, existing CRediT statement, all-author agreement sentence,
conflict-of-interest declaration, funding source, grant number, and no-funder-
role statement. The manuscript transparently records that exact backend Codex
model identifiers/versions were not retained for every session and does not
invent them. Before submission, the authors must still resolve every third-party
permission, synchronize and tag the public repository, and decide whether to complete the
untouched end-to-end and qualified expert studies required for the retained
title's stronger scientific interpretation.
