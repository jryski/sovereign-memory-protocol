import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_repository.py"


class ReviewPackageValidatorTests(unittest.TestCase):
    def run_validator(self, root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root), "--json", *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def write_manifest(self, root: pathlib.Path, paths: list[pathlib.Path]) -> None:
        entries = []
        for path in sorted(paths):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries.append(f"{digest}  {path.relative_to(root).as_posix()}")
        (root / "REVIEW-MANIFEST.sha256").write_text("\n".join(entries) + "\n")

    def test_public_project_links_do_not_require_private_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("[Program](https://github.com/jryski/sovereign-memory-core)\n")
            self.write_manifest(root, [readme])
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["private_identifier_scan"], "not_performed")

    def test_external_private_policy_scans_source_without_echoing_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = pathlib.Path(tmp)
            root = parent / "package"
            root.mkdir()
            source = root / "example.py"
            source.write_text("# SYNTHETIC-PRIVATE-ROUTE\n")
            policy = parent / "private.json"
            policy.write_text(json.dumps(["synthetic-private-route"]))
            self.write_manifest(root, [source])
            result = self.run_validator(root, "--private-identifiers", str(policy))
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertEqual(report["private_identifier_scan"], "performed")
            self.assertIn({"code": "SANITATION_PRIVATE_IDENTIFIER", "path": "example.py"}, report["errors"])
            self.assertNotIn("synthetic-private-route", result.stdout.lower())
            self.assertNotIn(str(policy), result.stdout)

    def test_invalid_or_missing_private_policy_fails_closed(self) -> None:
        for payload in (None, "{", "[]", '[""]', '["  "]', '[3]', '{}'):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as tmp:
                parent = pathlib.Path(tmp)
                root = parent / "package"
                root.mkdir()
                self.write_manifest(root, [])
                policy = parent / "private.json"
                if payload is not None:
                    policy.write_text(payload)
                result = self.run_validator(root, "--private-identifiers", str(policy))
                self.assertEqual(result.returncode, 1)
                report = json.loads(result.stdout)
                self.assertEqual(report["private_identifier_scan"], "invalid")
                self.assertIn({"code": "PRIVATE_POLICY_INVALID"}, report["errors"])

    def test_private_policy_cannot_be_packaged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            policy = root / "private.json"
            policy.write_text('["synthetic-private-route"]')
            self.write_manifest(root, [policy])
            result = self.run_validator(root, "--private-identifiers", str(policy))
            self.assertEqual(result.returncode, 1)
            self.assertIn({"code": "PRIVATE_POLICY_INSIDE_PACKAGE"}, json.loads(result.stdout)["errors"])

    def test_private_policy_uses_literals_not_regular_expressions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = pathlib.Path(tmp)
            root = parent / "package"
            root.mkdir()
            source = root / "example.py"
            source.write_text("# ordinary synthetic example\n")
            policy = parent / "private.json"
            policy.write_text('[".*"]')
            self.write_manifest(root, [source])
            result = self.run_validator(root, "--private-identifiers", str(policy))
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["private_identifier_scan"], "performed")

    def test_private_scan_does_not_silently_skip_non_utf8(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = pathlib.Path(tmp)
            root = parent / "package"
            root.mkdir()
            source = root / "example.bin"
            source.write_bytes(b"\xff")
            policy = parent / "private.json"
            policy.write_text('["synthetic-private-route"]')
            self.write_manifest(root, [source])
            result = self.run_validator(root, "--private-identifiers", str(policy))
            self.assertEqual(result.returncode, 1)
            self.assertIn({"code": "PRIVATE_SCAN_UNREADABLE", "path": "example.bin"}, json.loads(result.stdout)["errors"])

    def write_v02_package(
        self,
        root: pathlib.Path,
        *,
        positive_result: str = "pass `report_contract`",
        negative_result: str = "`TEST_FAILURE`",
    ) -> None:
        spec = root / "spec" / "08-immutability-and-chain-of-custody-v0.2.md"
        spec.parent.mkdir()
        spec.write_text("# Candidate\n\n- **CST-TEST-001:** A verifier MUST fail closed.\n")
        dimensions = root / "spec" / "05-verification.md"
        dimensions.write_text(
            "# Verification\n\n## Authoritative verification-dimension registry\n\n"
            "| Dimension | Meaning |\n|---|---|\n"
            "| `report_contract` | dimension |\n\n## Next\n"
        )
        registry = root / "spec" / "07-errors.md"
        registry.write_text(
            "# Errors\n\n| Code | Meaning |\n|---|---|\n"
            "| `TEST_FAILURE` | test |\n| `OTHER_FAILURE` | other |\n"
        )
        trace = root / "conformance" / "expectations" / "immutability-v0.2-traceability.md"
        trace.parent.mkdir(parents=True)
        trace.write_text(
            "# Traceability\n\n| Requirement family | Authoritative dimension |\n|---|---|\n"
            "| `test_family` | `report_contract` |\n\n"
            "| Requirement | Family | Code | Positive | Negative | Summary |\n"
            "|---|---|---|---|---|---|\n"
            "| `CST-TEST-001` | `test_family` | `TEST_FAILURE` | `V02-TEST-001-P` | `V02-TEST-001-N` | test |\n"
        )
        cases = root / "conformance" / "expectations" / "immutability-v0.2-cases.md"
        cases.write_text(
            "# Cases\n\n| Case | Input | Expected primary result |\n|---|---|---|\n"
            f"| `V02-TEST-001-P` | good | {positive_result} |\n"
            f"| `V02-TEST-001-N` | bad | {negative_result} |\n"
        )
        self.write_manifest(root, [cases, trace, dimensions, registry, spec])

    def test_manifest_closed_package_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Review package\n\n[Status](STATUS.md)\n")
            status = root / "STATUS.md"
            status.write_text("# Status\n\nDraft review package.\n")
            self.write_manifest(root, [readme, status])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["manifest_entries"], 2)
            self.assertEqual(report["errors"], [])

    def test_unlisted_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Review package\n")
            self.write_manifest(root, [readme])
            (root / "unlisted.md").write_text("# Undeclared\n")

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "MANIFEST_UNLISTED_FILE", "path": "unlisted.md"},
                report["errors"],
            )

    def test_broken_relative_markdown_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Review package\n\n[Missing](missing.md)\n")
            self.write_manifest(root, [readme])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {
                    "code": "BROKEN_RELATIVE_LINK",
                    "path": "README.md",
                    "detail": "missing.md",
                },
                report["errors"],
            )

    def test_private_identifier_and_generated_line_prefix_fail_sanitation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("1|# Review package\n\npostgresql://example.invalid/store\n")
            self.write_manifest(root, [readme])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            codes = {item["code"] for item in report["errors"]}
            self.assertIn("GENERATED_LINE_PREFIX", codes)
            self.assertIn("SANITATION_PRIVATE_IDENTIFIER", codes)

    def test_needs_revision_cannot_be_promoted_by_status_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Review package\n\n_Status: promoted_\n")
            draft = root / "draft.md"
            draft.write_text("# Draft\n\n_Status: **NEEDS REVISION**_\n")
            self.write_manifest(root, [readme, draft])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "STATUS_PROMOTION_CONFLICT", "path": "README.md"},
                report["errors"],
            )

    def test_parallel_spec_08_versions_require_explicit_legacy_supersession(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            legacy = root / "spec" / "08-immutability-and-chain-of-custody.md"
            legacy.parent.mkdir()
            legacy.write_text("# Legacy\n\n_Status: **NEEDS REVISION**_\n")
            successor = root / "spec" / "08-immutability-and-chain-of-custody-v0.2.md"
            successor.write_text("# Candidate\n")
            self.write_manifest(root, [legacy, successor])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {
                    "code": "SPEC_SUPERSESSION_UNDECLARED",
                    "path": "spec/08-immutability-and-chain-of-custody.md",
                },
                report["errors"],
            )

    def test_v02_requirement_missing_from_traceability_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            spec = root / "spec" / "08-immutability-and-chain-of-custody-v0.2.md"
            spec.parent.mkdir()
            spec.write_text("# Candidate\n\n- **CST-TEST-001:** A verifier MUST fail closed.\n")
            trace = root / "conformance" / "expectations" / "immutability-v0.2-traceability.md"
            trace.parent.mkdir(parents=True)
            trace.write_text("# Traceability\n")
            errors = root / "spec" / "07-errors.md"
            errors.write_text("# Errors\n\n| Code | Meaning |\n|---|---|\n| `TEST_FAILURE` | test |\n")
            dimensions = root / "spec" / "05-verification.md"
            dimensions.write_text("# Dimensions\n\n| Dimension | Meaning |\n|---|---|\n| `report_contract` | test |\n")
            cases = root / "conformance" / "expectations" / "immutability-v0.2-cases.md"
            cases.write_text("# Cases\n")
            self.write_manifest(root, [cases, trace, dimensions, errors, spec])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "TRACEABILITY_REQUIREMENT_MISSING", "detail": "CST-TEST-001"},
                report["errors"],
            )

    def test_manifest_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Before\n")
            self.write_manifest(root, [readme])
            readme.write_text("# After\n")

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "MANIFEST_HASH_MISMATCH", "path": "README.md"},
                report["errors"],
            )

    def test_json_report_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            readme = root / "README.md"
            readme.write_text("# Review package\n")
            self.write_manifest(root, [readme])

            first = self.run_validator(root)
            second = self.run_validator(root)

            self.assertEqual(first.returncode, 0)
            self.assertEqual(first.stdout, second.stdout)

    def test_lifecycle_state_cannot_be_registered_as_error_class(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            registry = root / "spec" / "07-errors.md"
            registry.parent.mkdir()
            registry.write_text(
                "# Errors\n\n| Code | Meaning |\n|---|---|\n"
                "| `TRANSFER_INCOMPLETE` | pending transfer |\n"
            )
            self.write_manifest(root, [registry])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "ERROR_CLASS_STATE_CONFLATION", "detail": "TRANSFER_INCOMPLETE"},
                report["errors"],
            )

    def test_case_primary_result_must_match_traceability_class(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root, negative_result="`OTHER_FAILURE`")

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {
                    "code": "CASE_PRIMARY_RESULT_MISMATCH",
                    "detail": "V02-TEST-001-N:TEST_FAILURE:OTHER_FAILURE",
                },
                report["errors"],
            )

    def test_case_pass_label_must_be_registered_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root, positive_result="pass `test_family`")

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {
                    "code": "CASE_PASS_DIMENSION_UNKNOWN",
                    "detail": "V02-TEST-001-P:test_family",
                },
                report["errors"],
            )

    def test_case_pass_result_must_name_a_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root, positive_result="pass lifecycle")

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {
                    "code": "CASE_PASS_DIMENSION_MISSING",
                    "detail": "V02-TEST-001-P",
                },
                report["errors"],
            )

    def test_positive_case_cannot_skip_pass_validation(self) -> None:
        for result_text in ("unknown", "`TEST_FAILURE`", "PASS `report_contract`"):
            with self.subTest(result=result_text), tempfile.TemporaryDirectory() as tmp:
                root = pathlib.Path(tmp)
                self.write_v02_package(root, positive_result=result_text)
                result = self.run_validator(root)
                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    {"code": "CASE_PASS_RESULT_MISSING", "detail": "V02-TEST-001-P"},
                    json.loads(result.stdout)["errors"],
                )

    def test_negative_primary_must_lead_the_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root, negative_result="unknown; secondary: `TEST_FAILURE`")
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn(
                {"code": "CASE_PRIMARY_RESULT_MISSING", "detail": "V02-TEST-001-N"},
                json.loads(result.stdout)["errors"],
            )

    def test_positive_dimension_must_match_its_requirement_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root, positive_result="pass `other_dimension`")
            dimensions = root / "spec" / "05-verification.md"
            dimensions.write_text(dimensions.read_text().replace(
                "## Next", "| `other_dimension` | other |\n\n## Next"
            ))
            self.write_manifest(root, [p for p in root.rglob("*")
                                      if p.is_file() and p.name != "REVIEW-MANIFEST.sha256"])
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn(
                {"code": "CASE_PASS_DIMENSION_MISMATCH", "detail": "V02-TEST-001-P"},
                json.loads(result.stdout)["errors"],
            )

    def test_planned_coverage_is_not_executed_conformance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            self.write_v02_package(root)
            cases = root / "conformance" / "expectations" / "immutability-v0.2-cases.md"
            cases.write_text("\n".join(line for line in cases.read_text().splitlines()
                                      if "V02-TEST-001-N" not in line) + "\n")
            self.write_manifest(root, [p for p in root.rglob("*")
                                      if p.is_file() and p.name != "REVIEW-MANIFEST.sha256"])
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            report = json.loads(result.stdout)
            self.assertEqual(report["planned_case_ids"], 2)
            self.assertEqual(report["documented_planned_case_ids"], 1)
            self.assertEqual(report["undocumented_planned_case_ids"], ["V02-TEST-001-N"])
            self.assertEqual(report["conformance_evaluation"], "not_performed")

    def test_status_value_cannot_masquerade_as_verification_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            spec = root / "spec" / "08-immutability-and-chain-of-custody-v0.2.md"
            spec.parent.mkdir()
            spec.write_text("# Candidate\n\n- **CST-TEST-001:** A verifier MUST fail closed.\n")
            dimensions = root / "spec" / "05-verification.md"
            dimensions.write_text(
                "# Verification\n\n| Status | Meaning |\n|---|---|\n| `pass` | state |\n\n"
                "## Authoritative verification-dimension registry\n\n"
                "| Dimension | Meaning |\n|---|---|\n| `report_contract` | dimension |\n\n"
                "## Next\n"
            )
            registry = root / "spec" / "07-errors.md"
            registry.write_text("# Errors\n\n| Code | Meaning |\n|---|---|\n| `TEST_FAILURE` | test |\n")
            trace = root / "conformance" / "expectations" / "immutability-v0.2-traceability.md"
            trace.parent.mkdir(parents=True)
            trace.write_text(
                "# Traceability\n\n| Requirement family | Authoritative dimension |\n|---|---|\n"
                "| `test_family` | `pass` |\n\n"
                "| Requirement | Family | Code | Positive | Negative | Summary |\n|---|---|---|---|---|---|\n"
                "| `CST-TEST-001` | `test_family` | `TEST_FAILURE` | `V02-TEST-001-P` | `V02-TEST-001-N` | test |\n"
            )
            cases = root / "conformance" / "expectations" / "immutability-v0.2-cases.md"
            cases.write_text("# Cases\n\n| Case | Input | Result |\n|---|---|---|\n| `V02-TEST-001-N` | bad | `TEST_FAILURE` |\n")
            self.write_manifest(root, [cases, trace, dimensions, registry, spec])

            result = self.run_validator(root)

            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertIn(
                {"code": "TRACEABILITY_DIMENSION_UNKNOWN", "detail": "test_family:pass"},
                report["errors"],
            )


if __name__ == "__main__":
    unittest.main()
