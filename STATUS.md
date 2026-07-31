# Protocol Status

_Last updated: 2026-07-31_
_Overall status: private pre-release review package_

| Area | Status | Meaning |
|---|---|---|
| Human-readable scope and boundary | Review draft | Suitable for critique; not a release claim |
| Logical record model | Skeleton draft | Terms and invariants present; profile details incomplete |
| Provenance and custody | Draft | Core distinction documented; vectors incomplete |
| Authority model | Draft | Dimensions defined; delegation/key semantics incomplete |
| Supersession lifecycle | Draft | Lifecycle distinctions defined; graph validation incomplete |
| Verification outcomes | Draft | Structured dimensions defined; stable registry incomplete |
| Conformance model | Draft | Neutrality boundary defined; complete vectors absent |
| Error taxonomy | Draft | Security precedence defined; registry incomplete |
| Immutability and custody chain | **NEEDS REVISION** | Adversarial P0 requirements remain open |
| External anchoring profiles | Informative research | No service, key, account, or deployment selected |
| Public release | Blocked | Sanitation, exact-artifact review, license, and promotion pending |

## Accepted direction

- Custody-semantic fields are write-once after their recording boundary.
- Corrections and lifecycle changes append successors or events.
- Authorized payload erasure remains possible and must leave only a privacy-safe minimum receipt.
- Mutable derived state is explicitly a rebuildable projection.

## Open P0 requirements

The immutability design is not an implementation-authorizing contract until it defines and tests:

1. exact durable recording/admission boundary and claim levels;
2. complete canonical event, signature, checkpoint, and receipt envelopes;
3. immutable historical authority, delegation, and key status;
4. registered streams, atomic append, replay, forks, equivocation, rollback, and freshness;
5. bilateral custody transfer;
6. retention, legal holds, erasure closure, and privacy-safe surviving receipts;
7. restore quarantine and non-resurrection;
8. canonical golden vectors, time semantics, lifecycle-graph validation, source-qualified completeness, zone privacy, and verifier resource bounds.

## Promotion gates

1. One editor produces a frozen candidate with exact hashes.
2. Independent security and architecture reviews identify exact hashes and partial coverage.
3. Every normative requirement maps to a result class and fixture.
4. Conflicts remain visible rather than silently resolved.
5. The principal explicitly promotes the exact artifact.
6. Implementation is separately authorized.
