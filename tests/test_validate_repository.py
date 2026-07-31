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
    def run_validator(self, root: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root), "--json"],
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
