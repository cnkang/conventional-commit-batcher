# Kimi CLI Setup

This repository already includes a local Kimi CLI skill definition:

- `.agents/skills/conventional-commit-batcher/SKILL.md` (recommended project-level path)

The skill always points execution to the canonical rules file:

- `references/core-rules.md`

## Automatic commit interception

Once the skill is discovered, it intercepts ALL commit-related operations
automatically. The agent cannot run `git add`, `git commit`, or `git push`
without first producing a Commit Plan and running safety gates. This applies
whether the user explicitly asks for batching or simply says "commit my
changes".

## Use in this repository

Open this repository in Kimi CLI. The skill is discovered automatically.

- Skill (auto-discovered): `conventional-commit-batcher`
- Slash command: `/skill:conventional-commit-batcher`

## Reuse in another repository

From target repository root:

```bash
mkdir -p .agents/skills/conventional-commit-batcher
cp <path-to-conventional-commit-batcher>/.agents/skills/conventional-commit-batcher/SKILL.md \
  .agents/skills/conventional-commit-batcher/
```

Then also copy rule/script files if the target repo does not already have them:

```bash
mkdir -p references scripts
cp <path-to-conventional-commit-batcher>/references/core-rules.md references/
cp <path-to-conventional-commit-batcher>/scripts/validate_conventional_commit.py scripts/
```

## Note on skill discovery

Kimi CLI discovers project-level skills from the first existing directory among:

1. `.agents/skills/` (recommended, used by this repository)
2. `.kimi/skills/`
3. `.claude/skills/`
4. `.codex/skills/`

If your target repository already uses a different path, place the skill directory there instead.
