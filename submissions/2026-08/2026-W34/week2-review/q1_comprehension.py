"""周检 Q1 · 推导式与生成器（Day 9 复习）

先读题内注释再动手。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/week2-review/q1_comprehension.py
预期输出：全部 assert 通过，最后打印 周检 Q1 过
"""


# ═══════════ 1. filter_even_squares ═══════════
# 要求：
#   - filter_even_squares(numbers: list) -> list
#   - 用一条列表推导式返回：输入里【偶数】的【平方】
#   - 例：filter_even_squares([1, 2, 3, 4]) == [4, 16]
# 坑：推导式里 if 过滤写在 for 后面：[x*x for x in numbers if 偶数]
def filter_even_squares(numbers: list) -> list:
    # 你的实现：
    return [x*x for x in numbers if x%2 == 0]  #相除用/，取余用%
     


# ═══════════ 2. long_words_gen ═══════════
# 要求：
#   - long_words_gen(words: list, min_len: int) -> 生成器
#   - 用【生成器表达式】惰性产出长度 >= min_len 的词
#   - 例：g = long_words_gen(["hi", "hello", "world"], 4)；next(g) == "hello"
# 坑：return (x for x in ...) 才是生成器；写 return [x for x in ...] 是列表推导式，会一次性算完，不惰性
def long_words_gen(words: list, min_len: int):  #要返回生成器
    # 你的实现：
    return (x for x in words if len(x) >= min_len)


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    assert filter_even_squares([1, 2, 3, 4]) == [4, 16], f"实际 {filter_even_squares([1, 2, 3, 4])}"
    assert filter_even_squares([]) == [], "空列表应返回空列表"

    g = long_words_gen(["hi", "hello", "world", "a"], 4)
    assert next(g) == "hello", "第一个达标词应是 hello"
    assert next(g) == "world", "第二个达标词应是 world"

    import types
    assert isinstance(g, types.GeneratorType), "long_words_gen 返回的必须是生成器（惰性），不是列表"

    print("周检 Q1 过")
