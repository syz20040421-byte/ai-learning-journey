"""daylog · 学习日志包（Day 13 · 模块与包实战）

包入口。学员只需填下面的导出语句。
"""
# ═══════════ 1. 导出公共 API ═══════════
# 要求：
#   - 从 .entries 导入 add_entry、load_entries
#   - 从 .stats 导入 total_minutes、most_studied
#   - 让调用方写 `from daylog import add_entry` 一句到位（这就是 __init__.py 的职责）
# 坑：相对导入用点开头（from .entries import ...）；不写导出，调用方就得写
#     from daylog.entries import add_entry，包结构形同虚设
# 你的实现：
...

__all__ = ["add_entry", "load_entries", "total_minutes", "most_studied"]
