# commit-msg Hook Example

Use this hook to enforce Conventional Commit validation during `git commit`.

`.git/hooks/commit-msg`:

```bash
#!/usr/bin/env bash
set -euo pipefail

MSG_FILE="$1"
SCRIPT_PATH="scripts/validate_conventional_commit.py"

if [ ! -f "$SCRIPT_PATH" ]; then
  echo "[commit-msg] validator not found: $SCRIPT_PATH"
  exit 1
fi

python3 "$SCRIPT_PATH" \
  --file "$MSG_FILE" \
  --max-subject-length 72 \
  --max-header-length 100
```

Make it executable:

```bash
chmod +x .git/hooks/commit-msg
```

Optional stricter mode:

```bash
python3 scripts/validate_conventional_commit.py \
  --file "$MSG_FILE" \
  --subject-lowercase-mode error \
  --imperative-mode error \
  --strict-scope
```

Optional `pre-commit` safety gate hook (covers sensitive/local-artefact/branch/conflict/large/empty checks):

`.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 scripts/precommit_safety_gate.py
```
