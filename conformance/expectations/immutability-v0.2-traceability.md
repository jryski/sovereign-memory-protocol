# Immutability v0.2 Requirement Traceability

_Status: generated review ledger; not conformance evidence_
_Source: `../../spec/08-immutability-and-chain-of-custody-v0.2.md`_

This ledger maps every identified v0.2 custody requirement to one requirement
family, one registered verification dimension through the family map below, one
blocking result class, and positive/negative fixture identifiers. Fixture
identifiers are normative-planning handles; machine-readable vectors are not
promoted by this ledger.

## Adversarial-review group coverage

| Review finding | v0.2 requirement groups |
|---|---|
| Exact recording boundary and claim levels | `CST-REC-*`, `CST-CLAIM-*`, `CST-VER-*` |
| Canonical event, signature, checkpoint, and receipt envelopes | `CST-ENV-*`, `CST-CAN-*`, `CST-CHK-*` |
| Historical identity, delegation, and key status | `CST-AUTH-*`, `CST-ALG-*` |
| Stream registry, atomic append, replay, fork, rollback, freshness | `CST-STR-*`, `CST-APP-*`, `CST-CHK-*` |
| Bilateral transfer | `CST-XFR-*` |
| Erasure closure, retention/holds, and privacy-safe receipts | `CST-RET-*`, `CST-ERA-*`, `CST-PRV-*` |
| Restore quarantine and non-resurrection | `CST-RST-*` |
| Canonical golden vectors and exact time semantics | `CST-CAN-*`, `CST-TIM-*` |
| Supersession graphs and deterministic projections | `CST-SUP-*` |
| Source-qualified completeness | `CST-CMP-*` |
| Metadata and zone privacy | `CST-PRV-*`, `CST-ENV-*` |
| Bounded verifier resources and offline evidence | `CST-RES-*`, `CST-OFF-*` |

## Requirement-family to authoritative-dimension map

The authoritative dimension identifiers are defined in
`../../spec/05-verification.md`. Requirement families below are grouping labels,
not alternate verification dimensions.

| Requirement family | Authoritative dimension |
|---|---|
| `claim_discipline` | `report_contract` |
| `field_mutability` | `field_mutability` |
| `recording_boundary` | `atomic_append` |
| `envelope_domain_binding` | `commitment_integrity` |
| `canonicalization` | `canonicalization` |
| `historical_authority` | `historical_authority` |
| `stream_registry` | `stream_registry` |
| `atomic_append` | `atomic_append` |
| `checkpoint_currentness` | `checkpoint_consistency` |
| `time_semantics` | `report_contract` |
| `lineage_projection` | `semantic_lineage` |
| `bilateral_transfer` | `transfer_state` |
| `retention_hold` | `retention_hold` |
| `erasure_closure` | `erasure_coverage` |
| `zone_privacy` | `zone_privacy` |
| `restore_non_resurrection` | `restore_authority` |
| `qualified_completeness` | `qualified_completeness` |
| `offline_portability` | `offline_portability` |
| `algorithm_agility` | `profile_support` |
| `resource_bounds` | `resource_bounds` |
| `verification_contract` | `report_contract` |

## Requirement-to-fixture map

| Requirement | Requirement family | Blocking result class | Positive fixture | Negative fixture | Summary |
|---|---|---|---|---|---|
| `CST-CLAIM-001` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-001-P` | `V02-CLAIM-001-N` | A verifier MUST distinguish authenticated custody history from substantive truth. Valid custody evidence MUST NOT be reported as proof that subject content is true, current, lawful, useful, or endorsed. |
| `CST-CLAIM-002` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-002-P` | `V02-CLAIM-002-N` | A verifier MUST distinguish admitted-event continuity from source completeness. A valid disclosed stream MUST NOT prove that no stream or pre-admission source item was omitted. |
| `CST-CLAIM-003` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-003-P` | `V02-CLAIM-003-N` | A verifier MUST distinguish internal validity from currentness. An internally valid prefix or restore MUST NOT be reported as current without independently retained freshness evidence required by the active profile. |
| `CST-CLAIM-004` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-004-P` | `V02-CLAIM-004-N` | A verifier MUST distinguish evidence availability from evidence validity. Missing, withheld, offline, erased, and invalid evidence are separate states. |
| `CST-CLAIM-005` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-005-P` | `V02-CLAIM-005-N` | An erasure result MUST name its evaluated custody boundary and MUST NOT claim universal or physical deletion beyond verified coverage. |
| `CST-CLAIM-006` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-006-P` | `V02-CLAIM-006-N` | A valid signature MUST establish only message integrity and key control under the signature profile. Semantic authority MUST be verified separately. |
| `CST-CLAIM-007` | `claim_discipline` | `CLAIM_OVERREACH` | `V02-CLAIM-007-P` | `V02-CLAIM-007-N` | Conformance reports MUST name exact protocol/profile versions, tested surfaces, fixture set, unavailable coverage, and each assurance dimension. They MUST NOT use an undifferentiated “custody-chain conformant” result. |
| `CST-FLD-001` | `field_mutability` | `LOCKED_FIELD_CHANGE` | `V02-FLD-001-P` | `V02-FLD-001-N` | Event identity, profile/version, event class, principal, custody zone, stream/epoch/position, predecessor or genesis marker, original temporal assertions, actor/runtime/credential claims, authority-at-write evidence, lineage, payload-state or commitment assertion, retention class, extension set, and algorithm-suite references MUST be immutable after recording. |
| `CST-FLD-002` | `field_mutability` | `LOCKED_FIELD_CHANGE` | `V02-FLD-002-P` | `V02-FLD-002-N` | Corrections, acceptance, rejection, conflict, supersession, retirement, withdrawal, transfer, hold, erasure, restore, key transition, checkpoint, and witness evidence MUST append events or receipts. They MUST NOT rewrite the historical envelope they affect. |
| `CST-FLD-003` | `field_mutability` | `LOCKED_FIELD_CHANGE` | `V02-FLD-003-P` | `V02-FLD-003-N` | Subject payload and commitment-opening material MAY be erased as a whole under an authorized erasure transition. Their absence without valid erasure evidence MUST NOT be reported as erasure. |
| `CST-FLD-004` | `field_mutability` | `LOCKED_FIELD_CHANGE` | `V02-FLD-004-P` | `V02-FLD-004-N` | Search indexes, vectors, graphs, rankings, summaries, caches, and context packs MUST be declared rebuildable projections. They MUST NOT become authoritative custody records merely through persistence or use. |
| `CST-FLD-005` | `field_mutability` | `LOCKED_FIELD_CHANGE` | `V02-FLD-005-P` | `V02-FLD-005-N` | A profile MUST publish its complete field mutability matrix. An unclassified field that can affect identity, authority, interpretation, ordering, lifecycle, or verification MUST fail profile validation. |
| `CST-REC-001` | `recording_boundary` | `RECORDING_BOUNDARY_VIOLATION` | `V02-REC-001-P` | `V02-REC-001-N` | A profile MUST define one durable recording boundary for each custody event. An implementation MUST NOT return recorded success before the canonical event bytes, event identifier, payload state or commitment, authority-at-write evidence, stream identity/epoch/position, predecessor, and resulting stream head are durably committed as one atomic outcome. |
| `CST-REC-002` | `recording_boundary` | `RECORDING_BOUNDARY_VIOLATION` | `V02-REC-002-P` | `V02-REC-002-N` | A failure before that boundary MUST leave no event that can be exported, checkpointed, verified, or presented as committed. A recoverable prepare state MUST be explicitly typed and MUST NOT be interpreted as recorded. |
| `CST-REC-003` | `recording_boundary` | `RECORDING_BOUNDARY_VIOLATION` | `V02-REC-003-P` | `V02-REC-003-N` | A successful retry MUST return the original committed outcome for the same scoped operation identifier and identical canonical input. Reuse with different canonical input MUST fail `REPLAY_CONFLICT`. |
| `CST-REC-004` | `recording_boundary` | `RECORDING_BOUNDARY_VIOLATION` | `V02-REC-004-P` | `V02-REC-004-N` | Immutability enforcement MUST cover every surface claimed by the implementation, including routine APIs, services, direct data access, import, restore, replication, migration, maintenance, and privileged tooling. Untested or unavailable surfaces MUST be reported. |
| `CST-REC-005` | `recording_boundary` | `RECORDING_BOUNDARY_VIOLATION` | `V02-REC-005-P` | `V02-REC-005-N` | Routine mutation prevention and privileged-tamper detection MUST be reported as different assurance dimensions. |
| `CST-ENV-001` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-001-P` | `V02-ENV-001-N` | The event commitment MUST bind all fields that affect identity, scope, authority, interpretation, ordering, lifecycle, payload state, or verification. |
| `CST-ENV-002` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-002-P` | `V02-ENV-002-N` | Event, payload, authority, checkpoint, transfer, erasure, restore, registry, and witness objects MUST use distinct domain-separation identifiers and unambiguous length framing. |
| `CST-ENV-003` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-003-P` | `V02-ENV-003-N` | Object commitments MUST bind principal, custody zone, stream, epoch, profile, and purpose where those scopes apply. Cross-principal, cross-zone, cross-stream, cross-epoch, cross-class, and cross-purpose substitution MUST fail. |
| `CST-ENV-004` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-004-P` | `V02-ENV-004-N` | Unknown critical extensions or schemas MUST fail semantic verification. Unknown noncritical extensions MAY remain uninterpreted only when exact canonical bytes and criticality are preserved through export and restore. |
| `CST-ENV-005` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-005-P` | `V02-ENV-005-N` | A human rendering MUST remain traceable to the exact committed bytes and MUST identify omitted, transformed, unresolved, or unsupported fields. |
| `CST-ENV-006` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-006-P` | `V02-ENV-006-N` | Secrets, bearer credentials, private key material, and payload-equivalent free text MUST NOT appear in durable custody envelopes. |
| `CST-ENV-007` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-007-P` | `V02-ENV-007-N` | Direct subject identity and reversible source locators MUST be replaced by scoped pseudonyms or separately erasable references unless a declared legal and privacy basis requires them. |
| `CST-ENV-008` | `envelope_domain_binding` | `DOMAIN_BINDING_INVALID` | `V02-ENV-008-P` | `V02-ENV-008-N` | Every event or receipt signature envelope MUST bind purpose, object, scope, key epoch, suite, and exact canonical commitment; cross-purpose or cross-scope validity is insufficient. |
| `CST-CAN-001` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-001-P` | `V02-CAN-001-N` | A canonicalization profile MUST define exact encoding, member ordering, array semantics, map-key rules, byte-string representation, and one canonical byte representation for every valid logical value. |
| `CST-CAN-002` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-002-P` | `V02-CAN-002-N` | It MUST define Unicode acceptance and normalization policy; malformed Unicode and prohibited normalization ambiguity MUST fail closed. |
| `CST-CAN-003` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-003-P` | `V02-CAN-003-N` | It MUST distinguish absent, null, empty, unknown, withheld, not-applicable, erased, and unavailable states wherever those meanings differ. |
| `CST-CAN-004` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-004-P` | `V02-CAN-004-N` | It MUST reject duplicate member names before semantic interpretation. |
| `CST-CAN-005` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-005-P` | `V02-CAN-005-N` | It MUST define integer and decimal grammar, numeric ranges, negative-zero behavior, and floating-point policy. Caller-language numeric coercion MUST NOT alter canonical meaning. |
| `CST-CAN-006` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-006-P` | `V02-CAN-006-N` | It MUST define timestamp grammar, precision, offsets, timezone, leap-second handling, and uncertainty representation. |
| `CST-CAN-007` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-007-P` | `V02-CAN-007-N` | Unsupported canonicalization versions and noncanonical alternate encodings MUST fail `NONCANONICAL_ENCODING` or `UNSUPPORTED_PROFILE` rather than being silently normalized at verification time. |
| `CST-CAN-008` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-008-P` | `V02-CAN-008-N` | A released profile MUST publish cross-implementation golden vectors containing logical input, exact canonical bytes, object commitment, and deterministic invalid-input outcomes. |
| `CST-CAN-009` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-009-P` | `V02-CAN-009-N` | A parser MUST reject trailing data, ambiguous framing, type confusion, and object-domain substitution. |
| `CST-CAN-010` | `canonicalization` | `NONCANONICAL_ENCODING` | `V02-CAN-010-P` | `V02-CAN-010-N` | Canonical bytes recorded under an older profile MUST remain the historical bytes. A later profile MUST NOT silently recanonicalize or rehash them. |
| `CST-AUTH-001` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-001-P` | `V02-AUTH-001-N` | Actor, runtime, credential/key, principal, authorization, and reviewer/acceptor MUST be represented as distinct assertions. |
| `CST-AUTH-002` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-002-P` | `V02-AUTH-002-N` | Historical authorization MUST resolve to immutable snapshots, content-addressed artifacts, or append-only authority events. Mutable URLs, aliases, current role rows, or current policy state MUST NOT establish authority at an earlier recording boundary. |
| `CST-AUTH-003` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-003-P` | `V02-AUTH-003-N` | Delegation MUST bind grantor, grantee, principal, custody zones, stream or object scope, permitted event classes and operations, assurance requirements, start and end conditions, constraints, delegation depth, and revocation semantics. |
| `CST-AUTH-004` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-004-P` | `V02-AUTH-004-N` | A delegate MUST NOT broaden its own authority or delegate beyond its allowed depth and scope. |
| `CST-AUTH-005` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-005-P` | `V02-AUTH-005-N` | A signature from a valid key with absent, expired, revoked, compromised, wrong-scope, or wrong-operation authority MUST NOT produce an authority pass. |
| `CST-AUTH-006` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-006-P` | `V02-AUTH-006-N` | Key evidence MUST append introduction, activation, scope, epoch, rotation, expiry, revocation, recovery, replacement, and compromise events as applicable. |
| `CST-AUTH-007` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-007-P` | `V02-AUTH-007-N` | Compromise analysis MUST use trusted stream/checkpoint ordering boundaries. Event-supplied wall-clock time alone MUST NOT place an event outside a compromise interval. |
| `CST-AUTH-008` | `historical_authority` | `AUTHORITY_UNVERIFIABLE` | `V02-AUTH-008-P` | `V02-AUTH-008-N` | Missing historical authority evidence MUST produce `AUTHORITY_UNVERIFIABLE`; it MUST NOT fall back to current authority state. |
| `CST-STR-001` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-001-P` | `V02-STR-001-N` | Each authority scope MUST commit to a stream registry or inventory root covering active, sealed, superseded, erased, retired, and replaced streams. |
| `CST-STR-002` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-002-P` | `V02-STR-002-N` | Stream identity MUST be collision-resistant and bound to principal, custody zone, stream profile, creation epoch, and a non-reusable genesis record. |
| `CST-STR-003` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-003-P` | `V02-STR-003-N` | Stream creation, epoch transition, sealing, replacement, supersession, erasure, and retirement MUST append registry lifecycle events. |
| `CST-STR-004` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-004-P` | `V02-STR-004-N` | A retired, erased, deleted, restored, or reinitialized stream identifier MUST NOT be reused as a new genesis stream. |
| `CST-STR-005` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-005-P` | `V02-STR-005-N` | Registry omission, unknown later genesis, registry/head mismatch, or unaccounted lifecycle transition MUST produce `STREAM_INVENTORY_INCOMPLETE` or a stronger integrity failure. |
| `CST-STR-006` | `stream_registry` | `STREAM_INVENTORY_INCOMPLETE` | `V02-STR-006-P` | `V02-STR-006-N` | A verifier MUST report disclosed-stream continuity separately from registry completeness. |
| `CST-APP-001` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-001-P` | `V02-APP-001-N` | Append MUST atomically validate the expected predecessor and epoch, assign the next contiguous position, reserve event and scoped operation identifiers, commit event and payload state, and advance the head. |
| `CST-APP-002` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-002-P` | `V02-APP-002-N` | An append implementation MUST NOT use last-write-wins resolution. |
| `CST-APP-003` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-003-P` | `V02-APP-003-N` | Concurrent mutually exclusive successors MUST yield one committed winner and explicit rejected/conflict outcomes, or an explicitly profiled branch model. They MUST NOT silently overwrite or discard a valid competitor. |
| `CST-APP-004` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-004-P` | `V02-APP-004-N` | Competing valid successors for the same predecessor/position MUST be preserved and reported `STREAM_FORK` or `EQUIVOCATION_DETECTED` according to evidence. |
| `CST-APP-005` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-005-P` | `V02-APP-005-N` | Competing signed checkpoints for the same scope, prior checkpoint, epoch, and covered position with different roots MUST be reported `EQUIVOCATION_DETECTED`. |
| `CST-APP-006` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-006-P` | `V02-APP-006-N` | Crash recovery MUST deterministically classify prepared, committed, rejected, and orphaned material. Prepared or orphaned material MUST NOT be checkpointed or exported as committed. |
| `CST-APP-007` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-007-P` | `V02-APP-007-N` | Replay identifiers MUST be bound to principal, zone, stream, epoch, event class, operation, and canonical input commitment. |
| `CST-APP-008` | `atomic_append` | `APPEND_RESULT_INVALID` | `V02-APP-008-P` | `V02-APP-008-N` | Cross-scope replay, same-ID/different-bytes, and changed-package retry MUST fail without append. |
| `CST-CHK-001` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-001-P` | `V02-CHK-001-N` | A checkpoint signature MUST cover the complete canonical checkpoint bytes and purpose context. |
| `CST-CHK-002` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-002-P` | `V02-CHK-002-N` | Inclusion proves membership only in the named checkpoint. It MUST NOT be reported as append-only consistency, absence, completeness, latestness, or non-equivocation evidence. |
| `CST-CHK-003` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-003-P` | `V02-CHK-003-N` | Append-only extension MUST be established through checkpoint ancestry plus a valid consistency proof or an equally explicit profile mechanism. |
| `CST-CHK-004` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-004-P` | `V02-CHK-004-N` | A profile MUST define leaf ordering, leaf/interior domain separation, odd-node behavior, empty-tree behavior, proof grammar, and proof resource ceilings. |
| `CST-CHK-005` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-005-P` | `V02-CHK-005-N` | Currentness claims MUST compare the presented checkpoint against an independently retained sufficiently recent trusted head or witness required by policy. |
| `CST-CHK-006` | `checkpoint_currentness` | `FRESHNESS_REQUIREMENT_UNMET` | `V02-CHK-006-P` | `V02-CHK-006-N` | A valid out-of-threshold checkpoint MUST report `dimension_status: stale`; a named currentness claim that nevertheless passes MUST produce `FRESHNESS_REQUIREMENT_UNMET` and identify the policy. |
| `CST-CHK-007` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-007-P` | `V02-CHK-007-N` | Witness or anchor outage MUST report unavailable or stale coverage and MUST NOT cause authorization fail-open or silent assurance downgrade. |
| `CST-CHK-008` | `checkpoint_currentness` | `CHECKPOINT_INVALID` | `V02-CHK-008-P` | `V02-CHK-008-N` | A profile claiming non-equivocation MUST define independent capture, gossip, monitoring, quorum, or consensus assumptions sufficient to expose conflicting heads. |
| `CST-TIM-001` | `time_semantics` | `TIME_SEMANTICS_INVALID` | `V02-TIM-001-P` | `V02-TIM-001-N` | Asserted effective time, source-observed time, ingestion time, recorder-time claim, checkpoint issuance claim, and externally witnessed time MUST remain distinct. |
| `CST-TIM-002` | `time_semantics` | `TIME_SEMANTICS_INVALID` | `V02-TIM-002-P` | `V02-TIM-002-N` | Stream position and checkpoint ancestry define custody order. Wall-clock time MUST NOT reorder committed events. |
| `CST-TIM-003` | `time_semantics` | `TIME_SEMANTICS_INVALID` | `V02-TIM-003-P` | `V02-TIM-003-N` | Profiles MUST declare clock source, precision, timezone/offset grammar, leap-second handling, uncertainty, and implausible-future and rollback thresholds. |
| `CST-TIM-004` | `time_semantics` | `TIME_SEMANTICS_INVALID` | `V02-TIM-004-P` | `V02-TIM-004-N` | Clock rollback or implausible future time MUST be reported without rewriting committed order or silently repairing the timestamp. |
| `CST-TIM-005` | `time_semantics` | `TIME_SEMANTICS_INVALID` | `V02-TIM-005-P` | `V02-TIM-005-N` | External time proves at most that a commitment existed no later than the witness assertion under its trust model. It MUST NOT prove occurrence time, truth, completeness, or authority. |
| `CST-SUP-001` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-001-P` | `V02-SUP-001-N` | Correction, conflict, supersession, acceptance, rejection, retirement, withdrawal, and transfer references MUST resolve to existing compatible targets in the authorized principal/zone scope unless an authorized cross-zone transfer profile permits otherwise. |
| `CST-SUP-002` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-002-P` | `V02-SUP-002-N` | Missing targets, self-links, prohibited cycles, wrong-scope links, illegal forks, and mutable authority references MUST fail deterministically. |
| `CST-SUP-003` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-003-P` | `V02-SUP-003-N` | Profiles MUST state whether competing corrections are prohibited, preserved as conflicts, or represented as explicit branches. |
| `CST-SUP-004` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-004-P` | `V02-SUP-004-N` | Current-winner selection MUST be deterministic, versioned, rebuildable, and based only on verified authority and lifecycle events. |
| `CST-SUP-005` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-005-P` | `V02-SUP-005-N` | A projection MUST identify its input checkpoint/event set, builder implementation/profile, build time, and freshness state. |
| `CST-SUP-006` | `lineage_projection` | `LINEAGE_INVALID` | `V02-SUP-006-P` | `V02-SUP-006-N` | Correction, rejection, withdrawal, supersession, erasure, or relevant authority failure MUST synchronously invalidate affected authoritative projections or prevent authoritative use until rebuild. |
| `CST-XFR-001` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-001-P` | `V02-XFR-001-N` | Every transfer event MUST bind one unique transfer identifier, sender and recipient principals/zones, sender authority, recipient authority where applicable, exact package/object commitment, source registry/checkpoint head, destination scope, transfer mode, obligations, expiry, and declared loss or transformation. |
| `CST-XFR-002` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-002-P` | `V02-XFR-002-N` | Sender release and recipient acceptance MUST be separate authorized events. |
| `CST-XFR-003` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-003-P` | `V02-XFR-003-N` | Possession, dispatch, byte receipt, or checksum verification MUST NOT imply semantic acceptance, truth, promotion, completed transfer, or destination authority. |
| `CST-XFR-004` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-004-P` | `V02-XFR-004-N` | Completion MUST require the profile-defined sender and recipient evidence and MUST reference the exact accepted commitment. |
| `CST-XFR-005` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-005-P` | `V02-XFR-005-N` | Exclusive, copied, and retained-custody modes MUST have distinct obligations and MUST NOT be inferred from one another. |
| `CST-XFR-006` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-006-P` | `V02-XFR-006-N` | Wrong recipient, changed package, expired offer, replayed acceptance, unilateral completion, missing recipient authority, and scope mismatch MUST fail. |
| `CST-XFR-007` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-007-P` | `V02-XFR-007-N` | Partial acceptance MUST enumerate accepted and rejected inventory commitments and MUST NOT be reported complete for the full offer. |
| `CST-XFR-008` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-008-P` | `V02-XFR-008-N` | Cancellation and expiry MUST append; they MUST NOT erase evidence of dispatch or receipt. |
| `CST-XFR-009` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-009-P` | `V02-XFR-009-N` | A destination MUST preserve origin attribution and MUST record destination acceptance separately. |
| `CST-XFR-010` | `bilateral_transfer` | `TRANSFER_STATE_VIOLATION` | `V02-XFR-010-P` | `V02-XFR-010-N` | Transfer disclosures MUST obey custody-zone privacy and selective-disclosure requirements. |
| `CST-RET-001` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-001-P` | `V02-RET-001-N` | The lifecycle MUST distinguish active retention, expiry, erasure requested, erasure pending, hold active, hold blocked, hold modified, hold released/expired, locally erased, external-copy pending, and outside-custody/unknown states. |
| `CST-RET-002` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-002-P` | `V02-RET-002-N` | A hold MUST bind authority, scope, policy version, basis code, start, review, expiry or release conditions, and affected operations. |
| `CST-RET-003` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-003-P` | `V02-RET-003-N` | A hold MUST NOT authorize unrelated processing, disclosure, cross-zone correlation, or indefinite retention beyond its declared scope and conditions. |
| `CST-RET-004` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-004-P` | `V02-RET-004-N` | Erasure blocked by a valid hold MUST append a minimized blocked/pending result and MUST NOT report erasure complete. |
| `CST-RET-005` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-005-P` | `V02-RET-005-N` | Hold narrowing, modification, release, expiry, and invalidation MUST append and preserve the prior state. |
| `CST-RET-006` | `retention_hold` | `RETENTION_STATE_INVALID` | `V02-RET-006-P` | `V02-RET-006-N` | An invalid, expired, unverifiable, or wrong-scope hold MUST NOT block erasure under the applicable policy. |
| `CST-ERA-001` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-001-P` | `V02-ERA-001-N` | Erasure scope MUST account for subject data in payloads, envelopes, quotes, identifiers, locators, indexes, vectors, summaries, caches, logs, replicas, exports, backups, external processors, ciphertext, key copies, wrappers, escrow, recovery material, crash artifacts, and other derivatives. |
| `CST-ERA-002` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-002-P` | `V02-ERA-002-N` | An erasure operation MUST append target, authority, policy basis code, requested scope, method, per-surface outcome, verification evidence, residual limitations, retry/expiry conditions, and resulting verification capability. |
| `CST-ERA-003` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-003-P` | `V02-ERA-003-N` | Per-surface outcomes MUST distinguish at least verified, failed, pending, unreachable, offline, stale, retained-by-policy, outside-custody, and unknown. |
| `CST-ERA-004` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-004-P` | `V02-ERA-004-N` | A durable erasure receipt MUST use bounded typed fields and MUST NOT retain free-text subject reasons, plaintext excerpts, direct subject identifiers, bearer credentials, mutable locators, commitment-opening material, payload-equivalent content, or unnecessary globally correlatable identifiers. |
| `CST-ERA-005` | `erasure_closure` | `PAYLOAD_STATE_UNVERIFIABLE` | `V02-ERA-005-P` | `V02-ERA-005-N` | Missing content without a valid erasure event MUST report payload state `unknown`, not erased; representing it as erased or available MUST produce `PAYLOAD_STATE_UNVERIFIABLE`. |
| `CST-ERA-006` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-006-P` | `V02-ERA-006-N` | Destroying one key or locator MUST NOT establish cryptographic erasure while required key copies, wrappers, escrow, recovery material, replicas, snapshots, or temporary copies remain unaccounted. |
| `CST-ERA-007` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-007-P` | `V02-ERA-007-N` | The complete surviving artifact and service/API set MUST meet the active profile's candidate-confirmation resistance for erased low-entropy content. A public salt beside a plaintext digest is insufficient. |
| `CST-ERA-008` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-008-P` | `V02-ERA-008-N` | Destruction of commitment-opening material MUST report the resulting loss of future payload-verification capability. |
| `CST-ERA-009` | `erasure_closure` | `LOCKED_FIELD_CHANGE` | `V02-ERA-009-P` | `V02-ERA-009-N` | Original canonical bytes and commitments MUST NOT be rewritten or replaced; an authorized derivative MUST bind the original commitment, transformation profile, removed-field classes, authority, and assurance loss and MUST NOT be represented as the original. |
| `CST-ERA-010` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-010-P` | `V02-ERA-010-N` | Full-fidelity archival restore and privacy-safe post-erasure export MUST be distinct profiles. Root equality is required only when the authorized retained artifact set is unchanged. |
| `CST-ERA-011` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-011-P` | `V02-ERA-011-N` | Erasure propagation to external recipients MUST report acknowledgement, completion, refusal, timeout, outside-custody, and unknown states separately. |
| `CST-ERA-012` | `erasure_closure` | `ERASURE_REQUIREMENT_UNMET` | `V02-ERA-012-P` | `V02-ERA-012-N` | An erasure receipt MUST NOT claim universal deletion or practical irrecoverability beyond the declared threat model and verified coverage. |
| `CST-PRV-001` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-001-P` | `V02-PRV-001-N` | Every immutable envelope field MUST have a privacy classification, retention/disclosure rule, and erasure or legal basis in the active profile. |
| `CST-PRV-002` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-002-P` | `V02-PRV-002-N` | Zone profiles MUST define separate namespaces, authorization policy, verifier policy, key scope, and disclosure policy. |
| `CST-PRV-003` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-003-P` | `V02-PRV-003-N` | Private roots, event counts, timing/cadence, reversible locators, actor identifiers, proof-access patterns, and globally correlatable identifiers MUST NOT cross zones without an authorized purpose-bound disclosure event. |
| `CST-PRV-004` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-004-P` | `V02-PRV-004-N` | Selective-disclosure evidence MUST bind audience, purpose, scope, validity interval, disclosed fields, source commitment, and replay protection. |
| `CST-PRV-005` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-005-P` | `V02-PRV-005-N` | Disclosure interfaces MUST be authorized and non-enumerable under the profile. Proof possession MUST NOT grant broader query or correlation authority. |
| `CST-PRV-006` | `zone_privacy` | `ZONE_DISCLOSURE_UNAUTHORIZED` | `V02-PRV-006-P` | `V02-PRV-006-N` | Aggregate checkpoints spanning zones require an explicit profile, leakage analysis, and authorization. Otherwise aggregation MUST fail. |
| `CST-RST-001` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-001-P` | `V02-RST-001-N` | A restored store MUST begin quarantined and non-authoritative. |
| `CST-RST-002` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-002-P` | `V02-RST-002-N` | Before activation it MUST reconcile required independently retained checkpoint/witness evidence, checkpoint ancestry, stream registry and heads, source inventory where claimed, key/delegation/revocation/compromise state, retention and holds, erasures and withdrawals after the snapshot, and authority policy. |
| `CST-RST-003` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-003-P` | `V02-RST-003-N` | A stale or partial restore MUST report the applicable dimension status and `operation_disposition: quarantined`; activation despite quarantine MUST produce `RESTORE_ACTIVATION_VIOLATION`. |
| `CST-RST-004` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-004-P` | `V02-RST-004-N` | A restore MUST NOT expose payloads whose later erasure, withdrawal, hold, transfer, or authority state is unknown under the required freshness policy. |
| `CST-RST-005` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-005-P` | `V02-RST-005-N` | A stale restore MUST NOT resurrect erased payload, expired authority, retired streams, superseded current state, or compromised key status. |
| `CST-RST-006` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-006-P` | `V02-RST-006-N` | Restore MUST preserve original event identity, stream/epoch/position, origin, recorded-time claim, canonical bytes, and commitments. |
| `CST-RST-007` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-007-P` | `V02-RST-007-N` | Restore MUST assign a distinct restore-instance identity and append a continuation, recovery, or promotion event before a writable authority can be established. |
| `CST-RST-008` | `restore_non_resurrection` | `RESTORE_ACTIVATION_VIOLATION` | `V02-RST-008-P` | `V02-RST-008-N` | A restored copy MUST NOT silently clone the writable authority of its source. |
| `CST-CMP-001` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-001-P` | `V02-CMP-001-N` | Every completeness claim MUST identify a frozen source scope, independently captured or authenticated source inventory/root, adapter version, extraction boundary, exclusions, and item disposition map. |
| `CST-CMP-002` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-002-P` | `V02-CMP-002-N` | Verification MUST distinguish admitted-stream continuity, declared-manifest accounting, authenticated-source-inventory accounting, and live-source completeness. |
| `CST-CMP-003` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-003-P` | `V02-CMP-003-N` | Live-source completeness MUST remain unknown unless the source supplies an authenticated snapshot or cursor contract covering the claim. |
| `CST-CMP-004` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-004-P` | `V02-CMP-004-N` | Inclusion evidence MUST NOT be represented as absence or completeness evidence. |
| `CST-CMP-005` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-005-P` | `V02-CMP-005-N` | Omission before manifest generation with no independently trustworthy source boundary MUST produce completeness unknown, not pass. |
| `CST-CMP-006` | `qualified_completeness` | `SOURCE_ACCOUNTING_INCOMPLETE` | `V02-CMP-006-P` | `V02-CMP-006-N` | Missing or unexplained in-scope inventory dispositions MUST fail `SOURCE_ACCOUNTING_INCOMPLETE`. |
| `CST-OFF-001` | `offline_portability` | `OFFLINE_CLAIM_UNSUPPORTED` | `V02-OFF-001-P` | `V02-OFF-001-N` | An offline-verification bundle MUST include or immutably reference canonical bytes, schemas/profiles, algorithm rules, event inventory, stream registry, authority/delegation/key history, revocation/compromise evidence, checkpoints, proofs, witness/anchor receipts, and coverage/loss manifests required by the claimed dimensions. |
| `CST-OFF-002` | `offline_portability` | `OFFLINE_CLAIM_UNSUPPORTED` | `V02-OFF-002-P` | `V02-OFF-002-N` | Trust roots and previously trusted heads MUST come from verifier configuration or a separately authenticated trust transition. They MUST NOT be silently trusted from the bundle under test. |
| `CST-OFF-003` | `offline_portability` | `OFFLINE_CLAIM_UNSUPPORTED` | `V02-OFF-003-P` | `V02-OFF-003-N` | Network, source, signer, schema registry, or provider unavailability MUST produce explicit unavailable/unsupported dimensions rather than causing online fallback or silent trust substitution. |
| `CST-OFF-004` | `offline_portability` | `OFFLINE_CLAIM_UNSUPPORTED` | `V02-OFF-004-P` | `V02-OFF-004-N` | A profile claiming provider exit MUST define export of all verification evidence, keys or public-key history, proof material, and tool/profile versions needed after provider removal. |
| `CST-ALG-001` | `algorithm_agility` | `ALGORITHM_POLICY_VIOLATION` | `V02-ALG-001-P` | `V02-ALG-001-N` | Algorithm and canonicalization identifiers MUST be authenticated and MUST bind their exact creation-time rules. |
| `CST-ALG-002` | `algorithm_agility` | `ALGORITHM_POLICY_VIOLATION` | `V02-ALG-002-P` | `V02-ALG-002-N` | Profiles MUST define creation and verification security floors, deprecation, expiry, unsupported behavior, and downgrade policy. |
| `CST-ALG-003` | `algorithm_agility` | `ALGORITHM_POLICY_VIOLATION` | `V02-ALG-003-P` | `V02-ALG-003-N` | Unknown, prohibited, deprecated-below-floor, or silently downgraded suites MUST fail or produce an explicit policy-unacceptable result; they MUST NOT silently pass. |
| `CST-ALG-004` | `algorithm_agility` | `ALGORITHM_POLICY_VIOLATION` | `V02-ALG-004-P` | `V02-ALG-004-N` | Algorithm or canonicalization migration MUST append a bridge event binding the final old-suite commitment/checkpoint to the first new-suite commitment/checkpoint. |
| `CST-ALG-005` | `algorithm_agility` | `ALGORITHM_POLICY_VIOLATION` | `V02-ALG-005-P` | `V02-ALG-005-N` | New profiles MUST NOT retroactively weaken the creation-time mutability matrix, field meaning, authority contract, or canonical bytes of historical events. |
| `CST-RES-001` | `resource_bounds` | `RESOURCE_LIMIT_EXCEEDED` | `V02-RES-001-P` | `V02-RES-001-N` | Every verifier profile MUST define immutable maximum event/object size, extension count and size, array/map cardinality, proof size, Merkle depth, reference depth, stream count, bundle size, and total verification work. |
| `CST-RES-002` | `resource_bounds` | `RESOURCE_LIMIT_EXCEEDED` | `V02-RES-002-P` | `V02-RES-002-N` | Oversized, cyclic, excessively deep, or work-amplifying input MUST fail deterministically with `RESOURCE_LIMIT_EXCEEDED` or `REFERENCE_CYCLE`. |
| `CST-RES-003` | `resource_bounds` | `RESOURCE_LIMIT_EXCEEDED` | `V02-RES-003-P` | `V02-RES-003-N` | Caller options MUST NOT silently broaden profile ceilings. A broader profile requires a distinct authenticated profile identifier. |
| `CST-RES-004` | `resource_bounds` | `RESOURCE_LIMIT_EXCEEDED` | `V02-RES-004-P` | `V02-RES-004-N` | Resource-limit failure MUST occur before unbounded allocation, recursion, external retrieval, or semantic rendering. |
| `CST-RES-005` | `resource_bounds` | `RESOURCE_LIMIT_EXCEEDED` | `V02-RES-005-P` | `V02-RES-005-N` | Limits and observed unavailable coverage MUST appear in verifier output. |
| `CST-VER-001` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-001-P` | `V02-VER-001-N` | Parser/resource safety, required-profile support, critical-extension support, canonical bytes, and commitment integrity MUST take precedence over semantic success claims. |
| `CST-VER-002` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-002-P` | `V02-VER-002-N` | Chain/checkpoint integrity MUST take precedence over lifecycle, transfer, erasure, restore, and current-state interpretation. |
| `CST-VER-003` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-003-P` | `V02-VER-003-N` | Missing witness coverage, stale checkpoints, incomplete registry, unknown authority, unavailable anchors, or skipped surfaces MUST NOT collapse into pass. |
| `CST-VER-004` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-004-P` | `V02-VER-004-N` | Primary and secondary failures MAY both be reported, but a lower-precedence success MUST NOT mask a blocking higher-precedence failure. |
| `CST-VER-005` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-005-P` | `V02-VER-005-N` | Stable machine-readable result and error codes MUST remain backward-compatible within a released profile version. |
| `CST-VER-006` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-006-P` | `V02-VER-006-N` | Aggregate counts MUST NOT substitute for per-case or per-dimension results. |
| `CST-VER-007` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-007-P` | `V02-VER-007-N` | A verification report MUST bind the exact input commitment, verifier implementation/version, profile set, trust configuration identifier, execution time, and resource limits. |
| `CST-VER-008` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-008-P` | `V02-VER-008-N` | Unsupported or unverified critical dimensions MUST make the corresponding conformance claim unavailable. |
| `CST-VER-009` | `verification_contract` | `VERIFICATION_RESULT_INVALID` | `V02-VER-009-P` | `V02-VER-009-N` | Dimension status, operation disposition, and error class MUST remain orthogonal; ordinary lifecycle state MUST NOT be encoded solely as an error or used as verification evidence. |

## Coverage statement

- Parsed requirements: **147**.
- Every parsed requirement has one positive and one negative fixture handle.
- A fixture handle does not count as implemented, executed, or passing.
- Requirement-specific secondary result classes may be added without replacing the primary blocking class above.
- Exact machine-readable inputs, expected canonical bytes, expected result objects, and resource ceilings remain required before normative promotion.
