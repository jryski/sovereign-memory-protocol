# SMP Immutability and Custody-Chain Conformance Cases

_Status: implementation-neutral review draft_
_Version: 0.1.0-draft.1_
_Last updated: 2026-07-31T08:52:40-04:00_
_Related draft: `../../spec/08-immutability-and-chain-of-custody.md`_

## 1. Result contract

Each runner must return a structured outcome containing:

- case identifier;
- event, stream, checkpoint, and trust-domain identifiers involved;
- outcome: `pass`, `fail`, `unknown`, `not_applicable`, or `not_checked`;
- stable error code where applicable;
- Eywa failure-taxonomy category where applicable;
- custody extension category where applicable;
- coverage, freshness, and unavailable surfaces;
- exact verifier implementation/profile version;
- expected and actual canonical/hash/checkpoint values without subject payload disclosure.

A runner must not report conformance from aggregate counts alone. Every case must have an independently inspectable result.

## 2. Failure taxonomy

Use Eywa's published names unchanged where applicable:

- **coverage gap** — support existed in source but no evidence or derived belief exists;
- **grounding gap** — a belief is unsupported or a hard value changed;
- **revision gap** — a correction or superseding event is not applied to current state;
- **scope gap** — memory from the wrong person/entity/scope is used;
- **temporal gap** — wrong ordering, time constraint, or validity window;
- **retrieval gap** — support exists but does not reach bounded context;
- **synthesis gap** — sufficient evidence reaches the answer model but output is wrong;
- **measurement gap** — semantically supported output is scored incorrectly.

Proposed custody-specific extensions:

- **authority violation** — an unauthorized actor, runtime, credential, principal, or workflow performs or is represented as having performed an authority-bearing transition;
- **custody/precedence violation** — canonicality, integrity, ordering, trust-domain, or verification-precedence failure is hidden, bypassed, or reported as a later semantic success.

The extension labels remain proposed pending joint protocol review. They do not rename Eywa's categories.

## 3. Canonical event cases

| ID | Input or operation | Expected outcome | Expected code/category |
|---|---|---|---|
| IMM-CAN-001 | Exact canonical event vector | accept | — |
| IMM-CAN-002 | Same logical object with member order changed | reject | `event_noncanonical`; custody/precedence |
| IMM-CAN-003 | Leading/trailing whitespace or alternate newline | reject | `event_noncanonical`; custody/precedence |
| IMM-CAN-004 | Duplicate JSON member | reject before semantic interpretation | `duplicate_member`; custody/precedence |
| IMM-CAN-005 | JSON number where decimal string is required | reject | `numeric_encoding_invalid`; custody/precedence |
| IMM-CAN-006 | Noncanonical integer string such as `01` or `+1` | reject | `sequence_not_canonical`; custody/precedence |
| IMM-CAN-007 | Invalid Unicode or prohibited surrogate | reject | `unicode_invalid`; custody/precedence |
| IMM-CAN-008 | Unknown event field included in bytes | preserve and hash, or reject per profile; never ignore | `unknown_field` or pass with opaque preservation |
| IMM-CAN-009 | Unknown algorithm suite | reject verification | `algorithm_unknown`; custody/precedence |
| IMM-CAN-010 | Downgraded suite under policy | fail or explicit reduced-assurance result; never silent pass | `algorithm_downgrade`; custody/precedence |
| IMM-CAN-011 | Unknown critical extension | reject verification | `critical_extension_unknown`; custody/precedence |
| IMM-CAN-012 | Unknown noncritical extension | preserve exact bytes and include in hash/export | pass with uninterpreted extension |

Integrity/canonicality checks precede event-class semantics. A doubly invalid event with a bad hash and unauthorized acceptance must report the integrity failure as the primary blocking outcome while retaining the authority finding as secondary evidence.

## 4. Per-field immutability cases

A runner must generate one case for every locked field declared by the active event profile. The following base cases are mandatory.

| ID | Attempted in-place change | Expected outcome |
|---|---|---|
| IMM-FLD-001 | protocol/profile version | `locked_field_change` |
| IMM-FLD-002 | event identifier | `locked_field_change` |
| IMM-FLD-003 | stream or trust-domain identifier | `locked_field_change` |
| IMM-FLD-004 | sequence or predecessor hash | `locked_field_change` |
| IMM-FLD-005 | event class | `locked_field_change` |
| IMM-FLD-006 | recorded time | `locked_field_change` |
| IMM-FLD-007 | original observed/effective-time assertion | `locked_field_change` |
| IMM-FLD-008 | record, subject, or evidence identity | `locked_field_change` |
| IMM-FLD-009 | actor, agent, runtime, host, tool, or principal assertion | `locked_field_change`; authority violation |
| IMM-FLD-010 | credential or authorization reference | `locked_field_change`; authority violation |
| IMM-FLD-011 | authority/assurance state at write time | `locked_field_change`; authority violation |
| IMM-FLD-012 | schema, policy, adapter, or algorithm-suite reference | `locked_field_change` |
| IMM-FLD-013 | correction, supersession, conflict, or transfer link | `locked_field_change`; revision or scope gap if consumed |
| IMM-FLD-014 | payload commitment | `locked_field_change`; grounding/custody violation |
| IMM-FLD-015 | event hash | `locked_field_change`; custody/precedence |

Each case must run through ordinary application, service/RPC, import/restore, and any privileged maintenance path that claims conformance. An implementation may prevent a privileged host owner from routine mutation yet cannot prove resistance to that owner without an independent witness.

## 5. Append and lineage cases

| ID | Scenario | Expected outcome/category |
|---|---|---|
| IMM-LIN-001 | Valid correction appends a new event and payload | pass; original canonical bytes unchanged |
| IMM-LIN-002 | Correction overwrites original payload | fail `history_rewrite`; revision gap |
| IMM-LIN-003 | Supersession marks precedence only in a mutable view | fail unless backed by appended event; revision gap |
| IMM-LIN-004 | Current-state view selects superseded assertion | fail; revision gap |
| IMM-LIN-005 | Historical query returns only current assertion | fail under historical-view contract; temporal gap |
| IMM-LIN-006 | Invalid or missing semantic predecessor | fail `lineage_unresolved` |
| IMM-LIN-007 | Self-correction or prohibited lineage cycle | fail `lineage_cycle` |
| IMM-LIN-008 | Two incompatible active assertions flattened without conflict event | fail; revision and grounding gap |
| IMM-LIN-009 | Evidence support is represented as authority acceptance | fail; authority violation |
| IMM-LIN-010 | Valid signer is represented as authorized principal without policy evidence | fail; authority violation |
| IMM-LIN-011 | Historical authorization/policy reference resolves to a mutable current object that changed | fail `historical_authority_unresolvable`; authority violation |
| IMM-LIN-012 | Concurrent mutually exclusive corrections | exactly one winner plus explicit conflict/rejection, or a declared branch contract; never silent last-write-wins |

## 6. Stream and checkpoint cases

| ID | Scenario | Expected outcome |
|---|---|---|
| IMM-STR-001 | Valid genesis and contiguous append | pass |
| IMM-STR-002 | Duplicate event ID | fail `duplicate_event_id` |
| IMM-STR-003 | Duplicate sequence | fail `duplicate_sequence` |
| IMM-STR-004 | Sequence gap | fail `stream_gap` |
| IMM-STR-005 | Reordered events with hashes unchanged | fail `hash_or_predecessor_mismatch` |
| IMM-STR-006 | Reordered events with all local hashes recomputed | fail relative to independently retained checkpoint |
| IMM-STR-007 | Fork from one predecessor | fail or return explicit unresolved fork; never last-write-wins |
| IMM-STR-008 | Valid prefix without later checkpoint visibility | pass as observed prefix; global completeness `unknown` |
| IMM-STR-009 | Privileged truncation before latest independent checkpoint | fail `checkpoint_regression` |
| IMM-STR-010 | Replay valid stream under another trust-domain/stream ID | fail domain binding |
| IMM-STR-011 | Identical retry with same operation/event ID | return original committed result; no duplicate append |
| IMM-STR-012 | Conflicting retry with reused operation/event ID | fail `idempotency_conflict` |
| IMM-STR-013 | Crash between payload durability and stream-head advance | recover deterministically; incomplete event cannot be checkpointed or presented committed |
| IMM-STR-014 | Checkpoint races an uncommitted append | checkpoint covers one atomic committed prefix only |
| IMM-CHK-001 | Correct inclusion proof | pass inclusion only |
| IMM-CHK-002 | Altered leaf/proof/root/tree size | fail deterministic proof verification |
| IMM-CHK-003 | Correct append-only consistency proof | pass consistency |
| IMM-CHK-004 | Unrelated roots represented as extension | fail consistency |
| IMM-CHK-005 | Valid signature from unknown key | signature cryptographically valid; signer trust `unknown`; no authority pass |
| IMM-CHK-006 | Ordinary key rotation | historical and new checkpoints verify under declared intervals |
| IMM-CHK-007 | Revoked/compromised key | affected interval reported uncertain/invalid under policy |
| IMM-CHK-008 | Stale or unreachable external anchor | local checkpoint may pass; anchor outcome `stale` or `offline` |
| IMM-CHK-009 | Split-view witness evidence | fail or conflict; preserve both receipts |
| IMM-CHK-010 | Same content restored with different event bytes | fail exact event/checkpoint identity even if semantic payload matches |
| IMM-CHK-011 | Signer presents two valid conflicting heads to isolated witnesses | non-equivocation fails unless gossip/monitor/quorum exposes conflict; preserve both heads |
| IMM-CHK-012 | Checkpoint older than declared maximum interval | local proof may pass; freshness `stale` |

## 7. Erasure cases

| ID | Scenario | Expected outcome |
|---|---|---|
| IMM-ERA-001 | Authorized payload deletion; all declared online surfaces verified | payload `erased`; unaffected chain passes; uncovered backups explicit |
| IMM-ERA-002 | Unauthorized erasure request | fail; authority violation; no payload mutation |
| IMM-ERA-003 | Payload missing without erasure event | `payload_unavailable_unknown`, not `erased` |
| IMM-ERA-004 | In-place blanking presented as correction | fail `history_rewrite` |
| IMM-ERA-005 | Key destruction claimed without key-custody evidence | erasure status `unknown` or partial |
| IMM-ERA-006 | Authority store cleared but projection remains | erasure partial/fail; projection residue reported |
| IMM-ERA-007 | Online stores cleared; offline backup unreachable | backup outcome `offline`; universal deletion forbidden |
| IMM-ERA-008 | Ordinary low-entropy plaintext hash retained | fail privacy profile unless explicit non-sensitive policy exception |
| IMM-ERA-009 | High-entropy commitment opening destroyed with payload | pass only under declared threat model and copy coverage |
| IMM-ERA-010 | Erasure receipt itself contains erased subject content or sensitive locator | fail data-minimization/privacy check |
| IMM-ERA-011 | Retry later clears previously pending backup | append new receipt; do not rewrite prior partial receipt |
| IMM-ERA-012 | Export made before erasure is restored | restore must preserve erasure status or require reconciliation before authority; stale snapshot explicit |
| IMM-ERA-013 | Erasure conflicts with legal/safety hold | append denied/pending outcome; never report completed |
| IMM-ERA-014 | One DEK destroyed but wrapped/escrowed/recovery key remains | erasure partial/fail with residual key coverage |
| IMM-ERA-015 | Commitment opening destroyed | report payload unopenable and explicit loss of future payload-verification capability |

Dictionary-resistance tests must use a published low-entropy candidate set and verify that retained public artifacts do not permit confirmation after authorized erasure. This cannot prove information was never copied before erasure.

## 8. Trust-domain and custody-transfer cases

| ID | Scenario | Expected outcome |
|---|---|---|
| IMM-XFR-001 | Valid release and destination acceptance | pass; origin attribution unchanged |
| IMM-XFR-002 | Destination rewrites origin actor/principal | fail; scope and authority violation |
| IMM-XFR-003 | Destination treats receipt as semantic acceptance | fail; authority violation |
| IMM-XFR-004 | Transfer package omits fields without lossiness declaration | fail accounting/coverage |
| IMM-XFR-005 | Separately governed custody-domain checkpoints aggregated without an approved profile | fail trust-domain boundary |
| IMM-XFR-006 | Explicit cross-domain aggregate discloses only approved opaque heads | pass only with leakage analysis and authorization evidence |
| IMM-XFR-007 | Receiver verifies bytes but not sender release authorization | integrity pass; authority unknown/fail |
| IMM-XFR-008 | Sender release passes; receiver unavailable | transfer incomplete; no destination acceptance claim |

## 9. Projection and restore cases

| ID | Scenario | Expected outcome |
|---|---|---|
| IMM-PRJ-001 | Mutable projection drifts | authority records remain valid; projection fails freshness/consistency |
| IMM-PRJ-002 | Projection rebuilt from same accepted source set and builder profile | deterministic expected root/result |
| IMM-PRJ-003 | Rebuild silently excludes a source event | fail coverage/accounting |
| IMM-PRJ-004 | Search answer is correct despite invalid event hash | custody failure remains primary; answer correctness cannot mask it |
| IMM-RST-001 | Export and clean restore reproduce event hashes/checkpoint roots | pass |
| IMM-RST-002 | Internally valid but stale snapshot restored | snapshot integrity pass; freshness/completeness fail or unknown |
| IMM-RST-003 | Restored stream lacks independent checkpoint receipts | local chain may pass; independent detection coverage absent |
| IMM-RST-004 | Restored erased payload reappears from stale backup | fail erasure reconciliation and authority promotion |
| IMM-RST-005 | Local chain is valid but newer independent checkpoint exists | fail freshness/latestness; do not promote restored store |

## 10. Authenticated source-inventory and completeness cases

| ID | Scenario | Expected outcome |
|---|---|---|
| IMM-CMP-001 | Presented custody stream has no internal gaps | admitted-prefix consistency pass; source completeness remains separate |
| IMM-CMP-002 | Source item omitted before manifest generation; no authenticated source snapshot exists | live-source completeness `unknown`; stronger claim forbidden |
| IMM-CMP-003 | Source item omitted relative to independently frozen source-inventory root | fail accounting/coverage |
| IMM-CMP-004 | Every frozen source item has exactly one or more explicit dispositions | manifest accounting pass |
| IMM-CMP-005 | Inclusion proof presented as proof that no omitted event exists | fail `completeness_overclaim` |
| IMM-CMP-006 | Required anchor unavailable beyond freshness window | corresponding witnessed-assurance level fails; no silent downgrade |

## 11. Required test surfaces

Before an implementation claims a level from the draft specification, testing must cover:

- public parser/verifier API;
- real CLI or package-verification seam;
- routine writer and service/RPC writer;
- direct DML or equivalent privileged path where applicable;
- export and clean restore outside the source provider;
- independent checkpoint copy or witness;
- offline verifier behavior;
- signer-key rotation and compromise simulation;
- projection rebuild;
- erasure across every declared online and offline surface;
- cross-domain denial.

Unexercised paths and unavailable external anchors must be reported with the conclusion.

## 12. Current coverage

This matrix is a draft contract, not an implementation claim. No machine-readable fixture set has been promoted. This matrix is incomplete relative to the adversarial review and must not be counted as passing conformance coverage.
