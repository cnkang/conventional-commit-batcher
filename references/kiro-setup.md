# Kiro CLI Setup

This repository already includes a local Kiro agent definition:

- `.kiro/agents/conventional-commit-batcher.json`
- `.kiro/prompts/conventional-commit-batcher.md`
- `.kiro/steering/commit-batching.md` (auto-loaded steering rules)
- `.kiro/hooks/guard-git-commit.json` (preToolUse hook for shell commands)

## Automatic commit interception

Kiro enforces commit interception through three layers:

1. **Steering file** (`.kiro/steering/commit-batching.md`): auto-included in
   every session, instructs the agent to activate the skill for any commit
   intent.
2. **preToolUse hook** (`.kiro/hooks/guard-git-commit.json`): intercepts shell
   commands before execution and blocks direct `git add`/`git commit`/`git push`
   unless the skill workflow has been followed.
3. **Agent prompt** (`.kiro/prompts/conventional-commit-batcher.md`): contains
   the mandatory interception section.

This means the agent cannot bypass the plan-first workflow regardless of how
the commit is initiated.

The prompt always points execution to the canonical rules file:

- `references/core-rules.md`

## Use in this repository

Open this repository in Kiro CLI and invoke the local agent:

- `conventional-commit-batcher`

## Reuse in another repository

From target repository root:

```bash
mkdir -p .kiro/agents .kiro/prompts .kiro/steering .kiro/hooks
cp <path-to-conventional-commit-batcher>/.kiro/agents/conventional-commit-batcher.json .kiro/agents/
cp <path-to-conventional-commit-batcher>/.kiro/prompts/conventional-commit-batcher.md .kiro/prompts/
cp <path-to-conventional-commit-batcher>/.kiro/steering/commit-batching.md .kiro/steering/
cp <path-to-conventional-commit-batcher>/.kiro/hooks/guard-git-commit.json .kiro/hooks/
```

Then also copy rule/script files if the target repo does not already have them:

```bash
mkdir -p references scripts
cp <path-to-conventional-commit-batcher>/references/core-rules.md references/
cp <path-to-conventional-commit-batcher>/scripts/validate_conventional_commit.py scripts/
```
