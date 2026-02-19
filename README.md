# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-10b981)](https://github.com/cnkang/conventional-commit-batcher/releases)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[中文文档](README.zh-CN.md)

Turn mixed local changes into clean, reviewable Conventional Commit batches.

## Why Use This Skill

- Plan-first workflow prevents accidental mixed commits.
- Clear batch boundaries make review, revert, and `git bisect` safer.
- Commit messages stay standards-compliant without manual policing.

## Who This Is For

- Developers with a messy working tree before opening a PR.
- Teams that want cleaner commit history for release/changelog tooling.
- Agent-driven workflows that need deterministic commit hygiene.

## 30s Quick Try

### A) Install as an Agent Skill (recommended)

```bash
npx skills add cnkang/conventional-commit-batcher
npx skills list
```

Then ask your agent:

```text
I have mixed changes in my working tree.
1) Inspect git status and diff.
2) Produce a full Commit Plan with logical batches.
3) Wait for my confirmation.
4) After I approve, stage and commit each batch with Conventional Commit messages.
```

### B) Use commit-msg hook only (no agent required)

```bash
cat > .git/hooks/commit-msg <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

MSG_FILE="$1"
SCRIPT_PATH="scripts/validate_conventional_commit.py"

if [ ! -f "$SCRIPT_PATH" ]; then
  echo "[commit-msg] validator not found: $SCRIPT_PATH"
  exit 1
fi

python3 "$SCRIPT_PATH" \
  --file "$MSG_FILE" \
  --max-subject-length 72 \
  --max-header-length 100
HOOK

chmod +x .git/hooks/commit-msg
```

## What You Should Expect

When used correctly, the skill should always output a plan before any commit:

```text
Commit Plan
Batch #1: feat(scope): ...
Intent: ...
Files/Hunks:
- ...
Staging commands:
- git add ...
Commit command:
- git commit -m "feat(scope): ..."
```

## When To Use / Skip

Use it when:

- one branch contains mixed intents (`feat` + `fix` + `docs` + `style`)
- you need reviewable commit boundaries before PR
- you want consistent Conventional Commit history across contributors

Skip it when:

- you only have one tiny, single-intent change
- commit history hygiene is not relevant for the task

## Quick Start Paths

1. Agent flow: load this skill and follow `references/core-rules.md`.
2. Validator CLI: `python3 scripts/validate_conventional_commit.py "feat(scope): add ..."`.
3. Hook flow: use the script above (or `references/commit-msg-hook-example.md`).

## Agent-Specific Setup

Use these docs only for tool-specific setup details:

- Codex: `references/codex-setup.md`
- Claude Code: `references/claude-setup.md`
- Kiro CLI: `references/kiro-setup.md`
- Kimi CLI: `references/kimi-setup.md`
- Qwen Code: `references/qwen-setup.md`
- Gemini CLI: `references/gemini-setup.md`

## Core Rule Source

All entrypoints delegate to one canonical rule file:

- `references/core-rules.md`

## Community and Feedback

- Bug reports and feature requests: GitHub Issues (`/.github/ISSUE_TEMPLATE/`)
- Product discussion and usage ideas: GitHub Discussions

## License

Apache-2.0 (`LICENSE`)
