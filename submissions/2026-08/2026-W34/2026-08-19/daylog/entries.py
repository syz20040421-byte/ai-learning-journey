"""daylog.entries · 数据层：条目的追加与读取（Day 13）

本文件只做「和日志条目本身打交道」的两件事：
  add_entry(...)     往内存列表里加一条今天的日志
  load_entries(...)  从磁盘 JSON 文件把全部条目读回内存
它不统计、不打印——那是 stats.py 和 main.py 的事。

本包统一的数据形状（别的文件里的 entries 参数也是它）：
  一条日志 = {"date": "2026-08-19", "topic": "模块与包", "minutes": 120}
  date / topic 是字符串，minutes 是整数；整个日志是这种 dict 组成的 list。

每个函数正上方有它的要求（作用 + 参数 + 返回 + 边界 + 坑）。写哪部分看哪部分。
"""
import json
from datetime import date
from pathlib import Path


# ═══════════ 1. add_entry ═══════════
# 作用：往日志列表末尾追加「今天学习了一条」。
# 参数：
#   entries: list —— 条目列表（元素是上面那种 dict）。第一次跑传 [] 即可
#   topic: str     —— 今天学的主题名，如 "模块与包"
#   minutes: int   —— 学了多久，分钟数
# 返回：list —— 【原列表本身】（原地修改，不新建）；追加后最后一个元素是
#         {"date": "今天", "topic": topic, "minutes": minutes}
# 要求：日期用 date.today().isoformat()，别手拼 "2026-08-19"（明天就错）
# 坑：date.today() 返回 date 对象不是字符串，isoformat() 才转成 "YYYY-MM-DD"
def add_entry(entries: list, topic: str, minutes: int) -> list:
    # 你的实现：
    add_dict = {}
    add_dict["date"] = date.today().isoformat()
    add_dict["topic"] = topic
    add_dict["minutes"] = minutes
    entries.append(add_dict)
    return entries


# ═══════════ 2. load_entries ═══════════
# 作用：把磁盘上的日志文件读回内存（add_entry 的逆向操作），返回条目列表。
# 参数：
#   path —— 日志文件的路径，传字符串或 Path 对象都行（如 daylog/study_log.json）
# 返回：list —— 文件里的条目列表；【文件不存在】或【文件为空】都返回 []，不抛异常
# 要求：
#   - 文件存在且有内容：json.load 读出来就是列表，直接返回
#   - 文件不存在：返回 []（日志文件第一次跑本来就不存在，不能抛异常）
#   - 文件存在但是空字符串：也返回 []（json.load 读空文件会抛 JSONDecodeError）
# 坑：open 要带 encoding="utf-8"；判断不存在用 Path(path).exists()，别用 try/except 硬接
def load_entries(path) -> list:
    # 你的实现：
    if not Path(path).exists():
        return []
    with open(path,'r',encoding="utf-8") as f:
        result = f.read()
        if not result:
            return []
        return json.loads(result)
        
