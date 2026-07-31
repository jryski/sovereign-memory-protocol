# 05 — Verification

_Status: Draft_

## Structured outcomes

A verifier MUST return dimensions rather than a single Boolean. Each applicable dimension distinguishes at least `pass`, `fail`, `unknown`, `not_applicable`, and `not_checked`; profiles add `stale`, `partial`, `offline`, or `unverifiable` where needed.

Minimum dimensions under review include:

- canonical bytes and profile support;
- event commitment and stream continuity;
- stream registry and inventory coverage;
- semantic lineage;
- authority and key status;
- payload and erasure state;
- transfer state;
- checkpoint signature, inclusion, and ancestry;
- witness or anchor coverage;
- freshness/currentness;
- source-qualified completeness;
- offline portability;
- tested write-surface coverage.

## Currentness

An old internally valid history can still be stale. A verifier lacking an independently retained sufficiently recent checkpoint or equivalent freshness evidence must report currentness as unknown or stale, not pass.

## Restore

An internally valid restore is quarantined until reconciled against required stream inventory, checkpoint ancestry, key status, retention/hold state, erasure history, and deployment policy. Stale restores must not resurrect erased payload or superseded authority.

## Security precedence

Integrity, canonicalization, unsupported-critical-extension, and resource-limit failures take precedence over semantic success claims. A verifier must not report successful correction, transfer, erasure, or authority when the covering custody evidence is invalid.
