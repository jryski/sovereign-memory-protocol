# Security policy

This repository publishes a protocol draft and its review-package tooling. Security-relevant reports include ambiguities that would let a conforming implementation leak data or misattribute authority, defects in the validator, and any committed secret or private data.

## Report a vulnerability privately

Use this repository's private vulnerability reporting form:
<https://github.com/jryski/sovereign-memory-protocol/security/advisories/new>

If the form is unavailable, email **jryski@gmail.com** instead.

Do not put exploit details, credentials, tokens, private hostnames or real
personal, household, business or customer records in a public issue, pull
request, discussion or CI log. Use synthetic examples and redacted output.

Where you can, include:

- the affected commit, tag or file;
- preconditions and the trust boundary involved;
- a minimal reproduction using synthetic data;
- demonstrated and likely impact;
- whether secrets or personal data were exposed; and
- a proposed mitigation, if known.

## Supported versions

No protocol release exists yet. The draft on `main` and its tooling
are maintained on a best-effort basis.

## Other components

Each repository in the program has its own private reporting form. If the issue
is in another component, report it there. The
[program map](https://github.com/WireSpeedComputing/sovereign-ai-os) lists
every component.

