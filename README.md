# Sovereign Memory Protocol (SMP)

SMP is an implementation-neutral protocol for **provenance, custody, authority, integrity, and portability in AI-accessed information systems**.

SMP began with AI memory, but the protocol boundary is broader than any one memory engine or database. It addresses a more general question:

> **When AI systems read, derive from, or mutate important information, can we prove what the information was, where it came from, what changed, who or what had authority, and what remains independently verifiable when the model, application, database, provider, or operator changes?**

Memory engines still decide what to remember, retrieve, rank, summarize, and answer. Existing enterprise systems still own their native records. SMP defines the evidence and authority semantics around those systems.

## Why this exists

An export can move bytes without preserving what those bytes meant, who asserted them, what evidence supported them, whether they were accepted, what they superseded, or whether a restored copy is stale.

Agentic workloads add a second problem: most existing systems were designed before non-human actors were given direct data access. "Read-only," "the agent did not change anything," and "this mutation was authorized" are often policy statements rather than independently testable claims.

SMP is intended to make those claims explicit, bounded, and independently evaluable.

> **Formats move bytes. SMP preserves custody, lineage, authority boundaries, and the evidence needed to evaluate change.**

## What the current draft specifies

The current draft package specifies implementation-neutral semantics for:

- evidence identity and source-to-derived lineage;
- proposal, inference, acceptance, conflict, correction, supersession, retirement, and withdrawal;
- actor, runtime, credential, principal, authorization, reviewer, and assurance distinctions;
- immutable custody envelopes, erasable payloads, and rebuildable projections;
- verification outcomes, coverage, unknown states, and claim limits;
- export, transfer, restore, freshness, provider-exit, and recovery evidence;
- explicit limits on truth, completeness, currentness, erasure, and availability claims.

The roadmap separately proposes additional protocol semantics for progressively governed introduction of AI/agent access to existing information systems. Those proposed semantics are not yet normative SMP requirements.

SMP does **not** require a universal record format, retrieval engine, vector database, storage product, cloud provider, or application architecture.

## Two important adoption patterns

### 1. Native SMP-aware systems

A memory platform or application can implement SMP directly: native records, custody events, authority transitions, export/restore, and conformance evidence are designed together.

Reference implementations belong outside this protocol repository.

### 2. Existing systems introduced to agentic workloads

SMP is being designed to support **in-situ** adoption without migrating the native payload first.

The current design proposal is an **Agent Access Integrity Boundary**: before an AI agent receives access to a legacy or existing system of record, establish a scoped, independently reviewable T0 reference over the protected surface. First agent access would then be bound to accepted enrollment evidence, and post-T0 changes would be evaluated against explicit observation, attribution, mediation, enforcement, and evidence-independence claims.

This does **not** prove the pre-T0 data was correct or historically untampered. It is intended to establish a forward evidence boundary.

See [docs/AGENT-ACCESS-INTEGRITY-BOUNDARY.md](docs/AGENT-ACCESS-INTEGRITY-BOUNDARY.md) and protocol issue #9. Peer review is not yet principal acceptance: independent reviewers returned `ACCEPT WITH AMENDMENTS` and `AMEND`. Principal acceptance and normative promotion are not recorded.

## Authority layers

SMP distinguishes three authority layers:

1. **Protocol**: implementation-neutral meaning, requirements, profiles, conformance semantics, and claim limits.
2. **Reference implementation**: portable mechanisms that demonstrate one implementation of the protocol.
3. **Deployment/application**: local identity, policy, UI, topology, credentials, adapters, and operational acceptance.

A repository, deployment, store, trust domain, and visibility class are not interchangeable concepts.

## Repository status

This repository is a **public, pre-release protocol draft**. Public visibility is not a standards release, license grant, or conformance result.

The following draft packages are now on `main`:

- PR #1 consolidated the foundation, including the PR #5 repair and PR #10 orientation work, at `fcff842063a8da127f2577c36c4c5316de9c0cce`.
- PR #11 added [Context Envelope v0.1](spec/09-context-envelope-v0.1.md).
- PR #12 added [Capability and Policy Contract v0.1](spec/10-capability-and-policy-v0.1.md).
- Historical exact-head review verdicts apply to their named artifacts and scope, not automatically to later edits.
- Issue #9 proposes the Agent Access Integrity Boundary concept and has independent peer dispositions of `ACCEPT WITH AMENDMENTS` / `AMEND`; principal acceptance is unrecorded.
- No public protocol release, conformance certification, or implementation authorization is implied by these documents.

See [STATUS.md](STATUS.md) for current maturity and [ROADMAP.md](ROADMAP.md) for sequencing.

To help, start with [CONTRIBUTING.md](CONTRIBUTING.md). Useful contributions include precise ambiguities, counterexamples, neutral test vectors, and small reviewable repairs. Do not post private deployment data or credentials.

## Documentation map

| Document | Purpose |
|---|---|
| [docs/WIKI.md](docs/WIKI.md) | Repository-native orientation/wiki index |
| [ROADMAP.md](ROADMAP.md) | Current protocol sequencing and major design lanes |
| [STATUS.md](STATUS.md) | Per-area maturity and promotion gates |
| [PRINCIPLES.md](PRINCIPLES.md) | Design constraints and non-goals |
| [GLOSSARY.md](GLOSSARY.md) | Shared terminology and epistemic states |
| [docs/AGENT-ACCESS-INTEGRITY-BOUNDARY.md](docs/AGENT-ACCESS-INTEGRITY-BOUNDARY.md) | Informative in-situ agent-access design proposal |
| [spec/00-overview.md](spec/00-overview.md) | Protocol scope and claims |
| [spec/01-records.md](spec/01-records.md) | Logical record and payload model |
| [spec/02-provenance-and-custody.md](spec/02-provenance-and-custody.md) | Evidence and lineage |
| [spec/03-authority.md](spec/03-authority.md) | Authority and attribution dimensions |
| [spec/04-supersession.md](spec/04-supersession.md) | Correction and lifecycle semantics |
| [spec/05-verification.md](spec/05-verification.md) | Structured verification outcomes |
| [spec/06-conformance.md](spec/06-conformance.md) | Conformance claims and fixtures |
| [spec/07-errors.md](spec/07-errors.md) | Stable errors and precedence |
| [spec/08-immutability-and-chain-of-custody-v0.2.md](spec/08-immutability-and-chain-of-custody-v0.2.md) | v0.2 custody-chain review candidate |
| [spec/09-context-envelope-v0.1.md](spec/09-context-envelope-v0.1.md) | Context exchange contract candidate |
| [spec/10-capability-and-policy-v0.1.md](spec/10-capability-and-policy-v0.1.md) | Capability and policy contract candidate |
| [conformance/README.md](conformance/README.md) | Neutral fixture contract |

## Review model

Protocol promotion requires review of exact artifacts. Peer agreement is evidence, not authority by itself.

A valid PASS must say what was evaluated. Defined criteria, evaluated criteria, passed criteria, and unavailable/unknown coverage are separate. Silence or an empty finding set is not evidence of a clean result.

Pull requests run the dependency-free review-package validator through `.github/workflows/review-package.yml`. Passing repository-integrity CI validates the package; it does not establish protocol correctness or implementation conformance.

## Licensing

No public license grant has been selected yet. The repository is public for inspection and discussion, but this visibility change does not select a license or establish an open-standard release. Licensing remains a separate maintainer decision.
