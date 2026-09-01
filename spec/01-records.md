# 01 — Records and Payloads

_Status: Skeleton draft_

## Three-layer model

A conforming profile distinguishes:

1. **immutable custody envelope** — identity, temporal assertions, attribution, authority-at-write, lineage, and integrity fields;
2. **write-once erasable payload** — subject content or evidence that may be removed through an authorized erasure lifecycle;
3. **rebuildable projection** — mutable derived state whose source set, builder version, and freshness are discoverable.

A system MUST NOT report projection mutation as historical custody mutation, or payload absence as proof of authorized erasure.

## Required logical distinctions

Records must preserve, as applicable:

- record and event identity;
- event class and profile version;
- principal, custody zone, stream, and epoch;
- observed, effective, and recorded-time claims;
- actor, runtime, credential, authorization, and reviewer assertions;
- evidence, source, payload, and derivation references;
- predecessor, correction, conflict, and supersession links;
- retention, hold, erasure, and payload state;
- algorithm and extension metadata.

Unknown, withheld, not-applicable, erased, unavailable, and invalid are distinct states. Omission or `null` must not silently conflate them.

## Payload state

A verifier should distinguish at least:

- present and verifiable;
- present but not openable under current policy;
- erased through an authorized transition;
- intentionally unverifiable after erasure;
- unavailable for unknown cause;
- inconsistent with its surviving custody receipt.
