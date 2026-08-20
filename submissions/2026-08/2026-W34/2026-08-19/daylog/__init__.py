"""daylog · 学习日志包（Day 13 · 模块与包实战）

包入口 = 调用方的「统一大门」。它的职责只有一个：把内部模块里的函数转发出来，
让外面的人写 `from daylog import add_entry` 一句到位，不用知道内部文件怎么拆。

四个文件的分工（先读这张表，再往下看单个文件）：
  __init__.py   包入口——只做导出转发，没有业务逻辑（本文件）
  entries.py    数据层——「加一条」add_entry / 「读全部」load_entries
  stats.py      统计层——「总分钟数」total_minutes / 「学得最多的主题」most_studied
  main.py       主流程——把上面两层串起来：读 → 加 → 存 → 统计 → 打印（程序入口）

贯穿全包的数据形状（所有函数的 entries 参数都是它）：
  一条日志 = {"date": "2026-08-19", "topic": "模块与包", "minutes": 120}
  整个日志 = 上面这种 dict 组成的 list
"""
# ═══════════ 1. 导出公共 API ═══════════
# 作用：把内部两个模块的函数「转发」到包门口，这是 __init__.py 的核心职责。
# 要求：
#   - 从 .entries 导入 add_entry、load_entries
#   - 从 .stats 导入 total_minutes、most_studied
#   - 填完这句，调用方写 `from daylog import add_entry` 就够了
# 坑：相对导入用点开头（from .entries import ...）；不写导出，调用方就得写
#     from daylog.entries import add_entry，包结构形同虚设
# 你的实现：
from .entries import add_entry, load_entries
from .stats import total_minutes, most_studied

__all__ = ["add_entry", "load_entries", "total_minutes", "most_studied"]
