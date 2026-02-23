# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-10b981)](https://github.com/cnkang/conventional-commit-batcher/releases)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[English](README.md)

![conventional-commit-batcher 社交预览图](assets/social-preview.png)

把混杂改动整理成清晰、可审查、可回滚的 Conventional Commit 批次。

## 自动拦截所有提交操作

安装后，本 skill 会自动拦截所有与提交相关的操作，而不仅仅是用户明确要求"拆分提交"时才生效。
当 agent 检测到任何 `git add`、`git commit` 或 `git push` 意图时，必须先走计划优先的工作流，
再执行任何 git 命令。

具体表现：
- 对 agent 说"帮我提交一下"就会触发完整流程。
- agent 会自动拆分批次、运行安全门禁、直接提交，默认不需要用户确认。
- 如果想在执行前先看计划，需要明确告诉 agent"先给我看提交计划"。
- 安全门禁（敏感数据、冲突标记、受保护分支等）触发时仍然需要用户确认，不受执行模式影响。

该行为通过各平台的入口文件在所有支持的平台（Codex、Claude Code、Kiro、Kimi、Qwen、
Gemini、OpenAI）上统一强制执行。

## 为什么用这个 Skill

- 先计划后提交，避免误把不相关改动提交在一起。
- 批次边界清晰，评审、回滚、`git bisect` 都更安全。
- 自动约束提交消息，减少人工校验负担。
- 内置提交前安全门禁，提前拦截高风险误操作。

## 适合谁

- PR 前工作区改动已经混杂的研发同学。
- 希望提交历史更干净、便于变更追踪的团队。
- 需要稳定提交流程的 agent 驱动开发场景。

## 30 秒快速试用

### A) 作为 Agent Skill 安装（推荐）

```bash
npx skills add cnkang/conventional-commit-batcher
npx skills list
```

然后对 agent 说：

```text
我现在工作区里有混杂改动，帮我用 Conventional Commit 提交。
```

agent 会自动检查、拆分、提交。如果想先看计划再执行：

```text
我现在工作区里有混杂改动。
先给我看提交计划，确认后再执行。
```

### B) 只用 git hook（不依赖 agent）

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

cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

python3 scripts/precommit_safety_gate.py
HOOK

chmod +x .git/hooks/pre-commit
```

## 你应该看到什么输出

默认情况下，skill 会自动执行：检查改动、拆分批次、运行安全门禁、直接提交。
每个批次提交后会报告提交内容。

如果想在执行前先看计划，明确要求即可：

```text
先给我看提交计划，确认后再执行。
```

在计划优先模式下，skill 会输出完整计划并等待确认：

```text
Commit Plan
Batch #1: feat(scope): ...
Intent: ...
Files/Hunks:
- ...
Staging commands:
- git add ...
Commit command:
- git commit -m "feat(scope): ..."
```

## 内置安全门禁

这个 skill 会在提交前检查新手常见误操作：

- 敏感信息（密钥、token、密码）误入提交
- 本地/生成文件误入版本历史（`.gitignore` 漏配）
- 误在受保护或发布分支上提交
- 暂存区残留冲突标记
- 二进制或大文件误提交
- 暂存区为空却执行提交

这些检查由 `scripts/precommit_safety_gate.py` 在每次提交前执行：

```bash
python3 scripts/precommit_safety_gate.py
```

- 返回 `0`：通过
- 返回 `2`：需要用户明确确认后再继续
- 返回 `3`：硬阻断，必须先修复

如果环境没有 Python，agent 必须按
[`references/core-rules.md`](references/core-rules.md) 中的手工 `git` 检查命令逐条执行，
并保持相同的拦截/确认策略。

## 为什么有脚本 + 无 Python 怎么办

- 不必强依赖 Python：Python 脚本是优先方案，不是唯一方案。
- 脚本的作用：把规则程序化，能做回归测试，并可复用到 hook/CI。
- 没有 Python 时：agent 按
  [`references/core-rules.md`](references/core-rules.md) 的同一套 `git` 命令逐条检查，
  并以相同方式输出结果、要求确认或阻断提交。
- 两种模式下，若命中敏感指示，会输出触发文件路径、命中片段，并给出“请先检查这些文件”的建议。

## 什么时候用 / 不用

建议使用：

- 通过 agent 执行任何提交操作时（自动拦截）
- 一个分支里混有多种意图（`feat` + `fix` + `docs` + `style`）
- 需要在 PR 前得到可审查的提交边界
- 希望团队提交历史一致、可追踪

可以跳过：

- 只有一个很小且单一意图改动
- 当前任务不依赖提交历史治理

注意：即使改动很简单可以跳过，只要 skill 已安装，agent 仍会输出 Commit Plan 并运行安全门禁。
计划可能只包含一个批次，这完全正常。

## 快速入口

1. Agent 流程：加载 skill，按 [`references/core-rules.md`](references/core-rules.md) 执行。
2. 提交消息校验：`python3 scripts/validate_conventional_commit.py "feat(scope): add ..."`。
3. 安全门禁校验（6 项）：`python3 scripts/precommit_safety_gate.py`。
4. 无 Python 回退：执行 [`references/core-rules.md`](references/core-rules.md) 的手工门禁命令。
5. Hook 流程：使用上面的脚本（或 [`references/commit-msg-hook-example.md`](references/commit-msg-hook-example.md)）。

## Commit 消息语言策略

- commit 消息文本（subject/body/footer）默认使用英语。
- 若用户明确要求其他语言，subject/body/footer 的文本可使用用户指定语言。
- Conventional Commit 语法标记保持标准且不翻译：`type`、可选 `scope`、`!`、`BREAKING CHANGE:`。
- 以 [`references/core-rules.md`](references/core-rules.md) 为唯一权威规则来源。
- 本节为非权威摘要；`references/core-rules.md` 才是唯一事实来源。

## Commit 正文最佳实践

- 正文可选：当标题不足以说明上下文时再填写。
- 保持简洁高信息密度：说明关键“改了什么、为什么改/影响什么”。
- 避免堆砌无意义文字，确保人类读者快速理解。
- 对于非常简单、标题已足够说明的改动，正文可留空。

## Agent 专项安装文档

只在需要工具接入细节时查看：

- Codex: [`references/codex-setup.md`](references/codex-setup.md)
- Claude Code: [`references/claude-setup.md`](references/claude-setup.md)
- Kiro CLI: [`references/kiro-setup.md`](references/kiro-setup.md)
- Kimi CLI: [`references/kimi-setup.md`](references/kimi-setup.md)
- Qwen Code: [`references/qwen-setup.md`](references/qwen-setup.md)
- Gemini CLI: [`references/gemini-setup.md`](references/gemini-setup.md)

## 核心规则来源

所有入口都委托到一个权威规则文件：

- [`references/core-rules.md`](references/core-rules.md)

## 社区与反馈

- Bug / 功能建议：GitHub Issues（[`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/)）
- 使用讨论 / 方案交流：GitHub Discussions

## License

[Apache-2.0](LICENSE)
