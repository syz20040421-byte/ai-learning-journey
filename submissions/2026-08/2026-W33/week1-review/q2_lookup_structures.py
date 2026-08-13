"""Q2 · 数据结构选型：dict O(1) vs list O(n)（Day 3 × Day 6）

Day 6 你把 load_scores 设计成 dict[str, list[int]]（人名 → 分数列表）。
这题把「为什么是 dict」变成能跑的对比：同一个功能，dict 版和 list 版各写一遍，
assert 验证行为一致，最后用 perf_demo() 亲手量一遍查找耗时。

要求：
1. records_to_dict(records) -> dict[str, list[int]]：
   (name, score) 元组列表 → 按名合并，同名分数进同一个列表，保持出现顺序
2. lookup_dict(d, name) -> list[int]：dict 版，一次 O(1) 命中；查不到返回 []
3. lookup_list(records, name) -> list[int]：list 版，线性扫描收集【所有】同名分数；查不到返回 []
4. perf_demo(records, name)：造 100_000 条随机记录，分别用两种 lookup 查 1000 次，打印耗时
   ——你会亲眼看到 O(1) 和 O(n) 差几个数量级
5. 思考题（写在函数 docstring 注释里）：
   班里有两个同名「张三」，dict 版会把他们的分数怎么处理？tuple 列表版呢？
   哪种能真正分清两个人？想真正分清，需要给每条记录额外加什么字段？
   - dict版会把两人的成绩放到同一个人身上
   - tuple版两个人的成绩分别在自己名字上，但是分不清具体是谁的
   - 我认为这两版都分不清
   - 加学号，学号是唯一的

坑：
- dict 的 key 必须可哈希——tuple 可以，list 不行
- lookup_list 要收集所有同名分数，不是找到第一个就 return
- 查不到返回 [] 而不是抛 KeyError，调用方就不用每次判空
- perf_demo 里查的是「出现过的名字」和「没出现过的名字」各测一遍，都打印
"""
from __future__ import annotations
import random
import time


def records_to_dict(records: list[tuple[str, int]]) -> dict[str, list[int]]:
    # 你的实现：遍历元组列表，同名分数 append 到同一个列表
    stu_dict = dict()
    for name,score in records:   #需要索引的时候才用enumerate
        if name not in stu_dict:
            stu_dict[name] = []
        stu_dict[name].append(score)                 
    return stu_dict

def lookup_dict(d: dict[str, list[int]], name: str) -> list[int]:
    # 你的实现：dict.get(name, []) 或 d[name] + 判 KeyError，二选一
    stu_score_list = d.get(name,[])
    return stu_score_list

def lookup_list(records: list[tuple[str, int]], name: str) -> list[int]:
    # 你的实现：线性扫描，收集所有 name 匹配的分数
    stu_score_list = list()
    for x in records:
        if x[0] == name:
            stu_score_list.append(x[1])
    return stu_score_list

def perf_demo(records: list[tuple[str, int]], name: str) -> None:
    """1000 次查询计时对比。dict 应远快于 list，肉眼可见。"""
    d = records_to_dict(records)

    t0 = time.perf_counter()
    for _ in range(1000):
        lookup_dict(d, name)
    t_dict = time.perf_counter() - t0

    t0 = time.perf_counter()
    for _ in range(1000):
        lookup_list(records, name)
    t_list = time.perf_counter() - t0

    print(f"dict 查 1000 次: {t_dict:.4f}s")
    print(f"list 查 1000 次: {t_list:.4f}s")
    print(f"list 慢 {t_list / max(t_dict, 1e-9):.1f} 倍")


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    # ① 行为一致性：同名合并 + 查分一致
    records = [("张三", 90), ("李四", 85), ("张三", 78), ("王五", 60)]
    d = records_to_dict(records)
    assert d == {"张三": [90, 78], "李四": [85], "王五": [60]}, d
    assert lookup_dict(d, "张三") == [90, 78]
    assert lookup_list(records, "张三") == [90, 78]
    assert lookup_dict(d, "不存在的人") == []
    assert lookup_list(records, "不存在的人") == []

    # ② 性能对比：100_000 条里查「出现过」和「没出现过」的名字
    random.seed(42)
    big_records = [(f"学生{random.randint(0, 99999)}", random.randint(0, 100)) for _ in range(100_000)]
    print("查出现过的名字:")
    perf_demo(big_records, big_records[0][0])
    print("查没出现过的名字:")
    perf_demo(big_records, "学生999999")

    print("Q2 全过")
