# 07 — Errors and Precedence

_Status: v0.2 review-candidate error-class registry_

Stable machine-readable errors are part of interoperability and security. Implementations may add diagnostic detail but must not change the normative meaning or hide a higher-priority integrity failure.

## Precedence

At minimum:

1. resource and parser safety;
2. profile and critical-extension support;
3. canonical bytes and commitment integrity;
4. chain, checkpoint, and rollback integrity;
5. authority and key status;
6. lifecycle, transfer, erasure, and semantic interpretation.

A lower-priority semantic result must not mask a higher-priority failure.

## Authoritative v0.2 error-class registry

This is the only v0.2 error-class registry. An error class identifies a violated
invariant, unsupported mandatory requirement, or named claim-policy violation.
The structured report separately carries `dimension_status`,
`operation_disposition`, affected dimension, object, scope, evidence, claim
policy, and secondary findings.

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
| `KEY_STATUS_REQUIREMENT_UNMET` | A named authority claim requires historical key status or compromise evidence that cannot be established |
| `STREAM_INVENTORY_INCOMPLETE` | The committed stream registry or lifecycle accounting is missing or inconsistent |
| `STREAM_ID_REUSED` | A retired, erased, restored, or reinitialized stream identity was reused as genesis |
| `STREAM_GAP` | A required position or predecessor is absent |
| `STREAM_FORK` | Competing stream successors exist without a conforming branch disposition |
| `APPEND_RESULT_INVALID` | A compare-and-append conflict was reported as committed success or otherwise misrepresented |
| `EQUIVOCATION_DETECTED` | Conflicting valid successors or checkpoints were presented for the same scope and position |
| `CHECKPOINT_INVALID` | Checkpoint structure, signature, proof, or coverage is invalid |
| `CHECKPOINT_DISCONTINUITY` | Required checkpoint ancestry or append-only consistency is absent or invalid |
| `FRESHNESS_REQUIREMENT_UNMET` | A named currentness claim was made although evidence exceeds its declared freshness threshold |
| `ROLLBACK_SUSPECTED` | Presented history predates independently retained freshness evidence |
| `TIME_SEMANTICS_INVALID` | Required time grammar, source, uncertainty, or dimension separation is invalid |
| `LINEAGE_INVALID` | A lifecycle or semantic-lineage edge is missing, cyclic, self-referential, or wrong-scope |
| `PROJECTION_INVALID` | An invalidated or stale projection was represented as current or derived from required verified inputs |
| `TRANSFER_STATE_VIOLATION` | Transfer state, transition, finality, or replay behavior violates the declared bilateral contract |
| `TRANSFER_SCOPE_INVALID` | Recipient, package, source head, destination scope, mode, or authority does not match the offer |
| `RETENTION_STATE_INVALID` | Retention, expiry, or legal-hold transition is missing, expired, unverifiable, or wrong-scope |
| `ERASURE_REQUIREMENT_UNMET` | A named erasure claim requires surfaces or key/copy layers that remain incomplete, unknown, or unavailable |
| `ERASURE_RECEIPT_UNSAFE` | A surviving receipt retains prohibited or payload-equivalent information |
| `PAYLOAD_STATE_UNVERIFIABLE` | Payload absence, presence, or erasure state is represented without required evidence |
| `ZONE_DISCLOSURE_UNAUTHORIZED` | Cross-zone disclosure, correlation, aggregation, or proof access lacks required authorization |
| `RESTORE_ACTIVATION_VIOLATION` | A restore was activated or exposed despite required quarantine or incomplete reconciliation |
| `NON_RESURRECTION_VIOLATION` | Restore exposed or promoted later-erased, withdrawn, retired, or invalid-authority state |
| `SOURCE_ACCOUNTING_INCOMPLETE` | A required authenticated source-inventory item lacks an explicit disposition |
| `COMPLETENESS_CLAIM_UNSUPPORTED` | A completeness claim exceeds its authenticated source or inventory boundary |
| `OFFLINE_CLAIM_UNSUPPORTED` | An offline/provider-exit claim lacks required portable profile, trust, key, proof, registry, or coverage evidence |
| `ALGORITHM_POLICY_VIOLATION` | A suite was accepted despite unknown, downgraded, expired, prohibited, or unbridged policy status |
| `RESOURCE_LIMIT_EXCEEDED` | An immutable profile ceiling was exceeded |
| `REFERENCE_CYCLE` | Object or lineage references exceed cycle rules or bounded depth |
| `VERIFICATION_RESULT_INVALID` | A report masks precedence, collapses unavailable coverage into pass, or omits required bindings |

The authoritative dimension-status and operation-disposition vocabularies are
defined in `05-verification.md`. They are not interchangeable with error classes.
Ordinary pending, partial, stale, quarantined, incomplete, conflict, or unknown
states do not require an error class unless a named claim policy is violated.
