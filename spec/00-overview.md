# 00 — Overview

_Status: Draft_

## Purpose

SMP defines portable custody semantics for evidence and memory-derived state. It enables an independent verifier to evaluate what was recorded, how it was derived, who was authorized, what changed later, what was transferred or erased, and whether a restored or exported history is consistent with named evidence.

## Normative scope

A complete future profile is expected to define:

- logical custody envelopes and erasable payload compartments;
- source evidence and derivation lineage;
- authority-at-write and review dispositions;
- correction, conflict, supersession, retirement, withdrawal, and erasure;
- export, transfer, verification, and restore receipts;
- canonical bytes, algorithms, extension behavior, and resource limits;
- implementation-neutral fixtures and deterministic outcomes.

## Explicit claim limits

SMP verification can authenticate presented evidence and history under a declared profile. It does not automatically prove:

- substantive truth;
- events never submitted or admitted;
- complete disclosure without an authenticated source inventory;
- latest state without independently retained freshness evidence;
- availability of withheld payloads or witnesses;
- erasure of copies outside the evaluated custody scope.

## Profiles

The base logical model remains independent of storage and cryptographic providers. Profiles may define concrete encodings, algorithms, anchoring, packaging, or deployment assurances, but must declare trust assumptions, privacy leakage, dependencies, failure behavior, and provider-exit evidence.
