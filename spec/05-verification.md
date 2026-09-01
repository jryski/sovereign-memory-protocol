# 05 — Verification

_Status: Draft_

## Structured outcomes

A verifier MUST return dimensions rather than a single Boolean. Every report
MUST represent three orthogonal fields: `dimension_status`,
`operation_disposition`, and zero or more `error_class` values.

### Dimension-status vocabulary

| Status | Meaning |
|---|---|
| `pass` | The dimension's named requirements verified within declared scope |
| `fail` | One or more named requirements for the dimension were violated |
| `unknown` | Evidence is insufficient to decide the dimension |
| `not_applicable` | The dimension does not apply under the declared profile and input |
| `not_checked` | The dimension was deliberately not evaluated and coverage is explicit |
| `stale` | Evidence is internally valid but outside the declared freshness bound |
| `partial` | Only a declared subset of required scope or surfaces was verified |
| `offline` | Required external evidence was unavailable and no portable evidence closed the dimension |
| `unsupported` | A mandatory profile, extension, algorithm, or dimension is unsupported |
| `policy_unacceptable` | Evidence may be technically interpretable but fails the declared claim policy |

### Operation-disposition vocabulary

| Disposition | Meaning |
|---|---|
| `accepted` | Operation was admitted under its operation contract |
| `rejected` | Operation was not admitted |
| `conflict` | Operation lost a deterministic precondition or concurrency conflict |
| `pending` | Operation has not reached its required terminal state |
| `no_op` | Replay or already-satisfied operation made no new state transition |
| `partial` | A declared subset completed and remaining scope is explicit |
| `quarantined` | Operation output exists but activation/exposure is denied |
| `cancelled` | Authorized cancellation reached a terminal state |
| `expired` | The operation's validity interval ended before completion |
| `finalized` | Required operation-specific finality conditions were satisfied |

Ordinary pending, partial, stale, quarantined, incomplete, conflict, or unknown
states MUST NOT be encoded solely as error classes. A named claim policy MAY
elevate such a state to a blocking policy violation, but the underlying status
or disposition and the policy identifier MUST remain explicit.

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

A conformance result MUST report `dimension_status` separately from
`operation_disposition` and `error_class`. Operation acceptance MUST NOT be used
as evidence that verification passed. An error class MUST identify a violated
invariant, unsupported mandatory requirement, or named claim-policy violation;
it MUST NOT substitute for ordinary lifecycle state.

## Currentness

An old internally valid history can still be stale. A verifier lacking an independently retained sufficiently recent checkpoint or equivalent freshness evidence must report currentness as unknown or stale, not pass.

## Restore

An internally valid restore is quarantined until reconciled against required stream inventory, checkpoint ancestry, key status, retention/hold state, erasure history, and deployment policy. Stale restores must not resurrect erased payload or superseded authority.

## Security precedence

Integrity, canonicalization, unsupported-critical-extension, and resource-limit failures take precedence over semantic success claims. A verifier must not report successful correction, transfer, erasure, or authority when the covering custody evidence is invalid.
