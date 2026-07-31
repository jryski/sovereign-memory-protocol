# 08 — Immutable Fields and Chain-of-Custody Verification v0.2

_Status: review candidate; not accepted, implementation-authorizing, or release-ready_
_Version: 0.2.0-draft.1_
_Last updated: 2026-07-31_

## 1. Scope and requirement language

This document defines the implementation-neutral SMP custody contract for write-once custody semantics, append-only lifecycle changes, separately erasable subject payloads, registered custody streams, historical authority, transfer, checkpoints, verification, export, and restore.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative when written in capitals, following RFC 2119 and RFC 8174.

This candidate does not select a database, cloud, signer service, timestamp authority, transparency log, ledger, or deployment. Concrete encodings, algorithms, witnesses, packaging, and assurance floors belong to versioned profiles. A profile MUST satisfy every applicable core requirement and MUST NOT weaken a creation-time requirement for historical events.

## 2. Claim boundary

- **CST-CLAIM-001:** A verifier MUST distinguish authenticated custody history from substantive truth. Valid custody evidence MUST NOT be reported as proof that subject content is true, current, lawful, useful, or endorsed.
- **CST-CLAIM-002:** A verifier MUST distinguish admitted-event continuity from source completeness. A valid disclosed stream MUST NOT prove that no stream or pre-admission source item was omitted.
- **CST-CLAIM-003:** A verifier MUST distinguish internal validity from currentness. An internally valid prefix or restore MUST NOT be reported as current without independently retained freshness evidence required by the active profile.
- **CST-CLAIM-004:** A verifier MUST distinguish evidence availability from evidence validity. Missing, withheld, offline, erased, and invalid evidence are separate states.
- **CST-CLAIM-005:** An erasure result MUST name its evaluated custody boundary and MUST NOT claim universal or physical deletion beyond verified coverage.
- **CST-CLAIM-006:** A valid signature MUST establish only message integrity and key control under the signature profile. Semantic authority MUST be verified separately.
- **CST-CLAIM-007:** Conformance reports MUST name exact protocol/profile versions, tested surfaces, fixture set, unavailable coverage, and each assurance dimension. They MUST NOT use an undifferentiated “custody-chain conformant” result.

## 3. Logical model and mutability classes

Every profile MUST classify every logical field as exactly one of:

1. **immutable envelope** — fixed after the recording boundary;
2. **append-only evidence** — later evidence may be appended without replacing prior evidence;
3. **write-once erasable payload** — not editable in place, but removable through an authorized erasure transition;
4. **rebuildable projection** — mutable derived state whose authoritative inputs and builder contract remain identified.

- **CST-FLD-001:** Event identity, profile/version, event class, principal, custody zone, stream/epoch/position, predecessor or genesis marker, original temporal assertions, actor/runtime/credential claims, authority-at-write evidence, lineage, payload-state or commitment assertion, retention class, extension set, and algorithm-suite references MUST be immutable after recording.
- **CST-FLD-002:** Corrections, acceptance, rejection, conflict, supersession, retirement, withdrawal, transfer, hold, erasure, restore, key transition, checkpoint, and witness evidence MUST append events or receipts. They MUST NOT rewrite the historical envelope they affect.
- **CST-FLD-003:** Subject payload and commitment-opening material MAY be erased as a whole under an authorized erasure transition. Their absence without valid erasure evidence MUST NOT be reported as erasure.
- **CST-FLD-004:** Search indexes, vectors, graphs, rankings, summaries, caches, and context packs MUST be declared rebuildable projections. They MUST NOT become authoritative custody records merely through persistence or use.
- **CST-FLD-005:** A profile MUST publish its complete field mutability matrix. An unclassified field that can affect identity, authority, interpretation, ordering, lifecycle, or verification MUST fail profile validation.

The core mutability matrix is:

| Logical field or field set | Required class | Change mechanism |
|---|---|---|
| Protocol, object, schema, and creation-time profile versions | immutable envelope | append bridge or successor under a new profile |
| Event/object identifier and class | immutable envelope | new event/object |
| Principal and custody-zone scope | immutable envelope | authorized transfer event |
| Stream identifier, epoch, position, predecessor, and genesis marker | immutable envelope | registry/epoch transition plus new event |
| Actor, runtime, credential/key binding, and authority-at-write evidence | immutable envelope | append authority/key evidence; never rewrite the historical claim |
| Original effective, observed, ingestion, and recorder-time assertions | immutable envelope | append correction or supersession |
| Source, evidence, subject, semantic-lineage, transfer, and lifecycle references | immutable envelope | append successor/lifecycle event |
| Canonical bytes, domain, extension inventory, and algorithm identifiers | immutable envelope | append profile bridge; preserve old bytes |
| Retention class, legal basis, and payload-state assertion at recording | immutable envelope | append retention, hold, or erasure transition |
| Subject/evidence payload and commitment-opening material | write-once erasable payload | authorized erasure transition with explicit assurance loss |
| Signatures, checkpoints, witnesses, authority events, and receipts | append-only evidence | append additional evidence or invalidating lifecycle event |
| Current state, search, vector, graph, ranking, summary, cache, and context-pack output | rebuildable projection | invalidate and rebuild from verified inputs |

## 4. Durable recording boundary

- **CST-REC-001:** A profile MUST define one durable recording boundary for each custody event. An implementation MUST NOT return recorded success before the canonical event bytes, event identifier, payload state or commitment, authority-at-write evidence, stream identity/epoch/position, predecessor, and resulting stream head are durably committed as one atomic outcome.
- **CST-REC-002:** A failure before that boundary MUST leave no event that can be exported, checkpointed, verified, or presented as committed. A recoverable prepare state MUST be explicitly typed and MUST NOT be interpreted as recorded.
- **CST-REC-003:** A successful retry MUST return the original committed outcome for the same scoped operation identifier and identical canonical input. Reuse with different canonical input MUST fail `REPLAY_CONFLICT`.
- **CST-REC-004:** Immutability enforcement MUST cover every surface claimed by the implementation, including routine APIs, services, direct data access, import, restore, replication, migration, maintenance, and privileged tooling. Untested or unavailable surfaces MUST be reported.
- **CST-REC-005:** Routine mutation prevention and privileged-tamper detection MUST be reported as different assurance dimensions.

## 5. Canonical custody envelope

Every recorded event MUST bind these logical fields:

- protocol and event-profile identifiers;
- canonicalization and algorithm-suite identifiers;
- event identifier and event class;
- principal and custody-zone identifiers;
- stream identifier, epoch, and contiguous position;
- predecessor commitment or explicit non-reusable genesis marker;
- actor, runtime, credential/key, and authority-at-write evidence;
- asserted effective time, source-observed time, and recorder-time claim, each with explicit state;
- subject, record, evidence, and source references appropriate to the class;
- lifecycle and semantic-lineage references;
- payload state and computationally appropriate commitment, or explicit no-payload marker;
- retention, legal-hold, and erasure classifications;
- extension inventory with criticality;
- commitment purpose and domain.

- **CST-ENV-001:** The event commitment MUST bind all fields that affect identity, scope, authority, interpretation, ordering, lifecycle, payload state, or verification.
- **CST-ENV-002:** Event, payload, authority, checkpoint, transfer, erasure, restore, registry, and witness objects MUST use distinct domain-separation identifiers and unambiguous length framing.
- **CST-ENV-003:** Object commitments MUST bind principal, custody zone, stream, epoch, profile, and purpose where those scopes apply. Cross-principal, cross-zone, cross-stream, cross-epoch, cross-class, and cross-purpose substitution MUST fail.
- **CST-ENV-004:** Unknown critical extensions or schemas MUST fail semantic verification. Unknown noncritical extensions MAY remain uninterpreted only when exact canonical bytes and criticality are preserved through export and restore.
- **CST-ENV-005:** A human rendering MUST remain traceable to the exact committed bytes and MUST identify omitted, transformed, unresolved, or unsupported fields.
- **CST-ENV-006:** Secrets, bearer credentials, private key material, and payload-equivalent free text MUST NOT appear in durable custody envelopes.
- **CST-ENV-007:** Direct subject identity and reversible source locators MUST be replaced by scoped pseudonyms or separately erasable references unless a declared legal and privacy basis requires them.
- **CST-ENV-008:** Every event or receipt signature envelope MUST bind signature purpose, object type, principal and custody-zone scope, stream/epoch where applicable, key identifier and epoch, algorithm suite, and the exact canonical object commitment. A signature valid only under a different purpose, object, scope, epoch, or suite MUST fail `DOMAIN_BINDING_INVALID`.

## 6. Canonicalization profiles

- **CST-CAN-001:** A canonicalization profile MUST define exact encoding, member ordering, array semantics, map-key rules, byte-string representation, and one canonical byte representation for every valid logical value.
- **CST-CAN-002:** It MUST define Unicode acceptance and normalization policy; malformed Unicode and prohibited normalization ambiguity MUST fail closed.
- **CST-CAN-003:** It MUST distinguish absent, null, empty, unknown, withheld, not-applicable, erased, and unavailable states wherever those meanings differ.
- **CST-CAN-004:** It MUST reject duplicate member names before semantic interpretation.
- **CST-CAN-005:** It MUST define integer and decimal grammar, numeric ranges, negative-zero behavior, and floating-point policy. Caller-language numeric coercion MUST NOT alter canonical meaning.
- **CST-CAN-006:** It MUST define timestamp grammar, precision, offsets, timezone, leap-second handling, and uncertainty representation.
- **CST-CAN-007:** Unsupported canonicalization versions and noncanonical alternate encodings MUST fail `NONCANONICAL_ENCODING` or `UNSUPPORTED_PROFILE` rather than being silently normalized at verification time.
- **CST-CAN-008:** A released profile MUST publish cross-implementation golden vectors containing logical input, exact canonical bytes, object commitment, and deterministic invalid-input outcomes.
- **CST-CAN-009:** A parser MUST reject trailing data, ambiguous framing, type confusion, and object-domain substitution.
- **CST-CAN-010:** Canonical bytes recorded under an older profile MUST remain the historical bytes. A later profile MUST NOT silently recanonicalize or rehash them.

## 7. Historical authority and key lifecycle

- **CST-AUTH-001:** Actor, runtime, credential/key, principal, authorization, and reviewer/acceptor MUST be represented as distinct assertions.
- **CST-AUTH-002:** Historical authorization MUST resolve to immutable snapshots, content-addressed artifacts, or append-only authority events. Mutable URLs, aliases, current role rows, or current policy state MUST NOT establish authority at an earlier recording boundary.
- **CST-AUTH-003:** Delegation MUST bind grantor, grantee, principal, custody zones, stream or object scope, permitted event classes and operations, assurance requirements, start and end conditions, constraints, delegation depth, and revocation semantics.
- **CST-AUTH-004:** A delegate MUST NOT broaden its own authority or delegate beyond its allowed depth and scope.
- **CST-AUTH-005:** A signature from a valid key with absent, expired, revoked, compromised, wrong-scope, or wrong-operation authority MUST NOT produce an authority pass.
- **CST-AUTH-006:** Key evidence MUST append introduction, activation, scope, epoch, rotation, expiry, revocation, recovery, replacement, and compromise events as applicable.
- **CST-AUTH-007:** Compromise analysis MUST use trusted stream/checkpoint ordering boundaries. Event-supplied wall-clock time alone MUST NOT place an event outside a compromise interval.
- **CST-AUTH-008:** Missing historical authority evidence MUST produce `AUTHORITY_UNVERIFIABLE`; it MUST NOT fall back to current authority state.

## 8. Stream registry and lifecycle

- **CST-STR-001:** Each authority scope MUST commit to a stream registry or inventory root covering active, sealed, superseded, erased, retired, and replaced streams.
- **CST-STR-002:** Stream identity MUST be collision-resistant and bound to principal, custody zone, stream profile, creation epoch, and a non-reusable genesis record.
- **CST-STR-003:** Stream creation, epoch transition, sealing, replacement, supersession, erasure, and retirement MUST append registry lifecycle events.
- **CST-STR-004:** A retired, erased, deleted, restored, or reinitialized stream identifier MUST NOT be reused as a new genesis stream.
- **CST-STR-005:** Registry omission, unknown later genesis, registry/head mismatch, or unaccounted lifecycle transition MUST produce `STREAM_INVENTORY_INCOMPLETE` or a stronger integrity failure.
- **CST-STR-006:** A verifier MUST report disclosed-stream continuity separately from registry completeness.

## 9. Atomic append, replay, forks, and equivocation

- **CST-APP-001:** Append MUST atomically validate the expected predecessor and epoch, assign the next contiguous position, reserve event and scoped operation identifiers, commit event and payload state, and advance the head.
- **CST-APP-002:** An append implementation MUST NOT use last-write-wins resolution.
- **CST-APP-003:** Concurrent mutually exclusive successors MUST yield one committed winner and explicit rejected/conflict outcomes, or an explicitly profiled branch model. They MUST NOT silently overwrite or discard a valid competitor.
- **CST-APP-004:** Competing valid successors for the same predecessor/position MUST be preserved and reported `STREAM_FORK` or `EQUIVOCATION_DETECTED` according to evidence.
- **CST-APP-005:** Competing signed checkpoints for the same scope, prior checkpoint, epoch, and covered position with different roots MUST be reported `EQUIVOCATION_DETECTED`.
- **CST-APP-006:** Crash recovery MUST deterministically classify prepared, committed, rejected, and orphaned material. Prepared or orphaned material MUST NOT be checkpointed or exported as committed.
- **CST-APP-007:** Replay identifiers MUST be bound to principal, zone, stream, epoch, event class, operation, and canonical input commitment.
- **CST-APP-008:** Cross-scope replay, same-ID/different-bytes, and changed-package retry MUST fail without append.

## 10. Checkpoints, witnesses, and currentness

A checkpoint MUST bind:

- checkpoint profile and suite;
- principal and custody-zone scope;
- stream/epoch or registry coverage;
- inclusive covered ranges, event count, and covered stream heads;
- first and last event commitments where applicable;
- Merkle or accumulator construction and root;
- prior checkpoint identifier and commitment, or explicit checkpoint genesis;
- signer role, key identifier, and key epoch;
- issuance-time claim and maximum freshness interval;
- extension inventory and signature purpose.

- **CST-CHK-001:** A checkpoint signature MUST cover the complete canonical checkpoint bytes and purpose context.
- **CST-CHK-002:** Inclusion proves membership only in the named checkpoint. It MUST NOT be reported as append-only consistency, absence, completeness, latestness, or non-equivocation evidence.
- **CST-CHK-003:** Append-only extension MUST be established through checkpoint ancestry plus a valid consistency proof or an equally explicit profile mechanism.
- **CST-CHK-004:** A profile MUST define leaf ordering, leaf/interior domain separation, odd-node behavior, empty-tree behavior, proof grammar, and proof resource ceilings.
- **CST-CHK-005:** Currentness claims MUST compare the presented checkpoint against an independently retained sufficiently recent trusted head or witness required by policy.
- **CST-CHK-006:** A valid checkpoint older than the declared age/count threshold MUST report `CHECKPOINT_STALE`.
- **CST-CHK-007:** Witness or anchor outage MUST report unavailable or stale coverage and MUST NOT cause authorization fail-open or silent assurance downgrade.
- **CST-CHK-008:** A profile claiming non-equivocation MUST define independent capture, gossip, monitoring, quorum, or consensus assumptions sufficient to expose conflicting heads.

## 11. Time semantics

- **CST-TIM-001:** Asserted effective time, source-observed time, ingestion time, recorder-time claim, checkpoint issuance claim, and externally witnessed time MUST remain distinct.
- **CST-TIM-002:** Stream position and checkpoint ancestry define custody order. Wall-clock time MUST NOT reorder committed events.
- **CST-TIM-003:** Profiles MUST declare clock source, precision, timezone/offset grammar, leap-second handling, uncertainty, and implausible-future and rollback thresholds.
- **CST-TIM-004:** Clock rollback or implausible future time MUST be reported without rewriting committed order or silently repairing the timestamp.
- **CST-TIM-005:** External time proves at most that a commitment existed no later than the witness assertion under its trust model. It MUST NOT prove occurrence time, truth, completeness, or authority.

## 12. Supersession graph and projections

- **CST-SUP-001:** Correction, conflict, supersession, acceptance, rejection, retirement, withdrawal, and transfer references MUST resolve to existing compatible targets in the authorized principal/zone scope unless an authorized cross-zone transfer profile permits otherwise.
- **CST-SUP-002:** Missing targets, self-links, prohibited cycles, wrong-scope links, illegal forks, and mutable authority references MUST fail deterministically.
- **CST-SUP-003:** Profiles MUST state whether competing corrections are prohibited, preserved as conflicts, or represented as explicit branches.
- **CST-SUP-004:** Current-winner selection MUST be deterministic, versioned, rebuildable, and based only on verified authority and lifecycle events.
- **CST-SUP-005:** A projection MUST identify its input checkpoint/event set, builder implementation/profile, build time, and freshness state.
- **CST-SUP-006:** Correction, rejection, withdrawal, supersession, erasure, or relevant authority failure MUST synchronously invalidate affected authoritative projections or prevent authoritative use until rebuild.

## 13. Bilateral custody transfer

A transfer state machine MUST distinguish at least `offered`, `dispatched`, `bytes_received`, `verified`, `accepted`, `rejected`, `partially_accepted`, `completed`, `cancelled`, `expired`, and `pending`.

- **CST-XFR-001:** Every transfer event MUST bind one unique transfer identifier, sender and recipient principals/zones, sender authority, recipient authority where applicable, exact package/object commitment, source registry/checkpoint head, destination scope, transfer mode, obligations, expiry, and declared loss or transformation.
- **CST-XFR-002:** Sender release and recipient acceptance MUST be separate authorized events.
- **CST-XFR-003:** Possession, dispatch, byte receipt, or checksum verification MUST NOT imply semantic acceptance, truth, promotion, completed transfer, or destination authority.
- **CST-XFR-004:** Completion MUST require the profile-defined sender and recipient evidence and MUST reference the exact accepted commitment.
- **CST-XFR-005:** Exclusive, copied, and retained-custody modes MUST have distinct obligations and MUST NOT be inferred from one another.
- **CST-XFR-006:** Wrong recipient, changed package, expired offer, replayed acceptance, unilateral completion, missing recipient authority, and scope mismatch MUST fail.
- **CST-XFR-007:** Partial acceptance MUST enumerate accepted and rejected inventory commitments and MUST NOT be reported complete for the full offer.
- **CST-XFR-008:** Cancellation and expiry MUST append; they MUST NOT erase evidence of dispatch or receipt.
- **CST-XFR-009:** A destination MUST preserve origin attribution and MUST record destination acceptance separately.
- **CST-XFR-010:** Transfer disclosures MUST obey custody-zone privacy and selective-disclosure requirements.

## 14. Retention and legal holds

- **CST-RET-001:** The lifecycle MUST distinguish active retention, expiry, erasure requested, erasure pending, hold active, hold blocked, hold modified, hold released/expired, locally erased, external-copy pending, and outside-custody/unknown states.
- **CST-RET-002:** A hold MUST bind authority, scope, policy version, basis code, start, review, expiry or release conditions, and affected operations.
- **CST-RET-003:** A hold MUST NOT authorize unrelated processing, disclosure, cross-zone correlation, or indefinite retention beyond its declared scope and conditions.
- **CST-RET-004:** Erasure blocked by a valid hold MUST append a minimized blocked/pending result and MUST NOT report erasure complete.
- **CST-RET-005:** Hold narrowing, modification, release, expiry, and invalidation MUST append and preserve the prior state.
- **CST-RET-006:** An invalid, expired, unverifiable, or wrong-scope hold MUST NOT block erasure under the applicable policy.

## 15. Erasure closure and privacy-safe receipts

- **CST-ERA-001:** Erasure scope MUST account for subject data in payloads, envelopes, quotes, identifiers, locators, indexes, vectors, summaries, caches, logs, replicas, exports, backups, external processors, ciphertext, key copies, wrappers, escrow, recovery material, crash artifacts, and other derivatives.
- **CST-ERA-002:** An erasure operation MUST append target, authority, policy basis code, requested scope, method, per-surface outcome, verification evidence, residual limitations, retry/expiry conditions, and resulting verification capability.
- **CST-ERA-003:** Per-surface outcomes MUST distinguish at least verified, failed, pending, unreachable, offline, stale, retained-by-policy, outside-custody, and unknown.
- **CST-ERA-004:** A durable erasure receipt MUST use bounded typed fields and MUST NOT retain free-text subject reasons, plaintext excerpts, direct subject identifiers, bearer credentials, mutable locators, commitment-opening material, payload-equivalent content, or unnecessary globally correlatable identifiers.
- **CST-ERA-005:** Missing content without a valid erasure event MUST report `PAYLOAD_UNAVAILABLE_UNKNOWN`, not erased.
- **CST-ERA-006:** Destroying one key or locator MUST NOT establish cryptographic erasure while required key copies, wrappers, escrow, recovery material, replicas, snapshots, or temporary copies remain unaccounted.
- **CST-ERA-007:** The complete surviving artifact and service/API set MUST meet the active profile's candidate-confirmation resistance for erased low-entropy content. A public salt beside a plaintext digest is insufficient.
- **CST-ERA-008:** Destruction of commitment-opening material MUST report the resulting loss of future payload-verification capability.
- **CST-ERA-009:** Erasure MUST NOT require rewriting unaffected custody-event commitments. If an immutable field itself contains erasable subject data, the profile MUST define an authorized privacy transformation and its explicit assurance loss; undeclared in-place redaction is nonconforming.
- **CST-ERA-010:** Full-fidelity archival restore and privacy-safe post-erasure export MUST be distinct profiles. Root equality is required only when the authorized retained artifact set is unchanged.
- **CST-ERA-011:** Erasure propagation to external recipients MUST report acknowledgement, completion, refusal, timeout, outside-custody, and unknown states separately.
- **CST-ERA-012:** An erasure receipt MUST NOT claim universal deletion or practical irrecoverability beyond the declared threat model and verified coverage.

## 16. Selective disclosure and custody-zone privacy

- **CST-PRV-001:** Every immutable envelope field MUST have a privacy classification, retention/disclosure rule, and erasure or legal basis in the active profile.
- **CST-PRV-002:** Zone profiles MUST define separate namespaces, authorization policy, verifier policy, key scope, and disclosure policy.
- **CST-PRV-003:** Private roots, event counts, timing/cadence, reversible locators, actor identifiers, proof-access patterns, and globally correlatable identifiers MUST NOT cross zones without an authorized purpose-bound disclosure event.
- **CST-PRV-004:** Selective-disclosure evidence MUST bind audience, purpose, scope, validity interval, disclosed fields, source commitment, and replay protection.
- **CST-PRV-005:** Disclosure interfaces MUST be authorized and non-enumerable under the profile. Proof possession MUST NOT grant broader query or correlation authority.
- **CST-PRV-006:** Aggregate checkpoints spanning zones require an explicit profile, leakage analysis, and authorization. Otherwise aggregation MUST fail.

## 17. Restore quarantine and non-resurrection

- **CST-RST-001:** A restored store MUST begin quarantined and non-authoritative.
- **CST-RST-002:** Before activation it MUST reconcile required independently retained checkpoint/witness evidence, checkpoint ancestry, stream registry and heads, source inventory where claimed, key/delegation/revocation/compromise state, retention and holds, erasures and withdrawals after the snapshot, and authority policy.
- **CST-RST-003:** An internally valid but stale or incompletely witnessed restore MUST report `RESTORE_QUARANTINED` and MUST NOT become authoritative.
- **CST-RST-004:** A restore MUST NOT expose payloads whose later erasure, withdrawal, hold, transfer, or authority state is unknown under the required freshness policy.
- **CST-RST-005:** A stale restore MUST NOT resurrect erased payload, expired authority, retired streams, superseded current state, or compromised key status.
- **CST-RST-006:** Restore MUST preserve original event identity, stream/epoch/position, origin, recorded-time claim, canonical bytes, and commitments.
- **CST-RST-007:** Restore MUST assign a distinct restore-instance identity and append a continuation, recovery, or promotion event before a writable authority can be established.
- **CST-RST-008:** A restored copy MUST NOT silently clone the writable authority of its source.

## 18. Qualified completeness

- **CST-CMP-001:** Every completeness claim MUST identify a frozen source scope, independently captured or authenticated source inventory/root, adapter version, extraction boundary, exclusions, and item disposition map.
- **CST-CMP-002:** Verification MUST distinguish admitted-stream continuity, declared-manifest accounting, authenticated-source-inventory accounting, and live-source completeness.
- **CST-CMP-003:** Live-source completeness MUST remain unknown unless the source supplies an authenticated snapshot or cursor contract covering the claim.
- **CST-CMP-004:** Inclusion evidence MUST NOT be represented as absence or completeness evidence.
- **CST-CMP-005:** Omission before manifest generation with no independently trustworthy source boundary MUST produce completeness unknown, not pass.
- **CST-CMP-006:** Missing or unexplained in-scope inventory dispositions MUST fail `SOURCE_ACCOUNTING_INCOMPLETE`.

## 19. Offline evidence bundle

- **CST-OFF-001:** An offline-verification bundle MUST include or immutably reference canonical bytes, schemas/profiles, algorithm rules, event inventory, stream registry, authority/delegation/key history, revocation/compromise evidence, checkpoints, proofs, witness/anchor receipts, and coverage/loss manifests required by the claimed dimensions.
- **CST-OFF-002:** Trust roots and previously trusted heads MUST come from verifier configuration or a separately authenticated trust transition. They MUST NOT be silently trusted from the bundle under test.
- **CST-OFF-003:** Network, source, signer, schema registry, or provider unavailability MUST produce explicit unavailable/unsupported dimensions rather than causing online fallback or silent trust substitution.
- **CST-OFF-004:** A profile claiming provider exit MUST define export of all verification evidence, keys or public-key history, proof material, and tool/profile versions needed after provider removal.

## 20. Algorithm and profile evolution

- **CST-ALG-001:** Algorithm and canonicalization identifiers MUST be authenticated and MUST bind their exact creation-time rules.
- **CST-ALG-002:** Profiles MUST define creation and verification security floors, deprecation, expiry, unsupported behavior, and downgrade policy.
- **CST-ALG-003:** Unknown, prohibited, deprecated-below-floor, or silently downgraded suites MUST fail or produce an explicit policy-unacceptable result; they MUST NOT silently pass.
- **CST-ALG-004:** Algorithm or canonicalization migration MUST append a bridge event binding the final old-suite commitment/checkpoint to the first new-suite commitment/checkpoint.
- **CST-ALG-005:** New profiles MUST NOT retroactively weaken the creation-time mutability matrix, field meaning, authority contract, or canonical bytes of historical events.

## 21. Verifier resource bounds

- **CST-RES-001:** Every verifier profile MUST define immutable maximum event/object size, extension count and size, array/map cardinality, proof size, Merkle depth, reference depth, stream count, bundle size, and total verification work.
- **CST-RES-002:** Oversized, cyclic, excessively deep, or work-amplifying input MUST fail deterministically with `RESOURCE_LIMIT_EXCEEDED` or `REFERENCE_CYCLE`.
- **CST-RES-003:** Caller options MUST NOT silently broaden profile ceilings. A broader profile requires a distinct authenticated profile identifier.
- **CST-RES-004:** Resource-limit failure MUST occur before unbounded allocation, recursion, external retrieval, or semantic rendering.
- **CST-RES-005:** Limits and observed unavailable coverage MUST appear in verifier output.

## 22. Deterministic verification results

A verifier MUST return structured dimensions. Each applicable dimension MUST distinguish `pass`, `fail`, `unknown`, `not_applicable`, and `not_checked`; applicable profiles add `stale`, `partial`, `offline`, `unsupported`, `forked`, `equivocating`, `quarantined`, or `policy_unacceptable`.

Reports MUST use the authoritative verification-dimension registry in
`05-verification.md`. This section adds custody-chain requirements to those
dimensions; it does not define competing local dimension names.

Profiles and reports MUST use separate claim tags rather than inferring stronger
claims from lower layers. The initial claim vocabulary is:

| Claim tag | Narrow meaning |
|---|---|
| `FIELD_ENFORCED` | Named locked fields resisted mutation on the reported tested surfaces |
| `LOCAL_CHAIN_VALID` | Disclosed canonical events form a valid local chain relative to the presented head |
| `CHECKPOINT_SIGNED` | A checkpoint signature and signer-key binding verified; authority and currentness remain separate |
| `INDEPENDENTLY_WITNESSED` | Named independent witness evidence verified for the stated checkpoint and coverage |
| `CURRENTNESS_VERIFIED` | Presented state reconciled to independently retained freshness evidence under the profile |
| `ERASURE_PARTIAL` | One or more declared erasure surfaces remain incomplete, unavailable, or unknown |
| `ERASURE_VERIFIED_WITHIN_SCOPE` | Erasure met the named boundary, threat model, surface inventory, and confirmation-resistance test |
| `OFFLINE_VERIFIABLE` | Declared dimensions verify without provider, source, signer, registry, or network access |
| `ROLLBACK_SUSPECTED` | Presented history predates or conflicts with trusted freshness evidence |
| `EQUIVOCATION_DETECTED` | Conflicting valid successors or checkpoints exist for the same exclusive scope/position |

- **CST-VER-001:** Parser/resource safety, required-profile support, critical-extension support, canonical bytes, and commitment integrity MUST take precedence over semantic success claims.
- **CST-VER-002:** Chain/checkpoint integrity MUST take precedence over lifecycle, transfer, erasure, restore, and current-state interpretation.
- **CST-VER-003:** Missing witness coverage, stale checkpoints, incomplete registry, unknown authority, unavailable anchors, or skipped surfaces MUST NOT collapse into pass.
- **CST-VER-004:** Primary and secondary failures MAY both be reported, but a lower-precedence success MUST NOT mask a blocking higher-precedence failure.
- **CST-VER-005:** Stable machine-readable result and error codes MUST remain backward-compatible within a released profile version.
- **CST-VER-006:** Aggregate counts MUST NOT substitute for per-case or per-dimension results.
- **CST-VER-007:** A verification report MUST bind the exact input commitment, verifier implementation/version, profile set, trust configuration identifier, execution time, and resource limits.
- **CST-VER-008:** Unsupported or unverified critical dimensions MUST make the corresponding conformance claim unavailable.
- **CST-VER-009:** A result MUST report verification outcome separately from operation disposition. Acceptance, rejection, conflict, pending, no-op, partial acceptance, or quarantine MUST NOT be used as evidence that verification passed.

## 23. Minimum conformance surfaces

A conformance claim MUST test every claimed applicable surface, including:

- public parser and verifier API;
- ordinary writer and service/RPC writer;
- import and package ingestion;
- direct or privileged maintenance path where claimed;
- replication/migration path where claimed;
- export and provider-independent restore;
- checkpoint signer, independent witness copy, and offline verifier;
- key rotation, revocation, and compromise simulation;
- projection invalidation and deterministic rebuild;
- transfer retry/reject/expiry/partial paths;
- hold and erasure across every declared online/offline surface;
- stale restore and non-resurrection;
- canonicalization ambiguity and resource-exhaustion vectors.

Untested, inaccessible, stale, offline, or unavailable surfaces MUST be listed beside the conclusion.

## 24. Core/profile boundary

The normative core defines the logical objects, required bindings, state machines, claim limits, structured outcomes, and security floors above. Separate versioned profiles define concrete:

- canonical encodings and golden bytes;
- commitment and signature suites;
- Merkle/accumulator construction and proofs;
- checkpoint cadence and witness policy;
- timestamp, transparency, or consensus mechanisms;
- packaging and offline bundle formats;
- privacy/erasure threat models and candidate-confirmation tests;
- deployment assurance levels and resource ceilings.

No profile may represent a provider account, database trigger, local root match, valid signer, or public ledger receipt as satisfying dimensions it does not test.

## 25. Promotion status

This v0.2 document is an additive review candidate. It does not rewrite or promote the v0.1 draft, does not authorize implementation, and does not assert conformance. Promotion requires an exact-hash traceability ledger mapping every requirement to deterministic outcomes and fixtures, independent review of the exact artifact, preserved disagreements, and explicit principal approval. Implementation remains a separate gate.
