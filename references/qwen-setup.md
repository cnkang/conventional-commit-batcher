# Qwen Code Setup

This repository already includes shared Agent Skills definitions that Qwen Code auto-discovers:

- `.agents/agents/conventional-commit-batcher.md` (subagent)
- `.agents/skills/conventional-commit-batcher/SKILL.md` (skill)

Both point execution to the canonical rules file:

- `references/core-rules.md`

## Automatic commit interception

Once discovered, the skill and subagent intercept ALL commit-related operations
automatically. The agent cannot run `git add`, `git commit`, or `git push`
without first producing a Commit Plan and running safety gates. This applies
whether the user explicitly asks for batching or simply says "commit my
changes".

## Use in this repository

Open this repository in Qwen Code. The skill and subagent are discovered automatically.

- Skill: model-invoked when your request matches commit batching
- SubAgent: invoke explicitly or let the main AI delegate

## Reuse in another repository

From target repository root:

```bash
mkdir -p .agents/agents .agents/skills/conventional-commit-batcher
cp <path-to-conventional-commit-batcher>/.agents/agents/conventional-commit-batcher.md .agents/agents/
cp <path-to-conventional-commit-batcher>/.agents/skills/conventional-commit-batcher/SKILL.md .agents/skills/conventional-commit-batcher/
```

Then also copy rule/script files if the target repo does not already have them:

```bash
mkdir -p references scripts
cp <path-to-conventional-commit-batcher>/references/core-rules.md references/
cp <path-to-conventional-commit-batcher>/scripts/validate_conventional_commit.py scripts/
```

## Optional native directories

Qwen Code also supports native `.qwen/skills` and `.qwen/agents` directories. This repository uses `.agents/*` to reduce duplicate hidden directories across CLIs.
