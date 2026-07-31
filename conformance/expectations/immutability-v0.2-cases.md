# Immutability v0.2 Adversarial Case Catalog

_Status: review catalog; identifiers are stable planning handles, not executed fixtures_
_Related specification: `../../spec/08-immutability-and-chain-of-custody-v0.2.md`_
_Related result registry: `../../spec/07-errors.md`_
_Related traceability: `immutability-v0.2-traceability.md`_

Every case must produce a structured result containing the exact input commitment, protocol/profile and verifier versions, trust-configuration identifier, applicable resource ceilings, primary and secondary findings, unavailable surfaces, and per-dimension state. Aggregate pass counts are insufficient.

## 1. Recording boundary and write surfaces

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-REC-001-P` | Canonical event, payload state, authority evidence, position, predecessor, and head commit atomically before success | pass `recording_boundary` |
| `V02-REC-001-N` | Success returns before payload state or head is durable | `RECORDING_BOUNDARY_VIOLATION` |
| `V02-REC-002-N` | Prepared event becomes visible to export/checkpoint after crash | `PREPARED_NOT_COMMITTED` |
| `V02-REC-003-P` | Identical scoped retry returns original event and position | pass `atomic_append` |
| `V02-REC-003-N` | Same operation ID carries different canonical bytes | `REPLAY_CONFLICT` |
| `V02-REC-004-N` | Locked-field mutation succeeds through import, restore, replication, migration, maintenance, or privileged path | `LOCKED_FIELD_CHANGE` plus affected surface |
| `V02-REC-005-N` | Routine trigger coverage is reported as privileged-tamper detection | `CLAIM_OVERREACH` |

## 2. Canonicalization and envelope closure

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-CAN-001-P` | Golden logical input produces exact published canonical bytes and commitment | pass `canonicalization` |
| `V02-CAN-002-N` | Unicode variant or malformed surrogate changes interpretation | `NONCANONICAL_ENCODING` |
| `V02-CAN-003-N` | Absent, null, empty, erased, unknown, and withheld are conflated | `NONCANONICAL_ENCODING` |
| `V02-CAN-004-N` | Duplicate member name is accepted or interpreted last-write-wins | `NONCANONICAL_ENCODING` |
| `V02-CAN-005-N` | Negative zero, exponent, overflow, or caller numeric coercion changes value | `NONCANONICAL_ENCODING` |
| `V02-CAN-006-N` | Timestamp offset, precision, leap-second, or uncertainty violates profile grammar | `TIME_SEMANTICS_INVALID` |
| `V02-CAN-007-N` | Unsupported canonicalization version is silently normalized | `UNSUPPORTED_PROFILE` |
| `V02-CAN-008-P` | Independent implementations match exact bytes and commitments for every golden vector | pass `canonicalization` |
| `V02-CAN-009-N` | Trailing data or ambiguous framing is accepted | `NONCANONICAL_ENCODING` |
| `V02-CAN-010-N` | Old event is silently recanonicalized under a newer profile | `COMMITMENT_MISMATCH` |
| `V02-ENV-002-N` | Event bytes substitute for payload, checkpoint, transfer, erasure, restore, authority, registry, or witness object | `DOMAIN_BINDING_INVALID` |
| `V02-ENV-003-N` | Valid object replays across principal, zone, stream, epoch, class, or purpose | `DOMAIN_BINDING_INVALID` |
| `V02-ENV-004-N` | Unknown critical field is ignored | `UNKNOWN_CRITICAL_EXTENSION` |
| `V02-ENV-004-P` | Unknown noncritical field remains byte-preserved through export/restore | pass with uninterpreted extension |
| `V02-ENV-005-N` | Human rendering omits a committed critical field without disclosure | `VERIFICATION_RESULT_INVALID` |
| `V02-ENV-006-N` | Durable receipt contains secret, bearer credential, or payload-equivalent content | `SECRET_IN_DURABLE_ENVELOPE` |
| `V02-ENV-008-N` | A valid signature is replayed under a different purpose, object type, principal, zone, stream, epoch, key epoch, or suite | `DOMAIN_BINDING_INVALID` |

## 3. Authority, delegation, keys, and algorithms

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-AUTH-002-N` | Historical event resolves authorization through a mutable current role, URL, alias, or policy row | `AUTHORITY_UNVERIFIABLE` |
| `V02-AUTH-003-P` | Delegation binds grantor/grantee, scope, operations, interval, constraints, and depth | pass `historical_authority` |
| `V02-AUTH-004-N` | Delegate broadens scope or exceeds delegation depth | `AUTHORITY_SCOPE_INVALID` |
| `V02-AUTH-005-N` | Cryptographically valid key signs wrong principal, zone, stream, class, operation, or interval | `AUTHORITY_SCOPE_INVALID` |
| `V02-AUTH-006-P` | Key introduction, rotation, expiry, revocation, recovery, and replacement preserve historical evidence | pass `historical_authority` |
| `V02-AUTH-007-N` | Backdated post-compromise event uses self-asserted time to escape suspect interval | `KEY_STATUS_REQUIREMENT_UNMET` |
| `V02-AUTH-008-N` | Missing historical authority falls back to current authority | `AUTHORITY_UNVERIFIABLE` |
| `V02-ALG-003-N` | Unknown, expired, below-floor, or downgraded suite silently passes | `ALGORITHM_POLICY_VIOLATION` |
| `V02-ALG-004-P` | Old/new suite bridge binds final-old and first-new checkpoints | pass `algorithm_agility` |
| `V02-ALG-005-N` | New profile retroactively weakens old locked fields or meaning | `ALGORITHM_POLICY_VIOLATION` |

## 4. Stream registry, append, checkpoint, and rollback

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-STR-001-N` | Valid disclosed stream omits another active stream from the committed registry | `STREAM_INVENTORY_INCOMPLETE` |
| `V02-STR-003-P` | Create, epoch change, seal, replace, erase, and retire append registry events | pass `stream_registry` |
| `V02-STR-004-N` | Deleted, retired, erased, restored, or reinitialized stream ID is reused as genesis | `STREAM_ID_REUSED` |
| `V02-STR-005-N` | Unknown later genesis or registry/head mismatch is accepted | `STREAM_INVENTORY_INCOMPLETE` |
| `V02-APP-001-P` | True concurrent compare-and-append yields one committed contiguous successor | pass `atomic_append` |
| `V02-APP-002-N` | Last-write-wins discards a competitor | `APPEND_RESULT_INVALID` |
| `V02-APP-003-P` | Competing mutually exclusive corrections produce winner plus explicit rejection/conflict | pass `atomic_append` |
| `V02-APP-004-N` | Same predecessor/position has two valid successors | `STREAM_FORK` or `EQUIVOCATION_DETECTED` |
| `V02-APP-005-N` | Same checkpoint position/prior head has two signed roots | `EQUIVOCATION_DETECTED` |
| `V02-APP-006-N` | Crash-orphaned event is checkpointed | `PREPARED_NOT_COMMITTED` |
| `V02-APP-007-N` | Operation ID is replayed across scope | `REPLAY_CONFLICT` |
| `V02-CHK-002-N` | Inclusion proof is represented as append-only consistency or latestness | `CLAIM_OVERREACH` |
| `V02-CHK-003-N` | Unrelated roots are represented as checkpoint ancestry | `CHECKPOINT_DISCONTINUITY` |
| `V02-CHK-004-N` | Leaf order or odd-node behavior differs from the profile | `CHECKPOINT_INVALID` |
| `V02-CHK-005-N` | Trusted older valid head is reported current despite newer independent head | `ROLLBACK_SUSPECTED` |
| `V02-CHK-006-N` | Checkpoint exceeds maximum age/count but reports current | `FRESHNESS_REQUIREMENT_UNMET` |
| `V02-CHK-007-N` | Witness outage causes authorization fail-open or silent downgrade | `VERIFICATION_RESULT_INVALID` |
| `V02-CHK-008-N` | Two isolated clients receive signer-valid split views with no reported coverage limitation | `EQUIVOCATION_DETECTED` or non-equivocation unknown |

## 5. Time, lineage, and projections

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-TIM-001-N` | Effective, observed, recorder, checkpoint, and witness time are collapsed | `TIME_SEMANTICS_INVALID` |
| `V02-TIM-002-N` | Wall-clock value reorders committed stream position | `TIME_SEMANTICS_INVALID` |
| `V02-TIM-004-N` | Clock rollback or implausible future time is silently repaired | `TIME_SEMANTICS_INVALID` |
| `V02-TIM-005-N` | External witness time is represented as occurrence time or authority | `CLAIM_OVERREACH` |
| `V02-SUP-001-N` | Successor targets missing, wrong-principal, or wrong-zone record | `LINEAGE_INVALID` |
| `V02-SUP-002-N` | Self-link, prohibited cycle, illegal fork, or mutable authority edge is accepted | `LINEAGE_INVALID` or `REFERENCE_CYCLE` |
| `V02-SUP-003-P` | Competing corrections follow the profile's conflict/branch rule | pass `lineage_projection` |
| `V02-SUP-004-N` | Current-winner projection depends on insertion order or unverified authority | `PROJECTION_INVALID` |
| `V02-SUP-006-N` | Erasure, withdrawal, or supersession leaves stale projection authoritative | `PROJECTION_INVALID` |

## 6. Bilateral transfer

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-XFR-001-P` | Offer binds parties, package, source head, destination, mode, obligations, expiry, and loss declaration | pass `bilateral_transfer` through offered state |
| `V02-XFR-002-P` | Sender release and recipient acceptance are distinct authorized events | pass `bilateral_transfer` |
| `V02-XFR-003-N` | Dispatch, possession, byte receipt, or checksum is represented as semantic acceptance | `TRANSFER_STATE_VIOLATION` |
| `V02-XFR-004-N` | Sender unilaterally declares completion | `TRANSFER_STATE_VIOLATION` |
| `V02-XFR-005-N` | Copied custody is represented as exclusive release | `TRANSFER_SCOPE_INVALID` |
| `V02-XFR-006-N` | Wrong recipient, changed package, expired offer, replayed acceptance, or missing recipient authority | `TRANSFER_SCOPE_INVALID` |
| `V02-XFR-007-P` | Partial acceptance commits accepted and rejected inventory subsets | pass `bilateral_transfer` as partial, not complete |
| `V02-XFR-007-N` | Partial acceptance is reported complete for full offer | `TRANSFER_STATE_VIOLATION` |
| `V02-XFR-008-P` | Cancellation or expiry appends while preserving dispatch/receipt evidence | pass lifecycle |
| `V02-XFR-009-N` | Destination rewrites origin attribution | `LOCKED_FIELD_CHANGE` |
| `V02-XFR-010-N` | Transfer proof leaks unauthorized cross-zone identifiers or roots | `ZONE_DISCLOSURE_UNAUTHORIZED` |

## 7. Retention, holds, erasure, and privacy

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-RET-002-P` | Hold binds authority, scope, policy, start, review, expiry/release, and affected operations | pass `retention_hold` |
| `V02-RET-003-N` | Hold authorizes unrelated processing, disclosure, correlation, or indefinite retention | `RETENTION_STATE_INVALID` |
| `V02-RET-004-P` | Valid hold blocks erasure with minimized pending result | pass hold state; erasure not complete |
| `V02-RET-005-P` | Hold narrowing/release/expiry appends without rewriting prior state | pass lifecycle |
| `V02-RET-006-N` | Expired, unverifiable, or wrong-scope hold blocks erasure | `RETENTION_STATE_INVALID` |
| `V02-ERA-001-N` | Subject data survives in quote, identifier, vector, cache, log, replica, export, backup, key wrapper, or recovery material | `ERASURE_REQUIREMENT_UNMET` |
| `V02-ERA-003-N` | Offline or unreachable backup is counted verified | `ERASURE_REQUIREMENT_UNMET` |
| `V02-ERA-004-N` | Receipt contains subject reason, excerpt, direct identity, mutable locator, commitment-opening material, or payload-equivalent data | `ERASURE_RECEIPT_UNSAFE` |
| `V02-ERA-005-N` | Missing payload without erasure event is reported erased | `PAYLOAD_STATE_UNVERIFIABLE` |
| `V02-ERA-006-N` | One data key is destroyed while wrapper, escrow, recovery, snapshot, or temporary key copy remains | `ERASURE_REQUIREMENT_UNMET` |
| `V02-ERA-007-N` | Surviving artifact/API set confirms low-entropy erased candidate | `ERASURE_RECEIPT_UNSAFE` |
| `V02-ERA-008-P` | Opening destruction reports intentional future verification loss | pass with reduced payload-verification capability |
| `V02-ERA-009-N` | Original canonical bytes are rewritten, or a redacted derivative is represented as the original event | `LOCKED_FIELD_CHANGE` |
| `V02-ERA-010-N` | Privacy-safe export is required to reproduce pre-erasure archival root | `CLAIM_OVERREACH` |
| `V02-ERA-011-N` | External-recipient propagation timeout is reported complete | `ERASURE_REQUIREMENT_UNMET` |
| `V02-ERA-012-N` | Receipt claims universal deletion beyond declared boundary | `CLAIM_OVERREACH` |
| `V02-PRV-003-N` | Root, cadence, cardinality, locator, actor, or proof access enables unauthorized cross-zone correlation | `ZONE_DISCLOSURE_UNAUTHORIZED` |
| `V02-PRV-004-N` | Selective disclosure lacks audience, purpose, interval, fields, source commitment, or replay protection | `ZONE_DISCLOSURE_UNAUTHORIZED` |
| `V02-PRV-006-N` | Separately governed zones share aggregate checkpoint without profile, leakage analysis, and authority | `ZONE_DISCLOSURE_UNAUTHORIZED` |

## 8. Restore, completeness, and offline verification

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-RST-001-P` | Restored store begins quarantined | pass `restore_non_resurrection` |
| `V02-RST-002-N` | Restore omits registry, latest checkpoint, authority, key, hold, erasure, or inventory reconciliation | `RESTORE_ACTIVATION_VIOLATION` |
| `V02-RST-003-N` | Internally valid stale snapshot reports `stale`/`quarantined` but is nevertheless activated | `ROLLBACK_SUSPECTED` plus `RESTORE_ACTIVATION_VIOLATION` |
| `V02-RST-004-N` | Restore exposes payload whose later erasure state is unknown | `NON_RESURRECTION_VIOLATION` |
| `V02-RST-005-N` | Restore resurrects erased payload, expired authority, retired stream, superseded state, or compromised key status | `NON_RESURRECTION_VIOLATION` |
| `V02-RST-006-N` | Restore rewrites origin, event identity, position, time claim, canonical bytes, or commitment | `COMMITMENT_MISMATCH` |
| `V02-RST-007-P` | Distinct restore-instance and continuation/promotion event precede writable authority | pass `restore_non_resurrection` |
| `V02-RST-008-N` | Restored copy silently clones source writable authority | `RESTORE_ACTIVATION_VIOLATION` |
| `V02-CMP-001-P` | Authenticated frozen source inventory has explicit disposition for every in-scope item | pass `qualified_completeness` |
| `V02-CMP-003-N` | Live-source completeness is claimed without authenticated snapshot/cursor | `COMPLETENESS_CLAIM_UNSUPPORTED` |
| `V02-CMP-004-N` | Inclusion proof is presented as absence/completeness proof | `CLAIM_OVERREACH` |
| `V02-CMP-005-N` | Item omitted before manifest without independent source boundary; verifier reports complete | `COMPLETENESS_CLAIM_UNSUPPORTED` |
| `V02-CMP-006-N` | Frozen source item has no disposition | `SOURCE_ACCOUNTING_INCOMPLETE` |
| `V02-OFF-001-N` | Offline bundle lacks required schemas, registry, authority/key history, proofs, or coverage manifest | `OFFLINE_CLAIM_UNSUPPORTED` |
| `V02-OFF-002-N` | Bundle supplies its own silently trusted root/head | `AUTHORITY_UNVERIFIABLE` |
| `V02-OFF-003-N` | Offline verifier silently fetches mutable online trust state | `VERIFICATION_RESULT_INVALID` |
| `V02-OFF-004-P` | Source, signer, provider, and network are absent; portable evidence still verifies declared dimensions | pass `offline_portability` |

## 9. Verifier resource and reporting behavior

| Case | Scenario | Expected primary result |
|---|---|---|
| `V02-RES-001-P` | Profile pins object/proof/reference/stream/bundle/work ceilings | pass `resource_bounds` |
| `V02-RES-002-N` | Oversized object, huge extension, pathological Merkle depth, or cyclic reference exceeds ceiling | `RESOURCE_LIMIT_EXCEEDED` or `REFERENCE_CYCLE` |
| `V02-RES-003-N` | Caller option silently broadens profile ceiling | `UNSUPPORTED_PROFILE` |
| `V02-RES-004-N` | Limit check occurs only after unbounded allocation, recursion, retrieval, or rendering | `RESOURCE_LIMIT_EXCEEDED` plus implementation safety failure |
| `V02-VER-001-N` | Semantic success masks parser, critical-extension, canonicalization, or commitment failure | `VERIFICATION_RESULT_INVALID` |
| `V02-VER-002-N` | Successful transfer/erasure/restore masks chain or checkpoint failure | `VERIFICATION_RESULT_INVALID` |
| `V02-VER-003-N` | Missing witness, stale checkpoint, incomplete registry, unknown authority, or skipped path collapses into pass | `VERIFICATION_RESULT_INVALID` |
| `V02-VER-006-N` | Aggregate counts substitute for inspectable per-case outcomes | `VERIFICATION_RESULT_INVALID` |
| `V02-VER-007-N` | Report omits input, verifier/profile, trust configuration, time, or resource-limit binding | `VERIFICATION_RESULT_INVALID` |
| `V02-VER-009-N` | Accepted, rejected, pending, conflict, no-op, partial, or quarantined operation disposition is used as verification evidence | `VERIFICATION_RESULT_INVALID` |

## 10. Promotion condition

This catalog does not satisfy conformance by existing. Before normative promotion, each referenced fixture must have exact machine-readable input, exact canonical bytes where applicable, expected structured result, stable primary/secondary codes, and declared resource ceiling. Skipped, inaccessible, stale, offline, or unavailable surfaces remain visible and do not count as pass.
