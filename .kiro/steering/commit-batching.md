---
inclusion: auto
---

# Commit Batching Rules

This repository uses an auto-execute commit batching workflow.

## Skill Activation (IMPORTANT)

When the user asks to commit, stage, push changes, or anything related to `git add` / `git commit` / `git push`, you MUST activate the `conventional-commit-batcher` skill FIRST before performing any git operations. This skill handles the full commit workflow including batching, validation, and safety checks.

Do NOT run `git add` or `git commit` directly without going through the skill's workflow.

## Default Behavior: Auto-Execute

By default, the skill inspects changes, splits into logical batches, runs safety gates, and commits directly — without waiting for user confirmation. Only pause and show the Commit Plan if the user explicitly asks to review the plan first.

## Canonical Rules

Before any `git add` or `git commit`, read and follow `references/core-rules.md`.
