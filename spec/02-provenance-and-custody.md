# 02 — Provenance and Custody

_Status: Draft_

## Evidence before derived claims

A derived claim MUST identify the source evidence or explicitly state that no qualifying evidence is available. A structurally valid evidence reference does not make the claim true, accepted, current, or complete.

## Epistemic states

Implementations must not collapse:

- source evidence;
- system observation;
- agent inference;
- proposal;
- accepted assertion;
- rejected assertion;
- conflict;
- correction;
- superseded, retired, or withdrawn state.

## Source accounting

Completeness is always relative to a boundary. A completeness claim requires:

1. an authenticated frozen source inventory or cursor boundary;
2. a manifest binding every in-scope item to one or more explicit dispositions;
3. reconciliation with zero unexplained in-scope items;
4. a statement of unavailable sources and unobserved intervals.

A valid chain of disclosed events does not prove that undisclosed streams or pre-admission source items do not exist.

## Custody receipt

A receipt should bind the profile, scope, artifact or manifest commitment, producing and receiving parties where applicable, recorded boundary, operation outcome, known omissions, and verifier evidence. Receipts must minimize subject data and must not embed payload-equivalent free text.
