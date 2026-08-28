# Protocol Status

_Last updated: 2026-08-27_  
_Overall status: private pre-release protocol program; baseline integration and new profile design in progress_

## Current state

| Area | Status | Meaning |
|---|---|---|
| Human-readable scope and boundary | Review draft | Suitable for critique; not a release claim |
| Logical record model | Skeleton draft | Terms and invariants present; profile details incomplete |
| Provenance and custody | Draft | Core distinction documented; vectors incomplete |
| Authority model | Draft | Actor/runtime/credential/principal distinctions defined; assurance work continues |
| Supersession lifecycle | Draft | Lifecycle distinctions defined; graph validation incomplete |
| Verification outcomes | Draft | Structured dimensions and fail-closed claim discipline defined |
| Conformance model | Draft | Neutrality boundary defined; complete machine-readable vectors absent |
| Error taxonomy | Draft | Stable result/error separation present; registry hardening continues |
| Immutability/custody chain v0.1 | **NEEDS REVISION / preserved** | Historical review draft remains evidence, not current authority |
| Immutability/custody chain v0.2 | **Reviewed draft lineage** | PR #1 carries the package; PR #5 repairs trace/result consistency and validator enforcement |
| PR #5 bounded repair | **Exact-head ACCEPT** | Repair head `4210473d70ebe68abe70e9775753025ea2c74305`; verdict applies only to the bounded repair |
| Combined PR #5-on-#1 baseline | **Pending** | Must be integrated, frozen, validated, and freshly exact-head reviewed before baseline merge |
| Evaluability / proof quality | Proposed extraction | Protocol-level semantics identified from Core evidence; not yet normative |
| Implementation self-description | Proposed extraction | Needed to make mappings/extensions/deviations explicit |
| Claim scope / topology | Proposed extraction | Local miss must not become global absence without evaluated coverage |
| Human approval / actor assurance | Proposed extraction | Approval semantics belong in protocol; authentication/UI remain downstream |
| Agent Access Integrity Boundary | **Concept accepted with amendments** | Issue #9; forward T0 evidence boundary for introducing agent access to existing systems in situ |
| External anchoring profiles | Informative research | No mandatory witness/anchor mechanism selected |
| Review-package CI | Draft / active on PRs | Manifest, sanitation, registry, traceability, and package-integrity checks; not protocol conformance |
| Public release | Blocked | Baseline, vectors, sanitation, license, publication, and exact promotion remain pending |

## Important current claim limits

- SMP remains a **protocol draft**, not a certification.
- A checksum or root authenticates observed bytes under stated assumptions; it does not prove external truth.
- A T0 enrollment/reference cannot prove the data was correct or untampered before T0.
- Shared credentials place a ceiling on actor attribution.
- "Read-only" must be evaluated over effective reachable write surfaces, not inferred from absence of ordinary DML grants.
- Recovery/provider exit is a separate claim from integrity, provenance, or currentness.
- PostgreSQL-specific mechanisms belong in an implementation/profile layer, not in implementation-neutral protocol semantics.

## Accepted direction

- Custody-semantic fields are write-once after their recording boundary.
- Corrections and lifecycle changes append successors or events.
- Authorized payload erasure remains possible and must leave only a privacy-safe minimum receipt.
- Mutable derived state is explicitly a rebuildable projection.
- Verification reports separate definition, evaluation, outcome, coverage, and claim limits.
- Authority is multidimensional; actor labels are not identity proof.
- Implementation differences are classified as mappings, extensions, profiles, deviations, limitations, or violations rather than forced into schema parity.
- Existing systems may be protected in situ as agentic access is introduced; payload migration is not a prerequisite to establishing a post-T0 evidence boundary.

## Immediate protocol work

1. Integrate PR #5 onto the PR #1 lineage.
2. Freeze the combined exact head and rerun validator/CI.
3. Obtain fresh independent exact-head review; predecessor verdicts do not transfer automatically.
4. Establish the private draft baseline only after that review.
5. Add the missing protocol semantic areas in bounded review slices:
   - evaluability/proof quality;
   - implementation self-description;
   - claim scope/topology;
   - human approval/actor assurance.
6. Revise issue #9 into an Agent Access Integrity Boundary design/threat/conformance matrix using orthogonal assurance dimensions before any normative profile draft.
7. Add implementation-neutral machine-readable fixtures and a non-PostgreSQL neutrality runner before broad conformance claims.
8. Keep PostgreSQL, object-storage, Git, SaaS, and other substrate mechanics in substrate profiles/reference implementations.

## Promotion gates

1. One editor produces a frozen candidate with exact hashes.
2. Independent security/architecture review names the exact artifact and coverage.
3. Every normative requirement maps to a registered result and fixture/evidence plan.
4. Defined, evaluated, passed, unsupported, unknown, and not-evaluated remain distinct.
5. Conflicts and coverage gaps remain visible rather than silently normalized.
6. The principal explicitly promotes the exact artifact.
7. Implementation, deployment, publication, and licensing are separately authorized.

See [ROADMAP.md](ROADMAP.md) for sequencing and [docs/WIKI.md](docs/WIKI.md) for the orientation index.
