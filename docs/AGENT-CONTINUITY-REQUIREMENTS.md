# Persistent agent continuity: requirements proposal

Captured: 2026-11-02.

**Informative design input, not normative SMP, protocol acceptance,
implementation authorization, or evidence of deployed isolation.**

This records a program use case for the existing protocol. It does not
replace the [protocol scope](../README.md), invent a separate standard,
require a particular database, or move runtime orchestration into SMP.

## User outcome

An owner should be able to replace models, runtimes, applications, and
storage without losing the meaning of personal knowledge, a persistent
assistant's identity, or a team's useful work.

A model supplies reasoning. The owner-controlled environment preserves
identity, evidence, decisions, instructions, role learning, relationships,
permissions, and ongoing responsibilities. Personalization should work
through authorized context rather than require contributions to provider
foundation-model training. Optional private adaptation is not a core
requirement or the sole canonical carrier of knowledge.

## Many brains on a shared foundation

One platform may support multiple persistent agent brains with shared
understanding and distinct roles. A brain is logical durable state, not a
mandatory database or machine per agent and not a claim of personhood.

Keep human principal, stable agent identity, role, brain/workspace, and
execution separate. A model upgrade changes available competence, not
identity or permission. A smaller model may require narrower tasks;
access to the same evidence does not imply equal reasoning quality.

The primary assistant may commission specialists within explicit
human-approved delegation. A specialist receives an authorized view of
shared evidence and its own continuing workspace, not a copy of all data
or the parent's credentials. Existing access is not automatically delegable.
Persistent state does not require continuous inference.

## Proposed semantic requirements

### Identity and instructions

Preserve stable identity and versioned character, preferences, behavioral
instructions, operating practices, and attribution of changes. Distinguish
human-defined, jointly agreed, and agent-authored material. A SOUL-style
file may be a representation; no particular filename is required.

An agent may curate its own working state within scope without gaining
authority to alter shared facts, another identity, or access policy.
Instructions, factual evidence, executable capabilities, and grants are
not interchangeable records.

### Shared evidence and distinct working state

Preserve ownership, purpose, visibility, source lineage, time, epistemic
state, and correction history. Shared understanding is not unrestricted
read access or universal agreement. An agent's private hypothesis remains
attributed; promotion into shared accepted knowledge is a separate event.

A namespace label or claimed actor name is not authenticated isolation.
Read, owned write, shared publication, acceptance, delegation, revocation,
and erasure have distinct authority semantics and enforcement evidence.

### Continuing work and learning

Preserve role charters, responsibilities, decisions, checkpoints, action
receipts, failures, outcomes, and reusable tested practices. Distinguish
proposed action, authorization, attempt, confirmed effect, and unresolved
external outcome. A replacement must reconcile uncertain effects before
retrying a consequential operation.

### Context and execution

A bounded context projection should identify applicable identity and
instruction versions, source versions, freshness, omissions, relevant
work state, and actual permitted capabilities. Summaries and embeddings
remain derived/rebuildable views rather than the only durable meaning.

Model/provider/runtime metadata belongs to the execution record where
observable. Do not trust a model's self-description as runtime evidence.
Do not imply that an instruction describing a tool makes that tool available.

### Portability and exit

Preserve identifiers, attribution, relationships, temporal meaning,
decision status, identity history, role state, and policy requirements.
Declare source omissions and unsupported semantics. Fail visibly where a
destination cannot enforce a required authority boundary.

Credentials must be re-established under destination authority, not copied
as ordinary memory. Retention and erasure include relevant derivatives
within the defined control boundary. Revocation cannot undo prior disclosure.
Integrity verification is not proof that a claim is true.

## Proposed conformance scenarios

Use synthetic records and two distinct identities:

1. Both read one explicitly shared fact while maintaining different identity
   versions, preferences, and owned working notes.
2. Each writes an attributed proposed record within its own scope; independent
   readback verifies the result.
3. Cross-agent private access, unauthorized shared acceptance, and grant
   modification are denied at the real enforcement boundary.
4. Correction preserves applicable lineage and makes current, superseded,
   conflicting, stale, and unknown states distinguishable.
5. Replace the executing model and start a fresh session. Preserve identity,
   relevant decisions, own memory and work checkpoint; report capability limits.
6. Concurrent runs do not silently duplicate consequential effects or overwrite
   identity changes. Fork and merge semantics remain explicit.
7. Revoke access and test denial; export/import through another adapter and
   expose unsupported requirements instead of silently dropping meaning.

These are candidate scenarios, not claims that a suite exists or passes.
A test must state exact artifacts, environment, evaluated criteria, and
unavailable coverage. Peer agreement is not principal acceptance.

## Ownership and open questions

SMP owns portable meaning and claim limits. Reference implementations own
mechanisms and conformance evidence. Access components own authenticated
runtime mediation. Runtimes own profile loading and execution integration.
Deployments own their data, identity policy, retention, and acceptance.

Open: stable identity and brain identifiers; identity evolution and forks;
self-curation versus shared promotion; concurrent updates; retention across
projections; behavior qualification across models; unsupported-extension
handling; and lossiness reporting during migration. Map these to existing
SMP concepts before proposing new records or normative requirements.

## Provenance

Derived from the principal's founding conversation, the 18 October 2026
Sovereign AI Continuity charter/manifesto drafts, and the 2 November 2026
clarification that a shared brain platform should support distinct developing
agents and role-specific learning. This is an attributed synthesis, not a
verbatim transcript or independently reviewed design.

Private identities, deployment locators, operational payloads, and channel
messages are deliberately omitted. Publication/release status follows the
owning repository; sanitized prose alone does not authorize publication.
