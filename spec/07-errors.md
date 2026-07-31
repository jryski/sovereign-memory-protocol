# 07 — Errors and Precedence

_Status: Draft registry shape_

Stable machine-readable errors are part of interoperability and security. Implementations may add diagnostic detail but must not change the normative meaning or hide a higher-priority integrity failure.

## Proposed classes

| Class | Meaning |
|---|---|
| `UNSUPPORTED_PROFILE` | Required profile or algorithm is not supported |
| `UNKNOWN_CRITICAL_EXTENSION` | A critical extension cannot be interpreted |
| `NONCANONICAL_ENCODING` | Input does not match the required canonical bytes |
| `COMMITMENT_MISMATCH` | Recomputed commitment differs |
| `STREAM_GAP` | Required predecessor or sequence is absent |
| `STREAM_FORK` | Competing successors or heads exist |
| `CHECKPOINT_DISCONTINUITY` | Checkpoint ancestry or consistency fails |
| `ROLLBACK_SUSPECTED` | Presented history is older than retained freshness evidence |
| `AUTHORITY_UNVERIFIABLE` | Historical authority cannot be established |
| `REPLAY_CONFLICT` | An operation identifier was reused with different content |
| `TRANSFER_INCOMPLETE` | Bilateral transfer has not finalized |
| `ERASURE_PARTIAL` | Required erasure scope remains incomplete |
| `RESTORE_QUARANTINED` | Restore has not passed freshness and lifecycle reconciliation |
| `RESOURCE_LIMIT_EXCEEDED` | Normative verifier ceiling was exceeded |

## Precedence

At minimum:

1. resource and parser safety;
2. profile and critical-extension support;
3. canonical bytes and commitment integrity;
4. chain, checkpoint, and rollback integrity;
5. authority and key status;
6. lifecycle, transfer, erasure, and semantic interpretation.

A lower-priority semantic result must not mask a higher-priority failure.

## v0.2 custody-chain result registry

The following codes are the review-candidate registry used by
`08-immutability-and-chain-of-custody-v0.2.md`. A code identifies the blocking
condition; the structured report still carries the affected dimension, object,
scope, evidence, and secondary findings.

| Code | Blocking meaning |
|---|---|
| `CLAIM_OVERREACH` | Evidence is represented as proving a stronger property than its declared scope supports |
| `FIELD_CLASS_UNDEFINED` | A verification-relevant field has no mutability classification |
| `LOCKED_FIELD_CHANGE` | A recorded immutable-envelope field differs from its committed value |
| `RECORDING_BOUNDARY_VIOLATION` | Success or visibility occurred without the complete atomic durable outcome |
| `PREPARED_NOT_COMMITTED` | Prepared or orphaned material was presented as recorded |
| `REPLAY_CONFLICT` | A scoped operation identifier was reused with different canonical input |
| `DOMAIN_BINDING_INVALID` | Object type, purpose, principal, zone, stream, epoch, or class binding is invalid |
| `SECRET_IN_DURABLE_ENVELOPE` | A durable envelope contains prohibited secret or payload-equivalent material |
| `UNSUPPORTED_PROFILE` | A required protocol, canonicalization, algorithm, or object profile is unsupported |
| `UNKNOWN_CRITICAL_EXTENSION` | A critical extension or schema cannot be interpreted |
| `NONCANONICAL_ENCODING` | Input is ambiguous, malformed, noncanonical, or not exactly framed |
| `COMMITMENT_MISMATCH` | Recomputed object commitment differs from the committed value |
| `AUTHORITY_UNVERIFIABLE` | Historical semantic authority cannot be established from immutable evidence |
| `AUTHORITY_SCOPE_INVALID` | Authority exists but not for the principal, zone, stream, event class, operation, or interval |
| `KEY_STATUS_INDETERMINATE` | Required historical key status or compromise interval cannot be established |
| `STREAM_INVENTORY_INCOMPLETE` | The committed stream registry or lifecycle accounting is missing or inconsistent |
| `STREAM_ID_REUSED` | A retired, erased, restored, or reinitialized stream identity was reused as genesis |
| `STREAM_GAP` | A required position or predecessor is absent |
| `STREAM_FORK` | Competing stream successors exist without a conforming branch disposition |
| `APPEND_CONFLICT` | Atomic compare-and-append preconditions failed |
| `EQUIVOCATION_DETECTED` | Conflicting valid successors or checkpoints were presented for the same scope and position |
| `CHECKPOINT_INVALID` | Checkpoint structure, signature, proof, or coverage is invalid |
| `CHECKPOINT_DISCONTINUITY` | Required checkpoint ancestry or append-only consistency is absent or invalid |
| `CHECKPOINT_STALE` | Checkpoint evidence exceeds the declared age or count threshold |
| `ROLLBACK_SUSPECTED` | Presented history predates independently retained freshness evidence |
| `TIME_SEMANTICS_INVALID` | Required time grammar, source, uncertainty, or dimension separation is invalid |
| `LINEAGE_INVALID` | A lifecycle or semantic-lineage edge is missing, cyclic, self-referential, or wrong-scope |
| `PROJECTION_STALE` | A projection is invalidated or not derived from the required verified inputs |
| `TRANSFER_INCOMPLETE` | Required bilateral transfer evidence has not finalized |
| `TRANSFER_SCOPE_INVALID` | Recipient, package, source head, destination scope, mode, or authority does not match the offer |
| `RETENTION_STATE_INVALID` | Retention, expiry, or legal-hold transition is missing, expired, unverifiable, or wrong-scope |
| `ERASURE_PARTIAL` | One or more required erasure surfaces or key/copy layers remain incomplete |
| `ERASURE_RECEIPT_UNSAFE` | A surviving receipt retains prohibited or payload-equivalent information |
| `PAYLOAD_UNAVAILABLE_UNKNOWN` | Payload is absent without valid erasure evidence |
| `ZONE_DISCLOSURE_UNAUTHORIZED` | Cross-zone disclosure, correlation, aggregation, or proof access lacks required authorization |
| `RESTORE_QUARANTINED` | Restore has not passed freshness, lifecycle, authority, inventory, and erasure reconciliation |
| `NON_RESURRECTION_VIOLATION` | Restore exposed or promoted later-erased, withdrawn, retired, or invalid-authority state |
| `SOURCE_ACCOUNTING_INCOMPLETE` | A required authenticated source-inventory item lacks an explicit disposition |
| `COMPLETENESS_UNKNOWN` | No independently trustworthy source boundary supports a stronger completeness claim |
| `OFFLINE_EVIDENCE_INCOMPLETE` | Required portable profile, trust, key, proof, registry, or coverage evidence is absent |
| `ALGORITHM_POLICY_UNACCEPTABLE` | Suite is unknown, downgraded, expired, deprecated below floor, or not bridged as required |
| `RESOURCE_LIMIT_EXCEEDED` | An immutable profile ceiling was exceeded |
| `REFERENCE_CYCLE` | Object or lineage references exceed cycle rules or bounded depth |
| `VERIFICATION_RESULT_INVALID` | A report masks precedence, collapses unavailable coverage into pass, or omits required bindings |

Report states such as `unknown`, `not_checked`, `partial`, `offline`, `stale`,
`unsupported`, `forked`, `equivocating`, `quarantined`, and
`policy_unacceptable` are not interchangeable with the blocking codes above.
They describe dimension state and coverage; a profile defines which states block
which claim.
