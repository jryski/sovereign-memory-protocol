# Program role: Sovereign Memory Protocol

> **Program:** Sovereign AI OS  
> **Role class:** implementation-neutral protocol  
> **Ecosystem context:** reference implementation and downstream deployment architecture

## Mission

Sovereign Memory Protocol defines portable, implementation-neutral semantics for AI memory custody, provenance, authority, lifecycle, correction, conflict, transfer, and conformance.

It exists so that durable meaning can survive changes in models, providers, applications, runtimes, and storage implementations.

## This repository owns

- normative terminology and protocol contracts within its declared scope;
- portable representation of evidence, provenance, authority, lifecycle, and transfer semantics;
- conformance requirements that can be implemented by more than one runtime;
- versioning and compatibility rules for the protocol.

## This repository does not own

- storage-engine-specific schemas or migrations;
- household or business ontology;
- planning-board schemas or workflow policy;
- user or agent authentication implementation;
- model selection, agent runtime, connectors, UI, or deployment operations;
- real user, household, or business data.

## Downstream consumers

- the reference implementation and alternative conforming runtimes;
- Household OS and private household deployments;
- business authority stores and other business deployments;
- importers, exporters, review tools, and federated/local-file profiles.

## Planning and work-plane relationship

Household and business planning systems benefit from provenance, authority, temporal state, correction, and receipt semantics. That does not make kanban columns, task assignment, lease duration, calendar synchronization, or company approval policy part of this protocol.

A planning concept should move into SMP only when it is genuinely implementation-neutral, broadly required for memory custody or transfer, and accepted through the protocol's governance process. Deployment convenience is not sufficient.

## Agent boundary

Do not broaden protocol scope to solve a local repository problem. First determine whether the issue belongs in a reference implementation, access layer, deployment ontology, planning plane, runtime, or connector. Preserve explicit unknowns rather than inventing protocol requirements from incomplete context.

No implementation or deployment may claim protocol conformance merely because it uses similar names. Conformance requires the protocol's stated evidence.
