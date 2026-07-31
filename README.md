# Sovereign Memory Protocol (SMP)

SMP is an implementation-neutral custody and verification protocol for AI memory.

Memory engines decide what to remember, how to retrieve it, and how to answer. SMP addresses a different question: **can memory evidence, derived claims, authority, corrections, erasure, transfer, and recovery remain inspectable and portable when the model, application, database, provider, or operator changes?**

## Why this exists

An export can move bytes without preserving what those bytes meant, who asserted them, what evidence supported them, whether they were accepted, what they superseded, or whether a restored copy is stale. SMP is intended to make those custody properties explicit and independently testable.

> Formats move bytes. SMP preserves custody, lineage, and authority boundaries.

## Scope

SMP specifies:

- evidence identity and source-to-derived lineage;
- proposal, inference, acceptance, conflict, correction, supersession, retirement, and withdrawal semantics;
- actor, runtime, credential, principal, authorization, and reviewer distinctions;
- immutable custody envelopes, erasable payloads, and rebuildable projections;
- implementation-neutral verification outcomes and conformance fixtures;
- export, transfer, restore, freshness, and provider-exit evidence;
- explicit limits on truth, completeness, currentness, erasure, and availability claims.

SMP does **not** specify a universal memory-record format, retrieval engine, ranking model, vector database, answer policy, or storage product. A memory engine may implement SMP without replacing its own internal schema or retrieval design.

## Repository status

This repository is **private and pre-release**. The document tree is populated for review, not published as an accepted standard.

- Sections marked **Draft** are unstable proposals.
- A normative `MUST` in a draft is a proposed requirement, not evidence that any implementation conforms.
- `spec/08-immutability-and-chain-of-custody.md` is explicitly **NEEDS REVISION** after adversarial review.
- No implementation, deployment, key service, external anchor, or conformance certification is supplied here.

See [STATUS.md](STATUS.md) for section maturity and [PRINCIPLES.md](PRINCIPLES.md) for the protocol boundary.

## Document map

| Document | Purpose |
|---|---|
| [GLOSSARY.md](GLOSSARY.md) | Shared terms and epistemic states |
| [PRINCIPLES.md](PRINCIPLES.md) | Design constraints and non-goals |
| [STATUS.md](STATUS.md) | Per-section maturity and review gates |
| [REVIEW-MANIFEST.sha256](REVIEW-MANIFEST.sha256) | Exact SHA-256 review manifest |
| [spec/00-overview.md](spec/00-overview.md) | Protocol scope and claims |
| [spec/01-records.md](spec/01-records.md) | Logical record and payload model |
| [spec/02-provenance-and-custody.md](spec/02-provenance-and-custody.md) | Evidence and lineage |
| [spec/03-authority.md](spec/03-authority.md) | Authority and attribution dimensions |
| [spec/04-supersession.md](spec/04-supersession.md) | Correction and lifecycle semantics |
| [spec/05-verification.md](spec/05-verification.md) | Structured verification outcomes |
| [spec/06-conformance.md](spec/06-conformance.md) | Conformance claims and fixtures |
| [spec/07-errors.md](spec/07-errors.md) | Stable errors and precedence |
| [spec/08-immutability-and-chain-of-custody.md](spec/08-immutability-and-chain-of-custody.md) | Immutable fields and custody-chain draft |
| [conformance/README.md](conformance/README.md) | Neutral fixture contract |
| [notes/adjacent-memory-systems.md](notes/adjacent-memory-systems.md) | Non-competitive composition boundary |

## Review model

Protocol promotion requires review of exact artifact hashes. Peer agreement is evidence, not authority by itself. Implementation conformance must be reported by dimension and tested surface; a single undifferentiated “SMP conformant” badge is not defined by this draft.

## Licensing

No public license grant has been selected yet. Until a license is added, ordinary copyright rules apply. Do not redistribute or treat this private review repository as an open standard release.
