# conventional-commit-batcher

[English](README.md)

把"混杂改动"拆成可审查、可回滚、可追踪的 Conventional Commit 批次，并强制先出计划再执行提交。

## 这个项目解决什么问题

很多仓库在开发后会出现以下痛点：

- 一个提交里混了功能、重构、格式化、文档改动，评审困难
- 提交信息不规范，后续变更追踪和自动化发布受影响
- AI 或人工在拆分提交时边界不稳定，容易误混文件/误拆 hunk

这个项目把这些操作收敛为统一流程，并提供可执行校验脚本。

## 核心优势

- 计划先行：先输出 `Commit Plan`，确认后才允许 `git add`/`git commit`
- 单一规则源：核心规则只维护在 `references/core-rules.md`
- 跨 Agent 一致：Codex、Claude、Kiro、Kimi、Qwen Code、Gemini CLI 都引用同一规则文件，避免多处漂移
- 工程可落地：提供 commit message 校验脚本与 hook 示例
- 可审查历史：强制按意图分批，提交历史更清晰

## 对人和 AI 都友好的结构

- `references/core-rules.md`: 唯一权威规则（Single Source of Truth）
- `SKILL.md`: Codex 入口（薄封装，指向核心规则）
- `AGENTS.md`: Codex CLI 仓库级加载入口
- `CLAUDE.md`: Claude Code 项目级指令入口
- `.claude/agents/conventional-commit-batcher.md`: Claude 子代理入口
- `.claude/commands/commit-batch.md`: Claude 命令入口
- `.kiro/agents/conventional-commit-batcher.json`: Kiro agent 入口
- `.kiro/prompts/conventional-commit-batcher.md`: Kiro prompt 入口
- `.kiro/steering/commit-batching.md`: Kiro 自动加载的 steering 规则
- `.agents/skills/conventional-commit-batcher/SKILL.md`: 共享 skill 入口（Kimi/Qwen/Gemini）
- `.agents/agents/conventional-commit-batcher.md`: 共享子代理入口（Qwen/Gemini）
- `.github/workflows/ci.yml`: GitHub Actions CI（检查 + 模拟测试）
- `agents/openai.yaml`: OpenAI agent 入口
- `scripts/validate_conventional_commit.py`: Conventional Commit 校验器
- `scripts/test_validate_conventional_commit.py`: 校验器单元测试
- `references/plan-examples.md`: 典型拆分示例
- `references/codex-setup.md` / `references/claude-setup.md` / `references/kiro-setup.md` / `references/kimi-setup.md` / `references/qwen-setup.md` / `references/gemini-setup.md`: 跨仓库复用说明

## 快速使用

### Codex

- Skill 模式：加载 `SKILL.md`，触发 `conventional-commit-batcher`
- Repo 模式（Codex CLI）：自动读取 `AGENTS.md`
- 两种模式都要求先读取 `references/core-rules.md`

### Claude Code

本仓库已内置 `.claude/agents` 和 `.claude/commands`，可直接使用：

- 通过子代理调用：`conventional-commit-batcher`
- 或命令：`/project:commit-batch`

### Kiro CLI

本仓库已内置 `.kiro/agents` 与 `.kiro/prompts`：

- agent: `conventional-commit-batcher`
- 入口配置：`.kiro/agents/conventional-commit-batcher.json`
- 运行规则来源：`references/core-rules.md`

### Qwen Code

本仓库已内置 `.agents/skills` 与 `.agents/agents`，Qwen 可自动发现：

- skill（模型自动匹配）：`conventional-commit-batcher`
- subagent（显式委派或自动委派）：`conventional-commit-batcher`
- 运行规则来源：`references/core-rules.md`

### Gemini CLI

本仓库已内置 `.agents/skills` 与 `.agents/agents`，Gemini 可自动发现：

- skill（模型自动匹配）：`conventional-commit-batcher`
- subagent（显式委派或自动委派）：`conventional-commit-batcher`
- 运行规则来源：`references/core-rules.md`

### Kimi CLI

本仓库已内置 `.agents/skills`，自动发现：

- skill（自动发现）：`conventional-commit-batcher`
- 斜杠命令：`/skill:conventional-commit-batcher`
- 运行规则来源：`references/core-rules.md`

## 消息校验示例

```bash
python3 scripts/validate_conventional_commit.py \
  --max-subject-length 72 \
  --max-header-length 100 \
  "feat(auth): add refresh token rotation"
```

## CI

`/.github/workflows/ci.yml` 会执行：

- Python 语法检查（`py_compile`）
- 单元测试（`pytest`）
- CLI 模拟校验（覆盖合法/非法 commit message）
- 在临时 git 仓库中做 `commit-msg` hook 端到端模拟

## 设计原则

- 一套规则，多入口加载
- 入口文件只做"路由"，不复制核心规则
- 规则变更只改 `references/core-rules.md`
