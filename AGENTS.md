# Repository Guidelines

This repository provides a cross-CLI commit batching skill.

## Commit Interception (MANDATORY)

When the user asks to commit, stage, push changes, or when you are about to run
`git add`, `git commit`, or `git push`, you MUST follow the commit batching
workflow defined in `references/core-rules.md` BEFORE executing any git
staging or commit command.

Do NOT run `git add` or `git commit` directly. Always:
1. Read `references/core-rules.md`
2. Inspect changes and split into logical batches
3. Run safety gates before each commit
4. **Auto-execute by default:** stage and commit directly
5. Only output the full Commit Plan and wait for confirmation if the user
   explicitly asks to review the plan first
6. Validate each commit message

This applies to ALL commit scenarios, not just when the user explicitly asks
for "batching".

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
