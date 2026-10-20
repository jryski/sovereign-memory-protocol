# Security policy

The Sovereign Memory Protocol is a specification, conformance material and a repository validator. In scope: specification text that would let a conforming implementation grant authority it should not, conformance cases that pass an unsafe implementation, validator flaws, and any committed secret or private data.

## Report a vulnerability privately

Use this repository's private vulnerability reporting form: open the
**Security** tab and choose **Report a vulnerability**. (This repository's
validator rejects owner identifiers in public text, so the form is named
rather than linked.)

If the form is unavailable, open a public issue that says only "private security contact requested", with no details, and a maintainer will arrange a private channel.

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

No production release of the Sovereign Memory Protocol is supported. `main` and tagged pre-releases
are maintained on a best-effort basis.

## Other components

Each repository in the program has its own private reporting form. If the issue
is in another component, report it there. The
[program map](https://github.com/WireSpeedComputing/sovereign-ai-os) lists
every component.
