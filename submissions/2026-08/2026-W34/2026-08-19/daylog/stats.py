"""daylog.stats · 学习统计（Day 13）

每个函数正上方有它的要求（行为 + 边界 + 坑）。
"""


# ═══════════ 1. total_minutes ═══════════
# 要求：
#   - total_minutes(entries: list) -> int：所有条目 minutes 求和
#   - 空列表返回 0
# 坑：列表推导式 [e["minutes"] for e in entries] + sum() 一行搞定（Day 9 的推导式用上了）
def total_minutes(entries: list) -> int:
    # 你的实现：
    """ 传统写法
    if not entries:
        return 0
    return sum(x for x in entries)
    """
    return sum(e["minutes"] for e in entries)


# ═══════════ 2. most_studied ═══════════
# 要求：
#   - most_studied(entries: list) -> str：返回【累计学习分钟数最多】的 topic
#   - 空列表返回 ""（空字符串）
#   - 并列时返回先出现的那个（Day 11 你实测过：max 并列返回第一个）
# 坑：看清是「累计」——先建 topic → 分钟数 的 dict 再 max(dict, key=dict.get)；
#     直接 max(entries, key=...) 只能找「单条最多」，不是「累计最多」
def most_studied(entries: list) -> str:
    # 你的实现：
    if not entries:
        return ""
    min_dict = {}
    for x in entries:
        y = x["topic"]
        if y not in min_dict:
            min_dict[y] = x["minutes"]
            continue
        min_dict[y] = min_dict[y] + x["minutes"]
    re_str = max(min_dict, key= min_dict.get) #找键值最大的键名
    return re_str
