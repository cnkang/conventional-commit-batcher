# Project Instructions

This repository provides a cross-CLI commit batching skill.

## Single Rule Source

- Always treat `references/core-rules.md` as the authoritative workflow.
- Do not duplicate or redefine commit batching rules in loader files.

## Cross-CLI Entrypoints

- Codex: `SKILL.md`, `AGENTS.md`
- Claude Code: `.claude/agents/conventional-commit-batcher.md`, `.claude/commands/commit-batch.md`
- Kiro CLI: `.kiro/agents/conventional-commit-batcher.json`, `.kiro/steering/commit-batching.md`
- Kimi CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`
- Qwen Code: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- Gemini CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- OpenAI: `agents/openai.yaml`

All entrypoints delegate to `references/core-rules.md`.
