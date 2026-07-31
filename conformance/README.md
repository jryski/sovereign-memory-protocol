# Conformance

_Status: Draft structure; not a certification suite_

This directory contains implementation-neutral fixtures, expected outcomes, and optional profiles. It must not make a particular database, language, cloud, or cryptographic service a hidden protocol dependency.

- `fixtures/` — canonical inputs and operations, added only after the corresponding normative contract stabilizes;
- `expectations/` — case matrices and expected structured outcomes;
- `profiles/` — concrete encoding, algorithm, packaging, or assurance profiles.

The v0.1 immutability matrix is historical review material. The additive v0.2 case catalog and traceability ledger assign stable planning handles to the revised requirements, result classes, and positive/negative fixtures. They are not machine-readable vectors or passing evidence. Empty fixture directories are intentional; absence must not be reported as passing coverage.
