# Contributing to SMP

SMP is a public protocol draft. Help make its meaning precise and independently testable without tying it to one database, model or deployment.

## Start with a bounded question

- Name the document, section, version and exact revision.
- Explain the ambiguity or failure using a synthetic counterexample.
- Distinguish a proposed requirement from an implementation choice.
- State the expected outcome and what evidence could establish it.

Use issues for design questions and small pull requests for repairs. Inspect existing issues and pull requests before opening a competing implementation. Prefer one editor and independent reviewers for each candidate.

## Keep private information out

Use synthetic identities, records and examples. Do not submit credentials, personal data, internal coordination logs or private deployment addresses. Do not put live vulnerability details in a public issue. Use private vulnerability reporting if enabled, or obtain a private reporting route from a maintainer first.

## Validate a change

From the repository root, with Python 3:

```text
python -m unittest discover -s tests -v
python scripts/validate_repository.py --root . --json
```

Refresh `REVIEW-MANIFEST.sha256` after changes using sorted repository-relative paths and SHA-256 of exact file bytes. Exclude the manifest itself, Git internals and validator-excluded caches. Include new files. Do not adjust expected results merely to make a check pass.

In the pull request, record the base and candidate commit, changed scope, manifest digest, commands, results and untested areas. Keep exact commit and tree coordinates in the review record, not inside a self-referential manifest.

## What a passing check means

Repository validation checks package integrity and selected document consistency. It does not execute the protocol case catalog or prove implementation conformance. Planned identifiers, documented scenarios and evaluated outcomes are different evidence.

Reviews apply to exact artifacts and stated coverage. A merge, public repository, empty findings list or predecessor review does not automatically approve new semantics or a release. Protocol promotion and deployment acceptance remain separate decisions.

## Licensing

The specification, conformance material and documentation are licensed under Creative Commons Attribution 4.0 International. See [LICENSE](LICENSE) and [COPYRIGHT](COPYRIGHT). Executable tooling in the README scope map is licensed under the Apache License, Version 2.0. See [LICENSE-CODE](LICENSE-CODE).

Contributions are accepted under the Developer Certificate of Origin. See [DCO.md](DCO.md). Do not copy material you lack permission to contribute, and do not silently replace these licenses or assume broader reuse rights.
