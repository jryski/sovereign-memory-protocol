# 08 — Immutable Fields and Chain-of-Custody Verification

_Status: **NEEDS REVISION**; private pre-release review draft_
_Version: 0.1.0-draft.2_
_Last updated: 2026-07-31_

**Supersession record:** This v0.1 draft is explicitly superseded by
[`spec/08-immutability-and-chain-of-custody-v0.2.md`](08-immutability-and-chain-of-custody-v0.2.md).
It is retained only as a **non-normative historical** review artifact. Its capitalized requirement
keywords do not govern the current draft lineage, implementation claims, or conformance results.

> **Adversarial review notice:** The accepted write-once/correction/authorized-erasure direction is preserved, but this mechanism is not an implementation-authorizing contract. Before promotion it must close the exact recording boundary, complete canonical envelopes, historical authority and key status, registered-stream and anti-rollback semantics, bilateral transfer, erasure closure, restore quarantine, canonical golden vectors, temporal and lifecycle-graph semantics, source-qualified completeness, metadata privacy, and bounded verifier resources.

## 1. Scope

This document defines implementation-neutral requirements for:

- fields that cannot be rewritten after an event is recorded;
- correction, supersession, lifecycle, custody-transfer, and erasure events;
- deterministic event commitments and ordered custody streams;
- signed checkpoints and optional external anchoring;
- verification outcomes and conformance behavior.

It does not require a particular database, cloud, blockchain, transparency-log vendor, or payload format. Retrieval quality is outside this specification.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as normative requirements in the style of RFC 2119 and RFC 8174 when written in capitals.

## 2. Accepted principle

Custody-semantic fields are write-once. After an event is recorded, a conforming system **MUST NOT** rewrite its identity, original temporal assertions, source and authority attribution, lineage, or integrity commitments.

A correction or lifecycle change **MUST** append a new event. The new event **MUST** identify the affected record or prior event and **MUST NOT** replace the original canonical event bytes.

Immutability is not permanent retention. A subject payload **MAY** be removed by an authorized erasure operation. The system **MUST** preserve a minimal, privacy-safe erasure receipt and **MUST** report the coverage and residual limitations of erasure.

Mutable indexes, vectors, graphs, summaries, caches, and context packs **MUST** be declared rebuildable projections. They **MUST NOT** be treated as the authoritative custody record.

## 3. Concepts

### 3.1 Custody event

A custody event is the smallest authoritative, write-once statement that something was recorded, attributed, accepted, corrected, superseded, transferred, retired, erased, verified, or anchored.

### 3.2 Subject payload

The subject payload is the content or evidence governed by a custody event. It may be inline, externally referenced, encrypted, or absent after erasure. Its storage location is not the custody event itself.

### 3.3 Semantic lineage

Semantic lineage links a correction, supersession, conflict, acceptance, rejection, retirement, or withdrawal to the record or assertion whose interpretation changed. Semantic lineage does not establish byte ordering.

### 3.4 Custody stream

A custody stream is an ordered append-only sequence within one declared trust domain and partition. A sequence number establishes recorded order in that stream; it does not prove real-world occurrence order.

### 3.5 Projection

A projection is disposable state derived from custody events and payloads. Projection mutation is permitted only when the authoritative sources and deterministic rebuild contract remain identified.

### 3.6 Checkpoint

A checkpoint commits to a prefix of a custody stream. A signature attributes the checkpoint to a key; an independent anchor may add externally witnessed existence or ordering. Neither proves semantic truth or legitimate authority by itself.

## 4. Required event classes

A profile **MUST** represent at least the following semantics, whether or not it uses these exact labels:

- `record`: create an assertion or evidence record;
- `correct`: append a corrected assertion while preserving the original;
- `supersede`: declare precedence without deleting history;
- `accept` and `reject`: record authority disposition separately from source support;
- `conflict`: preserve incompatible claims without flattening them;
- `retire` or `withdraw`: end current use without rewriting historical validity;
- `custody_transfer`: record transfer between custodians or trust boundaries;
- `erase`: record an authorized payload-erasure attempt and outcome;
- `key_transition`: identify signer-key introduction, rotation, revocation, or compromise;
- `checkpoint`: commit to a stream prefix;
- `anchor_receipt`: associate a checkpoint with independently witnessed evidence.

Profiles **MAY** add event classes, but unknown classes **MUST** remain distinguishable and **MUST NOT** be silently interpreted as acceptance or authority.

## 5. Normative mutability matrix

Every normative profile **MUST** publish a field matrix. The following minimum classifications apply.

| Field or field class | Required disposition | Requirement |
|---|---|---|
| protocol and event profile/version | immutable | Identifies the parsing and verification contract used at write time. |
| event identifier | immutable | Globally unique within the declared identifier scheme. Reuse is an error. |
| custody stream identifier and trust-domain identifier | immutable | Cross-domain movement appends a transfer event; it does not rewrite origin. |
| stream sequence number | immutable | Unique and contiguous under the stream profile. |
| previous event hash or genesis marker | immutable | Binds recorded order. |
| event class | immutable | Lifecycle meaning cannot be relabeled later. |
| recorded time | immutable | Time asserted by the recorder. A better timestamp appends a correction or verification event. |
| original effective/observed-time assertion | immutable | A corrected assertion appends; the historical assertion remains inspectable. |
| record, subject, and evidence identifiers | immutable | A replacement receives a distinct event identity and explicit lineage. |
| actor, agent, runtime, host, tool, and principal assertions | immutable | Unknown is explicit; later corroboration appends and does not strengthen the historical claim in place. |
| credential, key, and authorization references at write time | immutable | References only; secrets are forbidden. Later revocation does not alter historical attribution. |
| authority/assurance state at write time | immutable | Later acceptance, rejection, or assurance changes append disposition events. |
| opaque source/evidence identity and commitment | immutable as recorded | The event retains the historical commitment; it does not silently retarget evidence. |
| sensitive source locator and commitment-opening material | write-once while present; erasable as a whole | Store in a separately erasable compartment. The event carries an opaque reference or commitment, not necessarily the sensitive locator itself. |
| schema, policy, adapter, and algorithm-suite references | immutable | Verification uses the historical contract, subject to explicit safe-failure rules. |
| semantic predecessor, correction, supersession, conflict, and transfer links | immutable | A mistaken link is corrected by an appended event. |
| payload commitment active at write time | immutable as recorded | The commitment bytes remain historical; privacy-sensitive verification material may be erasable. |
| event hash | immutable | Recomputed from canonical event bytes; never repaired in place. |
| event signatures and witness receipts | append-only | Additional signatures or revocation evidence may append. Existing receipts are not replaced. |
| subject payload | write-once while present; erasable as a whole | In-place editing is forbidden. Correction writes a new payload. Authorized erasure may remove bytes or keys. |
| lifecycle, authority, and current-state history | append-only events | A mutable current-state view is only a projection. |
| erasure outcome and coverage | append-only events | Failed, partial, stale, offline, backup, and projection coverage remain explicit. |
| search/vector/graph/ranking/cache/context-pack state | rebuildable projection | Mutation is allowed; source set, builder version, and freshness MUST remain discoverable. |

A profile **MUST NOT** classify a field as merely “mutable” without stating whether changes append authority events, replace erasable payload, or rebuild a projection.

## 6. Canonical event envelope

### 6.1 Required logical fields

A canonical event envelope **MUST** contain:

- `protocol`;
- `event_profile`;
- `event_id`;
- `event_class`;
- `stream_id`;
- `trust_domain`;
- `sequence`;
- `previous_event_hash` or an explicit genesis marker;
- `recorded_at`;
- original effective or observed-time assertion, or explicit `unknown`/`not_applicable`;
- subject/record/evidence references appropriate to the event class;
- actor, runtime, principal, credential, and authorization assertions, each allowing explicit `unknown`;
- schema, policy, adapter, and algorithm-suite references;
- semantic lineage links;
- payload commitment metadata or an explicit no-payload marker.

Optional fields **MUST** be covered by canonicalization. An implementation **MUST NOT** exclude an unknown field from hashing merely because it does not understand it.

Every extension field **MUST** declare whether it is critical to verification. An unknown critical extension **MUST** fail verification. An unknown noncritical extension **MAY** remain uninterpreted, but its exact canonical bytes **MUST** remain covered by the event hash and preserved through export/restore.

### 6.2 Data model restrictions

The base JSON profile:

- **MUST** encode the envelope as UTF-8 JSON;
- **MUST** use the JSON Canonicalization Scheme in RFC 8785;
- **MUST** reject duplicate member names, invalid Unicode, non-I-JSON numbers, and noncanonical bytes;
- **MUST** encode sequence counters, byte counts, and other unbounded integers as canonical decimal strings rather than JSON numbers;
- **MUST** encode timestamps as UTC RFC 3339 strings with explicit precision declared by the event profile;
- **MUST** represent unknown, withheld, not-applicable, and erased states explicitly rather than conflating them with an omitted field or JSON `null`.

An alternative encoding profile **MAY** be defined, but it **MUST** specify one canonical byte representation, domain separation, duplicate-field rejection, Unicode policy, numeric policy, and a bidirectional mapping to the logical event model.

### 6.3 Event hash

The proposed base suite computes:

```text
event_hash = SHA-256(
  UTF8("SMP-CUSTODY-EVENT-v1\u0000") || canonical_event_without_event_hash
)
```

`previous_event_hash` is inside `canonical_event_without_event_hash`. The stored `event_hash` field is not included in its own preimage.

Profiles **MUST** identify the algorithm suite. Verifiers **MUST NOT** silently substitute an unknown or weaker suite.

## 7. Stream ordering and append behavior

1. The genesis event **MUST** have sequence `"1"` and the profile's explicit genesis marker.
2. Every later event **MUST** increment the prior sequence by exactly one and contain the prior event hash.
3. Duplicate event identifiers, duplicate sequence numbers, gaps, forks, and predecessor mismatches **MUST** fail verification.
4. Concurrent writers **MUST** use a sequencer, compare-and-append primitive, consensus mechanism, or equivalent serialization boundary. Last-write-wins is nonconforming.
5. Event-ID reservation, event append, payload/commitment durability, predecessor validation, and stream-head advancement **MUST** be linearizable per stream or implemented as an explicitly recoverable protocol whose incomplete state cannot be checkpointed or presented as committed.
6. A retry **MUST** reuse a stable operation/event identifier. An identical replay **MUST** return the original committed outcome; conflicting reuse **MUST** fail.
7. Where one semantic successor is required, concurrent successors **MUST** produce exactly one winner and one or more explicit conflicts/rejections. If branches are valid domain semantics, the profile **MUST** define branch identity, merge/selection authority, and deterministic current-state projection.
8. A verifier **MUST** distinguish a valid observed prefix from a claim that the stream is globally complete.
9. A checkpoint or external witness is required to detect privileged truncation relative to an independently held prior head.
10. Reusing an erased or retired stream identifier as a new genesis stream is forbidden.

## 8. Signed Merkle checkpoints

The proposed base checkpoint profile commits to the ordered event hashes for stream sequences `1..tree_size`.

- Leaf hash: `SHA-256(0x00 || event_hash_bytes)`.
- Interior hash: `SHA-256(0x01 || left_hash || right_hash)`.
- Empty-tree behavior and odd-node behavior **MUST** be specified by the checkpoint profile; the proposed profile follows the RFC 6962-style history-tree algorithm rather than duplicating the final odd node.
- Checkpoint canonical bytes **MUST** include protocol/profile, stream/trust-domain identifiers, tree size, root hash, last event hash, issue time, algorithm suite, and signer key identifier.
- A signature **MUST** cover the canonical checkpoint bytes and declared context string.
- Inclusion proofs show membership in one checkpoint. Consistency proofs show append-only extension between checkpoints. Neither proves that omitted source events were ever submitted.

A checkpoint signer can create two independently valid but conflicting histories. A profile claiming non-equivocation **MUST** require independent checkpoint capture, witness gossip/monitoring, quorum, or consensus sufficient for its threat model. It **MUST** define checkpoint cadence and a maximum freshness interval; evidence older than that interval is stale rather than current.

A verifier **MUST** report separately:

- event-chain validity;
- checkpoint signature validity;
- inclusion-proof validity;
- consistency with a named prior checkpoint;
- signer trust/revocation status at verification time and at signing time where known;
- external-anchor status and freshness;
- completeness scope and unobserved intervals.

## 9. Signers, keys, and algorithm agility

1. Key identifiers **MUST** be stable references or fingerprints, never secret material.
2. Key introduction, rotation, revocation, recovery, and compromise **MUST** append evidence.
3. Historical signatures **MUST** remain verifiable after ordinary rotation.
4. A compromise event **MUST** state the earliest known or suspected compromise time. Verifiers **MUST** label signatures in the affected interval as uncertain or invalid under policy; they **MUST NOT** rewrite them.
5. Algorithm suites **MUST** be explicitly versioned and domain-separated.
6. Downgrade to an unknown, deprecated, or weaker suite **MUST** fail unless an explicit verifier policy authorizes it and reports the reduced assurance.
7. Signer authorization and cryptographic signature validity are separate outcomes. Possession of a valid key does not prove legitimate semantic authority.
8. Deployment key custody, hardware protection, quorum, and recovery are profile/policy concerns and **MUST** be declared when a deployment makes tamper-resistance claims.

Actor, credential, authorization, schema, policy, and key references that affect verification **MUST** resolve to immutable snapshots, content-addressed artifacts, or versioned authority events. A mutable URL or current database row alone is insufficient because later edits could launder historical authority.

An algorithm transition **MUST** append a transition event that binds the last commitment under the old suite to the first commitment or checkpoint under the new suite. Where both suites remain acceptable, the transition **SHOULD** be signed and verifiable under both. Re-encoding or rehashing old events under a new suite **MUST NOT** replace their original bytes or commitments.

## 10. Erasure without historical rewrite

### 10.1 Required semantics

An erasure operation **MUST** append an `erase` event containing:

- target payload and event references;
- authorization source and requesting principal;
- reason and policy basis, subject to minimization;
- intended scope: authority store, projections, caches, traces/logs, exports, replicas, backups, hosted copies, and external processors;
- method: byte deletion, key destruction, redaction, retention expiry, or other declared method;
- per-scope outcome: verified, failed, pending, unreachable, offline, stale, retained by policy, or unknown;
- verifier, verification time, and evidence references;
- residual limitations and next retry/expiry condition.

An erasure receipt **MUST NOT** claim universal deletion when a copy, backup, processor, or verification surface was not covered.

If erasure conflicts with a legal hold, safety hold, or other controlling retention duty, the operation **MUST** append a denied or pending outcome with minimized rationale and authority evidence. It **MUST NOT** report erasure complete.

### 10.2 Commitment privacy

A plain unsalted hash of low-entropy subject data can permit offline confirmation after deletion. Therefore:

- a privacy-sensitive payload commitment **MUST** be computationally hiding under the declared threat model;
- verification material such as a high-entropy randomizer or keyed-commitment key **SHOULD** be stored with the erasable payload compartment and destroyed when post-erasure verification would enable dictionary confirmation;
- a salt retained beside a low-entropy digest does not make that digest privacy-safe;
- randomized authenticated encryption and ciphertext commitments **MAY** be used, provided ciphertext, keys, replicas, and nonce/tag metadata receive explicit erasure coverage;
- a retained plaintext digest **MUST** be justified by data classification and policy, not by the assumption that hashes are anonymous;
- an erasure claim **MUST** state that already disclosed or independently copied information cannot be made unknown again.

Destroying a key is operational evidence of cryptographic erasure, not mathematical proof that no key copy exists. Verification **MUST** report the custody and coverage used to support the claim.

Cryptographic-erasure coverage **MUST** account for data-encryption keys, key-encryption keys, wrapped/escrowed/recovery copies, snapshots, crash dumps, temporary material, replicas, and backups. Deliberately destroying commitment-opening material **MUST** be reported as loss of future payload-verification capability, not only as a successful deletion.

### 10.3 Chain continuity after erasure

Erasure **MUST NOT** require rewriting event hashes. The original event and its commitment may remain, but sensitive locators, payload bytes, decryption keys, and commitment-opening material may reside in a separately erasable compartment. A verifier **MUST** be able to distinguish:

- intact event/chain integrity;
- payload present and commitment-openable;
- payload erased and commitment intentionally unopenable;
- payload unavailable for an unknown reason;
- inconsistent or falsely claimed erasure.

## 11. Custody transfer and trust-domain isolation

A transfer across custodians or trust domains **MUST** append a receipt identifying:

- sender and recipient domains;
- transferred object and package commitments;
- release and acceptance events;
- transfer method and evidence;
- policy and authorization references;
- source and destination verification outcomes;
- fields intentionally omitted, transformed, or erased;
- time and ordering uncertainty.

A receiving domain **MUST NOT** rewrite origin attribution. Acceptance into the destination authority state is a distinct event.

Correction, supersession, transfer, and acceptance links **MUST** resolve to an existing compatible object in the same declared principal and trust domain unless an authorized cross-domain transfer profile says otherwise. Missing targets, self-links, prohibited cycles, scope mismatches, and unauthorized cross-zone links **MUST** fail validation.

Checkpoints for physically or administratively separated custody domains **MUST NOT** be combined if the resulting metadata would violate their declared confidentiality boundary. Cross-domain aggregation requires an explicit profile and leakage analysis.

## 12. Optional anchoring profiles

The base protocol requires no external ledger. A profile may anchor a signed checkpoint through:

- an independently retained witness;
- an RFC 3161 timestamp authority;
- a transparency log with inclusion and consistency proofs;
- a public timestamping system;
- a signed repository/release artifact;
- a permissioned consensus ledger.

Every anchoring profile **MUST** declare:

- operator and trust assumptions;
- data disclosed externally;
- submission and confirmation semantics;
- offline and outage behavior;
- reorganization, equivocation, or split-view risks;
- verifier dependencies and long-term evidence retention;
- cost and rate limits;
- key and account custody;
- privacy and correlation leakage;
- provider-exit and receipt-export behavior.

A blockchain or permissioned ledger **MUST NOT** be described as proving truth, authority, lawful processing, or erasure. It may strengthen ordering, witnessing, and tamper evidence under its stated threat model.

## 13. Verification outcomes

A verifier **MUST** return structured outcomes and **MUST NOT** collapse all failures into a Boolean. Minimum outcome dimensions are:

- `canonical_bytes`;
- `event_hash`;
- `stream_chain`;
- `semantic_lineage`;
- `locked_field_policy`;
- `payload_state`;
- `erasure_state`;
- `checkpoint_signature`;
- `checkpoint_inclusion`;
- `checkpoint_consistency`;
- `signer_status`;
- `anchor_status`;
- `anchor_freshness`;
- `authority_status`;
- `coverage`;
- `completeness_claim`.

Each dimension **MUST** distinguish at least pass, fail, unknown, not-applicable, and not-checked. Stale, partial, offline, and unverifiable states **SHOULD** be separate where applicable.

Integrity failures **MUST** take precedence over semantic-content interpretation. A verifier must not report a well-formed correction or successful erasure when the covering event hash or chain is invalid.

## 13.1 Completeness and latestness

Hash chains, inclusion proofs, and checkpoints prove properties only of admitted events. A verifier **MUST** distinguish:

- no gaps in the presented admitted-event prefix;
- consistency with a named prior independently retained checkpoint;
- every item in a frozen manifest is dispositioned;
- every item in an independently authenticated source inventory is represented in that manifest;
- completeness relative to a live source, which is `unknown` unless the source supplies an authenticated snapshot/cursor contract;
- freshness relative to the profile's checkpoint/anchor cadence.

An inclusion proof **MUST NOT** be represented as an absence proof, global completeness proof, or proof that the signer presented its latest history. A third-party completeness claim requires an independently captured or authenticated source-inventory root plus reconciliation that binds every disposition to that inventory.

## 13.2 Restore and authority

A restored store **MUST NOT** become authoritative merely because its local chain is internally valid. Promotion after restore requires reconciliation against the latest required independent checkpoint/witness, key-status evidence, erasure history, source-inventory/accounting contract, and deployment policy. A stale but internally valid snapshot **MUST** be reported as stale and **MUST NOT** resurrect erased payload or superseded authority.

## 14. Minimum conformance cases

A conforming implementation **MUST** pass implementation-neutral vectors covering:

1. canonical event acceptance and noncanonical equivalent rejection;
2. attempted in-place changes to each locked field;
3. valid appended correction preserving original bytes;
4. authority acceptance/rejection separate from evidence support;
5. stream gap, reorder, duplicate, fork, replay, and truncation relative to a prior checkpoint;
6. semantic self-reference and invalid predecessor links;
7. valid Merkle inclusion and append-only consistency proofs;
8. altered leaf, root, proof, checkpoint, and signature failures;
9. signer rotation, revocation, compromise interval, and unknown signer;
10. algorithm downgrade and unknown suite rejection;
11. clean export/restore reproducing event hashes and checkpoint roots;
12. authorized complete, partial, failed, pending, and offline erasure outcomes;
13. low-entropy post-erasure dictionary-resistance under the commitment profile;
14. erased payload versus unexplained missing payload distinction;
15. cross-domain transfer preserving origin and requiring destination acceptance;
16. cross-domain checkpoint aggregation denial unless explicitly profiled;
17. projection drift followed by deterministic rebuild;
18. privileged rewrite or truncation detected against an independent checkpoint;
19. valid observed prefix reported without overclaiming global completeness;
20. timestamp uncertainty and recorded-order versus effective-time distinction.
21. atomic/linearizable append, idempotent retry, and competing-writer behavior;
22. signer equivocation exposed through independent witnesses or explicitly reported as uncovered;
23. authenticated source-inventory reconciliation versus admitted-stream consistency;
24. unknown critical extension failure and noncritical extension byte preservation;
25. legal-hold denial/pending behavior and crypto-erasure key-copy coverage;
26. stale restore prevented from resurrecting erased payload or becoming authoritative.

## 15. Claim levels

A deployment **MUST** state the level actually verified:

- **L0 — policy declared:** field matrix and append semantics are documented.
- **L1 — routine mutation prevented:** ordinary and service write paths reject locked-field rewrites.
- **L2 — portable tamper detection:** canonical event hashes, stream chains, signed checkpoints, export, and restore verify independently.
- **L3 — independently witnessed:** checkpoint evidence is held outside the primary authority store and freshness is reported.
- **L4 — multi-party ordered:** a declared consensus profile addresses mutually distrustful writers or custodians.

Higher levels do not imply source truth, semantic authority, completeness, confidentiality, lawful retention, or verified erasure unless those dimensions are separately reported.

## 16. Security considerations

Conforming profiles and implementations must address:

- canonicalization ambiguity and duplicate members;
- fork, truncation, replay, reorder, and cross-stream substitution;
- timestamp backdating and clock uncertainty;
- signer compromise, rollback, and algorithm downgrade;
- witness equivocation and transparency-log split views;
- denial of append or checkpoint publication;
- metadata and traffic-analysis leakage;
- low-entropy commitment guessing;
- orphaned payloads and stale projections after erasure;
- backup and replica lag;
- compromised privileged operators and unverifiable completeness;
- parser resource limits and fail-closed errors;
- cross-domain correlation and identity leakage;
- restoration from stale but internally valid snapshots.

## 17. Draft review status

This section remains a review draft. Normative promotion requires exact-artifact review, requirement-to-fixture traceability, and explicit principal approval. Peer convergence or a passing implementation test does not independently promote the text.

## 18. Informative references

- RFC 2119 and RFC 8174 — normative requirement vocabulary.
- RFC 3339 — Internet timestamps.
- RFC 8785 — JSON Canonicalization Scheme.
- RFC 6962 and RFC 9162 — Merkle history-tree, inclusion, and consistency-proof concepts.
- RFC 3161 — time-stamp protocol.
- RFC 8032 — Ed25519 signatures.

Exact profiles must pin the referenced version, algorithm identifiers, and interoperability vectors before release.
