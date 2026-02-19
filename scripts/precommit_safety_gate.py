#!/usr/bin/env python3
"""Run commit-time safety gates for common risky staging mistakes."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Sequence


EXIT_OK = 0
EXIT_CONFIRMATION_REQUIRED = 2
EXIT_BLOCKED = 3

PROTECTED_BRANCH_RE = re.compile(r"^(main|master|release/.+|hotfix/.+)$")
CONFLICT_MARKER_RE = re.compile(r"^(<<<<<<< |=======|>>>>>>> )")

SENSITIVE_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env(\..*)?$", re.IGNORECASE),
    re.compile(r"\.(pem|key|p12|jks)$", re.IGNORECASE),
    re.compile(r"(^|/)(id_rsa|id_dsa|id_ed25519)$", re.IGNORECASE),
    re.compile(
        r"(secret|secrets|credential|credentials|token|password)", re.IGNORECASE
    ),
)

SENSITIVE_CONTENT_PATTERNS = (
    re.compile(r"BEGIN .*PRIVATE KEY", re.IGNORECASE),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"access[_-]?token", re.IGNORECASE),
    re.compile(r"secret[_-]?key", re.IGNORECASE),
    re.compile(r"client[_-]?secret", re.IGNORECASE),
    re.compile(r"password\s*[:=]", re.IGNORECASE),
)

LOCAL_ARTIFACT_PATTERNS = (
    re.compile(r"(^|/)\.env(\..*)?$", re.IGNORECASE),
    re.compile(r"(^|/)\.DS_Store$", re.IGNORECASE),
    re.compile(
        r"(^|/)(node_modules|dist|build|coverage|target|out|tmp|temp)/", re.IGNORECASE
    ),
    re.compile(r"(^|/)\.(cache|pytest_cache|ruff_cache|mypy_cache)/", re.IGNORECASE),
    re.compile(r"(^|/)__pycache__/", re.IGNORECASE),
    re.compile(r"\.(log|tmp|cache|bak|swp|swo)$", re.IGNORECASE),
)


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str  # "block" | "confirm"
    message: str
    details: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pre-commit safety gates for staged changes."
    )
    parser.add_argument(
        "--max-file-size-kb",
        type=int,
        default=512,
        help="Large file threshold in KB (default: 512).",
    )
    parser.add_argument(
        "--allow-sensitive",
        action="store_true",
        help="Acknowledge and allow sensitive file/content findings.",
    )
    parser.add_argument(
        "--allow-local-artifacts",
        action="store_true",
        help="Acknowledge and allow local/generated artifact findings.",
    )
    parser.add_argument(
        "--allow-protected-branch",
        action="store_true",
        help="Acknowledge and allow committing on protected/release branches.",
    )
    parser.add_argument(
        "--allow-large-or-binary",
        action="store_true",
        help="Acknowledge and allow large/binary staged artifacts.",
    )
    return parser.parse_args()


def run_git(
    args: Sequence[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
        check=check,
    )


def split_null_terminated(output: str) -> list[str]:
    return [part for part in output.split("\0") if part]


def extract_added_lines(diff_text: str) -> list[str]:
    added_lines: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            continue
        if line.startswith("+"):
            added_lines.append(line[1:])
    return added_lines


def extract_added_lines_by_file(diff_text: str) -> dict[str, list[str]]:
    added_lines_by_file: dict[str, list[str]] = {}
    current_file: str | None = None

    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            candidate = line[4:]
            if candidate == "/dev/null":
                current_file = None
                continue
            if candidate.startswith("b/"):
                candidate = candidate[2:]
            current_file = candidate
            added_lines_by_file.setdefault(current_file, [])
            continue

        if (
            line.startswith("+")
            and not line.startswith("+++ ")
            and current_file is not None
        ):
            added_lines_by_file[current_file].append(line[1:])

    return added_lines_by_file


def parse_numstat_lines(numstat_text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in numstat_text.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        rows.append((parts[0], parts[1], parts[2]))
    return rows


def matches_any(path: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    return any(pattern.search(path) for pattern in patterns)


def evaluate_findings(
    *,
    branch: str,
    staged_paths: Sequence[str],
    staged_has_changes: bool,
    added_lines: Sequence[str],
    added_lines_by_file: dict[str, Sequence[str]] | None = None,
    numstat_rows: Sequence[tuple[str, str, str]],
    file_sizes: dict[str, int],
    max_file_size_kb: int,
    allow_sensitive: bool,
    allow_local_artifacts: bool,
    allow_protected_branch: bool,
    allow_large_or_binary: bool,
) -> list[Finding]:
    findings: list[Finding] = []

    if not staged_has_changes:
        findings.append(
            Finding(
                code="empty_staged",
                severity="block",
                message="Staged area is empty. Do not run commit with no staged changes.",
                details=(),
            )
        )
        return findings

    if (not allow_protected_branch) and PROTECTED_BRANCH_RE.search(branch):
        findings.append(
            Finding(
                code="protected_branch",
                severity="confirm",
                message="Current branch looks protected or release-oriented.",
                details=(branch,),
            )
        )

    conflict_lines = [line for line in added_lines if CONFLICT_MARKER_RE.search(line)]
    if conflict_lines:
        findings.append(
            Finding(
                code="conflict_markers",
                severity="block",
                message="Unresolved merge conflict markers found in staged content.",
                details=tuple(conflict_lines[:5]),
            )
        )

    if not allow_sensitive:
        sensitive_paths = [
            path for path in staged_paths if matches_any(path, SENSITIVE_PATH_PATTERNS)
        ]
        sensitive_content_matches: list[str] = []
        sensitive_content_files: set[str] = set()

        if added_lines_by_file:
            for path, lines in added_lines_by_file.items():
                for line in lines:
                    if not matches_any(line, SENSITIVE_CONTENT_PATTERNS):
                        continue
                    sensitive_content_files.add(path)
                    if len(sensitive_content_matches) < 5:
                        sensitive_content_matches.append(
                            f"{path}: {line.strip()[:120]}"
                        )
        else:
            for line in added_lines:
                if not matches_any(line, SENSITIVE_CONTENT_PATTERNS):
                    continue
                if len(sensitive_content_matches) < 5:
                    sensitive_content_matches.append(line)

        if sensitive_paths:
            findings.append(
                Finding(
                    code="sensitive_paths",
                    severity="confirm",
                    message="Potentially sensitive file paths found in staged changes. Please review these files before commit.",
                    details=tuple(sorted(sensitive_paths)[:10]),
                )
            )
        if sensitive_content_matches:
            details: list[str] = []
            if sensitive_content_files:
                details.extend(
                    f"file: {path}" for path in sorted(sensitive_content_files)[:10]
                )
            details.extend(f"match: {item}" for item in sensitive_content_matches)

            findings.append(
                Finding(
                    code="sensitive_content",
                    severity="confirm",
                    message="Potentially sensitive content patterns found in staged additions. Please check these files/hunks.",
                    details=tuple(details[:12]),
                )
            )

    if not allow_local_artifacts:
        local_artifacts = [
            path for path in staged_paths if matches_any(path, LOCAL_ARTIFACT_PATTERNS)
        ]
        if local_artifacts:
            findings.append(
                Finding(
                    code="local_artifacts",
                    severity="confirm",
                    message="Local/generated artifact patterns found in staged paths.",
                    details=tuple(sorted(local_artifacts)[:10]),
                )
            )

    if not allow_large_or_binary:
        binary_paths = sorted(
            {
                path
                for added, deleted, path in numstat_rows
                if added == "-" or deleted == "-"
            }
        )
        large_paths = sorted(
            {
                path
                for path, size in file_sizes.items()
                if size > max_file_size_kb * 1024
            }
        )
        if binary_paths or large_paths:
            details = list(binary_paths)
            details.extend(
                f"{path} ({file_sizes[path]} bytes)"
                for path in large_paths
                if path not in binary_paths
            )
            findings.append(
                Finding(
                    code="large_or_binary",
                    severity="confirm",
                    message="Potential binary or large files found in staged content.",
                    details=tuple(details[:10]),
                )
            )

    return findings


def print_report(findings: Sequence[Finding]) -> None:
    if not findings:
        print("[Safety Gate] PASS")
        return

    print("[Safety Gate] FAIL")
    for finding in findings:
        prefix = "[BLOCK]" if finding.severity == "block" else "[CONFIRM]"
        print(f"{prefix} {finding.message}")
        for detail in finding.details:
            print(f"  - {detail}")
        if finding.code in {"sensitive_paths", "sensitive_content"}:
            print(
                "  - suggestion: review the listed files, remove/redact accidental secrets, or confirm they are intentional test/rule text."
            )


def required_ack_flags(findings: Sequence[Finding]) -> list[str]:
    flags: set[str] = set()
    for finding in findings:
        if finding.code in {"sensitive_paths", "sensitive_content"}:
            flags.add("--allow-sensitive")
        elif finding.code == "local_artifacts":
            flags.add("--allow-local-artifacts")
        elif finding.code == "protected_branch":
            flags.add("--allow-protected-branch")
        elif finding.code == "large_or_binary":
            flags.add("--allow-large-or-binary")
    return sorted(flags)


def staged_file_sizes(repo_root: Path, staged_paths: Sequence[str]) -> dict[str, int]:
    sizes: dict[str, int] = {}
    for rel_path in staged_paths:
        file_path = repo_root / rel_path
        if not file_path.exists() or not file_path.is_file():
            continue
        try:
            sizes[rel_path] = file_path.stat().st_size
        except OSError:
            continue
    return sizes


def main() -> int:
    args = parse_args()

    try:
        repo_root = Path(
            run_git(["rev-parse", "--show-toplevel"]).stdout.strip()
        ).resolve()
        branch = run_git(["branch", "--show-current"]).stdout.strip()

        staged_quiet = run_git(["diff", "--cached", "--quiet"], check=False)
        staged_has_changes = staged_quiet.returncode != 0

        staged_paths = split_null_terminated(
            run_git(["diff", "--cached", "--name-only", "-z"]).stdout
        )
        staged_diff = run_git(["diff", "--cached", "--unified=0", "--no-color"]).stdout
        added_lines = extract_added_lines(staged_diff)
        added_lines_by_file = extract_added_lines_by_file(staged_diff)
        numstat_rows = parse_numstat_lines(
            run_git(["diff", "--cached", "--numstat"]).stdout
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "unknown git error"
        print(
            f"[Safety Gate] ERROR: failed to inspect git state: {stderr}",
            file=sys.stderr,
        )
        return 1

    findings = evaluate_findings(
        branch=branch,
        staged_paths=staged_paths,
        staged_has_changes=staged_has_changes,
        added_lines=added_lines,
        added_lines_by_file=added_lines_by_file,
        numstat_rows=numstat_rows,
        file_sizes=staged_file_sizes(repo_root, staged_paths),
        max_file_size_kb=args.max_file_size_kb,
        allow_sensitive=args.allow_sensitive,
        allow_local_artifacts=args.allow_local_artifacts,
        allow_protected_branch=args.allow_protected_branch,
        allow_large_or_binary=args.allow_large_or_binary,
    )

    print_report(findings)

    blocked = any(item.severity == "block" for item in findings)
    if blocked:
        print(
            "Resolve [BLOCK] findings before commit. Confirmation flags cannot bypass them.",
            file=sys.stderr,
        )
        return EXIT_BLOCKED

    confirmation = any(item.severity == "confirm" for item in findings)
    if confirmation:
        flags = required_ack_flags(findings)
        flag_hint = " ".join(flags)
        print(
            "Explicit confirmation required before commit. "
            f"After user approval, rerun with: python3 scripts/precommit_safety_gate.py {flag_hint}",
            file=sys.stderr,
        )
        return EXIT_CONFIRMATION_REQUIRED

    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
