# Project Instructions

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

## Cross-CLI Entrypoints

- Codex: `SKILL.md`, `AGENTS.md`
- Claude Code: `.claude/agents/conventional-commit-batcher.md`, `.claude/commands/commit-batch.md`
- Kiro CLI: `.kiro/agents/conventional-commit-batcher.json`, `.kiro/steering/commit-batching.md`
- Kimi CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`
- Qwen Code: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- Gemini CLI: `.agents/skills/conventional-commit-batcher/SKILL.md`, `.agents/agents/conventional-commit-batcher.md`
- OpenAI: `agents/openai.yaml`

All entrypoints delegate to `references/core-rules.md`.
