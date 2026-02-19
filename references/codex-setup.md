# Codex CLI Setup

This project supports two Codex loading paths.

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
