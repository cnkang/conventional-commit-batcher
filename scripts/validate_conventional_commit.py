#!/usr/bin/env python3
"""Validate Conventional Commit messages with practical quality rules."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Sequence

ALLOWED_TYPES = (
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
)

NON_IMPERATIVE_START_RE = re.compile(
    r"^(added|adding|fixed|fixing|removed|removing|updated|updating|changed|changing)\b",
    re.IGNORECASE,
)
BREAKING_FOOTER_RE = re.compile(r"^BREAKING CHANGE:\s+\S")
GENERIC_FOOTER_RE = re.compile(r"^[A-Za-z-]+:\s+\S")
BREAKING_CHANGE_RE = re.compile(r"\bbreaking\s+changes?\b", re.IGNORECASE)


def build_header_re(allow_underscore_scope: bool) -> re.Pattern[str]:
    scope_tail_chars = r"a-z0-9\-./_"
    if not allow_underscore_scope:
        scope_tail_chars = r"a-z0-9\-./"

    scope_pattern = rf"[a-z0-9][{scope_tail_chars}]*"
    return re.compile(
        rf"^(?P<type>{'|'.join(ALLOWED_TYPES)})"
        rf"(?:\((?P<scope>{scope_pattern})\))?"
        rf"(?P<breaking>!)?"
        rf": "
        rf"(?P<subject>.+)$"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Conventional Commit message."
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="Commit message text. If omitted, use --file or --stdin.",
    )
    parser.add_argument("--file", help="Read commit message from file.")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read commit message from standard input.",
    )
    parser.add_argument(
        "--max-subject-length",
        type=int,
        default=72,
        help="Maximum subject length (default: 72).",
    )
    parser.add_argument(
        "--max-header-length",
        type=int,
        default=100,
        help="Maximum full header length (default: 100).",
    )
    parser.add_argument(
        "--strict-scope",
        action="store_true",
        help="Disallow underscore (_) in scope names.",
    )
    parser.add_argument(
        "--subject-lowercase-mode",
        choices=("off", "warn", "error"),
        default="warn",
        help="Enforce subject lowercase style when subject starts with a letter.",
    )
    parser.add_argument(
        "--imperative-mode",
        choices=("off", "warn", "error"),
        default="warn",
        help="Flag non-imperative leading verbs (added/adding/fixed/fixing...).",
    )
    return parser.parse_args()


def read_message(args: argparse.Namespace) -> str:
    if args.message:
        return args.message.strip("\n")

    if args.file:
        return Path(args.file).read_text(encoding="utf-8").strip("\n")

    if args.stdin:
        return sys.stdin.read().strip("\n")

    raise ValueError("Provide message text, --file, or --stdin.")


def is_footer_line(line: str) -> bool:
    return bool(BREAKING_FOOTER_RE.match(line) or GENERIC_FOOTER_RE.match(line))


def is_valid_footer_section(lines: Sequence[str]) -> bool:
    for line in lines:
        if not line.strip():
            continue
        if is_footer_line(line):
            continue
        if line.startswith((" ", "\t")):
            continue
        return False
    return True


def first_alpha_char(value: str) -> str | None:
    for char in value:
        if char.isalpha():
            return char
    return None


def add_style_message(
    style_mode: str, message: str, errors: list[str], warnings: list[str]
) -> None:
    if style_mode == "error":
        errors.append(message)
    elif style_mode == "warn":
        warnings.append(message)


def validate(
    message: str,
    max_subject_length: int,
    max_header_length: int,
    allow_underscore_scope: bool,
    subject_lowercase_mode: str,
    imperative_mode: str,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    lines = message.splitlines()
    if not lines:
        return (["Message is empty."], warnings)

    header = lines[0]
    header_for_match = header.strip()
    if header != header_for_match:
        errors.append("Header must not contain leading/trailing spaces.")

    header_re = build_header_re(allow_underscore_scope)
    match = header_re.match(header_for_match)
    if not match:
        return (
            [
                "Header must match '<type>(<scope>)!: <subject>' using allowed Conventional Commit types."
            ],
            warnings,
        )

    commit_type = match.group("type")
    subject = match.group("subject")
    has_breaking_bang = bool(match.group("breaking"))

    if commit_type not in ALLOWED_TYPES:
        errors.append(f"Type '{commit_type}' is not allowed.")

    if len(header_for_match) > max_header_length:
        errors.append(
            f"Header length {len(header_for_match)} exceeds max {max_header_length}."
        )

    if subject.endswith("."):
        errors.append("Subject must not end with a period.")

    if len(subject) > max_subject_length:
        errors.append(
            f"Subject length {len(subject)} exceeds max {max_subject_length}."
        )

    if subject != subject.strip():
        errors.append("Subject must not contain leading/trailing spaces.")

    if "  " in subject:
        errors.append("Subject must not contain consecutive spaces.")

    first_alpha = first_alpha_char(subject)
    if first_alpha and first_alpha.isupper():
        add_style_message(
            subject_lowercase_mode,
            "Subject should start with lowercase when the first letter is alphabetic.",
            errors,
            warnings,
        )

    if NON_IMPERATIVE_START_RE.match(subject.strip()):
        add_style_message(
            imperative_mode,
            "Subject should use imperative mood (for example 'add' instead of 'added/adding').",
            errors,
            warnings,
        )

    has_extra_content = len(lines) > 1
    if has_extra_content:
        if lines[1].strip():
            errors.append(
                "If body or footer exists, insert exactly one blank line after header."
            )
        elif len(lines) > 2 and not lines[2].strip():
            errors.append(
                "If body or footer exists, insert exactly one blank line after header."
            )

    content_lines = lines[2:] if len(lines) > 2 else []
    first_footer_index: int | None = None
    if content_lines:
        first_non_empty_index: int | None = None
        for index, line in enumerate(content_lines):
            if line.strip():
                first_non_empty_index = index
                break

        if (
            first_non_empty_index is not None
            and is_footer_line(content_lines[first_non_empty_index])
            and is_valid_footer_section(content_lines[first_non_empty_index:])
        ):
            first_footer_index = first_non_empty_index
        else:
            for index, line in enumerate(content_lines):
                if line.strip():
                    continue
                next_index = index + 1
                while (
                    next_index < len(content_lines)
                    and not content_lines[next_index].strip()
                ):
                    next_index += 1
                if next_index >= len(content_lines):
                    break
                if is_footer_line(content_lines[next_index]):
                    first_footer_index = next_index
                    break

    if first_footer_index is not None:
        body_lines = content_lines[:first_footer_index]
        footer_lines = content_lines[first_footer_index:]

        if body_lines and body_lines[-1].strip():
            errors.append("Insert one blank line between body and footer.")

        if not is_valid_footer_section(footer_lines):
            errors.append("Footer section contains invalid non-footer lines.")

    has_breaking_footer = any(BREAKING_FOOTER_RE.match(line) for line in lines[1:])
    mentions_breaking_change = bool(BREAKING_CHANGE_RE.search(message))
    if mentions_breaking_change and not (has_breaking_bang or has_breaking_footer):
        errors.append(
            "Message mentions breaking changes; add '!' in header or 'BREAKING CHANGE:' footer."
        )

    return errors, warnings


def print_items(prefix: str, items: Sequence[str]) -> None:
    print(prefix)
    for item in items:
        print(f"- {item}")


def main() -> int:
    args = parse_args()

    try:
        message = read_message(args)
    except Exception as exc:  # pragma: no cover
        print(f"[ERROR] {exc}")
        return 2

    errors, warnings = validate(
        message=message,
        max_subject_length=args.max_subject_length,
        max_header_length=args.max_header_length,
        allow_underscore_scope=not args.strict_scope,
        subject_lowercase_mode=args.subject_lowercase_mode,
        imperative_mode=args.imperative_mode,
    )
    if errors:
        print_items("[INVALID] Conventional Commit check failed:", errors)
        if warnings:
            print_items("[WARN] Style suggestions:", warnings)
        return 1

    if warnings:
        print_items(
            "[WARN] Conventional Commit is valid with style suggestions:", warnings
        )
        return 0

    print("[OK] Conventional Commit message is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
