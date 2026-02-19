# Repository Guidelines

This repository provides a cross-CLI commit batching skill.

## Single Rule Source

- Always treat `references/core-rules.md` as the authoritative workflow.
- Do not duplicate or redefine commit batching rules in loader files.

## Codex CLI Loader

- Codex skill entry: `SKILL.md`
- In repository mode, follow this sequence:
  1. Read `SKILL.md`
  2. Read `references/core-rules.md`
  3. Execute commit batching per required plan-first contract

## Cross-CLI Entrypoints

- Codex: `SKILL.md`
- Claude Code: `CLAUDE.md`, `.claude/agents/conventional-commit-batcher.md`, `.claude/commands/commit-batch.md`
- Kiro CLI: `.kiro/agents/conventional-commit-batcher.json`, `.kiro/steering/commit-batching.md`
- Kimi CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`
- Qwen Code: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- Gemini CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- OpenAI: `agents/openai.yaml`

All entrypoints must delegate to `references/core-rules.md`.
