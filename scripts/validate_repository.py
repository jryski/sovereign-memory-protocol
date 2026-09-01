#!/usr/bin/env python3
"""Validate an exact SMP protocol review package.

The validator is dependency-free, deterministic, read-only, and emits a stable
JSON report when invoked with ``--json``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any
from urllib.parse import unquote

MANIFEST_NAME = "REVIEW-MANIFEST.sha256"
EXCLUDED_DIRECTORIES = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}
MANIFEST_LINE = re.compile(r"^([0-9a-f]{64})  ([^\x00\r\n]+)$")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
DOCUMENT_SUFFIXES = {".md", ".json", ".toml", ".txt", ".yaml", ".yml"}
PRIVATE_IDENTIFIER = re.compile(
    r"(?i)(?:supabase|postgres(?:ql)?|sovereign-memory-core|jryski|"
    r"AI-MEMORY-ATLAS|claude-warden|model[._-]?channel|\bHOUSE\b|\bVAULT\b|"
    r"\bLocutus\b|\bAriadne\b|\bWarden\b|(?:\b\d{1,3}\.){3}\d{1,3}\b)"
)
SECRET_PATTERNS = (
    re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s/:]+:[^\s/@]+@"),
    re.compile(r"(?i)\bpassword\s*[:=]\s*[^\s`]+"),
)
STATUS_LINE = re.compile(r"(?i)^\s*_?status\s*:\s*(.+?)_?\s*$")
PROMOTED_STATUS = re.compile(
    r"(?i)^(?:\*\*)?(?:promoted|accepted normative|normative baseline|conformant)(?:\*\*)?(?:\s|$)"
)
STATE_LIKE_ERROR_CLASSES = {
    "ALGORITHM_POLICY_UNACCEPTABLE",
    "APPEND_CONFLICT",
    "CHECKPOINT_STALE",
    "COMPLETENESS_UNKNOWN",
    "ERASURE_PARTIAL",
    "KEY_STATUS_INDETERMINATE",
    "OFFLINE_EVIDENCE_INCOMPLETE",
    "PAYLOAD_UNAVAILABLE_UNKNOWN",
    "PROJECTION_STALE",
    "RESTORE_QUARANTINED",
    "TRANSFER_INCOMPLETE",
}


def error(code: str, path: str | None = None, detail: str | None = None) -> dict[str, str]:
    item = {"code": code}
    if path is not None:
        item["path"] = path
    if detail is not None:
        item["detail"] = detail
    return item


def repository_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not EXCLUDED_DIRECTORIES.intersection(path.parts)
        and path.name != MANIFEST_NAME
    )


def parse_manifest(root: pathlib.Path, errors: list[dict[str, str]]) -> dict[str, str]:
    manifest = root / MANIFEST_NAME
    if not manifest.is_file():
        errors.append(error("MANIFEST_MISSING", MANIFEST_NAME))
        return {}
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        errors.append(error("MANIFEST_UNREADABLE", MANIFEST_NAME))
        return {}
    entries: dict[str, str] = {}
    previous = ""
    for number, line in enumerate(text.splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        match = MANIFEST_LINE.fullmatch(line)
        if match is None:
            errors.append(error("MANIFEST_LINE_INVALID", MANIFEST_NAME, str(number)))
            continue
        digest, relative = match.groups()
        pure = pathlib.PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or relative in {"", MANIFEST_NAME}:
            errors.append(error("MANIFEST_PATH_INVALID", relative))
            continue
        if relative in entries:
            errors.append(error("MANIFEST_DUPLICATE_PATH", relative))
            continue
        if previous and relative <= previous:
            errors.append(error("MANIFEST_ORDER_INVALID", relative))
        previous = relative
        entries[relative] = digest
    return entries


def validate_markdown_links(root: pathlib.Path, paths: list[pathlib.Path], errors: list[dict[str, str]]) -> None:
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(error("MARKDOWN_UNREADABLE", path.relative_to(root).as_posix()))
            continue
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
            if re.match(r"^(?:https?://|mailto:|#)", target):
                continue
            relative_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not relative_target:
                continue
            resolved = (path.parent / relative_target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(error("RELATIVE_LINK_ESCAPES_ROOT", path.relative_to(root).as_posix(), target))
                continue
            if not resolved.exists():
                errors.append(error("BROKEN_RELATIVE_LINK", path.relative_to(root).as_posix(), target))


def validate_sanitation(root: pathlib.Path, paths: list[pathlib.Path], errors: list[dict[str, str]]) -> None:
    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if path.suffix.lower() in DOCUMENT_SUFFIXES:
            for number, line in enumerate(text.splitlines(), 1):
                if re.match(r"^\d+\|", line):
                    errors.append(error("GENERATED_LINE_PREFIX", relative, str(number)))
                if PRIVATE_IDENTIFIER.search(line):
                    errors.append(error("SANITATION_PRIVATE_IDENTIFIER", relative, str(number)))
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(error("SECRET_PATTERN_DETECTED", relative))
                break


def validate_status_consistency(root: pathlib.Path, paths: list[pathlib.Path], errors: list[dict[str, str]]) -> None:
    metadata: list[tuple[str, str]] = []
    needs_revision = False
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()[:20]
        except (OSError, UnicodeError):
            continue
        for line in lines:
            match = STATUS_LINE.match(line)
            if match is None:
                continue
            value = match.group(1).strip()
            metadata.append((path.relative_to(root).as_posix(), value))
            if "NEEDS REVISION" in value.upper():
                needs_revision = True
    if needs_revision:
        for relative, value in metadata:
            if PROMOTED_STATUS.match(value):
                errors.append(error("STATUS_PROMOTION_CONFLICT", relative))


def validate_spec_supersession(root: pathlib.Path, errors: list[dict[str, str]]) -> None:
    legacy_relative = "spec/08-immutability-and-chain-of-custody.md"
    successor_relative = "spec/08-immutability-and-chain-of-custody-v0.2.md"
    legacy = root / legacy_relative
    successor = root / successor_relative
    if not legacy.is_file() or not successor.is_file():
        return
    try:
        text = legacy.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    normalized = " ".join(text.lower().split())
    if (
        "superseded" not in normalized
        or successor_relative.lower() not in normalized
        or "non-normative historical" not in normalized
    ):
        errors.append(error("SPEC_SUPERSESSION_UNDECLARED", legacy_relative))


def validate_registry_orthogonality(root: pathlib.Path, errors: list[dict[str, str]]) -> None:
    registry = root / "spec" / "07-errors.md"
    if not registry.is_file():
        return
    try:
        text = registry.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return
    codes = set(re.findall(r"^\| `([A-Z][A-Z0-9_]+)` \|", text, re.MULTILINE))
    for code in sorted(codes & STATE_LIKE_ERROR_CLASSES):
        errors.append(error("ERROR_CLASS_STATE_CONFLATION", detail=code))


def validate_v02_traceability(root: pathlib.Path, errors: list[dict[str, str]]) -> dict[str, int]:
    empty_metrics = {
        "requirements": 0,
        "traceability_rows": 0,
        "case_rows": 0,
        "registered_codes": 0,
        "registered_dimensions": 0,
    }
    relative_paths = {
        "spec": "spec/08-immutability-and-chain-of-custody-v0.2.md",
        "trace": "conformance/expectations/immutability-v0.2-traceability.md",
        "registry": "spec/07-errors.md",
        "dimensions": "spec/05-verification.md",
        "cases": "conformance/expectations/immutability-v0.2-cases.md",
    }
    paths = {name: root / relative for name, relative in relative_paths.items()}
    if not any(path.exists() for path in paths.values()):
        return empty_metrics
    for name, path in paths.items():
        if not path.is_file():
            errors.append(error("TRACEABILITY_ARTIFACT_MISSING", relative_paths[name]))
            return empty_metrics

    spec = paths["spec"].read_text(encoding="utf-8")
    trace = paths["trace"].read_text(encoding="utf-8")
    registry = paths["registry"].read_text(encoding="utf-8")
    dimensions = paths["dimensions"].read_text(encoding="utf-8")
    cases = paths["cases"].read_text(encoding="utf-8")
    requirements = re.findall(r"^- \*\*(CST-[A-Z]+-\d+):\*\*\s*(.+)$", spec, re.MULTILINE)
    requirement_ids = [identifier for identifier, _ in requirements]
    trace_rows = re.findall(
        r"^\| `(CST-[A-Z]+-\d+)` \| `([^`]+)` \| `([A-Z][A-Z0-9_]+)` \| `(V02-[A-Z]+-\d+-P)` \| `(V02-[A-Z]+-\d+-N)` \|",
        trace,
        re.MULTILINE,
    )
    trace_ids = [row[0] for row in trace_rows]
    registry_codes = set(re.findall(r"^\| `([A-Z][A-Z0-9_]+)` \|", registry, re.MULTILINE))
    dimension_section = re.search(
        r"^## Authoritative verification-dimension registry\s*$\n(.*?)(?=^## |\Z)",
        dimensions,
        re.MULTILINE | re.DOTALL,
    )
    dimension_ids = (
        set(re.findall(r"^\| `([a-z][a-z0-9_]+)` \|", dimension_section.group(1), re.MULTILINE))
        if dimension_section is not None
        else set()
    )
    family_map = dict(
        re.findall(r"^\| `([a-z][a-z0-9_]+)` \| `([a-z][a-z0-9_]+)` \|$", trace, re.MULTILINE)
    )
    case_rows = re.findall(
        r"^\| `(V02-[A-Z]+-\d+(?:-[PN])?)` \|.*?\| (.*?) \|$",
        cases,
        re.MULTILINE,
    )
    case_ids = [identifier for identifier, _ in case_rows]
    case_codes = set(re.findall(r"`([A-Z][A-Z0-9_]+)`", cases))
    trace_by_negative_fixture = {
        negative: (identifier, code)
        for identifier, _family, code, _positive, negative in trace_rows
    }

    for identifier in sorted(set(requirement_ids) - set(trace_ids)):
        errors.append(error("TRACEABILITY_REQUIREMENT_MISSING", detail=identifier))
    for identifier in sorted(set(trace_ids) - set(requirement_ids)):
        errors.append(error("TRACEABILITY_REQUIREMENT_UNKNOWN", detail=identifier))
    for identifier in sorted({value for value in requirement_ids if requirement_ids.count(value) > 1}):
        errors.append(error("REQUIREMENT_ID_DUPLICATE", detail=identifier))
    for identifier in sorted({value for value in trace_ids if trace_ids.count(value) > 1}):
        errors.append(error("TRACEABILITY_ID_DUPLICATE", detail=identifier))
    for identifier, text in requirements:
        if re.search(r"\bMUST(?: NOT)?\b", text) is None:
            errors.append(error("REQUIREMENT_NORMATIVE_KEYWORD_MISSING", detail=identifier))
    for identifier, family, code, positive, negative in trace_rows:
        dimension = family_map.get(family)
        if dimension is None:
            errors.append(error("TRACEABILITY_FAMILY_UNMAPPED", detail=f"{identifier}:{family}"))
        elif dimension not in dimension_ids:
            errors.append(error("TRACEABILITY_DIMENSION_UNKNOWN", detail=f"{family}:{dimension}"))
        if code not in registry_codes:
            errors.append(error("TRACEABILITY_CODE_UNREGISTERED", detail=f"{identifier}:{code}"))
        prefix = identifier.replace("CST-", "V02-")
        if positive != f"{prefix}-P" or negative != f"{prefix}-N":
            errors.append(error("TRACEABILITY_FIXTURE_ID_INVALID", detail=identifier))
    for code in sorted(case_codes - registry_codes - {"PASS"}):
        errors.append(error("CASE_CODE_UNREGISTERED", detail=code))
    for identifier, result in case_rows:
        if identifier in trace_by_negative_fixture:
            _requirement, expected_code = trace_by_negative_fixture[identifier]
            primary_match = re.search(r"`([A-Z][A-Z0-9_]+)`", result)
            if primary_match is None:
                errors.append(error("CASE_PRIMARY_RESULT_MISSING", detail=identifier))
            elif primary_match.group(1) != expected_code:
                errors.append(
                    error(
                        "CASE_PRIMARY_RESULT_MISMATCH",
                        detail=f"{identifier}:{expected_code}:{primary_match.group(1)}",
                    )
                )
        if identifier.endswith("-P") and result.startswith("pass "):
            dimension_match = re.search(r"`([a-z][a-z0-9_]+)`", result)
            if dimension_match is None:
                errors.append(error("CASE_PASS_DIMENSION_MISSING", detail=identifier))
            elif dimension_match.group(1) not in dimension_ids:
                errors.append(
                    error(
                        "CASE_PASS_DIMENSION_UNKNOWN",
                        detail=f"{identifier}:{dimension_match.group(1)}",
                    )
                )
    for identifier in sorted({value for value in case_ids if case_ids.count(value) > 1}):
        errors.append(error("CASE_ID_DUPLICATE", detail=identifier))

    return {
        "requirements": len(requirement_ids),
        "traceability_rows": len(trace_rows),
        "case_rows": len(case_ids),
        "registered_codes": len(registry_codes),
        "registered_dimensions": len(dimension_ids),
    }


def validate(root: pathlib.Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    entries = parse_manifest(root, errors)
    actual_paths = {path.relative_to(root).as_posix(): path for path in repository_files(root)}

    for relative in sorted(entries):
        path = actual_paths.get(relative)
        if path is None:
            errors.append(error("MANIFEST_FILE_MISSING", relative))
            continue
        try:
            actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            errors.append(error("MANIFEST_FILE_UNREADABLE", relative))
            continue
        if actual_digest != entries[relative]:
            errors.append(error("MANIFEST_HASH_MISMATCH", relative))

    for relative in sorted(set(actual_paths) - set(entries)):
        errors.append(error("MANIFEST_UNLISTED_FILE", relative))

    validate_markdown_links(root, list(actual_paths.values()), errors)
    validate_sanitation(root, list(actual_paths.values()), errors)
    validate_status_consistency(root, list(actual_paths.values()), errors)
    validate_spec_supersession(root, errors)
    validate_registry_orthogonality(root, errors)
    metrics = validate_v02_traceability(root, errors)

    errors.sort(key=lambda item: (item["code"], item.get("path", ""), item.get("detail", "")))
    return {
        "schema": "smp-review-validation/1",
        "status": "pass" if not errors else "fail",
        "manifest_entries": len(entries),
        "checked_files": len(actual_paths),
        **metrics,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    root = pathlib.Path(args.root).resolve()
    report = validate(root)
    if args.json:
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    else:
        print(f"{report['status']}: {report['checked_files']} files, {len(report['errors'])} errors")
        for item in report["errors"]:
            suffix = f" {item['path']}" if "path" in item else ""
            print(f"{item['code']}{suffix}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
