# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-10b981)](https://github.com/cnkang/conventional-commit-batcher/releases)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[中文文档](README.zh-CN.md)

Split mixed changes into reviewable, revertible, traceable Conventional Commit batches with an agent-first, mandatory plan-first workflow.

## What / Why

- Plan first, then stage/commit by isolated intent.
- Keep commit history clean for review, bisect, and rollback.
- Enforce message quality with validator, tests, CI, and commit-msg hook.

## 30s Quick Try

### A) Install as an Agent Skill (recommended)

```bash
npx skills add cnkang/conventional-commit-batcher
npx skills list
```

Then ask your agent:

```text
I have mixed changes in my working tree. Create a commit plan first, wait for my confirmation, then commit in logical batches.
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

## Quick Start Paths

1. Agent flow: load this skill and follow `references/core-rules.md`.
2. Validator CLI: run `python3 scripts/validate_conventional_commit.py "feat(scope): add ..."`.
3. Hook flow: use the hook script above (or `references/commit-msg-hook-example.md`).

## Agent-Specific Setup

Use these docs only when you need tool-specific setup details:

- Codex: `references/codex-setup.md`
- Claude Code: `references/claude-setup.md`
- Kiro CLI: `references/kiro-setup.md`
- Kimi CLI: `references/kimi-setup.md`
- Qwen Code: `references/qwen-setup.md`
- Gemini CLI: `references/gemini-setup.md`

## Core Workflow Contract

The canonical rules live in one file: `references/core-rules.md`.

All loaders route to this file:

- `SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.claude/agents/conventional-commit-batcher.md`
- `.claude/commands/commit-batch.md`
- `.kiro/agents/conventional-commit-batcher.json`
- `.kiro/prompts/conventional-commit-batcher.md`
- `.kiro/steering/commit-batching.md`
- `.agents/skills/conventional-commit-batcher/SKILL.md`
- `.agents/agents/conventional-commit-batcher.md`
- `agents/openai.yaml`

## Validation and CI

`/.github/workflows/ci.yml` runs:

- Python syntax check (`py_compile`)
- Lint checks (`ruff check`)
- Format checks (`ruff format --check`)
- Unit tests (`pytest`)
- CLI simulation checks (valid/invalid messages)
- End-to-end `commit-msg` hook simulation in a temporary git repository

## Release and Versioning

- `SKILL.md` version is currently `1.0.0`.
- Create a matching git tag for releases: `v<skill-version>`.
- Pushing `v*` tags triggers automatic GitHub Release creation via `/.github/workflows/release.yml`.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Community and Feedback

- Bug reports and feature requests: GitHub Issues (templates included in `/.github/ISSUE_TEMPLATE/`)
- Product discussion and usage ideas: GitHub Discussions

## License

Apache-2.0 (`LICENSE`)
