"""Day 5 练习：从文件读成绩 load_scores（摸底遗留 04 题）。

任务要求（验收标准）：
- load_scores(path) 读取文件，每行格式 "姓名,分数"
- 忽略空行；坏行（无逗号/分数非整数）跳过并打印 "第 N 行跳过：<原因>"
- 文件不存在 → 打印清晰提示，返回 {}（不能有 traceback 冒出来）
- 用 with open(...) 读，encoding="utf-8"，for line in f 逐行迭代
- 解析逻辑复制昨天的 parse_score_line（含两个 raise）
- 写 assert 覆盖：正常文件全解析、文件不存在返回 {}
- 末尾加「文件不存在」演示：load_scores("不存在的文件.txt")
"""
from typing import Tuple


def parse_score_line(line: str) -> Tuple[str, int]:
    # 复制昨天 parse_scores.py 里的实现（含两个 raise）
    pass  # 删掉这句，写你的实现


def load_scores(path: str) -> dict[str, int]:
    # 你的实现：with open + try/except FileNotFoundError + 逐行解析
    pass  # 删掉这句，写你的实现


# 你的 assert 写在这里（正常文件全解析 / 文件不存在返回 {}）
# 注意：测试用的 scores.txt 要自己造，放在本目录


# 文件不存在演示（打印提示、返回 {}、无 traceback）：
# print(load_scores("不存在的文件.txt"))
