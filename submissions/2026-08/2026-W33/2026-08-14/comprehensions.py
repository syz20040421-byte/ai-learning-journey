"""Day 9 · 推导式与生成器（Week 2 开张）

第 1 周你把 dict/list/set 用熟了。今天开始第 2 周的第一课：
用推导式把「先建空容器再 for 循环 append」的套路压缩成一行，
再认识生成器——它和列表长得像，但内存行为完全不同。

要求（先读任务书「今日知识点预习」再动手）：
1. squares_of_evens(n) -> list[int]：
   用【列表推导式】返回 [0, n) 中所有偶数的平方。
   例：squares_of_evens(6) == [0, 4, 16]（0², 2², 4²；5 不是偶数所以不算）
2. word_lengths(text) -> dict[str, int]：
   用【字典推导式】把句子拆成单词，返回 {单词: 长度}。
   例：word_lengths("a bb ccc") == {"a": 1, "bb": 2, "ccc": 3}
   注意：text.split() 按空白切，标点不用管。
3. unique_chars(words) -> set[str]：
   用【集合推导式】收集所有单词里出现过的字母。
   例：unique_chars(["ab", "bc"]) == {"a", "b", "c"}
4. first_n_squares(n) -> generator：
   写一个【生成器函数】（用 yield），依次产出 0², 1², ..., (n-1)²。
   不是返回列表！自测会验证它是生成器。
5. sum_squares_upto(n) -> int：
   用【生成器表达式】求和 0² + 1² + ... + (n-1)²，只写一行 return。
   例：sum_squares_upto(4) == 0 + 1 + 4 + 9 == 14

坑（预习里有详解）：
- 列表推导式能重复遍历、能 len()；生成器只能从头到尾走一遍
- 生成器函数用 yield，不用 return 列表——写了 return [] 就错了
- 集合推导式的结果是无序的，别拿它和列表比较顺序

自测：填空后运行
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W33/2026-08-14/comprehensions.py
预期输出：全部 assert 通过，最后打印 Day 9 全过
"""
from __future__ import annotations

"""
1. squares_of_evens(n) -> list[int]：
   用【列表推导式】返回 [0, n) 中所有偶数的平方。
   例：squares_of_evens(6) == [0, 4, 16]（0², 2², 4²；5 不是偶数所以不算）
def squares_of_evens(n: int) -> list[int]:
    # 你的实现：列表推导式
    pass
"""
def squares_of_evens(n: int) -> list[int]:
    squares = [x * x for x in range(n) if x % 2 == 0]
    return squares
"""
2. word_lengths(text) -> dict[str, int]：
   用【字典推导式】把句子拆成单词，返回 {单词: 长度}。
   例：word_lengths("a bb ccc") == {"a": 1, "bb": 2, "ccc": 3}
   注意：text.split() 按空白切，标点不用管。split()返回列表
"""
def word_lengths(text: str) -> dict[str, int]:
    str_list = text.split()
    str_dict = {x:len(x) for x in str_list}
    return str_dict
"""
3. unique_chars(words) -> set[str]：
   用【集合推导式】收集所有单词里出现过的字母。
   例：unique_chars(["ab", "bc"]) == {"a", "b", "c"}
"""
def unique_chars(words: list[str]) -> set[str]:
    return  {y for x in words for y in x}   
"""
4. first_n_squares(n) -> generator：
   写一个【生成器函数】（用 yield），依次产出 0², 1², ..., (n-1)²。
   不是返回列表！自测会验证它是生成器。
"""
def first_n_squares(n: int) -> object:
    for i in range(n):
        yield i*i

"""
5. sum_squares_upto(n) -> int：
   用【生成器表达式】求和 0² + 1² + ... + (n-1)²，只写一行 return。
   例：sum_squares_upto(4) == 0 + 1 + 4 + 9 == 14
"""
def sum_squares_upto(n: int) -> int:
    return sum(i*i for i in range(n))


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    assert squares_of_evens(6) == [0, 4, 16], squares_of_evens(6)
    assert squares_of_evens(1) == [0]
    assert squares_of_evens(0) == []

    assert word_lengths("a bb ccc") == {"a": 1, "bb": 2, "ccc": 3}
    assert word_lengths("") == {}
    
    assert unique_chars(["ab", "bc"]) == {"a", "b", "c"}
    assert unique_chars([]) == set()

    gen = first_n_squares(4)
    assert iter(gen) is gen, "first_n_squares 必须返回生成器（可迭代自身）"
    assert list(gen) == [0, 1, 4, 9], list(gen)

    assert sum_squares_upto(4) == 14
    assert sum_squares_upto(1) == 0

    print("Day 9 全过")
