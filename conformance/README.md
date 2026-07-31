# Conformance

_Status: Draft structure; not a certification suite_

This directory contains implementation-neutral fixtures, expected outcomes, and optional profiles. It must not make a particular database, language, cloud, or cryptographic service a hidden protocol dependency.

- `fixtures/` — canonical inputs and operations, added only after the corresponding normative contract stabilizes;
- `expectations/` — case matrices and expected structured outcomes;
- `profiles/` — concrete encoding, algorithm, packaging, or assurance profiles.

The first immutability case matrix is review material and does not yet cover every adversarial P0 requirement. Empty fixture directories are intentional; absence must not be reported as passing coverage.
