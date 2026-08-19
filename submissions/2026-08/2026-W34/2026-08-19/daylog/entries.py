"""daylog.entries · 学习条目的追加与读取（Day 13）

每个函数正上方有它的要求（行为 + 边界 + 坑）。写哪部分看哪部分。
"""
import json
from datetime import date
from pathlib import Path


# ═══════════ 1. add_entry ═══════════
# 要求：
#   - add_entry(entries: list, topic: str, minutes: int) -> list
#   - 往 entries 里追加一条 {"date": 今天日期, "topic": topic, "minutes": minutes}
#   - 日期用 date.today().isoformat()，别手拼 "2026-08-19"（明天就错）
#   - 直接修改并返回【原列表】（不新建）
# 坑：date.today() 返回 date 对象不是字符串，isoformat() 才转成 "YYYY-MM-DD"
def add_entry(entries: list, topic: str, minutes: int) -> list:
    # 你的实现：
    ...


# ═══════════ 2. load_entries ═══════════
# 要求：
#   - load_entries(path) -> list：用 json.load 读文件，返回条目列表
#   - 文件不存在时返回 []（日志文件第一次跑本来就不存在，不能抛异常）
#   - 文件存在但内容是空字符串时也返回 []（json.load 空文件会抛 JSONDecodeError）
# 坑：open 要带 encoding="utf-8"；判断不存在用 Path(path).exists()，别用 try/except 硬接
def load_entries(path) -> list:
    # 你的实现：
    ...
