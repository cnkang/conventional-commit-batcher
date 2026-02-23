# Claude Code Setup

This project is directly Claude-compatible because repository-level entrypoints are already included:

- `CLAUDE.md` (auto-loaded project instructions with commit interception rules)
- `.claude/agents/conventional-commit-batcher.md`
- `.claude/commands/commit-batch.md`

## Automatic commit interception

`CLAUDE.md` is loaded automatically by Claude Code for every session. It
contains a mandatory commit interception section that prevents the agent from
running `git add`, `git commit`, or `git push` without first following the
plan-first workflow. This means the skill activates for ANY commit operation,
not just when the user explicitly asks for batching.

Both agent and command entrypoints load the same canonical rules file:

- `references/core-rules.md`

No extra copy step is required when using Claude Code in this repository.

## Reuse in another repository

From the target repository root:

```bash
mkdir -p .claude/agents
cp <path-to-conventional-commit-batcher>/.claude/agents/conventional-commit-batcher.md \
  .claude/agents/conventional-commit-batcher.md
```

Use from Claude Code with a direct delegation prompt, for example:

```text
Use the conventional-commit-batcher subagent to split my current diff into logical commits.
```

## Optional: install slash command

```bash
mkdir -p .claude/commands
cp <path-to-conventional-commit-batcher>/.claude/commands/commit-batch.md \
  .claude/commands/commit-batch.md
```

Then run:

```text
/project:commit-batch
```

## Sync rule

When behavior changes, update only `references/core-rules.md`.
`SKILL.md`, `.claude/agents/*`, and `.claude/commands/*` should stay as thin loaders that point to this file.
