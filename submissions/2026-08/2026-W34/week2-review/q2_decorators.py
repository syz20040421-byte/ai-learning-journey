"""周检 Q2 · 带参数装饰器（Day 10 复习）

先读题内注释再动手。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/week2-review/q2_decorators.py
预期输出：全部 assert 通过，最后打印 周检 Q2 过
"""
import functools


# ═══════════ 1. repeat(times) ═══════════
# 要求：
#   - repeat(times: int) 是【带参数】装饰器：让被装饰函数执行 times 次，返回【最后一次】的结果
#   - 用法：@repeat(3) 装饰的 ping("x") 会执行 3 次，返回第 3 次的返回值
#   - 坑：带参数装饰器必须三层嵌套——
#       外层 repeat(times) 收参数，
#       中层 decorator(func) 收函数，
#       内层 wrapper(*args, **kwargs) 收调用参数并执行 func
def repeat(times: int):
    # 你的实现（三层嵌套）：
    ...


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    calls = []

    @repeat(3)
    def ping(msg: str) -> str:
        calls.append(msg)
        return f"pong:{msg}"

    result = ping("x")
    assert result == "pong:x", f"应返回最后一次执行的结果，实际 {result}"
    assert len(calls) == 3, f"应执行 3 次，实际 {len(calls)} 次"

    print("周检 Q2 过")
