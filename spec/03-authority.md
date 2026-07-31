# 03 — Authority and Attribution

_Status: Draft_

## Separate dimensions

The protocol distinguishes:

- **actor** — who or what is asserted to have acted;
- **runtime** — the execution environment;
- **credential or key** — authentication or signature evidence;
- **principal** — the authority root for the scope;
- **authorization** — why the action was permitted;
- **reviewer or acceptor** — who promoted or rejected a proposal.

A valid signature proves control of a key for a message. It does not, by itself, prove that the signer was authorized for the principal, custody zone, stream, event class, or time/sequence scope.

## Historical authority

Authorization, delegation, policy, credential, and assurance evidence used for historical verification MUST resolve to immutable snapshots, content-addressed artifacts, or append-only authority events. Mutable aliases or current role assignments MUST NOT establish authority at the earlier recording boundary.

## Key lifecycle

Concrete profiles must define key introduction, scope, epoch, rotation, expiry, revocation, recovery, and compromise. Historical signatures remain evidence, but verifier outcomes account for the key's authorization and compromise status for the relevant interval.

## Delegation

Delegation must bind delegator, delegate, principal, allowed operations, custody scope, start and end conditions, policy version, and revocation semantics. A delegate cannot broaden its own authority through a custody event.
