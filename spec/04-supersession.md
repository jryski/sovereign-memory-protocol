# 04 — Corrections, Supersession, and Lifecycle

_Status: Draft_

## Append, do not rewrite

Corrections and lifecycle changes append new events. The original canonical event bytes and original temporal and authority assertions remain inspectable.

## Distinct relations

- **corrects** — supplies a replacement assertion while preserving the error or limitation being corrected;
- **supersedes** — declares precedence for a named scope and rationale;
- **conflicts with** — preserves incompatible claims without choosing a winner;
- **retires** — ends current operational use;
- **withdraws** — removes current sponsorship or acceptance;
- **accepts/rejects** — records authority disposition separately from evidence support.

Profiles must define allowed target classes, principal and custody-zone compatibility, cardinality, cycle rules, branch selection, and deterministic current-state projection.

## Time

A later recorded event may assert an earlier effective time. Recorded order, claimed effective order, and independently witnessed order remain separate. Backdating does not rewrite when the original event was recorded.

## Erasure interaction

Erasure changes payload availability, not historical lineage. Lifecycle edges must not require retaining erased subject content or payload-equivalent metadata.
