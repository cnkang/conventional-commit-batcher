# Core Rules (Canonical)

This file is the single source of truth for commit batching behavior across:

- Codex
- Claude Code
- Kiro CLI
- Kimi CLI
- Qwen Code
- Gemini CLI
- OpenAI agents

## Execute Workflow

1. Inspect current repository state.
2. Produce a full Commit Plan in the required format.
3. Wait for explicit user confirmation.
4. Stage and commit one logical batch at a time.
5. Validate every commit message before each commit.
6. Run commit normally and let commit-time checks execute.
7. Re-check history and working tree after each batch.

## Inspect Repository State

Run:

```bash
git status --short
git diff --stat
git diff
```

If staged changes already exist, inspect both staged and unstaged:

```bash
git diff --cached --stat
git diff --cached
```

Classify each changed file by intent:

- behavior change (`feat`, `fix`, `perf`, `refactor`)
- tests (`test`)
- docs (`docs`)
- tooling or CI (`build`, `ci`, `chore`)
- formatting-only (`style`)

## Commit Plan Output Contract (Required)

Output this exact structure before any staging/commit:

```text
Commit Plan
Batch #1: <type(scope): subject>
Intent: <why this batch exists>
Files/Hunks:
- <path> (whole file | specific hunk intent)
Staging commands:
- git add <path>
- git add -p <path>   # when partial staging is needed
Commit command:
- git commit -m "<type(scope): subject>"

Batch #2: <...>
...
```

Hard gates:

- Do not run `git add` or `git commit` until user confirms the plan.
- If user requests plan changes, regenerate the full plan and wait for
  confirmation again.
- If intent boundaries are uncertain, ask for clarification before execution.

## Batching Rules

- Keep one commit for one purpose.
- Separate formatting-only edits from behavior changes.
- Separate refactor from fix unless inseparable.
- Keep tests with the behavior they validate.
- Group lockfile updates with the dependency change that requires them.
- Place prerequisite commits first
  (refactor before feature, feature before docs).

Reject:

- one large mixed commit
- unrelated files in same commit without shared purpose
- commit headers that do not match actual changes

## Stage and Commit Each Batch

Stage only the current batch:

```bash
git add <file1> <file2>
# or
git add -p
```

Verify staged content:

```bash
git diff --cached --stat
git diff --cached
```

Validate message:

```bash
python3 scripts/validate_conventional_commit.py \
  --max-subject-length 72 \
  --max-header-length 100 \
  "<type(scope): subject>"
```

Commit:

```bash
git commit -m "<type(scope): subject>"
```

After each batch, report:

- committed header
- staged file list included in commit
- what remains unstaged/uncommitted

## Commit-Time Checks Policy

- If repository defines commit-time checks (`pre-commit`, `commit-msg`, Husky,
  lint-staged), treat them as mandatory.
- Never use `git commit --no-verify` when checks are configured.
- If no checks are configured, continue normal commit flow.
- If any commit-time check fails:
  - stop further commit attempts immediately
  - report failure output to user quickly
  - wait for user decision before continuing

## Conventional Commit Rules

Allowed types:

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `perf`
- `test`
- `build`
- `ci`
- `chore`
- `revert`

Constraints:

- Header format: `<type>(<scope>)!: <subject>`
- Scope optional; validator supports `_` by default
- `!` optional and used for breaking changes
- Subject in English
- No trailing period in subject
- Subject max length default `72`
- Header max length default `100`
- If body/footer exists, keep one blank line after header

Breaking change rule:

- If message indicates breaking change, require either `!` in header
  or `BREAKING CHANGE:` footer.

Style warnings (default validator behavior):

- Subject starts lowercase when first letter is alphabetic
- Prefer imperative verb (`add`, `fix`, `remove`) over forms like
  `added`, `adding`, `fixed`

## Quality Checks

After each commit:

```bash
git log --oneline -n 5
```

After all batches:

```bash
git status --short
```

Expectations:

- commit order explains evolution clearly
- each commit is independently reviewable
- headers align with actual content
- no leftover partial staging mistakes

## Failure Feedback Template

When commit-time checks fail, return:

```text
[Commit Check Failure Report]
Repository: <absolute-path>
Branch: <branch-name>
Attempted Commit Header: <type(scope): subject>
Failed Check Name: <pre-commit | commit-msg | husky hook name | lint-staged task>
Failed Command: <exact command if visible>
Exit Code: <code or unknown>

Key Error (first 20-60 relevant lines):
<concise excerpt>

What Passed Before Failure:
- Conventional header validation: <pass/fail>
- Staged diff review: <done/not done>

Current Git State:
- `git status --short`
<output>
- `git diff --cached --stat`
<output>

Quick Reproduction:
1. <step>
2. <step>
3. `git commit -m "<same message>"`

Suggested Next Step:
<one concrete fix direction or request permission to investigate>
```

Minimum diagnostics:

- failing hook/check name and command
- exit code
- concise error excerpt
- staged state snapshot
- exact commit message used
