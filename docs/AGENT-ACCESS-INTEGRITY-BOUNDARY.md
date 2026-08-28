# Agent Access Integrity Boundary

_Status: informative design proposal; not normative SMP text_  
_Source discussion: protocol issue #9 and independent review on 2026-08-27_

## Problem

Existing enterprise and personal data systems were generally designed before autonomous or semi-autonomous AI agents became direct actors.

Before a novel agentic workload is allowed to access a legacy or existing system of record, an operator should be able to establish:

- what protected surface existed immediately before agent access;
- what access surface was actually granted;
- whether that surface changed afterward;
- whether changes were attributable to an agent, human, application, administrator, system process, or an ambiguous set;
- whether an agent mutation passed through a declared capability/approval boundary;
- whether unexplained drift can be distinguished from expected change;
- what evidence remains independently verifiable without migrating the native payload.

The native data stays in place.

SMP supplies the forward provenance/custody/integrity evidence boundary around the introduction of the novel actor.

## Naming and claim limit

The earlier working name "Pre-Agent Integrity Enrollment" can overstate the guarantee.

A T0 commitment does **not** prove the pre-T0 state was correct, complete, authentic, or historically untampered.

It establishes a reference boundary:

> At accepted T0, protected surface S was observed and committed under evidence set E. Pre-T0 provenance is unknown except where separately evidenced. Post-T0 observations and mutations are covered only to the degree stated by the assurance dimensions.

For that reason this document uses **Agent Access Integrity Boundary** as the current working name.

## Conceptual flow

```text
native system of record
        |
        | before agent access
        v
protected-surface manifest
        |
        +-- native identities
        +-- included/excluded fields or units
        +-- expected non-agent writers
        +-- reachable write paths
        +-- schema/config/security coordinates
        |
        v
T0 reference / commitment
        |
        +-- canonical roots / manifests
        +-- tool and configuration versions
        +-- evidence-independence statement
        +-- operator/verifier evidence
        v
accepted enrollment receipt
        |
        v
ACCESS_ENABLED
        |
        v
agentic access
        |
        +-- reads / access evidence
        +-- observations / change stream
        +-- authorized mutations
        +-- non-agent/system mutations
        +-- unexplained drift / UNKNOWN
```

## T0 bootstrap ceremony

A strong enrollment should record:

1. the protected-surface manifest before agent credential activation;
2. native system identity and exact scope;
3. exact capture tool/query/config/version;
4. canonical serialization and root/commitment procedure;
5. pre-access audit evidence showing whether any agent principal already had access;
6. operator and verifier identities/assurance;
7. evidence-independence mechanism;
8. accepted enrollment receipt;
9. an `ACCESS_ENABLED` event bound to that receipt.

If independent witnessing is absent, the enrollment is self-attested/observed and must say so.

Possible stronger witness mechanisms include co-signature by a distinct principal, an external timestamp authority, or an append-only transparency log. The protocol should specify assurance semantics without requiring one service.

## Assurance is orthogonal

Do not use one scalar "SMP level."

A deployment may have strong actor identity but incomplete change observation, or excellent change capture but weak evidence independence.

Candidate dimensions include:

| Dimension | Question |
|---|---|
| `baseline_reference` | What exact T0 state/surface was committed and can it be reproduced? |
| `surface_scope` | Is the protected and excluded surface explicit and versioned? |
| `observation_continuity` | Would relevant changes have been observed, including gaps/failover? |
| `actor_distinguishability` | Can the native mutation be attributed to one actor/credential rather than an ambiguous set? |
| `mediation` | Must agent mutations pass through governed capability seams? |
| `enforcement` | Can the agent bypass those seams? |
| `temporal_continuity` | Are migrations, restores, PITR, replicas, and re-anchors explicitly chained? |
| `evidence_independence` | Can the source writer retroactively alter the only evidence? |
| `recovery_currentness` | Can recovery be verified without confusing reproducibility with latestness? |

Named profiles may bundle dimensions, but conformance should still report the dimensions independently.

## Protected surface

The protected surface is itself security-sensitive evidence and must be inside the commitment chain.

It may declare:

- database/schema/table/view/object namespace;
- native keys or object identities;
- columns/fields/units included;
- exclusions and why they are excluded;
- mutable/derived/cache/index state;
- agent-readable scope;
- agent-writable capabilities;
- expected human/application/system writers;
- triggers/functions/jobs/queues/APIs that can cause mutation;
- external systems required to interpret the state.

Shrinking the manifest must create a new version/continuity event. It must not silently make an existing root look clean.

## Change observation and completeness

There are two different claims:

1. **A change was observed.**
2. **Any relevant change would have been observed.**

The second requires more than CDC being enabled.

A change-coverage contract should bind:

- native transaction/LSN/binlog/event coordinate;
- source stream identity;
- capture start/end watermarks;
- protected-surface version;
- stream retention and loss behavior;
- replay/deduplication behavior;
- lag/consumer health;
- write-path enumeration;
- proof each write path is instrumented or denied;
- periodic independent surface re-verification.

Gaps become `INCOMPLETE` or `UNKNOWN`; they do not disappear when later checks succeed.

## Actor attribution

If multiple actors share the same native credential, native attribution is ambiguous.

SMP may know which agent requested an operation, but it must not represent that as proof that the native mutation was caused by that agent unless a trustworthy mediation/credential boundary connects the two.

Attribution evidence should preserve the candidate set/assurance rather than manufacture a singular actor.

## Effective read-only

"Read-only" is not merely the absence of `INSERT`, `UPDATE`, and `DELETE`.

A substrate profile must enumerate reachable mutation paths appropriate to that substrate, potentially including:

- non-DML privileges such as truncate/trigger/reference equivalents;
- stored procedures and security-definer/escalated routines;
- role and group membership closure;
- object creation or trigger attachment;
- queues/jobs/event sinks;
- FDW/dblink/external API writes;
- object-store writes/deletes;
- admin/control-plane capabilities;
- indirect write/exfiltration compositions.

A profile can only claim the paths it evaluated.

## Drift and suspension

Candidate durable states include:

- `ENROLLED`
- `ACCESS_PENDING`
- `ACCESS_ENABLED`
- `OBSERVED`
- `CHANGE_CAPTURED`
- `AUTHORIZED_AGENT_MUTATION`
- `AUTHORIZED_NON_AGENT_MUTATION`
- `EXPECTED_SYSTEM_MUTATION`
- `UNATTRIBUTED_CHANGE`
- `INTEGRITY_MISMATCH`
- `INCOMPLETE`
- `UNKNOWN`
- `SUSPENDED`
- `RESTORE_QUARANTINED`

`UNKNOWN` and `INTEGRITY_MISMATCH` are distinct.

Agent write authority should fail closed on either. A profile may define an explicitly bounded degraded-read mode for `UNKNOWN`, but any such interval must be time-bounded, receipted, and remain permanently visible in history.

A later successful check must not erase an earlier unknown interval.

## Continuity events

State discontinuities that may be legitimate must be explicit rather than normalized away:

- schema/data migrations;
- bulk maintenance;
- ETL;
- failover;
- replica promotion;
- PITR;
- restore;
- source replacement;
- canonicalization/profile changes.

A restored snapshot matching an old root proves reproduction of that snapshot. It does not prove latestness or non-resurrection.

Replicas are separate protected surfaces with declared derivation/replication relationships and lag semantics.

## Evidence-plane minimization

The evidence plane should store commitments and receipts, not become a second copy of the legacy payload.

Prefer:

- manifests;
- roots;
- chunk/page/segment commitments;
- byte lengths/counts;
- native transaction coordinates;
- bounded identifiers;
- actor/credential assurance;
- continuity receipts;
- references to separately held evidence.

Avoid:

- source values;
- raw query text containing literals;
- payload excerpts;
- guessable subject identifiers;
- per-cell hashes of low-entropy data.

Low-entropy hashes are enumerable and can become privacy leaks. Prefer row/page/segment commitments rather than cell-level commitments.

## Evidence independence

A self-attested root is useful monitoring evidence but is not independent custody.

Higher-assurance claims require that the source-side writer cannot retroactively rewrite the only accepted evidence.

Possible topologies include:

- a separately credentialed evidence store;
- independent co-signature;
- external timestamp/witness;
- append-only transparency log;
- content-addressed receipts anchored outside the source trust domain.

The protocol should expose the assurance, not force one topology.

## Substrate neutrality

The portable protocol should specify capabilities and evidence semantics.

Profiles specify mechanisms.

Examples:

- PostgreSQL: catalog/ACL closure, canonical snapshot rules, WAL/logical decoding, transaction/LSN continuity.
- MySQL: binlog, transaction, privilege/write-path profile.
- SQLite: file/checkpoint semantics and limitations.
- Git: commit/tree/ref identities and agent signer binding.
- Object storage: immutable/versioned object requirements, manifest/event/delete semantics.
- SaaS APIs: explicit lower assurance where complete write-path enumeration is unavailable.

Unsupported evidence is `UNSUPPORTED` or `INCOMPLETE`, never PASS.

## Threat-model cases required before normative promotion

At minimum:

- agent or attacker acts before T0;
- protected-surface manifest is shrunk;
- shared credential creates false singular attribution;
- capture stream has a gap;
- authorized bulk job changes many records;
- replica lag is mistaken for drift;
- PITR or restore occurs without continuity evidence;
- agent is labeled read-only but can mutate indirectly;
- evidence plane is compromised with source plane;
- verification job lies or is impersonated;
- evidence storage exhausts/fails;
- clock manipulation affects temporal evidence;
- low-entropy commitment is inverted;
- stale restore matches an old valid root;
- critical field/evidence is unavailable;
- first access occurs before enrollment acceptance.

## Next protocol work

Before this becomes normative:

1. reconcile the dimension registry;
2. define protected-surface and enrollment receipt schemas;
3. define canonical domain-separated commitment/root envelopes;
4. define `ACCESS_ENABLED`;
5. define observation/change coverage;
6. define actor/credential assurance;
7. freeze the drift/suspension state machine;
8. define stream/restore continuity;
9. define evidence-independence claims;
10. write implementation-neutral conformance fixtures;
11. write a PostgreSQL substrate profile separately from the portable core;
12. exercise at least one non-PostgreSQL profile.

No production enrollment is authorized by this document.
