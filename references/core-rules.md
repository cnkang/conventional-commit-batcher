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

## Batch Decision Rubric (5 Lines)

1. If primary intent differs, split commits.
2. If acceptance criteria differs, split commits.
3. If rollback decision differs, split commits.
4. If release timing differs, split commits.
5. If all four are the same, keep one cohesive commit.

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

## Sensitive Data Gate (Required)

Before every commit attempt, inspect staged file names and staged diff for
sensitive data risk.

High-risk file/path indicators (examples):

- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.p12`, `*.jks`
- `id_rsa`, `id_dsa`, `id_ed25519`
- files/paths containing `secret`, `secrets`, `credential`, `credentials`,
  `token`, `password`

High-risk content indicators (examples):

- `BEGIN ... PRIVATE KEY`
- `api_key`, `access_token`, `secret_key`, `client_secret`
- hardcoded password-like values in config or source

Hard requirement:

- If any high-risk indicator appears in a planned or staged batch, stop and ask
  user for explicit confirmation before commit.
- Do not proceed with `git commit` until user confirms those files/hunks are
  intentional.
- If user says accidental inclusion, unstage/remove the risky parts and update
  the plan before continuing.

## Ignore Rules Gate (Required)

Before staging and before each commit, verify that local-only or generated files
are not accidentally included.

Required checks:

```bash
git status --short --untracked-files=all
git ls-files --others --exclude-standard
```

Hard requirement:

- Cross-check staged files against `.gitignore` intent (local configs, caches,
  env files, temp/build artifacts).
- If a file looks local-only, generated, or environment-specific, stop and ask
  user to confirm whether it should be committed.
- If it should not be committed, remove it from staging immediately.
- If ignore rules are missing, update `.gitignore` (usually as a separate
  `chore` commit).
- If a tracked file should become ignored, untrack it first (for example
  `git rm --cached <path>`) and then update `.gitignore`.

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
- If sensitive-file or secret-risk indicators exist, require explicit user
  confirmation for those files/hunks before commit.
- If local-only/generated files appear in staged candidates, require explicit
  user confirmation before commit.

## Batching Rules

- Keep one commit for one purpose.
- File type alone is not a batch boundary signal.
- Even when files are all docs or all code, split batches if their intent,
  audience, or rule contract differs.
- If two changes are governed by different rules or acceptance criteria,
  they must be separate commits.
- Split by rollback unit: if one part may be reverted without reverting the
  other, they must not share one commit.
- Split by validation path: if changes rely on different checks
  (for example runtime tests vs docs/lint/hook rules), separate commits.
- Split by release timing: if one part can ship now and another should wait,
  separate commits.
- Do not over-split: if intent, acceptance criteria, rollback need, and release
  timing are the same, keep changes in one commit.
- Separate formatting-only edits from behavior changes.
- Separate refactor from fix unless inseparable.
- Keep tests with the behavior they validate.
- Group lockfile updates with the dependency change that requires them.
- Place prerequisite commits first
  (refactor before feature, feature before docs).

Before finalizing each batch, verify all answers are "yes":

- Same primary intent?
- Same acceptance criteria?
- Same rollback need?
- Same release timing?

If any answer is "no", split into different commits.
If all answers are "yes", prefer one cohesive commit.

Reject:

- one large mixed commit
- unrelated files in same commit without shared purpose
- bundling different rule contracts into one commit just because file type matches
- mixing user-facing docs with agent/skill contract updates in one docs commit
- mixing mechanical formatting with behavioral code changes in one code commit
- mixing CI/release pipeline edits with product/runtime behavior changes
- splitting one cohesive logical change into many tiny file-based commits
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

Run sensitive data checks on staged changes:

```bash
git diff --cached --name-only
git diff --cached
```

If risk indicators are detected, pause and ask user explicitly:

```text
[Sensitive Data Confirmation Required]
Potentially sensitive files/hunks detected in this batch:
- <path-or-hunk-summary>

Please confirm these are intentional and safe to commit.
Reply with explicit confirmation before I continue.
```

Run ignore/local-artifact checks:

```bash
git status --short --untracked-files=all
git diff --cached --name-only
```

If local-only or generated files are detected, pause and ask user explicitly:

```text
[Ignore Rule Confirmation Required]
Potentially local-only/generated files detected:
- <path>

These may belong in `.gitignore` instead of git history.
Please confirm whether to commit or exclude them.
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
