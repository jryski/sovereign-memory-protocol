# SMP Capability and Policy Contract v0.1

**Status:** candidate specification; documentation-only, implementation-neutral

**Version:** `capability-policy/v0.1`

**Normative language:** **MUST**, **MUST NOT**, **SHOULD**, and **MAY** have their usual requirement meanings.

> This document defines portable authority-decision inputs and decision semantics. It does not issue credentials, grant deployment authority, define a database schema, or claim implementation or conformance. Examples are synthetic.

## 1. Purpose and authority boundary

The Capability and Policy Contract represents who or what may request an operation, which authority asserted that permission, the scope and conditions of the assertion, and the policy evidence required for a current authorization decision.

It MUST distinguish:

- descriptive or scheduling metadata from enforceable authority;
- a principal from the client, agent, runtime, or credential acting for it;
- a capability definition from a capability grant;
- a grant from a bearer credential;
- token scope from application capability and database authorization;
- a proposal or review disposition from execution approval;
- policy evaluation from final resource enforcement; and
- historical evidence from current effective authority.

A capability or policy record is not self-authenticating. Possession of this document, a Context Envelope, a task assignment, an agent prompt, a model output, or an approval display MUST NOT by itself authorize execution.

## 2. Scheduling metadata is non-authoritative

Task priority, queue position, assignment, lease, due date, retry count, worker eligibility, status, labels, routing hints, model selection, and estimated cost are scheduling metadata. They MAY select which worker considers a task, but MUST NOT create, widen, prove, or replace authority.

A scheduler MAY reference a capability or policy decision by opaque identifier. It MUST NOT synthesize authority from task ownership, `assigned_to`, `claimed_by`, a successful lease, or a `done` status. A worker MUST re-authorize the exact requested action against current trusted state before execution.

## 3. Value status and explicit uncertainty

A required authority component whose value is not known MUST use an explicit value-status object rather than omission or inference:

```json
{"state":"unknown","reason":"grantor_not_resolved"}
```

Allowed value states are `known`, `unknown`, `unavailable`, `not_applicable`, and `conflict`.

- `unknown` means the value may exist but is not known.
- `unavailable` means the value may be known elsewhere but cannot currently be evaluated.
- `not_applicable` means the field does not apply under the named contract rule.
- `conflict` preserves two or more incompatible assertions and their provenance.

Unknown, unavailable, malformed, stale, or conflicted authority MUST NOT be normalized into permission. A conflict MUST NOT be resolved by array order, recency, status label, scheduler preference, or model judgment. It requires an explicit authorized resolution record.

## 4. Principal and actor model

The contract uses these distinct references:

| Object | Meaning | Authority rule |
| --- | --- | --- |
| `principal` | Human or non-human identity whose authority is evaluated | MUST be derived from verified identity or trusted policy state |
| `client` | OAuth client, application, connector, or agent acting for a principal | MUST NOT be treated as universally equivalent to the principal |
| `runtime` | Process or execution environment handling the request | Runtime identity alone grants no domain authority |
| `credential_ref` | Opaque reference to a credential class or verification event | MUST NOT contain secret bytes or function as a bearer credential |
| `grantor` | Principal or policy authority asserting a grant | MUST itself be authorized to grant the exact attenuated scope |
| `delegate` | Principal or client receiving attenuated authority | Receives no authority beyond the valid delegation chain |
| `reviewer` | Principal eligible to review a named proposal class | Review permission does not imply proposal, application, or administration permission |
| `system_worker` | Narrow backend actor applying an already-authorized operation | MUST have a separate policy envelope and cannot self-approve |

Human-readable names, email addresses, user-editable metadata, model names, host names, and scheduling-agent labels MUST NOT be authorization keys.

## 5. Normative object model

### 5.1 Capability definition

A `capability_definition` names a stable operation class. It MUST contain:

- `capability_id` and `contract_version`;
- allowed operation classes;
- resource-scope grammar;
- mandatory conditions and assurance floor;
- delegation policy;
- risk class;
- approval class, if any;
- required decision and receipt fields; and
- provenance and lifecycle status.

A definition describes meaning. It grants nothing.

### 5.2 Capability grant

A `capability_grant` MUST contain:

- `grant_id`, `capability_id`, and `contract_version`;
- `holder` and, where applicable, `client_binding`;
- `resource_scope` and `operations`;
- `conditions` and `assurance_requirement`;
- `granted_by`, `grant_basis`, and `provenance`;
- `granted_at`, `effective_at`, and `recorded_at`;
- `not_before` and exactly one expiry disposition: `expires_at`, `no_expiry_policy_ref`, or explicit value status;
- `delegation`: parent grant, chain depth, re-delegation permission, and attenuation evidence;
- `status`: `proposed`, `active`, `suspended`, `revoked`, `expired`, `superseded`, or `rejected`;
- `version` and any `supersedes` or `superseded_by` references; and
- current revocation-check requirements.

An active label is necessary but not sufficient. The grant MUST be re-evaluated against current policy, time, revocation, principal, client, resource, operation, record state, and assurance evidence.

A capability grant MUST NOT contain reusable secret material and MUST NOT be accepted as a credential. A consumer presented with only a grant object MUST deny execution.

### 5.3 Policy set

A `policy_set` MUST contain:

- `policy_set_id`, `version`, status, provenance, effective time, and recorded time;
- authority and scope of the policy issuer;
- applicable principal, client, runtime, resource, operation, and record-state selectors;
- allow, deny, approval, assurance, rate, time, row, byte, retention, disclosure, and escalation rules as applicable;
- conflict and precedence rules;
- revocation and freshness requirements;
- required external enforcement points; and
- supersession history.

A policy set MAY constrain a valid capability grant. It MUST NOT widen one. Explicit deny and unavailable mandatory evidence take precedence over allow.

### 5.4 Authorization request

An `authorization_request` describes one exact proposed operation and MUST contain:

- `request_id` and correlation reference;
- verified principal, client, runtime, and credential-verification references;
- operation and resource scope;
- normalized argument or payload digest where consequential;
- current record-state and assurance references;
- requested time and execution deadline;
- capability, policy, membership, approval, and integration references; and
- provenance for every derived identity or scope value.

Principal, tenant, workspace, owner, issuer, audience, client, approval, and capability identifiers derived from trusted context MUST NOT be accepted from model-controlled tool arguments.

### 5.5 Authorization decision

An `authorization_decision` MUST contain:

- `decision_id`, `request_id`, and `contract_version`;
- `outcome`: `allow`, `deny`, or `indeterminate`;
- evaluated principal, client, resource, operation, and action digest;
- exact capability-grant, policy, membership, approval, token-verification, credential, and record-state versions evaluated;
- defined, evaluated, passed, failed, unavailable, stale, and not-applicable dimensions;
- decision time, validity deadline, and single-use/replay disposition;
- denial or indeterminate class without forbidden-resource enumeration;
- evaluator identity and provenance; and
- external enforcement obligations.

`indeterminate` MUST fail closed. An allow decision does not override a later database, integration, runtime, or resource denial.

### 5.6 Revocation and supersession record

A `revocation_record` MUST contain revocation ID, target grant or delegation edge, authority, effective and recorded time, reason class, provenance, and affected descendant policy. Revocation MUST preserve history; it MUST NOT rewrite the original grant.

Suspension is temporary denial. Revocation terminates current authority. Supersession replaces the effective policy/grant version but preserves the predecessor. Expiry is time-based invalidity and MUST NOT be represented as revocation.

### 5.7 Approval record

An `approval_record` MUST bind:

- eligible approver and verified assurance;
- proposal and exact action/payload digest;
- capability and policy versions;
- approved resource and operation;
- issued, effective, expiry, and recorded times;
- single-use or bounded-use disposition;
- proposer/approver separation rule; and
- resulting application and receipt references when consumed.

A review status, GUI confirmation, chat message, task comment, or model statement is not an approval unless it is admitted as an approval record by the named trusted policy boundary. Editing the action invalidates prior approval.

### 5.8 Integration capability and credential reference

An `integration_capability` states what an external connector may attempt. It MUST identify the integration, owner, environment, allowed direction, operation classes, data classes, endpoint class, credential reference, expiry/revocation behavior, and downstream enforcement obligations.

A token scope is a ceiling on token use, not proof of application permission. An integration credential proves possession or identity only within its verified contract. It MUST be intersected with principal/client grants, application policy, resource state, and downstream authorization.

Secret values, refresh tokens, signing keys, database passwords, and reusable bearer tokens are outside this contract and MUST NOT appear in capability, policy, request, decision, or receipt objects.

### 5.9 Execution receipt

An `execution_receipt` records what the trusted execution boundary actually attempted. It MUST bind the authorization decision, exact action digest, executor, start/end time, external enforcement result, outcome, affected-resource references, and idempotency/replay disposition. A receipt is evidence, not retroactive authority.

## 6. Delegation and attenuation

Delegation is denied unless the parent capability definition and active grant explicitly permit it.

Every delegated grant MUST satisfy all of these invariants:

1. The grantor is currently authorized to delegate the capability.
2. Holder, client, resource, operation, data class, time window, usage count, and risk are equal to or narrower than the parent.
3. Child conditions are no weaker and assurance requirements are no lower.
4. Child expiry is no later than every ancestor expiry.
5. Re-delegation defaults to false and, when allowed, has an explicit maximum depth.
6. The complete parent chain remains addressable and version-bound.
7. Revocation, suspension, expiry, or supersession of a required ancestor invalidates descendant use unless an explicit independent basis exists.
8. A delegate cannot add approval, administration, application, policy-editing, or re-delegation authority absent from the parent.
9. An agent cannot transform scheduling assignment, possession of context, tool availability, or successful execution into a grant.
10. Delegation history is append-only; repair creates a successor rather than rewriting the chain.

When attenuation cannot be proven, the child grant is invalid.

## 7. Evaluation algorithm and precedence

A conforming evaluator MUST use current trusted state and the following fail-closed order:

1. Validate request structure, contract versions, normalized action, and resource grammar.
2. Verify principal, client, runtime, credential issuer, audience/resource, expiry, not-before time, and assurance where required.
3. Resolve current subject, client, membership, integration, capability definition, grant, delegation chain, policy set, approval, revocation, and record-state evidence.
4. Deny on malformed, revoked, suspended, expired, superseded-without-successor, conflicting, stale-required, unknown-required, or unavailable-required evidence.
5. Prove the requested resource and operation are within every capability and delegation scope.
6. Apply explicit denies, assurance requirements, risk rules, limits, approval rules, and proposer/approver separation.
7. Verify the runtime/tool contract exposes only the named operation and cannot widen caller arguments.
8. Produce a short-lived decision bound to the exact action and current evidence versions.
9. Submit the operation to downstream enforcement.
10. Treat database RLS, constraints, integration authorization, credential policy, and resource-state checks as additional mandatory gates. Any denial wins.
11. Emit a bounded receipt without secret material or forbidden-resource enumeration.

A cached allow MUST NOT survive expiry, revocation, policy or membership version change, action mutation, assurance downgrade, or a changed consequential record state.

## 8. Mapping across enforcement planes

| Plane | What it represents | What it cannot prove | Required mapping |
| --- | --- | --- | --- |
| Scheduling metadata | Priority, assignment, lease, routing, worker/model choice | Identity or authority | MAY reference policy decisions; MUST NOT create them |
| Capability definition | Stable meaning and constraints of an operation class | A holder is allowed now | Grant plus current policy evaluation |
| Capability grant | Authority assertion for holder/scope/conditions | Credential possession or final row permission | Bind to verified principal/client and current revocation state |
| User MCP tool contract | Named operation, schema, argument and output bounds | Database row authorization | Remove caller-selected authority fields; preserve verified context |
| OAuth/token scope | Issuer-defined token use ceiling | Membership, app grant, approval, row permission | Verify issuer/audience/client; intersect with protected policy state |
| Database grant and RLS | Relation reachability and row/operation predicates | Upstream UI intent or integration consent | Receive trustworthy per-request claims; remain final row gate |
| Integration credential | Authenticates connector/client to an external service | User/application permission for every action | Intersect with integration capability and downstream policy |
| Approval record | Eligible consent to one exact proposal/action | Application success or unrelated authority | Bind exact digest, policy version, time window, and single use |
| Authorization decision | Current evaluated intersection | Future validity or downstream acceptance | Short lifetime; downstream denial remains authoritative |
| Execution receipt | Observed execution outcome | Retroactive authority or external truth | Bind decision and action digest; preserve limitations |

## 9. Synthetic Household example

```json
{
  "contract_version": "capability-policy/v0.1",
  "capability_definition": {
    "capability_id": "context:request_evidence",
    "contract_version": "capability-policy/v0.1",
    "operations": ["request_evidence"],
    "resource_scope_grammar": "opaque household subject and item refs",
    "mandatory_conditions": ["conflict remains unresolved", "no mutation or disclosure expansion"],
    "assurance_floor": "verified_session",
    "delegation_policy": {"allowed": false},
    "risk_class": "read_support",
    "approval_class": "not_required",
    "required_decision_fields": ["principal", "client", "resource", "operation", "evidence_versions", "valid_until"],
    "required_receipt_fields": ["decision_id", "action_digest", "executor", "outcome"],
    "provenance": {"source_ref": "synthetic-capability-registry", "recorded_by": "example-policy-runtime"},
    "status": "candidate"
  },
  "grant": {
    "grant_id": "grant-household-example-1",
    "capability_id": "context:request_evidence",
    "contract_version": "capability-policy/v0.1",
    "holder": "principal:example-reviewer",
    "client_binding": "client:example-household-assistant",
    "resource_scope": {"subject_ref": "household:example-home", "item_refs": ["item-101", "item-119"]},
    "operations": ["request_evidence"],
    "conditions": ["conflict remains unresolved", "no mutation or disclosure expansion"],
    "assurance_requirement": "verified_session",
    "granted_by": "principal:example-policy-owner",
    "grant_basis": "policy:household-review-before-change/v3",
    "provenance": {"source_ref": "synthetic-policy-record", "recorded_by": "example-policy-runtime"},
    "granted_at": "2030-04-02T08:55:00Z",
    "effective_at": "2030-04-02T09:00:00Z",
    "recorded_at": "2030-04-02T08:56:00Z",
    "not_before": "2030-04-02T09:00:00Z",
    "expires_at": "2030-04-09T00:00:00Z",
    "delegation": {"parent_grant": {"state": "not_applicable", "reason": "direct_grant"}, "chain_depth": 0, "redelegation_allowed": false},
    "status": "active",
    "version": 1,
    "revocation_check": "required_at_execution"
  },
  "policy_set": {
    "policy_set_id": "policy:household-review-before-change",
    "version": 3,
    "status": "active",
    "provenance": {"source_ref": "synthetic-household-policy", "recorded_by": "example-policy-runtime"},
    "effective_at": "2030-04-02T09:00:00Z",
    "recorded_at": "2030-04-02T08:50:00Z",
    "issuer": "principal:example-policy-owner",
    "issuer_scope": {"subject_ref": "household:example-home"},
    "selectors": {"capability_id": "context:request_evidence", "record_state": "conflicted"},
    "rules": {"allow": ["request_evidence"], "deny": ["mutate_preference", "expand_disclosure"], "maximum_rows": 2},
    "precedence": "explicit_deny_and_unavailable_required_evidence_win",
    "revocation_freshness": "check_at_execution",
    "external_enforcement": ["integration read scope", "resource visibility policy"],
    "supersedes": {"state": "not_applicable", "reason": "first_version_in_example"}
  },
  "request": {
    "request_id": "request-household-example-1",
    "principal_ref": "principal:example-reviewer",
    "client_ref": "client:example-household-assistant",
    "runtime_ref": "runtime:example-household-worker",
    "credential_verification_ref": "verification:synthetic-session-1",
    "operation": "request_evidence",
    "resource_scope": {"subject_ref": "household:example-home", "item_refs": ["item-101", "item-119"]},
    "action_digest": "sha256:synthetic-household-request-digest",
    "record_state_refs": ["item-101:conflicted", "item-119:conflicted"],
    "assurance_refs": ["verification:synthetic-session-1"],
    "requested_at": "2030-04-02T09:05:00Z",
    "execution_deadline": "2030-04-02T09:06:00Z",
    "authority_refs": ["grant-household-example-1", "policy:household-review-before-change/v3"],
    "provenance": {"identity_source": "verified_context", "scope_source": "normalized_tool_contract"}
  },
  "decision": {
    "decision_id": "decision-household-example-1",
    "request_id": "request-household-example-1",
    "contract_version": "capability-policy/v0.1",
    "outcome": "allow",
    "evaluated_principal": "principal:example-reviewer",
    "evaluated_client": "client:example-household-assistant",
    "evaluated_resource": {"subject_ref": "household:example-home", "item_refs": ["item-101", "item-119"]},
    "evaluated_operation": "request_evidence",
    "action_digest": "sha256:synthetic-household-request-digest",
    "evaluated_refs": ["grant-household-example-1", "policy:household-review-before-change/v3"],
    "dimensions": {"defined": ["identity", "client", "scope", "policy", "record_state"], "evaluated": ["identity", "client", "scope", "policy", "record_state"], "passed": ["identity", "client", "scope", "policy", "record_state"], "failed": [], "unavailable": [], "stale": [], "not_applicable": ["human_approval"]},
    "decided_at": "2030-04-02T09:05:01Z",
    "valid_until": "2030-04-02T09:06:00Z",
    "replay_disposition": "single_use",
    "denial_class": {"state": "not_applicable", "reason": "allowed"},
    "evaluator": "policy-evaluator:example-v1",
    "provenance": {"evidence_refs": ["verification:synthetic-session-1", "grant-household-example-1", "policy:household-review-before-change/v3"]},
    "external_enforcement": ["integration read scope", "resource visibility policy"]
  },
  "scheduling_metadata": {
    "priority": 70,
    "assigned_worker": "agent:example-worker",
    "authority_effect": "none"
  }
}
```

The scheduler assignment does not grant `request_evidence`. The decision is valid only for the named principal, client, subject/items, operation, evidence versions, and short time window. No preference change or household mutation is permitted.

## 10. Synthetic Business example

```json
{
  "contract_version": "capability-policy/v0.1",
  "capability_definition": {
    "capability_id": "budget:propose_correction",
    "contract_version": "capability-policy/v0.1",
    "operations": ["propose_correction"],
    "resource_scope_grammar": "opaque business subject and proposal refs",
    "mandatory_conditions": ["proposal only", "no payment or canonical apply", "separate human review"],
    "assurance_floor": "verified_client_and_owner_session",
    "delegation_policy": {"allowed": true, "maximum_depth": 1, "redelegation_default": false},
    "risk_class": "staged_write",
    "approval_class": "separate_human_review",
    "required_decision_fields": ["principal", "client", "resource", "operation", "action_digest", "evidence_versions", "valid_until"],
    "required_receipt_fields": ["decision_id", "action_digest", "executor", "outcome"],
    "provenance": {"source_ref": "synthetic-capability-registry", "recorded_by": "example-policy-runtime"},
    "status": "candidate"
  },
  "parent_grant": {
    "grant_id": "grant-business-owner-1",
    "contract_version": "capability-policy/v0.1",
    "holder": "principal:example-team-owner",
    "client_binding": {"state": "not_applicable", "reason": "human_owner_grant"},
    "capability_id": "budget:propose_correction",
    "resource_scope": {"subject_ref": "business:example-team", "proposal_refs": ["proposal:budget-042"]},
    "operations": ["propose_correction"],
    "conditions": ["proposal only", "no payment or canonical apply"],
    "assurance_requirement": "verified_owner_session",
    "granted_by": "principal:example-business-policy-owner",
    "grant_basis": "policy:business-proposal/v2",
    "provenance": {"source_ref": "synthetic-owner-grant", "recorded_by": "example-policy-runtime"},
    "granted_at": "2030-04-01T12:00:00Z",
    "effective_at": "2030-04-02T00:00:00Z",
    "recorded_at": "2030-04-01T12:01:00Z",
    "not_before": "2030-04-02T00:00:00Z",
    "expires_at": "2030-04-30T00:00:00Z",
    "delegation": {"parent_grant": {"state": "not_applicable", "reason": "direct_grant"}, "chain_depth": 0, "redelegation_allowed": true, "maximum_depth": 1},
    "status": "active",
    "version": 1,
    "revocation_check": "required_at_execution"
  },
  "delegated_grant": {
    "grant_id": "grant-business-agent-1",
    "capability_id": "budget:propose_correction",
    "contract_version": "capability-policy/v0.1",
    "holder": "client:example-budget-agent",
    "client_binding": "client:example-budget-agent",
    "resource_scope": {"subject_ref": "business:example-team", "proposal_refs": ["proposal:budget-042"]},
    "operations": ["propose_correction"],
    "conditions": ["proposal only", "human review required", "no payment or canonical apply"],
    "assurance_requirement": "verified_client_and_owner_session",
    "granted_by": "principal:example-team-owner",
    "grant_basis": "grant-business-owner-1",
    "provenance": {"source_ref": "synthetic-delegation-record", "recorded_by": "example-policy-runtime"},
    "granted_at": "2030-04-02T08:50:00Z",
    "effective_at": "2030-04-02T09:00:00Z",
    "recorded_at": "2030-04-02T08:51:00Z",
    "not_before": "2030-04-02T09:00:00Z",
    "expires_at": "2030-04-02T17:00:00Z",
    "delegation": {"parent_grant": "grant-business-owner-1", "chain_depth": 1, "redelegation_allowed": false, "attenuation_verified": true},
    "status": "active",
    "version": 1,
    "revocation_check": "required_at_execution"
  },
  "policy_set": {
    "policy_set_id": "policy:business-proposal",
    "version": 2,
    "status": "active",
    "provenance": {"source_ref": "synthetic-business-policy", "recorded_by": "example-policy-runtime"},
    "effective_at": "2030-04-02T00:00:00Z",
    "recorded_at": "2030-04-01T11:00:00Z",
    "issuer": "principal:example-business-policy-owner",
    "issuer_scope": {"subject_ref": "business:example-team"},
    "selectors": {"capability_id": "budget:propose_correction", "risk_class": "staged_write"},
    "rules": {"allow": ["propose_correction"], "deny": ["approve_proposal", "apply_canonical_change", "approve_payment", "administer_grants"], "human_review_required": true},
    "precedence": "explicit_deny_and_unavailable_required_evidence_win",
    "revocation_freshness": "check_at_execution",
    "external_enforcement": ["named User MCP proposal tool", "database RLS", "proposal-state constraint"],
    "supersedes": {"state": "not_applicable", "reason": "first_version_in_example"}
  },
  "request": {
    "request_id": "request-business-example-1",
    "principal_ref": "principal:example-team-owner",
    "client_ref": "client:example-budget-agent",
    "runtime_ref": "runtime:example-business-worker",
    "credential_verification_ref": "verification:synthetic-business-session-1",
    "operation": "propose_correction",
    "resource_scope": {"subject_ref": "business:example-team", "proposal_refs": ["proposal:budget-042"]},
    "action_digest": "sha256:synthetic-proposal-digest",
    "record_state_refs": ["proposal:budget-042:draft"],
    "assurance_refs": ["verification:synthetic-business-session-1"],
    "requested_at": "2030-04-02T09:10:00Z",
    "execution_deadline": "2030-04-02T09:11:00Z",
    "authority_refs": ["grant-business-owner-1", "grant-business-agent-1", "policy:business-proposal/v2"],
    "provenance": {"identity_source": "verified_context", "scope_source": "normalized_tool_contract"}
  },
  "decision": {
    "decision_id": "decision-business-example-1",
    "request_id": "request-business-example-1",
    "contract_version": "capability-policy/v0.1",
    "outcome": "allow",
    "evaluated_principal": "principal:example-team-owner",
    "evaluated_client": "client:example-budget-agent",
    "evaluated_resource": {"subject_ref": "business:example-team", "proposal_refs": ["proposal:budget-042"]},
    "evaluated_operation": "propose_correction",
    "action_digest": "sha256:synthetic-proposal-digest",
    "evaluated_refs": ["grant-business-owner-1", "grant-business-agent-1", "policy:business-proposal/v2"],
    "dimensions": {"defined": ["identity", "client", "scope", "delegation", "policy", "record_state", "separation"], "evaluated": ["identity", "client", "scope", "delegation", "policy", "record_state", "separation"], "passed": ["identity", "client", "scope", "delegation", "policy", "record_state", "separation"], "failed": [], "unavailable": [], "stale": [], "not_applicable": ["execution_approval"]},
    "decided_at": "2030-04-02T09:10:01Z",
    "valid_until": "2030-04-02T09:11:00Z",
    "replay_disposition": "single_use",
    "denial_class": {"state": "not_applicable", "reason": "allowed"},
    "evaluator": "policy-evaluator:example-v1",
    "provenance": {"evidence_refs": ["verification:synthetic-business-session-1", "grant-business-owner-1", "grant-business-agent-1", "policy:business-proposal/v2"]},
    "external_enforcement": ["named User MCP proposal tool", "database RLS", "proposal-state constraint"]
  },
  "explicitly_absent_authority": ["approve_proposal", "apply_canonical_change", "approve_payment", "administer_grants"]
}
```

The agent may propose one exact correction. It cannot approve, apply, pay, administer grants, or re-delegate. A later approval must bind the exact proposal digest and a trusted worker must still pass database and integration enforcement.

## 11. Compatibility and fail-closed behavior

A v0.1 producer MUST emit the exact contract version. Consumers MUST preserve unknown extension members or report them unsupported and MUST NOT interpret an extension as authority.

Consumers MUST deny or return `indeterminate` for:

- missing required fields or unsupported required contract versions;
- caller-supplied identity or authority fields where trusted derivation is required;
- unknown, unavailable, conflicted, expired, suspended, revoked, or stale-required authority;
- invalid or widening delegation;
- missing current revocation evidence where policy requires it;
- token scope without a matching application grant;
- capability grant without verified principal/client context;
- approval not bound to the exact action and policy version;
- action, resource, or record state outside the evaluated scope;
- scheduler metadata presented as authority;
- missing downstream enforcement; or
- any operation not explicitly allowed by the runtime/tool contract.

Denial responses MUST NOT reveal whether a forbidden resource exists unless policy explicitly permits that disclosure.

## 12. Deferred conformance and security profile

v0.1 defines semantic objects and evaluation invariants only. It does not define or claim:

- canonical byte serialization or digest construction;
- signatures, MACs, key lifecycle, or credential issuance;
- OAuth token exchange or downstream bearer topology;
- database schemas, RLS implementations, policy languages, or integration APIs;
- replay-safe decision consumption or TOCTOU closure;
- distributed revocation propagation or cache invalidation;
- deterministic cross-implementation validators or fixture registries;
- cryptographic binding among provenance, grants, approvals, decisions, and receipts; or
- deployment conformance, certification, or security acceptance.

A separately versioned conformance/security profile MUST define those mechanisms before implementations rely on interoperability, authenticity, replay resistance, race-free application, or deterministic acceptance claims.

## 13. Minimum acceptance assertions

A future conformance profile should include positive and negative fixtures proving at least:

1. Scheduling assignment alone never authorizes an action.
2. Tool arguments cannot choose principal, issuer, audience, tenant, grant, policy, or credential origin.
3. Token scope alone never authorizes an application or database operation.
4. A valid grant with the wrong client, resource, operation, state, or assurance is denied.
5. Unknown or unavailable required authority returns fail-closed `indeterminate` or deny.
6. Explicit deny overrides allow.
7. A delegated grant cannot widen any parent dimension or outlive an ancestor.
8. Revoked, suspended, expired, or superseded required ancestors invalidate descendant use.
9. A reviewer cannot apply merely because it can review.
10. A proposer cannot self-approve where separation is required.
11. Editing an exact action invalidates approval and cached authorization.
12. Database RLS or downstream integration denial overrides an upstream allow decision.
13. A grant object cannot be used as a bearer credential.
14. Secrets never appear in contract objects, denials, logs, or receipts.
15. Historical grants, revocations, decisions, and receipts remain reconstructable after supersession.
16. Household and Business fixtures use the same contract without copied domain tables.
