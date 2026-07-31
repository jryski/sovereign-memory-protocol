# 06 — Conformance

_Status: Draft_

## No undifferentiated conformance claim

This draft does not define one binary “SMP conformant” claim. Reports identify the profile and version, exact fixture set, implementation version, tested surfaces, and each assurance dimension.

Candidate dimensions include:

- immutable-field enforcement;
- atomic append and replay safety;
- local chain verification;
- registered-stream coverage;
- signed-checkpoint coverage;
- independent witness coverage;
- freshness/currentness;
- authority and key-lifecycle verification;
- transfer semantics;
- erasure coverage;
- restore/non-resurrection behavior;
- offline portability.

## Neutral fixtures

Normative fixtures are portable data, operations, expected outcomes, and stable errors. Database-specific scripts, deployment manifests, and provider credentials belong in implementation repositories.

Every normative requirement should map to:

1. a requirement identifier;
2. one or more positive or negative fixture identifiers;
3. expected structured outcomes;
4. resource ceilings;
5. required and optional profile coverage.

Skipped, unavailable, stale, or partial cases are reported and are not counted as passes.
