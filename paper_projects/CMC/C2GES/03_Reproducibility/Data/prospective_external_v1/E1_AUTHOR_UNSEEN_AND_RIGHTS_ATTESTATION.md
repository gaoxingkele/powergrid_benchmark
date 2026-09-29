# E1 Author Unseen-Status and Access-Rights Attestation

Status: `UNSIGNED / REQUIRED BEFORE PROTOCOL FREEZE`

This form is evidence about author knowledge and legal access. It must be completed
by the corresponding author or an authorized data custodian. An AI agent may not
sign it or infer the answers.

## Proposed external cohort

- Cohort identifier:
- Inventory filename and SHA-256:
- Number of reports:
- Number of independent report series:
- Development/test series allocation record:
- Private dataset filename and SHA-256:
- Source organizations:
- Earliest source-publication date:
- Latest source-publication date:

## Unseen-status declaration

I confirm that, before the protocol-freeze timestamp recorded below:

1. the authors and analysts who designed, implemented, tuned, or will interpret
   C²GES did not open, read, parse, summarize, label, or inspect the report bodies,
   reference summaries, outcome-bearing excerpts, or system results for the
   proposed external-test cohort;
2. no proposed report or report series appears in `SEEN_EXCLUSION_REGISTRY.csv`;
3. any person who assembled the inventory without remaining blinded is identified
   as a data custodian and will not tune the system or interpret unblinded results;
4. titles or metadata exposed during source discovery have been recorded and the
   corresponding reports excluded if the frozen protocol treats such exposure as
   disqualifying; and
5. the external test will be opened only once through the hash-bound authorization
   and attempt registry described in `FORMAL_EXTERNAL_EXECUTION.md`.

## Access and redistribution declaration

For every inventory row, I confirm that the source is legally accessible for the
reported computational analysis. I have recorded the official source locator,
access date, governing terms or permission basis, and redistribution decision.
Source PDFs and verbatim derived text will not be redistributed unless permission
expressly allows it.

## Signature block

- Name:
- Role:
- Institution:
- Signature:
- Date and time (including timezone):
- Protocol-freeze timestamp:
- Notes or exceptions:

Any exception makes the affected report ineligible for the confirmatory test and
must be added to the seen-exclusion registry before authorization is generated.
