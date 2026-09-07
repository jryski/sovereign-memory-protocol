# Conformance

_Status: Draft structure; not a certification suite_

This directory contains implementation-neutral fixtures, expected outcomes, and optional profiles. It must not make a particular database, language, cloud, or cryptographic service a hidden protocol dependency.

- `fixtures/`: canonical inputs and operations, added only after the corresponding normative contract stabilizes;
- `expectations/`: case matrices and expected structured outcomes;
- `profiles/`: concrete encoding, algorithm, packaging, or assurance profiles.

The v0.1 immutability matrix is historical review material. The additive v0.2 case catalog and traceability ledger assign stable planning handles to the revised requirements, result classes, and positive/negative fixtures. They are not machine-readable vectors or passing evidence. Empty fixture directories are intentional; absence must not be reported as passing coverage.

## Read the validation receipt correctly

`scripts/validate_repository.py` reports package integrity separately from conformance:

| Field | Meaning |
| --- | --- |
| `status` | Integrity and selected document-consistency checks for the supplied package. |
| `planned_case_ids` | Unique positive and negative planning handles named by the v0.2 trace ledger. |
| `documented_planned_case_ids` | Those handles with a parseable case-catalog row. This is documentation coverage, not executed coverage. |
| `undocumented_planned_case_ids` | Planned handles without such a row. They remain visible even when package integrity passes. |
| `conformance_evaluation` | `not_performed`: this validator does not run an SMP implementation against protocol vectors. |

Documented positive cases must state `pass` followed by the registered dimension for the corresponding requirement family. Documented negative cases must begin with their primary registered result; a secondary result cannot stand in for a missing primary.

These metrics cover the v0.2 custody ledger only. They do not measure the Context Envelope or Capability/Policy candidates, prove the prose scenarios are complete, or establish any implementation's behavior. Future executable conformance receipts must name exact inputs, evaluated requirements, outcomes, unsupported areas and verifier/profile versions.
