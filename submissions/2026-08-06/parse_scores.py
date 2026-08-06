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
    # 你的实现：
    pass  # 删掉这句，写你的实现


def load_scores(lines: list[str]) -> dict[str, int]:
    # 你的实现：逐行调用 parse_score_line，坏行 try/except 捕获并跳过
    pass  # 删掉这句，写你的实现


# 你的 assert 写在这里（正常两行 / 无逗号坏行跳过 / 非整数坏行跳过 / 结果只含好行）
# 建议测试数据：
# lines = ["张三,90", "李四,abc", "王五", "赵六,85"]
# 期望结果：{"张三": 90, "赵六": 85}，两条坏行各打印一次跳过提示
