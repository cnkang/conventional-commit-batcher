#!/usr/bin/env python3
"""Unit tests for precommit_safety_gate.py."""

from precommit_safety_gate import evaluate_findings, print_report


def finding_codes(findings):
    return {finding.code for finding in findings}


def base_kwargs():
    return dict(
        branch="feature/demo",
        staged_paths=["src/app.py"],
        staged_has_changes=True,
        added_lines=["print('ok')"],
        numstat_rows=[("1", "0", "src/app.py")],
        file_sizes={"src/app.py": 12},
        max_file_size_kb=512,
        allow_sensitive=False,
        allow_local_artifacts=False,
        allow_protected_branch=False,
        allow_large_or_binary=False,
    )


def test_clean_staged_changes_pass():
    findings = evaluate_findings(**base_kwargs())
    assert findings == []


def test_empty_staged_blocks_commit():
    kwargs = base_kwargs()
    kwargs["staged_has_changes"] = False

    findings = evaluate_findings(**kwargs)
    assert "empty_staged" in finding_codes(findings)
    assert any(finding.severity == "block" for finding in findings)


def test_sensitive_path_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["staged_paths"] = [".env.production"]

    findings = evaluate_findings(**kwargs)
    assert "sensitive_paths" in finding_codes(findings)


def test_sensitive_content_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["added_lines"] = ["api_key = 'secret-value'"]
    kwargs["added_lines_by_file"] = {"scripts/demo.py": ["api_key = 'secret-value'"]}

    findings = evaluate_findings(**kwargs)
    assert "sensitive_content" in finding_codes(findings)
    sensitive_finding = [f for f in findings if f.code == "sensitive_content"][0]
    assert any(
        detail.startswith("file: scripts/demo.py")
        for detail in sensitive_finding.details
    )


def test_local_artifact_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["staged_paths"] = ["dist/bundle.js"]

    findings = evaluate_findings(**kwargs)
    assert "local_artifacts" in finding_codes(findings)


def test_protected_branch_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["branch"] = "main"

    findings = evaluate_findings(**kwargs)
    assert "protected_branch" in finding_codes(findings)


def test_conflict_markers_block_commit():
    kwargs = base_kwargs()
    kwargs["added_lines"] = ["<<<<<<< HEAD"]

    findings = evaluate_findings(**kwargs)
    assert "conflict_markers" in finding_codes(findings)
    assert any(finding.severity == "block" for finding in findings)


def test_binary_or_large_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["numstat_rows"] = [("-", "-", "assets/logo.png")]

    findings = evaluate_findings(**kwargs)
    assert "large_or_binary" in finding_codes(findings)


def test_large_file_requires_confirmation():
    kwargs = base_kwargs()
    kwargs["staged_paths"] = ["artifacts/big.bin"]
    kwargs["file_sizes"] = {"artifacts/big.bin": 900 * 1024}

    findings = evaluate_findings(**kwargs)
    assert "large_or_binary" in finding_codes(findings)


def test_allow_flags_suppress_confirm_findings():
    kwargs = base_kwargs()
    kwargs.update(
        {
            "branch": "main",
            "staged_paths": [".env", "dist/bundle.js", "assets/logo.png"],
            "added_lines": ["client_secret = 'value'"],
            "numstat_rows": [("-", "-", "assets/logo.png")],
            "file_sizes": {
                ".env": 20,
                "dist/bundle.js": 200,
                "assets/logo.png": 900 * 1024,
            },
            "allow_sensitive": True,
            "allow_local_artifacts": True,
            "allow_protected_branch": True,
            "allow_large_or_binary": True,
        }
    )

    findings = evaluate_findings(**kwargs)
    assert findings == []


def test_sensitive_report_has_review_suggestion(capsys):
    kwargs = base_kwargs()
    kwargs["added_lines"] = ["client_secret = 'value'"]
    kwargs["added_lines_by_file"] = {"scripts/demo.py": ["client_secret = 'value'"]}
    findings = evaluate_findings(**kwargs)

    print_report(findings)
    output = capsys.readouterr().out
    assert "scripts/demo.py" in output
    assert "suggestion: review the listed files" in output
