# Protocol Status

_Last updated: 2026-09-07_
_Overall status: public pre-release protocol draft; consolidated foundation and two shared-contract candidates on main_

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
| Consolidated foundation | **Merged draft** | PR #1 absorbed the PR #5 repair and PR #10 orientation work at `fcff842063a8da127f2577c36c4c5316de9c0cce`; this is not a released standard |
| Context Envelope v0.1 | **Merged candidate** | PR #11, `2494ce043c340d5d887fe0b118a9edeff4aedb85`; executable conformance remains unproven |
| Capability and Policy Contract v0.1 | **Merged candidate** | PR #12, `32b70a60521b78812ac8d7587d109397e4ab9376`; executable conformance remains unproven |
| Evaluability / proof quality | Proposed extraction | Protocol-level semantics identified from implementation evidence; not yet normative |
| Implementation self-description | Proposed extraction | Needed to make mappings/extensions/deviations explicit |
| Claim scope / topology | Proposed extraction | Local miss must not become global absence without evaluated coverage |
| Human approval / actor assurance | Proposed extraction | Approval semantics belong in protocol; authentication/UI remain downstream |
| Agent Access Integrity Boundary | **Peer-reviewed proposal; principal acceptance unrecorded** | Issue #9; independent dispositions `ACCEPT WITH AMENDMENTS` and `AMEND`; not normative or promoted |
| External anchoring profiles | Informative research | No mandatory witness/anchor mechanism selected |
| Review-package CI | Draft / active on PRs | Manifest, sanitation, registry, traceability, and package-integrity checks; not protocol conformance |
| Repository visibility | Public | Available for inspection and discussion; private deployment material remains out of scope |
| Protocol release | Not established | Normative promotion, vectors, license, release-boundary review and exact release approval remain separate gates |

## Important current claim limits

- SMP remains a **protocol draft**, not a certification.
- A checksum or root authenticates observed bytes under stated assumptions; it does not prove external truth.
- A T0 enrollment/reference cannot prove the data was correct or untampered before T0.
- Shared credentials place a ceiling on actor attribution.
- "Read-only" must be evaluated over effective reachable write surfaces, not inferred from absence of ordinary mutation grants.
- Recovery/provider exit is a separate claim from integrity, provenance, or currentness.
- Substrate-specific mechanisms belong in implementation/profile layers, not in implementation-neutral protocol semantics.

## Accepted direction

- Custody-semantic fields are write-once after their recording boundary.
- Corrections and lifecycle changes append successors or events.
- Authorized payload erasure remains possible and must leave only a privacy-safe minimum receipt.
- Mutable derived state is explicitly a rebuildable projection.
- Verification reports separate definition, evaluation, outcome, coverage, and claim limits.
- Authority is multidimensional; actor labels are not identity proof.
- Implementation differences are classified as mappings, extensions, profiles, deviations, limitations, or violations rather than forced into schema parity.

## Proposed direction under issue #9 review

- Existing systems may gain a forward agent-access evidence boundary in situ; payload migration need not be a prerequisite.
- The protected surface itself should be committed and versioned.
- Assurance should be reported as orthogonal dimensions rather than a scalar level.
- First access should be bound to accepted enrollment evidence.
- Attribution ambiguity, continuity gaps, and evidence-independence limits should be machine-visible rather than inferred.

These issue #9 directions have peer review support but do not yet record principal acceptance or normative promotion.

## Immediate protocol work

1. Preserve the merged foundation and its exact review history; do not repeat completed stack integration.
2. Keep repository status and navigation aligned with the Context Envelope and Capability/Policy candidates now on main.
3. Obtain fresh independent exact-head review for each new change; predecessor verdicts do not transfer automatically.
4. Separate planned case handles, documented cases and executed conformance evidence in every validation report.
5. Add the missing protocol semantic areas in bounded review slices:
   - evaluability/proof quality;
   - implementation self-description;
   - claim scope/topology;
   - human approval/actor assurance.
6. Revise issue #9 into an Agent Access Integrity Boundary design/threat/conformance matrix using orthogonal assurance dimensions before any normative profile draft.
7. Add implementation-neutral machine-readable fixtures and a deliberately different substrate neutrality runner before broad conformance claims.
8. Keep substrate-specific mechanics in substrate profiles/reference implementations.

## Promotion gates

1. One editor produces a frozen candidate with exact hashes.
2. Independent security/architecture review names the exact artifact and coverage.
3. Every normative requirement maps to a registered result and fixture/evidence plan.
4. Defined, evaluated, passed, unsupported, unknown, and not-evaluated remain distinct.
5. Conflicts and coverage gaps remain visible rather than silently normalized.
6. The principal explicitly promotes the exact artifact.
7. Implementation, deployment, publication, and licensing are separately authorized.

See [ROADMAP.md](ROADMAP.md) for sequencing and [docs/WIKI.md](docs/WIKI.md) for the orientation index.
