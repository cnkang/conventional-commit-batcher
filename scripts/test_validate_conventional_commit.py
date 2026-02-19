#!/usr/bin/env python3
"""Unit tests for validate_conventional_commit.py."""

import pytest

from validate_conventional_commit import validate

# --- Defaults shared across tests ---
DEFAULTS = dict(
    max_subject_length=72,
    max_header_length=100,
    allow_underscore_scope=True,
    subject_lowercase_mode="warn",
    imperative_mode="warn",
)


# ---- Valid messages ----


@pytest.mark.parametrize(
    "msg",
    [
        "feat(auth): add refresh token rotation",
        "fix(api): handle empty pagination cursor",
        "docs: update readme",
        "refactor(core): split parser into modules",
        "chore: bump dependencies",
        "style: normalize whitespace",
        "perf(db): add query index hint",
        "test(cache): add eviction edge cases",
        "build(deps): add zod",
        "ci: add lint step",
        "revert: undo last migration",
    ],
)
def test_valid_messages(msg):
    errors, _ = validate(msg, **DEFAULTS)
    assert errors == []


# ---- Breaking changes ----


def test_breaking_bang_valid():
    errors, _ = validate("feat(api)!: remove v1 endpoint", **DEFAULTS)
    assert errors == []


def test_breaking_footer_valid():
    msg = "feat(api): remove v1 endpoint\n\nBREAKING CHANGE: /v1/search removed"
    errors, _ = validate(msg, **DEFAULTS)
    assert errors == []


def test_breaking_mention_without_marker():
    msg = "feat(api): breaking change removal of v1 endpoint"
    errors, _ = validate(msg, **DEFAULTS)
    assert any("breaking" in e.lower() for e in errors)


def test_non_breaking_word_is_valid():
    errors, _ = validate("fix(test): stop breaking flaky suites", **DEFAULTS)
    assert errors == []


# ---- Header format errors ----


def test_invalid_type():
    errors, _ = validate("foo: do something", **DEFAULTS)
    assert errors != []


def test_missing_colon_space():
    errors, _ = validate("feat:no space", **DEFAULTS)
    assert errors != []


def test_trailing_period():
    errors, _ = validate("feat: add feature.", **DEFAULTS)
    assert any("period" in e.lower() for e in errors)


def test_header_too_long():
    long_subject = "a" * 90
    errors, _ = validate(
        f"feat: {long_subject}",
        max_header_length=50,
        **{k: v for k, v in DEFAULTS.items() if k != "max_header_length"},
    )
    assert any("header length" in e.lower() for e in errors)


def test_subject_too_long():
    long_subject = "a" * 80
    errors, _ = validate(
        f"feat: {long_subject}",
        max_subject_length=30,
        **{k: v for k, v in DEFAULTS.items() if k != "max_subject_length"},
    )
    assert any("subject length" in e.lower() for e in errors)


# ---- Body / footer structure ----


def test_missing_blank_line_after_header():
    msg = "feat: add feature\nsome body without blank line"
    errors, _ = validate(msg, **DEFAULTS)
    assert any("blank line" in e.lower() for e in errors)


def test_extra_blank_line_after_header():
    msg = "feat: add feature\n\n\nBody text"
    errors, _ = validate(msg, **DEFAULTS)
    assert any("blank line" in e.lower() for e in errors)


def test_valid_body():
    msg = "feat: add feature\n\nThis is the body."
    errors, _ = validate(msg, **DEFAULTS)
    assert errors == []


def test_body_line_with_colon_is_valid():
    msg = "feat: add feature\n\nNote: this is body text\nsecond line of body"
    errors, _ = validate(msg, **DEFAULTS)
    assert errors == []


def test_valid_footer():
    msg = "feat: add feature\n\nBody text.\n\nRefs: #123"
    errors, _ = validate(msg, **DEFAULTS)
    assert errors == []


# ---- Style warnings ----


def test_uppercase_subject_warns():
    _, warnings = validate("feat: Add feature", **DEFAULTS)
    assert any("lowercase" in w.lower() for w in warnings)


def test_non_imperative_warns():
    _, warnings = validate("feat: added new feature", **DEFAULTS)
    assert any("imperative" in w.lower() for w in warnings)


def test_uppercase_subject_error_mode():
    errors, _ = validate(
        "feat: Add feature",
        **{
            **DEFAULTS,
            "subject_lowercase_mode": "error",
        },
    )
    assert any("lowercase" in e.lower() for e in errors)


def test_non_imperative_error_mode():
    errors, _ = validate(
        "feat: added new feature",
        **{
            **DEFAULTS,
            "imperative_mode": "error",
        },
    )
    assert any("imperative" in e.lower() for e in errors)


# ---- Scope rules ----


def test_underscore_scope_allowed_by_default():
    errors, _ = validate("feat(my_scope): add thing", **DEFAULTS)
    assert errors == []


def test_underscore_scope_rejected_in_strict():
    errors, _ = validate(
        "feat(my_scope): add thing",
        **{
            **DEFAULTS,
            "allow_underscore_scope": False,
        },
    )
    assert errors != []


# ---- Edge cases ----


def test_empty_message():
    errors, _ = validate("", **DEFAULTS)
    assert errors != []


def test_consecutive_spaces_in_subject():
    errors, _ = validate("feat: add  feature", **DEFAULTS)
    assert any("consecutive" in e.lower() for e in errors)


def test_leading_trailing_spaces_in_subject():
    errors, _ = validate("feat:  add feature", **DEFAULTS)
    assert errors != []


def test_header_leading_space_is_invalid():
    errors, _ = validate(" feat: add feature", **DEFAULTS)
    assert any(
        "header must not contain leading/trailing spaces" in e.lower() for e in errors
    )


def test_header_trailing_space_is_invalid():
    errors, _ = validate("feat: add feature ", **DEFAULTS)
    assert any(
        "header must not contain leading/trailing spaces" in e.lower() for e in errors
    )
