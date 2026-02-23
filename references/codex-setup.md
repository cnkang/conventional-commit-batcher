# Codex CLI Setup

This project supports two Codex loading paths.

## Automatic commit interception

Once loaded, the skill intercepts ALL commit-related operations automatically.
The agent cannot run `git add`, `git commit`, or `git push` without first
producing a Commit Plan and running safety gates. This applies whether the user
explicitly asks for batching or simply says "commit my changes".

## Skill mode

Use `SKILL.md` as the Codex skill entrypoint.
The skill immediately routes execution to:

- `references/core-rules.md`

## Repository mode (Codex CLI)

Codex reads repository guidance from:

- `AGENTS.md`

`AGENTS.md` instructs Codex to load:

1. `SKILL.md`
2. `references/core-rules.md`

So both modes use the same rule source.
