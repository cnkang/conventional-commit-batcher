---
name: conventional-commit-batcher
description: Auto-split mixed changes into logical commit batches with validated Conventional Commit messages. Activate when user wants to git add, git commit, stage, or push changes.
---

# Conventional Commit Batcher

Automatically organize mixed Git changes into logical, reviewable commits following Conventional Commit best practices.

## Commit Interception (MANDATORY)

This skill MUST be activated for ANY commit-related operation, including:
- user asks to commit, stage, or push changes
- user asks to "save" or "check in" code
- any workflow that would result in `git add`, `git commit`, or `git push`

Do NOT run `git add` or `git commit` directly. Always follow the full workflow
in `references/core-rules.md`: inspect, split into batches, run safety gates,
and execute. By default, execute directly without waiting for user confirmation.
Only output the plan and wait for confirmation if the user explicitly asks to
review the plan first.
