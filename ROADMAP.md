# Sovereign Memory Protocol Roadmap

_Status: planning document; not normative protocol text_  
_Last updated: 2026-08-27_

This roadmap describes sequencing for the protocol repository. It does not authorize implementation, deployment, production enrollment, publication, or a release.

## North star

SMP should let an independent verifier answer, with bounded claims:

- what information or evidence was observed;
- where it came from and what authority asserted it;
- what changed, what superseded what, and what remained immutable;
- who or what was authorized to perform a transition;
- what was actually evaluated and what remains unknown;
- whether custody and provenance survive export, transfer, restore, provider change, or model/runtime change;
- when AI/agent access is introduced to an existing system, what protected surface/state was **observed and committed** at the access boundary and what can be proven about changes after that point.

The protocol should accomplish this without requiring one storage engine, one memory schema, one model, or a migration of existing payloads into an SMP-native database.

## Phase 0 — Establish the private protocol baseline

**Current.**

- Preserve PR #1 as the initial protocol package lineage.
- Apply the accepted bounded PR #5 repair onto that lineage.
- Freeze one new exact combined head.
- Run repository validator and CI.
- Obtain fresh exact-head independent review.
- Merge only the reviewed artifact through the approved private workflow.

**Exit:** one private draft baseline exists at an immutable reviewed coordinate.

## Phase 1 — Fill the semantic gaps exposed by operation

Add bounded implementation-neutral drafts for:

1. **Evaluability and proof quality**
   - defined vs evaluated vs passed;
   - explicit evidence population and claim limits;
   - positive controls and deliberately broken controls;
   - independent ground truth where claims require it.

2. **Implementation self-description**
   - protocol/profile pins;
   - representation mappings;
   - extensions, deviations, unsupported requirements;
   - conformance coverage.

3. **Claim scope and topology**
   - local result vs global claim;
   - coverage receipts;
   - incomplete/unreachable stores;
   - privacy-preserving inventory semantics.

4. **Human approval and actor assurance**
   - proposal vs authorization;
   - authenticated authorizer;
   - assurance level;
   - single-use approval and resulting custody receipt.

**Exit:** these semantics are reviewed as protocol concepts and backed by traceable fixtures.

## Phase 2 — Agent Access Integrity Boundary

Revise issue #9 into a protocol-quality design before normative promotion.

The current proposal: before a novel agentic principal is granted access to an existing data system, establish a scoped T0 reference over the protected surface, bind first access to accepted enrollment evidence, and evaluate post-T0 observations and mutations against explicit assurance dimensions.

Peer review currently records Ariadne `ACCEPT WITH AMENDMENTS` and Warden `AMEND`; principal acceptance and normative promotion are not recorded.

### Required revisions

- Rename away from "Pre-Agent Integrity Enrollment" where that phrase can imply proof of pre-T0 correctness.
- Model assurance as orthogonal dimensions rather than one scalar ladder.
- Define a bootstrap ceremony for T0.
- Include the protected-surface definition itself in the commitment.
- Distinguish observed change from completeness of change observation.
- Represent shared-credential attribution ambiguity explicitly, including a machine-evaluable attributed-set/candidate cardinality rather than a singular actor claim where evidence cannot distinguish one actor.
- Define continuity events for migrations, bulk jobs, failover, PITR, restore, and replica relationships.
- Define fail-closed `UNKNOWN`, drift, suspension, and degraded-read semantics.
- Keep the evidence plane commitment/receipt-first; avoid mirroring payloads.
- Require substrate-specific effective read-only/write-path enumeration.
- Bind the first `ACCESS_ENABLED` event to an accepted enrollment receipt.
- Define receipt domain separation and an explicit audience/verifier claim without turning receipts into bearer authorization.
- Define evidence independence by actual trust/write authority: separate credentials or stores do not create independent custody if the same authority can retroactively rewrite both planes.

### Suggested assurance dimensions

The exact registry remains to be designed, but reviews converge on independent dimensions such as:

- baseline/reference integrity;
- protected-surface scope;
- observation continuity/completeness;
- actor distinguishability / credential binding;
- mediation;
- enforcement;
- temporal continuity;
- evidence independence;
- recovery/currentness.

Named profiles may bundle dimensions; they must not replace dimensional reporting.

**Exit:** accepted design, threat model, state machine, evidence envelope, and conformance matrix. No production enrollment required.

## Phase 3 — Neutral conformance and vectors

- Stable requirement IDs.
- Machine-readable fixture schemas.
- Registered result/error/dimension vocabularies.
- Positive, negative, and broken-control fixtures.
- At least one deliberately different substrate runner/stub.
- Exact review-package and conformance receipts.
- Coverage reported separately from outcome.

**Exit:** protocol claims can be exercised without assumptions from one implementation family.

## Phase 4 — Substrate profiles

Substrate profiles define mechanisms needed to satisfy the portable protocol.

Initial candidates:

- transactional relational database: catalogs, privilege closure, transaction/change-log continuity, restore boundaries;
- version-control/filesystem: commit/tree/content identities and signer/actor binding;
- object storage: immutable/versioned objects, manifest roots, event coverage, delete/durability semantics;
- embedded database: file/checkpoint/change-observation semantics and limitations;
- SaaS/API systems: explicit lower-assurance profiles where write-path completeness cannot be attested.

Canonical serialization and write-path enumeration belong in each profile.

**Exit:** at least one reference implementation and one materially different substrate can produce comparable protocol claims without identical schemas.

## Phase 5 — Portability, transfer, recovery, and provider exit

- Golden export/transfer/restore vectors.
- Bilateral custody transfer.
- Retention/hold/erasure closure.
- Restore quarantine and non-resurrection.
- Source-qualified completeness and currentness.
- Offline verification and provider-exit evidence.
- Recovery claims explicitly separated from provenance/integrity claims.

## Phase 6 — Publication readiness

Before any public protocol release:

- private draft baseline accepted;
- normative surface stabilized;
- machine-readable vectors available;
- full-history/public-boundary sanitation;
- contribution/namespace decision;
- license decision;
- exact release manifest/checksums;
- known limitations and unsupported coverage;
- exact release tag review.

## Ongoing design rules

- **Use and translate; do not force convergence.**
- **Protocol requirements describe meaning; profiles describe mechanisms.**
- **PASS states what was evaluated. Silence is not evidence.**
- **Evidence and truth are different claims.**
- **Identity, authority, assurance, and runtime attribution are separate.**
- **Derived state is never authority merely because it is useful.**
- **Migration is optional unless the implementation genuinely requires it.**
- **Existing systems may gain an agent-access evidence boundary in situ if the profile's requirements are eventually accepted.**
