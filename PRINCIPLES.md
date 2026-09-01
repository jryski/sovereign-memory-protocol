# Principles and Non-Goals

_Status: Draft design constraints_

## Principles

1. **Custody, not a universal format.** Existing and future memory formats remain adapter surfaces.
2. **Evidence before promotion.** Derived claims remain proposals until authorized review promotes them.
3. **Custody is not truth.** Matching hashes authenticate bytes and lineage under stated assumptions; they do not establish external truth.
4. **History changes by append.** Corrections and lifecycle transitions preserve prior recorded claims.
5. **Erasure is distinct from mutation.** Write-once custody fields do not require permanent retention of subject payloads.
6. **Authority is multidimensional.** Actor, runtime, credential, principal, authorization, and reviewer are separate claims.
7. **Time is multidimensional.** Observed, effective, recorded, verified, and anchored time are not interchangeable.
8. **Projections are rebuildable.** Search, vector, graph, cache, ranking, summary, and context state never become authority merely through usefulness.
9. **Conformance is evidence.** Claims identify exact profile, version, tested surfaces, fixtures, and unavailable coverage.
10. **Portability includes failure.** Exports and transfers declare lossiness, omissions, unknowns, stale evidence, and unverifiable states.
11. **Providers are replaceable.** Storage engines, models, runtimes, signers, witnesses, and ledgers are profiles or implementations, not protocol owners.
12. **Privacy is structural.** Custody receipts minimize metadata and do not preserve payload-equivalent or guessable subject information after authorized erasure.

## Non-goals

SMP does not, by itself:

- decide what an AI system should remember;
- guarantee recall, ranking, or answer quality;
- prove a source statement true;
- prove events omitted before admission never existed;
- guarantee that unavailable external copies were erased;
- require one database, cloud, ledger, or signature suite;
- replace legal, safety, retention, or authorization policy;
- make a stale but internally valid restore current;
- turn a valid signer into a semantically authorized actor;
- define a consumer application or user interface.

## Claim discipline

Implementations must distinguish at least:

- routine mutation prevention;
- authenticated local history;
- checkpoint signature coverage;
- independently witnessed history;
- currentness or staleness;
- inventory/completeness scope;
- payload and erasure state;
- offline portability;
- unavailable or untested coverage.
