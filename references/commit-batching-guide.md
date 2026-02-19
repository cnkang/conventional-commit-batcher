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

## Sensitive Data Pre-Commit Check

Before each commit, run safety gates with the script (preferred):

```bash
python3 scripts/precommit_safety_gate.py
```

If Python is unavailable, run the manual checks below and apply the same
decision policy (`confirm` for risky cases, `block` for hard failures).

Script exit codes:

- `0`: pass
- `2`: explicit user confirmation required
- `3`: blocked, fix before commit

When a sensitive finding appears (script or manual fallback), report to user with:

- gate name (`Sensitive Data`)
- triggered files (exact paths)
- matched snippet examples
- concrete suggestion to review/remove/redact or explicitly confirm

Manual sensitive-data fallback checks:

Suggested checks:

```bash
git diff --cached --name-only | rg -i '(^|/)(\\.env(\\..*)?|id_rsa|id_dsa|id_ed25519)|\\.(pem|key|p12|jks)$|secret|credential|token|password'
git diff --cached | rg -i 'BEGIN .*PRIVATE KEY|api[_-]?key|access[_-]?token|secret[_-]?key|client[_-]?secret|password\\s*[:=]'
```

If any match appears:

- stop commit execution
- show matched file/hunk context briefly (with exact file paths)
- ask user for explicit confirmation that inclusion is intentional
- continue only after explicit confirmation

Recommended confirmation prompt:

```text
[Sensitive Data Confirmation Required]
Triggered files:
- <path>

Matched indicators:
- <path>: <snippet>

Please review these files. If this is accidental, I will unstage/redact first.
If intentional (for tests/docs/rules), reply with explicit confirmation.
```

If user says it was accidental:

- remove/unstage sensitive files or hunks
- update Commit Plan and staging commands
- re-run the checks before commit

## `.gitignore` and Local Artifact Check (Manual Fallback)

Before committing, verify local-only/generated files are not accidentally staged.

Suggested checks:

```bash
git status --short --untracked-files=all
git ls-files --others --exclude-standard
git diff --cached --name-only
```

Watch for typical accidental inclusions:

- local env/config files (`.env*`, local settings JSON)
- cache/state folders (`.cache`, tool state dirs, temp output)
- generated binaries/artifacts/logs
- machine-specific credentials or tokens

If detected:

- pause and ask user whether inclusion is intentional
- if not intentional, unstage/remove those files from commit
- if ignore coverage is missing, add rule in `.gitignore`
- prefer separate `chore` commit for `.gitignore` maintenance

## Beginner Safety Checks (Before Each Commit, Manual Fallback)

Run these checks to avoid common first-time mistakes:

```bash
git branch --show-current
git diff --cached | rg '^(<<<<<<< |=======|>>>>>>> )'
git diff --cached --numstat
git diff --cached --quiet
```

Interpretation:

- protected/release branch detected: ask for explicit confirmation first
- conflict marker match found: block commit and resolve conflicts
- unexpected large/binary artifact detected: ask for explicit confirmation
- `git diff --cached --quiet` exits `0`: nothing staged, do not run commit

Common beginner mistakes this prevents:

- committing on `main`/`master` unintentionally
- committing unresolved merge conflicts
- committing generated binaries/logs by mistake
- running `git commit` with an empty staged set

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
