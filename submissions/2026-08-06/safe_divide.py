"""Day 4 练习 ①：除零保护 safe_divide。

任务要求（验收标准）：
- b == 0 时 raise ValueError("除数不能为 0")，其他情况返回 a / b
- 用 try/except 包裹一个调用，捕获 ValueError 并打印它的消息
- 写 assert 覆盖：正常除法（safe_divide(10, 2) == 5.0）、除零真的抛 ValueError
"""
from typing import Union


def safe_divide(a: float, b: float) -> float:
    if b == 0:                              # ① 除数为 0 → 主动抛
        raise ValueError("除数不能为 0")
    return a / b                            # ② 否则正常除


# try/except 演示（捕获 ValueError 并打印消息）：
try:
    safe_divide(1, 0)                       # 这行会抛 ValueError
except ValueError as e:
    print(e)                                # 打印 "除数不能为 0"


# 你的 assert 写在这里（覆盖正常除法 / 除零抛 ValueError）
# 正常除法
assert safe_divide(10, 2) == 5.0

# 除零真的抛 ValueError（用题目给的 try 模式）
try:
    safe_divide(1, 0)
    raise AssertionError("应该抛出 ValueError")   # 没抛才会走到这 → 测试失败
except ValueError:
    pass                                        # 抛了 → 测试通过
