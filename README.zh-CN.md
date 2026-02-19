# conventional-commit-batcher

[![CI](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml/badge.svg)](https://github.com/cnkang/conventional-commit-batcher/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/cnkang/conventional-commit-batcher)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/agent--skill-conventional--commit--batcher-2563eb)](https://skills.sh)

[English](README.md)

把“混杂改动”拆成可审查、可回滚、可追踪的 Conventional Commit 批次，并通过 agent-first、plan-first 工作流强制先计划后执行。

支持 Codex、Claude Code、Kiro CLI、Kimi CLI、Qwen Code、Gemini CLI。

## 这个 Skill 是做什么的

这个仓库是一个可复用的 **Agent Skill**，专门用于提交规范治理。

- 给 AI Agent 用：产出符合规范的 Conventional Commits
- 强制 plan-first：先出批次计划，再执行 `git add` / `git commit`
- 内置可执行校验：脚本 + CI 保证提交信息质量

## 30 秒快速演示

### Before

- 一个大提交里混了功能、修复、重构、文档
- 评审噪音大，回滚风险高

### After

- 先生成 `Commit Plan`
- 确认后再执行分批提交
- `feat` / `fix` / `refactor` / `docs` / `chore` 各自独立、可追踪

```text
Commit Plan
Batch #1: feat(auth): add refresh token rotation
Batch #2: test(auth): cover refresh token rotation flows
Batch #3: docs(auth): document refresh token behavior
```

```bash
# 在你的 agent 中先调用 conventional-commit-batcher（仅输出计划）
# 审核 Commit Plan 后，再执行建议的分批命令
git add ...
git commit -m "feat(...): ..."
```

## 30 秒安装

### 推荐：skills.sh 生态

- 通过 [`npx skills`](https://skills.sh) 安装，并搜索 `conventional-commit-batcher`
- 一次安装，可在 Codex / Claude Code / Gemini CLI / Qwen Code / Kimi CLI / Kiro 复用

### 手动安装

- 克隆或复制本仓库到你的环境
- 按下方 Quick Start 选择对应 agent 入口
- 执行前统一先读取 `references/core-rules.md`

## 为什么值得转发

- **Plan-first commit batching**：先产出 `Commit Plan`，确认后才允许 `git add` / `git commit`
- **Single source of truth**：规则只维护在 `references/core-rules.md`
- **Executable validation**：validator + tests + CI + hook 模拟，保证最佳实践可执行

## 三个真实例子

1. `feat` + `test` + `docs` 拆分：认证功能改动、测试、文档各自独立
2. `refactor` 与 `fix` 拆分：机械重构与行为修复分开，便于 bisect/revert
3. `build(deps)` 与 `style` 拆分：依赖和 lockfile 原子提交，格式化改动单独提交

完整示例见：[`references/plan-examples.md`](references/plan-examples.md)

## 这个项目解决什么问题

很多仓库在开发后会出现以下痛点：

- 一个提交里混了功能、重构、格式化、文档改动，评审困难
- 提交信息不规范，后续变更追踪和自动化发布受影响
- AI 或人工在拆分提交时边界不稳定，容易误混文件或误拆 hunk

这个项目把这些操作收敛为统一流程，并提供可执行校验脚本。

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

- agent：`conventional-commit-batcher`
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

## 对人和 AI 都友好的结构

- `references/core-rules.md`: 唯一权威规则（single source of truth）
- `SKILL.md`: Codex 入口（薄封装，指向核心规则）
- `AGENTS.md`: Codex CLI 仓库级加载入口
- `CLAUDE.md`: Claude Code 项目级指令入口
- `.claude/agents/conventional-commit-batcher.md`: Claude 子代理入口
- `.claude/commands/commit-batch.md`: Claude 命令入口
- `.kiro/agents/conventional-commit-batcher.json`: Kiro agent 入口
- `.kiro/prompts/conventional-commit-batcher.md`: Kiro prompt 入口
- `.kiro/steering/commit-batching.md`: Kiro 自动加载 steering 规则
- `.agents/skills/conventional-commit-batcher/SKILL.md`: 共享 skill 入口（Kimi/Qwen/Gemini）
- `.agents/agents/conventional-commit-batcher.md`: 共享子代理入口（Qwen/Gemini）
- `.github/workflows/ci.yml`: GitHub Actions CI（检查 + 模拟测试）
- `agents/openai.yaml`: OpenAI agent 入口
- `scripts/validate_conventional_commit.py`: Conventional Commit 校验器
- `scripts/test_validate_conventional_commit.py`: 校验器单元测试
- `references/plan-examples.md`: 典型拆分示例
- `references/codex-setup.md` / `references/claude-setup.md` / `references/kiro-setup.md` / `references/kimi-setup.md` / `references/qwen-setup.md` / `references/gemini-setup.md`: 跨仓库复用说明

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
- CLI 模拟校验（覆盖合法和非法 commit message）
- 在临时 git 仓库中做 `commit-msg` hook 端到端模拟

## 设计原则

- 一套规则，多入口加载
- 入口文件只做“路由”，不复制核心规则
- 规则变更只改 `references/core-rules.md`
