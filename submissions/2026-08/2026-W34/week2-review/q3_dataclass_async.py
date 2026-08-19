"""周检 Q3 · dataclass + async（Day 11/12 复习）

先读题内注释再动手。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/week2-review/q3_dataclass_async.py
预期输出：全部 assert 通过，最后打印 周检 Q3 过
"""
import asyncio
from dataclasses import dataclass


# ═══════════ 1. @dataclass Movie ═══════════
# 要求：
#   - @dataclass class Movie：字段 title: str、rating: float
#   - 方法 summary() -> str：返回 f"{title}: {rating} 分"
# 坑：不用手写 __init__/__repr__/__eq__，dataclass 自动生成；方法照常定义在类里
@dataclass
class Movie:
    # 你的实现：
    title: str
    rating: float

    def summary(self) -> str:   # 类中传参传self
        return f"{self.title}: {self.rating} 分" 


# ═══════════ 2. top_movies ═══════════
# 要求：
#   - top_movies(movies: list) -> list：按 rating 从高到低排序，返回【新】列表
#   - 用 sorted(movies, key=..., reverse=True)——不要修改原列表
# 坑：sorted 返回新列表、不动原列表；list.sort() 会原地改原列表（这道题用前者）
def top_movies(movies: list) -> list:
    # 你的实现：
    new_list = sorted(movies, key=lambda m: m.rating, reverse=True) #lambda将实例对象指向m，排序依据指向m.rating
    return new_list


# ═══════════ 3. fetch_scores ═══════════
# 要求：
#   - async def fetch_scores(movies: list) -> list：用 asyncio.gather【并发】给每部电影"取评分"
#   - 函数内部定义 async def one(m: Movie)：await asyncio.sleep(0.01) 后返回 m.rating
#   - 返回评分列表，顺序与 movies 一致（gather 保序）
# 坑：gather(*tasks) 要星号展开；内部协程要 async def + await，否则是同步执行
async def fetch_scores(movies: list) -> list:
    # 你的实现：
    mov_list = []
    async def one(m: Movie):
        await asyncio.sleep(0.01)
        return m.rating
    for x in movies:
        mov_list.append(one(x))  #mov_list 是打包异步函数的列表
    result = await asyncio.gather(*mov_list)  #amait asyncio.gather()返回的是一个列表，*将mov_list解包
    return result


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    m1 = Movie("A", 8.5)
    m2 = Movie("B", 9.2)
    m3 = Movie("C", 7.0)
    assert m1.summary() == "A: 8.5 分", f"实际 {m1.summary()}"

    origin = [m1, m2, m3]
    ranked = top_movies(origin)
    assert [m.title for m in ranked] == ["B", "A", "C"], f"应降序 B>A>C，实际 {[m.title for m in ranked]}"
    assert [m.title for m in origin] == ["A", "B", "C"], "top_movies 不能修改原列表"

    scores = asyncio.run(fetch_scores(origin))
    assert scores == [8.5, 9.2, 7.0], f"评分应保序，实际 {scores}"

    print("周检 Q3 过")
