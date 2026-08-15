"""Day 10 · 装饰器入门 + 迭代器深化（Week 2）

昨天你写了生成器（yield）——今天把「函数是一等公民」和「迭代器协议」
这两块地基打上：装饰器 = 函数返回函数；for 循环 = iter() + next() + StopIteration。

要求（先读任务书「今日知识点预习」再动手）：
1. timer(func) -> function：计时装饰器。
   wrapper 里记录开始时间，调用原函数，打印 f"{函数名} 耗时 {x}s"，返回原结果。
2. slow_sum(n) -> int：用 @timer 装饰，算 1+2+...+n，内部 time.sleep(0.01) 模拟慢。
   验证：装饰器打印耗时，且 slow_sum(3) 返回值 == 6。
3. log_calls(func) -> function：日志装饰器。
   wrapper 打印 f"调用 {函数名}，参数 {args}"，然后调用原函数并返回结果。
4. make_adder(n) -> function：返回一个函数 add(x)，add(x) == n + x。
   例：make_adder(5)(3) == 8。
5. manual_iter(items) -> list：不用 for 循环，用 iter() + next() + try/except StopIteration
   手动遍历列表，返回收集到的元素列表。
   例：manual_iter([1, 2, 3]) == [1, 2, 3]。

坑（预习里有详解）：
- wrapper 必须 return result，漏了返回值就变 None
- wrapper 用 *args, **kwargs 透传，不要写死参数
- next() 越过末尾抛 StopIteration，用 try/except 捕获
- make_adder 返回的是函数对象，不是调用结果（别加括号）

自测：填空后运行
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W33/2026-08-16/decorators.py
预期输出：全部 assert 通过 + 计时日志，最后打印 Day 10 全过
"""
from __future__ import annotations
import time
from typing import Callable


def timer(func: Callable) -> Callable:
    # 你的实现：返回 wrapper，wrapper 计时后调用原函数并返回结果
    pass


def log_calls(func: Callable) -> Callable:
    # 你的实现：返回 wrapper，wrapper 打印调用日志后调用原函数
    pass


@timer
def slow_sum(n: int) -> int:
    # 你的实现：1+2+...+n，中间 time.sleep(0.01) 模拟慢操作
    pass


def make_adder(n: int) -> Callable:
    # 你的实现：返回一个函数 add，add(x) == n + x
    pass


def manual_iter(items: list) -> list:
    # 你的实现：iter() + next() + try/except StopIteration，返回收集的元素列表
    pass


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    assert slow_sum(3) == 6, f"slow_sum(3) == 6，实际 {slow_sum(3)}"
    assert slow_sum(10) == 55

    @log_calls
    def multiply(a, b):
        return a * b

    assert multiply(3, 4) == 12
    assert multiply(2, 9) == 18

    add5 = make_adder(5)
    assert add5(3) == 8
    assert add5(0) == 5
    assert make_adder(10)(-2) == 8

    assert manual_iter([1, 2, 3]) == [1, 2, 3]
    assert manual_iter([]) == []
    assert manual_iter(["a", "b"]) == ["a", "b"]

    print("Day 10 全过")
