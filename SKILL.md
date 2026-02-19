---
name: conventional-commit-batcher
version: 1.0.0
description: Inspect Git working tree changes, split mixed diffs into logically coherent commit batches, and produce validated English Conventional Commit messages with safe staging. Use when an AI coding agent needs to clean up mixed changes, prepare reviewable history before a PR, or perform staged commits without mixing unrelated intents.
---

# Conventional Commit Batcher

Use this skill to turn mixed changes into a clean, reviewable commit history.

## Single Source of Truth

- Always load and follow `references/core-rules.md` before any `git add` or `git commit`.
- Treat `references/core-rules.md` as the only authoritative rule set.
- Do not duplicate or redefine core workflow rules in other files.

## Cross-Loader Compatibility

- Codex entrypoint: this `SKILL.md`.
- Codex CLI repository entrypoint: `AGENTS.md`.
- Claude entrypoints:
  - `CLAUDE.md` (project-level instructions)
  - `.claude/agents/conventional-commit-batcher.md`
  - `.claude/commands/commit-batch.md`
- Kiro CLI entrypoint:
  - `.kiro/agents/conventional-commit-batcher.json`
  - `.kiro/steering/commit-batching.md` (auto-loaded context)
- Shared Agent Skills entrypoints (Kimi / Qwen / Gemini):
  - `.agents/skills/conventional-commit-batcher/SKILL.md` (skill)
  - `.agents/agents/conventional-commit-batcher.md` (subagent)
- OpenAI entrypoint:
  - `agents/openai.yaml`
- All entrypoints delegate to `references/core-rules.md`, so one rule file serves all systems.

## Note on `.agents/` directories

This repository uses `.agents/skills/` + `.agents/agents/` as the shared project-level path for Kimi, Qwen Code, and Gemini CLI. Claude Code and Kiro CLI still require their own native directories.

## Resources

- Canonical workflow and constraints: `references/core-rules.md`
- Codex CLI repo loader: `AGENTS.md`
- Claude project instructions: `CLAUDE.md`
- Claude loaders: `.claude/agents/conventional-commit-batcher.md`, `.claude/commands/commit-batch.md`
- Kiro loader: `.kiro/agents/conventional-commit-batcher.json`
- Kiro steering: `.kiro/steering/commit-batching.md`
- Shared skill (Kimi / Qwen / Gemini): `.agents/skills/conventional-commit-batcher/SKILL.md`
- Shared subagent (Qwen / Gemini): `.agents/agents/conventional-commit-batcher.md`
- OpenAI loader: `agents/openai.yaml`
- Commit splitting examples: `references/plan-examples.md`
- Additional guidance: `references/commit-batching-guide.md`
- commit-msg hook example: `references/commit-msg-hook-example.md`
- Codex setup notes: `references/codex-setup.md`
- Claude setup notes: `references/claude-setup.md`
- Kiro setup notes: `references/kiro-setup.md`
- Qwen Code setup notes: `references/qwen-setup.md`
- Gemini CLI setup notes: `references/gemini-setup.md`
- Kimi CLI setup notes: `references/kimi-setup.md`
- Validator: `scripts/validate_conventional_commit.py`
- Validator tests: `scripts/test_validate_conventional_commit.py`
