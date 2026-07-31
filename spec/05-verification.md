# 05 — Verification

_Status: Draft_

## Structured outcomes

A verifier MUST return dimensions rather than a single Boolean. Each applicable dimension distinguishes at least `pass`, `fail`, `unknown`, `not_applicable`, and `not_checked`; profiles add `stale`, `partial`, `offline`, or `unverifiable` where needed.

## Authoritative verification-dimension registry

This table is the authoritative core registry. Other normative sections and
fixtures MUST reference these identifiers and MUST NOT create conflicting local
dimension names. A profile MAY add namespaced dimensions, provided unsupported
dimensions remain explicit and are never counted as passes.

| Dimension | Narrow subject |
|---|---|
| `profile_support` | Required protocol, canonicalization, object, and algorithm profiles |
| `canonicalization` | Exact framing, canonical bytes, and critical-extension handling |
| `commitment_integrity` | Domain-bound object commitment and signature preimage |
| `field_mutability` | Locked-field enforcement on each named tested surface |
| `atomic_append` | Recording boundary, compare-and-append, replay, and crash recovery |
| `stream_continuity` | Event position, predecessor, gaps, forks, and disclosed head |
| `stream_registry` | Registered stream lifecycle and inventory accounting |
| `semantic_lineage` | Correction, supersession, conflict, and lifecycle graph |
| `historical_authority` | Actor, delegation, credential, key epoch, revocation, and compromise |
| `checkpoint_signature` | Checkpoint canonical bytes, signature, signer, and scope |
| `checkpoint_inclusion` | Membership in the named checkpoint |
| `checkpoint_consistency` | Checkpoint ancestry and append-only extension |
| `currentness` | Freshness against independently retained evidence |
| `witness_coverage` | Independent witness/anchor evidence and availability |
| `transfer_state` | Bilateral transfer transitions, scope, replay, and finality |
| `retention_hold` | Retention, expiry, legal-hold authority, and transitions |
| `payload_state` | Payload presence, absence, commitment, and availability |
| `erasure_coverage` | Per-surface erasure, keys/copies, confirmation resistance, and limitations |
| `zone_privacy` | Selective disclosure, metadata leakage, and cross-zone isolation |
| `restore_authority` | Quarantine, reconciliation, continuation, and non-resurrection |
| `qualified_completeness` | Manifest/source inventory accounting and declared boundaries |
| `offline_portability` | Provider-independent evidence and configured trust roots |
| `resource_bounds` | Profile ceilings and bounded failure behavior |
| `report_contract` | Result precedence, stable codes, exact-input and tool bindings |

## Verification outcome and operation disposition

A conformance result MUST report `verification_outcome` separately from
`operation_disposition`. `verification_outcome` uses the registered dimension
state and error-code vocabulary. `operation_disposition` MAY report values such
as `accepted`, `rejected`, `conflict`, `pending`, `no_op`, `partial`, or
`quarantined`. Operation acceptance MUST NOT be used as evidence that verification
passed.

## Currentness

An old internally valid history can still be stale. A verifier lacking an independently retained sufficiently recent checkpoint or equivalent freshness evidence must report currentness as unknown or stale, not pass.

## Restore

An internally valid restore is quarantined until reconciled against required stream inventory, checkpoint ancestry, key status, retention/hold state, erasure history, and deployment policy. Stale restores must not resurrect erased payload or superseded authority.

## Security precedence

Integrity, canonicalization, unsupported-critical-extension, and resource-limit failures take precedence over semantic success claims. A verifier must not report successful correction, transfer, erasure, or authority when the covering custody evidence is invalid.
