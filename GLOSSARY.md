# Glossary

_Status: Draft_

**Accepted** — a proposal explicitly promoted by an authorized principal or delegate for a named scope.

**Actor** — the entity asserted to have performed an operation. Actor identity is distinct from runtime, credential, principal, and authorization.

**Authority-at-write** — immutable evidence describing why an actor was authorized for a specific operation, scope, and recording boundary.

**Candidate** — a proposed derived record. Existence does not imply truth, acceptance, or authority.

**Checkpoint** — a signed commitment to a declared set or prefix of custody events. A checkpoint does not by itself prove completeness, freshness, non-equivocation, or semantic truth.

**Conflict** — two or more incompatible claims preserved without silent resolution.

**Correction** — a successor assertion that addresses an earlier assertion while preserving the earlier bytes and lineage.

**Custody event** — a write-once statement about recording, attribution, lifecycle, transfer, erasure, verification, or anchoring.

**Custody stream** — an ordered append-only event sequence within a declared scope and epoch.

**Derived state** — state computed from evidence or custody events. Derived state is not automatically authoritative.

**Effective time** — when an assertion claims to apply in the represented world. It is distinct from observed and recorded time.

**Evidence** — preserved source material or an evidence commitment used to support a claim. Evidence support is not external truth.

**Inference** — an agent- or system-derived claim that has not been accepted as human fact.

**Observed time** — when an observer claims an event or condition was encountered.

**Payload** — subject content governed by a custody envelope. A payload may be separately erasable.

**Principal** — the authority root for a named custody scope.

**Projection** — mutable, rebuildable state derived from authoritative inputs, such as an index, graph, cache, vector representation, summary, or context pack.

**Proposal** — a claim awaiting review or disposition.

**Recorded time** — time assigned at the durable recording boundary. It is an assertion by the recorder, not guaranteed real-world occurrence time.

**Retirement** — ending current operational use without asserting that a replacement is semantically superior.

**Scope** — the explicitly bounded principal, custody zone, stream set, object set, and operation class to which a claim applies.

**Supersession** — an appended relation declaring that one assertion has precedence over another for a stated scope and rationale.

**Transfer** — a bilateral custody transition requiring sender and recipient evidence. File possession alone is not completed transfer.

**Withdrawal** — retracting current sponsorship or acceptance while retaining historical custody evidence.
