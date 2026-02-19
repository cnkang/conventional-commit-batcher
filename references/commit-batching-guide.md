# Commit Batching Guide

## Decide Batch Boundaries

Use a new batch when any of these changes differ:

- purpose (feature vs fix vs cleanup)
- risk level (safe rename vs behavior change)
- audience (code change vs documentation)
- deployment impact (runtime code vs CI/tooling)

## Same File Type, Different Intent

Do not merge changes into one commit just because they are all `.md` or all
source code files.

Split into separate commits when one of these differs:

- rule contract (for example public README guidance vs skill/agent behavior contract)
- acceptance criteria (for example user-facing clarity vs strict execution behavior)
- target audience (for example end users vs maintainers/agents)

Quick check:

- if each part would have a different commit subject, split it
- if each part could be reverted independently, split it

Common wrong merges to avoid:

- public README copy updates + `SKILL.md` behavior contract updates
- runtime bug fix + CI workflow pipeline edits
- pure formatting/refactor sweep + behavior change in same touched files
- dependency/changelog docs update + unrelated feature docs update

## Avoid Over-Splitting

Do not split by file count or directory shape alone.

Keep changes in one commit when all are true:

- same primary intent
- same acceptance criteria
- same rollback decision
- same release timing

Common over-splitting to avoid:

- splitting one feature across multiple commits with no independent value
- splitting code and directly coupled tests when they should ship together
- splitting one cohesive docs update into many file-by-file commits

## Recommended Commit Order

1. Mechanical prep (`refactor`, `chore`, or `style`)
2. Main behavior (`feat`, `fix`, `perf`)
3. Tests (`test`) if not bundled with behavior commit
4. Docs (`docs`)
5. CI/build follow-up (`ci`, `build`)

## Header Examples

- `feat(auth): add refresh token rotation`
- `fix(api): handle empty pagination cursor`
- `refactor(core): split parser into modules`
- `test(cache): add eviction edge cases`
- `docs(readme): clarify local setup steps`

## Pre-commit Hook Policy

- Always run `git commit` without `--no-verify` when commit-time checks are configured.
- Treat configured commit-time checks (for example `pre-commit`, `commit-msg`, Husky, lint-staged) as mandatory gates.
- If no commit-time checks are configured, continue normal batching.
- If any configured check fails, stop batching and notify the user immediately with failing output.

## Failure Report Essentials

When checks fail, include these fields so users can forward context to AI/Agent directly:

- repository absolute path and branch
- attempted commit message header
- failed check name, failing command, and exit code
- concise error excerpt (first relevant lines, avoid full noisy log)
- `git status --short` and `git diff --cached --stat` outputs
- exact reproduction command
- one concrete suggested next action

## Body and Footer Examples

Body example:

```text
Align parser output with v2 AST schema.
Retain backward compatibility for existing plugins.
```

Footer examples:

```text
Refs: #123
```

```text
BREAKING CHANGE: remove deprecated /v1/search endpoint.
```
