---
description: Split mixed git changes into Conventional Commit batches and execute directly.
---

Use the `conventional-commit-batcher` subagent for this task.

Default behavior is auto-execute: inspect, split, run safety gates, and commit
directly. Only output the plan and wait for confirmation if the user explicitly
asks to review the plan first.

If the subagent is unavailable, execute directly but still read and follow:

- `references/core-rules.md`

Optional user constraints: $ARGUMENTS

