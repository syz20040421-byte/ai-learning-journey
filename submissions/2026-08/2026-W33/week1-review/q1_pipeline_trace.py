"""Q1 · 链路追踪：文件 IO + API(mock) + None 的流向

这周综合验收(Day 7)的压缩重演。不用真网络——fetch_fn 由外部传入，
你自己写一个假的 fetch 来模拟「超时返回 None」的城市，亲手验证 None
在链路里怎么被过滤、不过滤会崩在哪。

要求：
1. load_cities(path) -> list[dict]：读 cities_review.csv（表头 city,latitude,longitude），
   空行/坏行（经纬度不是数字）跳过并打印原因，文件不存在打印提示返回 []
   （复用 Day 5/Day 7 的逐行模式；这次用 csv.DictReader，别手拆字符串）
2. process_cities(cities_path, fetch_fn) -> list[dict]：
   对每个城市调 fetch_fn(lat, lon)，收集 {"city","temperature","weathercode"}；
   fetch_fn 返回 None 的城市跳过（这正是你 Day 7 主循环的 if tem is not None）
3. unsafe_process_cities(cities_path, fetch_fn) -> list[dict]：
   和 process_cities 一样，但故意不检查 None，直接取 data["temperature"]——
   用来观察会崩在哪一行。跑完自测看 TypeError 从哪来。
4. 思考题（写进函数 docstring 注释或当日笔记）：
   unsafe 版崩掉的那一行，如果 fetch_fn 返回 None，那一行到底在把 None 当什么用？
   - 'NoneType' object is not iterable，代码把 None 当作一个字典（或至少是可用的数据容器）来使用，试图用它去更新另一个字典，而它根本不是一个有效的数据结构。

坑：
- csv.DictReader 读进来的数字全是字符串，float() 失败要 continue，别忘
- fetch_fn 返回 None 时，data["temperature"] 会抛
  TypeError: 'NoneType' object is not subscriptable
- 自测里的 _fake_fetch 是假的，别把它写成真请求

自测：填空后运行
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W33/week1-review/q1_pipeline_trace.py
预期输出：
    [假 API] 北京 正常返回
    [假 API] 广州请求超时,返回 None
    process 结果只剩北京 → assert len(rows) == 1 通过
    [假 API] 广州请求超时,返回 None
    unsafe 如期崩掉: 'NoneType' object is not subscriptable
"""
from __future__ import annotations
import csv
from typing import Callable


def load_cities(path: str) -> list[dict]:
    # 你的实现：csv.DictReader 逐行读；空行/坏行 print 原因后 continue；文件不存在返回 []
    cities_list = []
    try:
        with open(path,'r',encoding='utf-8') as f:
            dict1 = csv.DictReader(f)
            i = 0
            for row in dict1:
                i += 1
                if not row:
                    print(f"第{i}行是空行")
                    continue
                try:
                    row["latitude"] = float(row["latitude"])
                    row["longitude"] = float(row["longitude"])
                except (ValueError,TypeError) as e1:
                    print(f"{row['city']}的经纬度有问题：{e1}，跳过")
                    continue
                cities_list.append(row)
    except FileNotFoundError as e:
        print(f"文件不存在：{e}")
        return []
    return cities_list

def process_cities(cities_path: str, fetch_fn: Callable) -> list[dict]:
    # 你的实现：load_cities → 逐个 fetch_fn(lat, lon) → None 跳过 → 组装 dict 列表
    cities_list = load_cities(cities_path)
    fetch_list = []
    for x in cities_list:
        date = dict()
        date["city"] = x["city"]
        date1 = fetch_fn(x["latitude"],x["longitude"])
        if date1 is not None:
            date.update(date1)
            fetch_list.append(date)
    return fetch_list

def unsafe_process_cities(cities_path: str, fetch_fn: Callable) -> list[dict]:
    # 你的实现：和 process_cities 一样，但【不】检查 None，直接 data["temperature"]
    cities_list = load_cities(cities_path)
    fetch_list = []
    for x in cities_list:
        date = dict()
        date["city"] = x["city"]
        date1 = fetch_fn(x["latitude"],x["longitude"])
        date.update(date1)
        fetch_list.append(date)
    return fetch_list

# ============ 自测（别改这里） ============
def _fake_fetch(lat: float, lon: float) -> dict | None:
    """假 API：北京正常返回；广州模拟超时返回 None。"""
    if lat == 23.1291 and lon == 113.2644:          # 广州
        print("[假 API] 广州请求超时,返回 None")
        return None
    if lat == 39.9042 and lon == 116.4074:          # 北京
        print("[假 API] 北京 正常返回")
        return {"temperature": 25.6, "weathercode": 0}
    print(f"[假 API] 未知坐标 {lat},{lon},返回 None")
    return None


if __name__ == "__main__":
    # cities_review.csv: 北京(正常) / 广州(会超时) / 月球(经纬度坏行,应被 load_cities 跳过)
    rows = process_cities("submissions/2026-08/2026-W33/week1-review/cities_review.csv", _fake_fetch)
    print("process 结果:", rows)
    assert len(rows) == 1, f"北京1行+广州None跳过+月球坏行跳过,应剩1行,实际 {len(rows)}"
    assert rows[0]["city"] == "北京"

    # unsafe 版应该崩在 data["temperature"] → TypeError
    try:
        unsafe_process_cities("submissions/2026-08/2026-W33/week1-review/cities_review.csv", _fake_fetch)
        assert False, "unsafe 版竟然没崩？"
    except TypeError as e:
        print("unsafe 如期崩掉:", e)

    print("Q1 全过")
