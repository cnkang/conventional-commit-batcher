# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[中文文档](README.zh-CN.md)

Split mixed changes into reviewable, revertible, traceable Conventional Commit batches with an agent-first, mandatory plan-first workflow.

Also works in Codex, Claude Code, Kiro CLI, Kimi CLI, Qwen Code, and Gemini CLI.

## Agent Skill Purpose

This repository is a reusable **agent skill** for commit hygiene.

- Built for AI agents to produce standards-compliant Conventional Commits
- Enforces plan-first batching before any `git add` / `git commit`
- Validates commit message quality with scriptable checks and CI

## 30s Quick Demo

### Before

- One large mixed commit (feature + fix + refactor + docs)
- Review is noisy and revert is risky

### After

- Generate `Commit Plan` first
- Execute isolated commit batches only after confirmation
- Keep `feat` / `fix` / `refactor` / `docs` / `chore` easy to review and rollback

```text
Commit Plan
Batch #1: feat(auth): add refresh token rotation
Batch #2: test(auth): cover refresh token rotation flows
Batch #3: docs(auth): document refresh token behavior
```

```bash
# Ask your agent to run conventional-commit-batcher in "plan only" mode.
# Review the plan, then execute the suggested staging/commit commands.
git add ...
git commit -m "feat(...): ..."
```

## Install in 30 Seconds

### Recommended: skills.sh

- Install via [`npx skills`](https://skills.sh), then search/install `conventional-commit-batcher`
- Use the same skill across Codex / Claude Code / Gemini CLI / Qwen Code / Kimi CLI / Kiro

### Manual Install

- Clone or copy this repository into your environment
- Choose the matching agent entrypoint from the Quick Start section below
- Always read `references/core-rules.md` before execution

## Why Teams Share This

- **Plan-first commit batching**: output `Commit Plan` first, then execute after explicit confirmation
- **Single source of truth**: rules only live in `references/core-rules.md`
- **Executable validation**: validator + tests + CI + hook simulation keep the standard enforceable

## Three Real Examples

1. `feat` + `test` + `docs` split for auth refresh token work
2. `refactor` and `fix` split to isolate mechanical changes from behavior fixes
3. `build(deps)` dependency + lockfile pairing, with unrelated `style` changes separated

Full plans: [`references/plan-examples.md`](references/plan-examples.md)

## Problem

Common pain points after a development session:

- A single commit mixes features, refactors, formatting, and docs
- Non-standard commit messages break changelog generation and automated releases
- Inconsistent batch boundaries when splitting commits manually or with AI

This project converges these operations into a unified workflow with an executable validator.

## Quick Start

### Codex

- Skill mode: load `SKILL.md`, trigger `conventional-commit-batcher`
- Repo mode (Codex CLI): auto-read `AGENTS.md`
- Both modes require reading `references/core-rules.md` first

### Claude Code

Built-in `.claude/agents` and `.claude/commands` are ready to use:

- Subagent: `conventional-commit-batcher`
- Slash command: `/project:commit-batch`

### Kiro CLI

Built-in `.kiro/agents` and `.kiro/prompts`:

- Agent: `conventional-commit-batcher`
- Config: `.kiro/agents/conventional-commit-batcher.json`
- Rules: `references/core-rules.md`

### Qwen Code

Built-in `.agents/skills` and `.agents/agents`, auto-discovered by Qwen:

- Skill (model-invoked): `conventional-commit-batcher`
- SubAgent (explicit or auto-delegated): `conventional-commit-batcher`
- Rules: `references/core-rules.md`

### Gemini CLI

Built-in `.agents/skills` and `.agents/agents`, auto-discovered by Gemini:

- Skill (model-invoked): `conventional-commit-batcher`
- SubAgent (explicit or auto-delegated): `conventional-commit-batcher`
- Rules: `references/core-rules.md`

### Kimi CLI

Built-in `.agents/skills`, auto-discovered:

- Skill (auto-discovered): `conventional-commit-batcher`
- Slash command: `/skill:conventional-commit-batcher`
- Rules: `references/core-rules.md`

## Project Structure

- `references/core-rules.md`: single source of truth (canonical rules)
- `SKILL.md`: Codex skill entrypoint (thin wrapper, delegates to core rules)
- `AGENTS.md`: Codex CLI repository-level loader
- `CLAUDE.md`: Claude Code project-level instructions
- `.claude/agents/conventional-commit-batcher.md`: Claude Code subagent
- `.claude/commands/commit-batch.md`: Claude Code slash command
- `.kiro/agents/conventional-commit-batcher.json`: Kiro agent
- `.kiro/prompts/conventional-commit-batcher.md`: Kiro prompt
- `.kiro/steering/commit-batching.md`: Kiro auto-loaded steering rules
- `.agents/skills/conventional-commit-batcher/SKILL.md`: shared skill entrypoint (Kimi/Qwen/Gemini)
- `.agents/agents/conventional-commit-batcher.md`: shared subagent entrypoint (Qwen/Gemini)
- `.github/workflows/ci.yml`: GitHub Actions CI (checks + simulations)
- `agents/openai.yaml`: OpenAI agent
- `scripts/validate_conventional_commit.py`: Conventional Commit validator
- `scripts/test_validate_conventional_commit.py`: validator unit tests
- `references/plan-examples.md`: batch splitting examples
- `references/codex-setup.md` / `references/claude-setup.md` / `references/kiro-setup.md` / `references/kimi-setup.md` / `references/qwen-setup.md` / `references/gemini-setup.md`: cross-repo reuse guides

## Validator Example

```bash
python3 scripts/validate_conventional_commit.py \
  --max-subject-length 72 \
  --max-header-length 100 \
  "feat(auth): add refresh token rotation"
```

## CI

`/.github/workflows/ci.yml` runs:

- Python syntax check (`py_compile`)
- Unit tests (`pytest`)
- CLI simulation checks for valid/invalid commit messages
- End-to-end `commit-msg` hook simulation in a temporary git repository

## Design Principles

- One rule set, multiple entrypoints
- Entrypoint files only route; they never duplicate core rules
- Rule changes only touch `references/core-rules.md`
