# AI_KnowledgeBase

13 周求职冲刺学习仓库（AI 应用开发 / LLM 应用工程师方向）。这里记录每日学习任务、笔记、作业提交与教练批改，是**学习过程的完整记录**，不是产品代码仓库（作品项目后续独立建仓）。

## 当前阶段

第 3 周：HTTP / FastAPI / SQL —— 目标是做出**线上可访问、手机能打开、带 pytest 测试**的 API 服务。

## 目录结构

| 目录 | 用途 |
|---|---|
| `daily/` | 每日任务书（教练生成） |
| `notes/` | 学员学习笔记 + 今日三问 |
| `submissions/` | 每日代码作业（含脚手架） |
| `review/` | 教练批改报告 |
| `scripts/`、`state/` | 自动化支撑 |

日期文件按 `YYYY-MM/YYYY-Www/`（月/ISO 周）归档，如 `daily/2026-08/2026-W34/2026-08-21.md`。

## 环境要求

- Python 3.11+（本仓库用 uv 管理，虚拟环境在 `.venv/`）
- Git（提交作业用）

## 安装依赖

```bash
cd "D:\work-coding\Knowledge base\AI_KnowledgeBase"
uv sync        # 按 pyproject.toml 安装；新增依赖用 uv add <包名>
```

## 运行示例（练习脚本）

```bash
".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-20/pydantic_practice.py
```

## 运行测试

（第 3 周起引入 pytest）

```bash
".venv/Scripts/python.exe" -m pytest tests/
```

## 已知限制

- GitHub 直连被墙，git 需走本机 Clash 代理（127.0.0.1:7897，已全局配置）
- httpbin.org 已挂（503），HTTP 练习用 httpbingo.org 替代（其 args/headers 值为数组，取字段带 `[0]`）
- 仓库路径含空格，命令中路径必须加引号
