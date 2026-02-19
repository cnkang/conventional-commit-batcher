# Commit Plan Examples

## Example 1: Mixed Diff -> 3 Batches

Context:

- `src/auth/service.ts` adds refresh-token rotation
- `src/auth/service.test.ts` adds tests
- `docs/auth.md` updates docs

Plan:

```text
Commit Plan
Batch #1: feat(auth): add refresh token rotation
Intent: ship auth behavior change independently
Files/Hunks:
- src/auth/service.ts (behavior change)
Staging commands:
- git add src/auth/service.ts
Commit command:
- git commit -m "feat(auth): add refresh token rotation"

Batch #2: test(auth): cover refresh token rotation flows
Intent: keep tests reviewable and tied to auth change
Files/Hunks:
- src/auth/service.test.ts (new and updated test cases)
Staging commands:
- git add src/auth/service.test.ts
Commit command:
- git commit -m "test(auth): cover refresh token rotation flows"

Batch #3: docs(auth): document refresh token behavior
Intent: separate developer-facing docs from runtime code
Files/Hunks:
- docs/auth.md (docs-only update)
Staging commands:
- git add docs/auth.md
Commit command:
- git commit -m "docs(auth): document refresh token behavior"
```

## Example 2: Refactor + Fix Split

Context:

- `src/parser/` has file moves + function rename
- one edge-case bug fix is mixed in `src/parser/reader.ts`

Plan:

```text
Commit Plan
Batch #1: refactor(parser): split reader utilities by concern
Intent: isolate mechanical restructuring with no behavior change
Files/Hunks:
- src/parser/index.ts (imports + exports only)
- src/parser/utils/*.ts (new module boundaries)
- src/parser/reader.ts (refactor hunks only via git add -p)
Staging commands:
- git add src/parser/index.ts src/parser/utils/*.ts
- git add -p src/parser/reader.ts
Commit command:
- git commit -m "refactor(parser): split reader utilities by concern"

Batch #2: fix(parser): handle trailing delimiter in empty blocks
Intent: capture bug fix separately for bisect/revert safety
Files/Hunks:
- src/parser/reader.ts (bug-fix hunk only)
- src/parser/reader.test.ts (targeted regression test)
Staging commands:
- git add -p src/parser/reader.ts
- git add src/parser/reader.test.ts
Commit command:
- git commit -m "fix(parser): handle trailing delimiter in empty blocks"
```

## Example 3: Dependency + Lockfile Pairing

Context:

- `package.json` adds `zod`
- `pnpm-lock.yaml` changes accordingly
- unrelated lint reformat appears in `src/app.ts`

Plan:

```text
Commit Plan
Batch #1: build(deps): add zod for schema validation
Intent: keep dependency intent and lockfile update atomic
Files/Hunks:
- package.json (dependency declaration)
- pnpm-lock.yaml (resolver output tied to package.json)
Staging commands:
- git add package.json pnpm-lock.yaml
Commit command:
- git commit -m "build(deps): add zod for schema validation"

Batch #2: style(app): normalize lint formatting
Intent: keep no-op formatting separate from dependency change
Files/Hunks:
- src/app.ts (format-only changes)
Staging commands:
- git add src/app.ts
Commit command:
- git commit -m "style(app): normalize lint formatting"
```
