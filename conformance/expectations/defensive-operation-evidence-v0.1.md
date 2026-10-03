# Defensive-operation evidence expectations

_Status: informative synthetic case catalog; not passing coverage_
_Catalog label: defensive-operation-evidence-v0.1_
_Last updated: 2026-10-03_
_Related proposal: issue 15. Refs #15. Related to #15._

This file is an informative synthetic case catalog for the defensive-operation evidence profile proposed in issue 15. It illustrates honest outcomes for retrieval, provenance, qualification, and authorization evidence. It is not a filled deployment record. It is not passing coverage.

The catalog assigns no conformance level. It proposes no protocol version bump. Normative SMP text is unchanged. Nothing in this file amends `spec/`, promotes a profile, or certifies an implementation.

Protocol conformance and model task performance are separate. A model task score, including a small model's success rate, is an evaluation. It is not an SMP compliance certificate. A fluent answer can still fail one of these cases when coverage, provenance, qualification, or authorization evidence is missing or overstated. A weak answer can still sit on an honest evidence record. This catalog does not score model task performance.

## How to read a case

Each case below states the same six parts:

1. Setup.
2. Expected result.
3. Positive variant.
4. Negative variant.
5. Broken-control discriminator.
6. Evidence locator.

The labels `DOE-*` are local planning handles for this informative catalog. They are not v0.2 traceability identifiers, not machine-readable fixtures, and not executed results. Placing this file under `conformance/expectations/` does not create fixture bytes under `conformance/fixtures/`. An empty fixture directory remains empty. Absence of executed vectors stays visible; it is not reported here as a pass.

Implementations may use differing schemas when they preserve the concepts named in a case. A deployment self-report remains a declaration until a separate verifier records tests, skipped or unknown requirements, and verifier assurance. This catalog contains none of those records.

## Synthetic placeholders

Every identifier in this catalog is synthetic. `TBD` marks a value the catalog intentionally leaves unbound. Examples include `synth-src-001`, `synth-fact-001`, and `synth-ev-loc-001`. These tokens name no host, no person, and no deployment. Where a case needs a subject role for authority, the role is Primary Users.

No field is a captured production value. No locator is a live address.

## Evidence concepts illustrated

Issue 15 proposes the following distinctions. This catalog uses them as informative expectations only. Mapping them onto current schemas, and any later normative text, remains future review work.

- Source coverage separates the declared source or snapshot, the observed or queryable set, and the set actually queried. Reconciliation disposition, unknown scope, and excluded scope stay explicit. Completeness is scoped and time-bound. Connectivity is not a global boolean.
- Retrieval outcome distinguishes found, ambiguity or conflict, no match within the searched scope, incomplete coverage, unavailable or not evaluated, and invalid request.
- Provenance keeps the exact source and version, the fact-to-ruling relationship, supersession, and the difference between effective time and recorded or import time. A derived summary does not become authoritative by being derived.
- Qualification binds an operation, suite, configuration, verifier, and evidence, and states validity and limits. Competence, authenticated identity, authorization, availability, and source integrity are separate claims.
- A write or execution receipt, when one is in scope, names the candidate or version, independently checked authority, the exact operation, prior and result state where they apply, idempotency, and outcome. A caller label or a supplied subject id is not authentication.

## DOE-SRC-001 — Incomplete or unavailable sources

A known fact can sit in a registered predecessor that this evaluation did not query, or that was unavailable. That situation has no global absent answer. Separately, an accessible source set that is incomplete must not disclose an inaccessible source through hints or counts.

**Setup.** Source inventory `synth-inv-001` at time `TBD` registers three sources. `synth-src-001` is a predecessor that is registered and either unqueried or unavailable for this evaluation. `synth-fact-001` exists only in `synth-src-001`. `synth-src-002` is accessible and is the source actually queried. `synth-src-003` is registered and inaccessible; it is outside the accessible set. The question under test is whether `synth-fact-001` holds. Snapshot identifiers are `synth-snap-001` for the queried source and `TBD` for the predecessor.

**Expected result.** The retrieval outcome for `synth-fact-001` is incomplete coverage, or unavailable or not evaluated, for the predecessor that was not queried or was unavailable. The outcome is not a global absent answer and not "no match" for the whole inventory. Declared scope, queryable scope, and actually queried scope remain three different statements. Completeness names `synth-snap-001` and the evaluation time `TBD` only. The response built from the accessible set does not disclose `synth-src-003` by name, hint, ordering, or count. A public count of accessible or queried sources stays the same whether or not `synth-src-003` is present in the inaccessible remainder.

**Positive variant.** The declared searchable snapshot is exactly the set that was queried, the predecessor disposition is an explicit exclusion that does not name an inaccessible source, and `synth-src-002` contains no support for the question. The outcome may be no match within that searched snapshot. Coverage cites `synth-inv-001`, `synth-snap-001`, and the queried set `{synth-src-002}` only.

**Negative variant.** The runner reports that `synth-fact-001` is globally absent while `synth-src-001` still holds it and was unqueried or unavailable. A second failure of this case is any accessible-set answer that reveals `synth-src-003` through a hint or a count, including a count shaped like a remainder (`TBD` accessible out of a larger registered total).

**Broken-control discriminator.** Treat as broken any coverage control that labels the outcome "incomplete" and still emits a public source count, ordering, or hint that changes when `synth-src-003` is added or removed from the inaccessible set while `{synth-src-002}` stays fixed. Also treat as broken a control that maps "queried sources returned nothing" onto a global absent code while inventory disposition for `synth-src-001` is `unqueried` or `unavailable`. Accurate prose about `synth-src-002` does not repair either break.

**Evidence locator.** `synth-ev-loc-001` (`TBD`). The locator refers to the coverage record for `synth-inv-001`: declared inventory, queried-set commitment `TBD`, disposition of `synth-src-001`, and a disclosure check that `synth-src-003` is absent from the output bytes.

## DOE-LIN-001 — Conflicts and supersession

An older narrative can conflict with an effective ruling. Lineage and currentness both remain. Similarity does not choose the current claim. An expired or superseded record and an unresolved conflict are different honest outcomes.

**Setup.** `synth-rec-010` is an older narrative asserting claim `synth-claim-old` for subject scope `synth-scope-001`. `synth-rul-011` is an effective ruling for the same scope asserting `synth-claim-new`. The ruling's effective time and its recorded or import time are both `TBD` and are not the same instant. Lexical similarity between the question and `synth-rec-010` is higher than similarity with `synth-rul-011`. Independently, `synth-rec-012` is expired or superseded for scope `synth-scope-001` with successor reference `TBD`. `synth-rec-013` and `synth-rec-014` are an unresolved conflict in scope `synth-scope-002` with no effective ruling. Primary Users are the subject role for both scopes.

**Expected result.** Currentness follows `synth-rul-011` for `synth-scope-001`. `synth-rec-010` stays on the lineage as historical narrative and is not selected as the current assertion because it is nearer to the question text. The fact-to-ruling relationship names both records and their exact source versions (`TBD`). A derived summary of the narrative does not become the authoritative current claim. The outcome for `synth-rec-012` is expired or superseded and names its successor. The outcome for `synth-rec-013` with `synth-rec-014` is unresolved conflict: both claims remain, and no winner is chosen. Those two outcomes use distinct result classes.

**Positive variant.** A current-state question on `synth-scope-001` returns `synth-rul-011`, preserves the lineage edge from `synth-rec-010`, and records effective time separately from recorded or import time. A question on `synth-scope-002` returns unresolved conflict for `synth-rec-013` and `synth-rec-014`. A question that lands on `synth-rec-012` returns superseded or expired with successor `TBD`, and does not reuse the conflict result class.

**Negative variant.** The runner returns `synth-rec-010` as current because similarity favors it, or it drops the lineage edge. A second failure is collapsing `synth-rec-012` and the unresolved pair into one outcome, so a superseded record and an unresolved conflict look the same.

**Broken-control discriminator.** Treat as broken a ranker presented as a currentness control when its selected record changes solely because similarity to the question changes, while `synth-rul-011` remains the effective ruling. Treat as broken a single result code, illustrated here as `synth-code-not-current`, that is emitted both for superseded `synth-rec-012` and for the unresolved pair. Preserving the older narrative text in storage does not repair a control that hides currentness or merges the two outcomes.

**Evidence locator.** `synth-ev-loc-002` (`TBD`). The locator refers to the lineage record: edge between `synth-rec-010` and `synth-rul-011`, effective interval `TBD`, supersession of `synth-rec-012`, and conflict disposition `unresolved` for `synth-rec-013` and `synth-rec-014`.

## DOE-BUD-001 — Bounded evidence retention

A small output budget either retains the required provenance and coverage or returns a bounded failure. Success that exceeds the budget, and success that silently strips evidence, are both outside the expected result.

**Setup.** The output ceiling is `synth-budget-001`, a byte or token bound whose concrete size is `TBD` and is smaller than the full evidence bundle for this question. Required provenance is source `synth-src-002` at version `TBD` and snapshot `synth-snap-001`. Required coverage is the declared set, the queried set, and the excluded or unknown disposition. The question itself is `synth-q-001`. The bundle that includes full payload text does not fit in `synth-budget-001`.

**Expected result.** The operation returns either a bounded record that still carries the required provenance and coverage fields and fits in `synth-budget-001`, or a bounded failure that names the ceiling and the missing evidence. The failure stays inside the resource limit. A success result larger than `synth-budget-001` is outside this case. A success result that fits only because provenance or coverage was removed without a stated omission is outside this case. Observed size and the ceiling both appear in the evidence record.

**Positive variant.** The runner returns a compact receipt within `synth-budget-001` that still names `synth-src-002`, version `TBD`, `synth-snap-001`, the queried set, and the disposition of anything excluded. Alternatively, the runner returns a bounded failure, keeps the success flag unset, and points at `synth-ev-loc-003` for the unsent remainder.

**Negative variant.** The runner returns success with an output larger than `synth-budget-001`. Or it returns success inside the ceiling after dropping source, version, snapshot, or coverage, with no omission flag.

**Broken-control discriminator.** Treat as broken a truncator that preserves an answer sentence, deletes the provenance or coverage block, and still sets the outcome to found or success. The discriminator inputs are the ceiling `synth-budget-001`, the measured output size, and the presence of the required fields. A correct sentence about `synth-q-001` does not repair a missing field or an oversized success.

**Evidence locator.** `synth-ev-loc-003` (`TBD`). The locator refers to the budget record: ceiling, observed size, retained provenance fields, and either the compact receipt or the bounded-failure outcome.

## DOE-SUB-001 — Unverified or substituted subjects

An unverified agent introduction, a substituted subject, and a self-signed PASS cannot assert trusted qualification.

**Setup.** Caller label `synth-agent-001` introduces itself and supplies subject id `synth-subj-claimed`. No independent verifier has checked that introduction. Enrolled subject `synth-subj-001` has a separate qualification binding. Substituted subject `synth-subj-002` is presented in its place. Artifact `synth-sig-001` is a self-signed PASS for suite `synth-suite-001`, configuration `synth-cfg-001`, and operation `synth-op-001`. The signer and the claimant are the same synthetic party. Competence, authenticated identity, authorization, availability, and source integrity are recorded as separate claims, each initially `TBD`. The subject role, where a role is required, is Primary Users. Caller labels and supplied subject ids are not authentication.

**Expected result.** Trusted qualification is not asserted from the introduction, from the substitution, or from `synth-sig-001`. Qualification state for those three inputs is unverified or denied. Cryptographic self-signature of PASS is a declaration by the claimant. It is not verifier evidence. `synth-subj-002` does not inherit the qualification of `synth-subj-001`. Identity, authorization, availability, and source integrity remain unset unless their own evidence is present. This case does not grade whether a model described the subjects correctly.

**Positive variant.** Independent verifier `synth-verifier-001` binds operation `synth-op-001`, suite `synth-suite-001`, configuration `synth-cfg-001`, subject `synth-subj-001`, and evidence `synth-ev-004`, with validity window `TBD`. That binding supports a qualification claim only for that subject and that configuration. The unverified introduction, the substituted subject, and `synth-sig-001` stay outside that claim.

**Negative variant.** The runner marks trusted qualification because `synth-agent-001` supplied a PASS bit, because `synth-subj-002` carried the display label of `synth-subj-001`, or because `synth-sig-001` verified under the claimant's own key.

**Broken-control discriminator.** Treat as broken a control that copies a caller-supplied PASS into the qualification field when the suite name equals `synth-suite-001`. Treat as broken a control that accepts subject substitution when display labels match and the bound subject id does not. A passing signature check on `synth-sig-001` is the broken control's own output; the discriminator still requires qualification assurance to remain untrusted for that artifact.

**Evidence locator.** `synth-ev-loc-004` (`TBD`). The locator refers to the binding record: verifier, suite, configuration `synth-cfg-001`, subject id, validity window `TBD`, and the disposition of `synth-sig-001` as unverified self-signature.

## DOE-AUTHZ-001 — Revoked authorization

Qualification may be valid. Authorization can still be revoked. Execution is then denied.

**Setup.** Qualification `synth-qual-001` is inside its validity window `TBD` for operation `synth-op-001`, suite `synth-suite-001`, and configuration `synth-cfg-001`. Authorization grant `synth-authz-001` for Primary Users is revoked. Revocation time is `TBD`, and the execution request is after that time. The qualification verifier and the authorization decision are different records. Decision id is `synth-dec-001`.

**Expected result.** Execution of `synth-op-001` is denied. Qualification validity and authorization status stay separate claims. `synth-qual-001` remains valid for the qualification claim and is not rewritten to explain the denial. The denial is not reported as a qualification failure. A valid qualification is not permission to execute. Historical qualification bytes stay inspectable. Any execution receipt for this request, if one is written, records outcome denied, decision `synth-dec-001`, and status revoked. The caller label is not the authorization check.

**Positive variant.** Before revocation, the same qualification together with an active authorization decision permits the operation and records a receipt that cites independently checked authority. After revocation, a fresh request is denied, `synth-qual-001` is unchanged, and the receipt outcome is denied.

**Negative variant.** Execution proceeds because `synth-qual-001` is valid and the revoked grant is ignored. Or the runner rewrites `synth-qual-001` to invalid so the denial appears to be a qualification failure.

**Broken-control discriminator.** Treat as broken a gate that allows execution when qualification is unexpired and does not read `synth-dec-001`. The discriminator fixture keeps `synth-qual-001` valid and sets `synth-authz-001` to revoked. Allowed execution on that fixture means the control is broken. Combining qualification and authorization with a logical or, so that either claim alone permits execution, is the same break.

**Evidence locator.** `synth-ev-loc-005` (`TBD`). The locator refers to decision `synth-dec-001` with status revoked, qualification `synth-qual-001` still valid, and the execution outcome denied.

## DOE-CFG-001 — Configuration changes

A change to the bound tool, model, or runtime configuration invalidates the relevant qualification evidence.

**Setup.** Qualification `synth-qual-002` binds tool `synth-tool-001`, model `synth-model-001`, and runtime `synth-runtime-001` under configuration `synth-cfg-001`. Verifier is `synth-verifier-001`. Suite is `synth-suite-001`. Operation is `synth-op-001`. One of the three bound elements then changes, producing configuration `synth-cfg-002`. The catalog treats each of the three changes as sufficient on its own: tool only, model only, or runtime only. The operation name and suite name stay the same. Authorization, if present, is a separate record and is not a substitute for the configuration binding. Concrete configuration digests are `TBD`.

**Expected result.** `synth-qual-002` is not valid for `synth-cfg-002`. The relevant qualification evidence is invalidated for the new configuration, or it is not applicable, until a new binding exists. The old evidence remains historical evidence for `synth-cfg-001` only. It is not reused silently. Model task performance on either configuration is out of scope for this case. A model that answers well under `synth-cfg-002` does not keep `synth-qual-002` valid.

**Positive variant.** New qualification `synth-qual-003` binds `synth-cfg-002` through `synth-verifier-001`, naming the changed tool, model, or runtime element. Further use of `synth-op-001` under `synth-cfg-002` cites `synth-qual-003`. `synth-qual-002` remains addressable as history for `synth-cfg-001`. Authorization is checked on its own record.

**Negative variant.** The runner reports `synth-qual-002` still valid after the change to `synth-cfg-002`, or it copies the old binding forward because the suite name and operation name matched.

**Broken-control discriminator.** Treat as broken a comparator that checks suite `synth-suite-001` and ignores the configuration digest. The discriminator changes exactly one of tool, model, or runtime, keeps the suite id fixed, and expects the qualification claim for `synth-cfg-002` to fail closed. A match on suite name alone does not repair that control.

**Evidence locator.** `synth-ev-loc-006` (`TBD`). The locator refers to the prior binding digest `TBD`, the observed configuration digest `TBD`, and the mismatched element (`tool`, `model`, or `runtime`).

## DOE-REC-001 — Bounded recovery or adapter failure

A weak lexical query and an adapter failure have bounded permitted recovery. Recovery does not invent absence.

**Setup.** Query `synth-q-001` is lexically weak: its tokens are ambiguous and its normalization is `TBD`. Source `synth-src-002` at snapshot `synth-snap-001` holds `synth-fact-002` for this question when the query is well formed. Adapter `synth-adp-001` fails while reading `synth-src-002`. Failure receipt is `synth-err-001`. Permitted recovery is a bounded reformulation or a bounded retry of the same authorized source. The attempt ceiling is `TBD`. Recovery does not add a source, does not drop `synth-src-002` from coverage, and does not continue past the ceiling.

**Expected result.** The weak query does not become "no match" and does not become a global absent answer. The adapter failure is unavailable or not evaluated for `synth-src-002`, which is a different outcome from no match within a scope that was actually searched. Recovery stays inside the declared attempt ceiling and names each attempt. If recovery completes inside the ceiling against the same source, the result is the real retrieval outcome and the failed attempt remains on the record. If recovery stops at the ceiling, the result is a bounded failure or incomplete coverage. Neither path invents absence of `synth-fact-002`.

**Positive variant.** One declared retry or one declared clarification queries only `synth-src-002`, stays within the attempt ceiling `TBD`, and returns the outcome supported by `synth-snap-001`, with `synth-err-001` retained. Or recovery stops at the ceiling, reports adapter failure, and leaves coverage of `synth-src-002` as unavailable or not evaluated.

**Negative variant.** After the weak parse or after `synth-err-001`, the runner reports that `synth-fact-002` is absent. Or recovery queries a source outside the declared set, exceeds the attempt ceiling, and still reports success.

**Broken-control discriminator.** Treat as broken a fallback that maps both an empty lexical parse and `synth-err-001` onto one absent code. The discriminator injects the adapter failure while `synth-fact-002` remains in `synth-src-002`. An absent answer on that injection means the control is broken. Also treat as broken an unbounded retry that eventually omits `synth-src-002` from coverage and then reports no match. Recording the adapter error string in a log, while the caller-visible outcome is still absence, does not repair the control.

**Evidence locator.** `synth-ev-loc-007` (`TBD`). The locator refers to adapter receipt `synth-err-001`, the attempt count, the recovery ceiling `TBD`, the queried source `synth-src-002`, and the final retrieval outcome.

## Claim limits

This catalog is informative. Passing coverage is not claimed, and no case above has been executed. No conformance level is stated. No protocol version is advanced. Normative SMP is unchanged, including authority, supersession, conformance, and custody-chain text.

The seven handles are `DOE-SRC-001`, `DOE-LIN-001`, `DOE-BUD-001`, `DOE-SUB-001`, `DOE-AUTHZ-001`, `DOE-CFG-001`, and `DOE-REC-001`. They document synthetic expectations for review of the issue 15 proposal. They are not a certification suite and not a deployment record.

Related drafts, which this catalog does not amend, include [authority](../../spec/03-authority.md), [supersession](../../spec/04-supersession.md), and [conformance](../../spec/06-conformance.md). Those drafts gain no requirement identifier from this catalog.
