# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-10b981)](https://github.com/cnkang/conventional-commit-batcher/releases)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[English](README.md)

把混杂改动拆成可审查、可回滚、可追踪的 Conventional Commit 批次，并通过 agent-first、plan-first 工作流强制先计划后执行。

## What / Why

- 先产出计划，再按意图分批 `git add` / `git commit`。
- 历史更干净，评审、回滚、`git bisect` 更高效。
- 通过校验器、测试、CI、hook 形成可执行的提交规范。

## 30 秒快速试用

### A) 作为 Agent Skill 安装（推荐）

```bash
npx skills add cnkang/conventional-commit-batcher
npx skills list
```

然后对 agent 说：

```text
我现在工作区里有混杂改动。先输出 Commit Plan，等我确认后再按批次提交。
```

### B) 只用 commit-msg hook（不依赖 agent）

```bash
cat > .git/hooks/commit-msg <<'HOOK'
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
HOOK

chmod +x .git/hooks/commit-msg
```

## 快速入口

1. Agent 流程：加载 skill，按 `references/core-rules.md` 执行。
2. 校验 CLI：`python3 scripts/validate_conventional_commit.py "feat(scope): add ..."`。
3. Hook 流程：使用上面的脚本（或 `references/commit-msg-hook-example.md`）。

## Agent 专项安装文档

只有在你需要某个工具的接入细节时再看这些文档：

- Codex: `references/codex-setup.md`
- Claude Code: `references/claude-setup.md`
- Kiro CLI: `references/kiro-setup.md`
- Kimi CLI: `references/kimi-setup.md`
- Qwen Code: `references/qwen-setup.md`
- Gemini CLI: `references/gemini-setup.md`

## 核心规则与入口关系

唯一权威规则文件：`references/core-rules.md`。

所有入口都路由到这一个规则文件：

- `SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `.claude/agents/conventional-commit-batcher.md`
- `.claude/commands/commit-batch.md`
- `.kiro/agents/conventional-commit-batcher.json`
- `.kiro/prompts/conventional-commit-batcher.md`
- `.kiro/steering/commit-batching.md`
- `.agents/skills/conventional-commit-batcher/SKILL.md`
- `.agents/agents/conventional-commit-batcher.md`
- `agents/openai.yaml`

## 校验与 CI

`/.github/workflows/ci.yml` 会执行：

- Python 语法检查（`py_compile`）
- 静态检查（`ruff check`）
- 格式检查（`ruff format --check`）
- 单元测试（`pytest`）
- CLI 模拟（合法/非法提交信息）
- 临时仓库中的 `commit-msg` hook 端到端模拟

## Release 与版本对齐

- `SKILL.md` 当前版本是 `1.0.0`。
- 发布时建议打同版本标签：`v<skill-version>`。
- 推送 `v*` 标签后，会由 `/.github/workflows/release.yml` 自动创建 GitHub Release。

示例：

```bash
git tag v1.0.0
git push origin v1.0.0
```

## 社区与反馈

- Bug / 功能建议：GitHub Issues（已提供 Issue 模板）
- 使用讨论 / 方案交流：GitHub Discussions

## License

Apache-2.0（`LICENSE`）
