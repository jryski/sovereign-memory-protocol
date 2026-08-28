# SMP Wiki / Orientation

_Status: repository-native orientation page; informative, not normative_

This file is the version-controlled source for high-level SMP orientation. If a GitHub Wiki is maintained separately, it should mirror this page rather than become a second authority.

## What is SMP?

The Sovereign Memory Protocol is an implementation-neutral protocol for preserving and evaluating:

- provenance;
- custody;
- authority;
- lineage;
- change/integrity evidence;
- verification coverage;
- portability and recovery claims

when AI systems interact with important information.

It began as a memory protocol. The current protocol direction intentionally supports both AI-native memory systems and existing data systems that are being opened to agentic workloads.

## What SMP is not

SMP is not:

- a database;
- a vector store;
- a universal memory schema;
- an answer-quality framework;
- a blockchain requirement;
- an AI identity provider;
- a replacement for native systems of record;
- proof that source data is true;
- proof of history that was never observed.

## The three authority layers

### Protocol

Owns meaning:

- records/evidence;
- provenance/custody;
- authority and assurance;
- lifecycle/supersession;
- verification/conformance;
- profiles and claim limits.

Repository: `sovereign-memory-protocol`.

### Reference implementation

Owns one portable implementation of protocol semantics.

For the current PostgreSQL work, this is `sovereign-memory-core`.

PostgreSQL mechanics must not silently become protocol requirements.

### Deployment/application

Owns:

- local authentication;
- credentials;
- UI;
- topology;
- operational policy;
- adapters;
- recovery operations;
- deployment acceptance.

A deployment may be SMP-conformant without copying the Core schema.

## Core concepts

### Custody is not truth

A valid hash can establish that bytes and lineage match a committed record. It does not prove that an external statement was true.

### Authority is multidimensional

Do not collapse these into one actor field:

- principal;
- runtime;
- client;
- credential/session;
- proposer;
- reviewer;
- authorizer;
- execution service.

Caller-supplied labels are assertions, not proof.

### Time is multidimensional

Observed time, effective time, recorded time, verified time, anchored time, and restore time are not interchangeable.

### History changes by append

Corrections and state transitions preserve prior recorded evidence rather than silently rewriting it.

### Derived state is rebuildable

Search indexes, vectors, summaries, caches, rankings, context projections, and other derived state are not authoritative merely because they are useful.

### PASS requires evaluability

A clean result must identify what was evaluated. Empty output, missing errors, or zero findings are not independently sufficient proof.

## Two adoption modes

### Native implementation

A new memory/data system implements SMP semantics directly.

### In-situ agent access boundary

An existing ERP, CRM, data warehouse, document store, object store, or other system remains in place.

Before a novel agentic identity is granted access:

1. declare the protected surface;
2. create a scoped T0 reference/commitment;
3. record the enrollment evidence and assurance limits;
4. bind first access to the accepted enrollment;
5. observe and classify changes after T0;
6. progressively permit narrow governed mutations only where identity, capability, and evidence are proven.

This is a **forward evidence boundary**, not certification of pre-T0 correctness.

See [AGENT-ACCESS-INTEGRITY-BOUNDARY.md](AGENT-ACCESS-INTEGRITY-BOUNDARY.md).

## Agent Access Integrity Boundary — current design direction

Independent review converges on these requirements:

- assurance should be reported as orthogonal dimensions;
- protected-surface scope must be committed and versioned;
- T0 trust requires a documented bootstrap ceremony and explicit evidence independence;
- shared credentials limit attribution;
- change capture requires write-path coverage, continuity, and gap semantics;
- "read-only" is an effective property across all reachable mutation paths;
- unexplained drift and UNKNOWN are durable states and must not silently become clean;
- restores/PITR/failover require continuity receipts;
- first agent access should be mechanically bound to accepted enrollment evidence;
- evidence should store commitments/receipts/references rather than become a shadow copy of source payloads.

The design remains proposed until these concepts are reconciled into a reviewed profile/conformance package.

## Repository map

- `README.md` — high-level orientation.
- `STATUS.md` — current maturity and gates.
- `ROADMAP.md` — sequencing.
- `PRINCIPLES.md` — durable design constraints.
- `GLOSSARY.md` — terminology.
- `spec/` — protocol sections and review candidates.
- `conformance/` — fixture/expectation/profile material.
- `notes/` — informative review history and open questions.
- `docs/` — high-level informative architecture/use-case documentation.

## Current major work

1. Integrate PR #5 onto PR #1 and freeze one combined exact baseline.
2. Add evaluability, self-description, claim-scope, and human-approval semantics.
3. Refine issue #9 into the Agent Access Integrity Boundary design/threat/conformance matrix.
4. Add portable machine-readable fixtures and a non-PostgreSQL runner.
5. Keep substrate mechanics in profiles/reference implementations.
6. Prepare publication/licensing only after the private protocol surface stabilizes.

See [../ROADMAP.md](../ROADMAP.md).

## How to read a protocol claim

Whenever a document says a property is satisfied, ask:

1. What exact artifact/version was evaluated?
2. What population or surface was in scope?
3. What evidence was used?
4. What was not evaluated?
5. Was the evidence independently derived or self-reported?
6. What does the result *not* prove?

That discipline is part of SMP, not merely its review process.
