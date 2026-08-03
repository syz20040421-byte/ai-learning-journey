#!/usr/bin/env python3
"""飞书群机器人推送（方案 A：自定义机器人 Webhook）

用法:
    python feishu_push.py --title "Day 1 任务" --file ../daily/2026-08-04.md
    python feishu_push.py --title "测试" --text "hello"
    python feishu_push.py --title "测试" --text "hello" --dry-run

Webhook 地址来源（按优先级）:
    1. --webhook 参数
    2. 环境变量 FEISHU_WEBHOOK_URL
    3. 同目录 .feishu_webhook 文件（单行纯文本）

只用标准库，无需 pip install。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WEBHOOK_FILE = SCRIPT_DIR / ".feishu_webhook"
TIMEOUT = 20
MAX_RETRIES = 3


def resolve_webhook(cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value.strip()
    env = os.environ.get("FEISHU_WEBHOOK_URL", "").strip()
    if env:
        return env
    if WEBHOOK_FILE.exists():
        content = WEBHOOK_FILE.read_text(encoding="utf-8").strip()
        # 允许文件里有注释行
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
    return None


def build_card(title: str, markdown_body: str) -> dict:
    """交互式卡片。飞书 lark_md 支持有限的 markdown 子集。"""
    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True, "enable_forward": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue",
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": markdown_body}}
            ],
        },
    }


def build_text(title: str, body: str) -> dict:
    return {"msg_type": "text", "content": {"text": f"{title}\n\n{body}"}}


def sanitize_for_lark_md(md: str) -> str:
    """飞书 lark_md 不支持表格和标题层级，做降级处理。

    支持: **bold** *italic* ~~del~~ [text](url) 无序列表 换行
    不支持: # 标题、| 表格 |、``` 代码块（会原样显示但难看）
    """
    out = []
    in_code = False
    for line in md.splitlines():
        stripped = line.strip()

        # 代码块围栏 -> 转成分隔提示
        if stripped.startswith("```"):
            in_code = not in_code
            out.append("---" if not in_code else "---")
            continue

        if in_code:
            out.append(line)
            continue

        # markdown 标题 -> 加粗
        if stripped.startswith("#"):
            text = stripped.lstrip("#").strip()
            if text:
                out.append(f"**{text}**")
            continue

        # 表格分隔行 -> 丢弃
        if set(stripped) <= set("|-: ") and "|" in stripped and "-" in stripped:
            continue

        # 表格行 -> 用 · 连接单元格
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            cells = [c for c in cells if c]
            if cells:
                out.append("· " + "  ·  ".join(cells))
            continue

        out.append(line)

    return "\n".join(out)


def truncate(text: str, limit: int = 20000) -> str:
    """飞书单条消息有大小限制，卡片约 30KB。留余量。"""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n…（内容过长已截断，完整版见 Obsidian）"


def send(webhook: str, payload: dict, dry_run: bool = False) -> tuple[bool, str]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    if dry_run:
        preview = json.dumps(payload, ensure_ascii=False, indent=2)
        return True, f"[DRY-RUN] 未实际发送。payload {len(body)} bytes:\n{preview[:1500]}"

    last_err = ""
    for attempt in range(1, MAX_RETRIES + 1):
        req = urllib.request.Request(
            webhook,
            data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read().decode("utf-8", "replace")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return False, f"响应不是 JSON: {raw[:300]}"

            # 飞书成功: {"code":0,"msg":"success"} 或 {"StatusCode":0,...}
            code = data.get("code", data.get("StatusCode", -1))
            if code == 0:
                return True, "发送成功"
            return False, f"飞书返回错误 code={code} msg={data.get('msg') or data.get('StatusMessage')}"

        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            last_err = f"HTTP {e.code}: {detail}"
        except urllib.error.URLError as e:
            last_err = f"网络错误: {e.reason}"
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"

        if attempt < MAX_RETRIES:
            time.sleep(2 ** attempt)

    return False, f"重试 {MAX_RETRIES} 次后失败: {last_err}"


def main() -> int:
    ap = argparse.ArgumentParser(description="推送消息到飞书群机器人")
    ap.add_argument("--title", required=True, help="卡片标题")
    ap.add_argument("--text", help="正文内容（markdown）")
    ap.add_argument("--file", help="从文件读正文")
    ap.add_argument("--webhook", help="Webhook 地址（覆盖环境变量和文件）")
    ap.add_argument("--plain", action="store_true", help="发纯文本而非卡片")
    ap.add_argument("--dry-run", action="store_true", help="只打印 payload 不发送")
    args = ap.parse_args()

    if not args.text and not args.file:
        print("错误: 需要 --text 或 --file", file=sys.stderr)
        return 2

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = (SCRIPT_DIR / p).resolve()
        if not p.exists():
            print(f"错误: 文件不存在 {p}", file=sys.stderr)
            return 2
        body = p.read_text(encoding="utf-8")
    else:
        body = args.text

    webhook = resolve_webhook(args.webhook)
    if not webhook and not args.dry_run:
        print(
            "错误: 未找到 Webhook 地址。请任选一种配置方式:\n"
            f"  1. 写入文件: {WEBHOOK_FILE}\n"
            "  2. 设置环境变量 FEISHU_WEBHOOK_URL\n"
            "  3. 用 --webhook 参数传入",
            file=sys.stderr,
        )
        return 3

    if webhook and not webhook.startswith("https://open.feishu.cn/open-apis/bot/"):
        print(f"警告: Webhook 地址格式看起来不对: {webhook[:60]}", file=sys.stderr)

    body = truncate(body)

    if args.plain:
        payload = build_text(args.title, body)
    else:
        payload = build_card(args.title, sanitize_for_lark_md(body))

    ok, msg = send(webhook or "https://dry.run/placeholder", payload, args.dry_run)
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
