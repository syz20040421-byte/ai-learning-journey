"""Day 4 练习 ①：除零保护 safe_divide。

任务要求（验收标准）：
- b == 0 时 raise ValueError("除数不能为 0")，其他情况返回 a / b
- 用 try/except 包裹一个调用，捕获 ValueError 并打印它的消息
- 写 assert 覆盖：正常除法（safe_divide(10, 2) == 5.0）、除零真的抛 ValueError
"""
from typing import Union


def safe_divide(a: float, b: float) -> float:
    # 你的实现：
    pass  # 删掉这句，写你的实现


# try/except 演示（捕获 ValueError 并打印消息）：
# 你的演示代码写在这里


# 你的 assert 写在这里（覆盖正常除法 / 除零抛 ValueError）
# 提示：断言「抛异常」可以这样写：
# try:
#     safe_divide(1, 0)
#     raise AssertionError("应该抛出 ValueError")
# except ValueError:
#     pass  # 期望的异常，测试通过
