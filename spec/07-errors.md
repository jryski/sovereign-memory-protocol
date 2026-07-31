# 07 — Errors and Precedence

_Status: Draft registry shape_

Stable machine-readable errors are part of interoperability and security. Implementations may add diagnostic detail but must not change the normative meaning or hide a higher-priority integrity failure.

## Proposed classes

| Class | Meaning |
|---|---|
| `UNSUPPORTED_PROFILE` | Required profile or algorithm is not supported |
| `UNKNOWN_CRITICAL_EXTENSION` | A critical extension cannot be interpreted |
| `NONCANONICAL_ENCODING` | Input does not match the required canonical bytes |
| `COMMITMENT_MISMATCH` | Recomputed commitment differs |
| `STREAM_GAP` | Required predecessor or sequence is absent |
| `STREAM_FORK` | Competing successors or heads exist |
| `CHECKPOINT_DISCONTINUITY` | Checkpoint ancestry or consistency fails |
| `ROLLBACK_SUSPECTED` | Presented history is older than retained freshness evidence |
| `AUTHORITY_UNVERIFIABLE` | Historical authority cannot be established |
| `REPLAY_CONFLICT` | An operation identifier was reused with different content |
| `TRANSFER_INCOMPLETE` | Bilateral transfer has not finalized |
| `ERASURE_PARTIAL` | Required erasure scope remains incomplete |
| `RESTORE_QUARANTINED` | Restore has not passed freshness and lifecycle reconciliation |
| `RESOURCE_LIMIT_EXCEEDED` | Normative verifier ceiling was exceeded |

## Precedence

At minimum:

1. resource and parser safety;
2. profile and critical-extension support;
3. canonical bytes and commitment integrity;
4. chain, checkpoint, and rollback integrity;
5. authority and key status;
6. lifecycle, transfer, erasure, and semantic interpretation.

A lower-priority semantic result must not mask a higher-priority failure.
