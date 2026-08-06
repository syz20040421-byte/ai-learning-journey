"""Day 4 练习 ②：带校验的分数解析 parse_scores。

任务要求（验收标准）：
- parse_score_line(line) 解析 "姓名,分数"（如 "张三,90"）
  - 没有逗号 → raise ValueError("缺少逗号")
  - 分数不是整数 → raise ValueError("分数不是整数")
  - 正常 → 返回 (姓名, 分数) 元组
- load_scores(lines) 逐行调用 parse_score_line
  - 某行抛 ValueError 时：打印 "第 N 行跳过：<原因>"，继续处理下一行（不能中断）
  - 正常行收进返回的 dict {姓名: 分数}
- 写 assert 覆盖：正常两行、坏行（无逗号）被跳过、坏行（分数非整数）被跳过、返回 dict 只含好行
"""
from typing import Tuple


def parse_score_line(line: str) -> Tuple[str, int]:
    parts = line.split(",")             # ① 按逗号切开
    if len(parts) < 2:                  # ② 没切出两半 → 没有逗号 → 抛
        raise ValueError("缺少逗号")
    name, score_str = parts[0], parts[1]
    if not score_str.isdigit():         # ③ 分数部分不是纯数字 → 抛
        raise ValueError("分数不是整数")
    return name, int(score_str)         # ④ 全过了 → 返回 (姓名, 分数)


def load_scores(lines: list[str]) -> dict[str, int]:
    scores = {}
    for i, line in enumerate(lines, start=1):   # ① 行号从 1 开始
        try:                                     # ② 兜底接异常
            name, score = parse_score_line(line)
        except ValueError as e:                  # ③ 不区分种类，都接住
            print(f"第 {i} 行跳过：{e}")          #    打印原因（e 就是错误消息）
            continue                             # ④ 跳过这行，继续下一行
        scores[name] = score                     # ⑤ 好行收进 dict
    return scores


# ========== assert 测试 ==========
lines = ["张三,90", "李四,abc", "王五", "赵六,85"]
result = load_scores(lines)

# 场景1：正常两行解析正确 + 场景4：dict 只含好行
assert result == {"张三": 90, "赵六": 85}
# 场景2：无逗号坏行（王五）被跳过
assert "王五" not in result
# 场景3：非整数坏行（李四,abc）被跳过
assert "李四" not in result

# 补充：parse_score_line 单测（正常路径）
assert parse_score_line("张三,90") == ("张三", 90)
