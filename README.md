# conventional-commit-batcher

[中文文档](README.zh-CN.md)

Split mixed changes into reviewable, revertible, traceable Conventional Commit batches with a mandatory plan-first workflow.

## Problem

Common pain points after a development session:

- A single commit mixes features, refactors, formatting, and docs — hard to review
- Non-standard commit messages break changelog generation and automated releases
- Inconsistent batch boundaries when splitting commits manually or with AI

This project converges these operations into a unified workflow with an executable validator.

## Key Benefits

- Plan first: output a `Commit Plan`, execute only after explicit confirmation
- Single rule source: all rules live in `references/core-rules.md`
- Cross-agent consistency: Codex, Claude, Kiro, Kimi, Qwen Code, Gemini CLI all reference the same rule file
- Production-ready: includes commit message validator script and hook example
- Reviewable history: batches by intent, producing cleaner git history

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

## Quick Start

### Codex

- Skill mode: load `SKILL.md`, triggers `conventional-commit-batcher`
- Repo mode (Codex CLI): auto-reads `AGENTS.md`
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
- Entrypoint files only route — they never duplicate core rules
- Rule changes only touch `references/core-rules.md`
