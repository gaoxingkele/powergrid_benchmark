# E2 Human-Annotation Data Management Plan

Status: `DRAFT FOR INSTITUTIONAL REVIEW`

## Data classes

1. **Identity key:** names, contacts, signatures, qualification evidence, and the
   mapping between names and coded identifiers.
2. **Restricted work packets:** source-context excerpts, report locators, and any
   material whose redistribution permission is absent.
3. **Scientific labels:** blinded task responses, pre-adjudication agreement,
   adjudication records, aggregate validity metrics, and error taxonomy.
4. **Public derivatives:** non-identifying aggregate metrics, confusion matrices,
   claim-gate decisions, file hashes, and non-verbatim provenance.

## Access control

- The identity key is held by the responsible investigator, separately from labels.
- Annotator A and B receive separate read-only packets and cannot access each
  other's outputs before agreement is frozen.
- The analyst receives coded labels only.
- Restricted source text remains in an institution-approved private location and
  is excluded from the public release manifest.

## Integrity and chronology

- Every input packet, guide, raw annotation, and adjudication file receives a
  SHA-256 digest and timestamp.
- Pre-adjudication statistics are generated before either raw file is released for
  adjudication.
- Corrections are append-only and state the reason, author, time, and affected hash.
- AI-generated or synthetic labels are stored outside the human-evidence directory
  and cannot be joined as if produced by a human annotator.

## Retention and deletion

The responsible institution must set the retention period, secure storage system,
backup policy, and permitted deletion/withdrawal window. Public aggregate records
must not permit re-identification. At expiry, the identity key and restricted work
packets are deleted or archived only under the institutional determination and
source-license conditions.

## Required institutional fields

- Approved storage system:
- Authorized roles:
- Retention period:
- Backup location and encryption policy:
- Withdrawal/deletion deadline:
- Incident-reporting contact:
- Permitted public data classes:
