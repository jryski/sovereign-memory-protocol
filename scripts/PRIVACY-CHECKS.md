# Private identifier checks

The public checker contains generic sanitation and credential patterns, not an inventory of private deployments or people. Public repository links are not private identifiers merely because they identify the author or another project.

For an additional private check, keep a JSON array of nonempty literal strings outside the repository and review package. Pass its absolute path:

```text
python scripts/validate_repository.py --root . --json --private-identifiers /outside/package/private-identifiers.json
```

Matching is case-insensitive substring matching, not regular expressions. The optional scan covers all package files that can be read as UTF-8, including source code. An unreadable file fails that scan rather than silently passing. Reports include file locations, but never matching terms or policy contents. Missing, malformed, empty or in-package policy files fail validation. Never commit the private list, embed it in fixtures, or publish its contents in a review log.

Without this option, `private_identifier_scan` is `not_performed`. Public CI still checks package integrity, document consistency and generic sanitation. A passing public check is not evidence that private identifiers are absent. With a valid policy, `performed` means the scan ran; inspect overall status and errors for its outcome. A clean scan only covers the supplied literal strings and current package, not encoded variants, unknown sensitive content or Git history.

Removing an identifier from the current checker does not remove it from published history. History changes require a separate decision; this repair does not rewrite history.
