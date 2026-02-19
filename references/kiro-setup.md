# Kiro CLI Setup

This repository already includes a local Kiro agent definition:

- `.kiro/agents/conventional-commit-batcher.json`
- `.kiro/prompts/conventional-commit-batcher.md`

The prompt always points execution to the canonical rules file:

- `references/core-rules.md`

## Use in this repository

Open this repository in Kiro CLI and invoke the local agent:

- `conventional-commit-batcher`

## Reuse in another repository

From target repository root:

```bash
mkdir -p .kiro/agents .kiro/prompts
cp <path-to-conventional-commit-batcher>/.kiro/agents/conventional-commit-batcher.json .kiro/agents/
cp <path-to-conventional-commit-batcher>/.kiro/prompts/conventional-commit-batcher.md .kiro/prompts/
```

Then also copy rule/script files if the target repo does not already have them:

```bash
mkdir -p references scripts
cp <path-to-conventional-commit-batcher>/references/core-rules.md references/
cp <path-to-conventional-commit-batcher>/scripts/validate_conventional_commit.py scripts/
```
