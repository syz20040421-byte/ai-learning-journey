"""Q3 · 错误处理不对称：读可以软失败，写不行（Day 4 × Day 5 × Day 7）

你三个函数的失败策略不一样：load_cities 返回 []、fetch_weather 返回 None、
save_results 没有任何防护。这题把「写文件失败」变成可运行的场景：
save_results_checked 失败时打印具体原因并返回 False（不崩、不吞），
再验证：读不存在的文件 → []；写不存在的目录 → False 且程序继续跑。

要求：
1. load_cities_safe(path) -> list[dict]：文件不存在打印提示返回 []（复用 Q1 的 load_cities 即可）
2. save_results_checked(rows, path) -> bool：
   - 成功写入 → True
   - 失败 → 打印具体错误（错误信息要能看出是哪一步挂了）→ 返回 False
   - 提示：open(path, "w") 时目录不存在会抛 FileNotFoundError，磁盘问题会抛 OSError
     ——FileNotFoundError 是 OSError 的子类，一个 except OSError 就能全接住
3. 思考题（写在 docstring 的注释里）：
   读失败返回 [] 让程序继续，写失败为什么不建议同样「软失败」？
   （提示：写一半崩了，文件里剩半截；下游程序读到半截数据会以为是完整的）
   - 读失败不会使数据发生变化，写失败会，而且还会影响文件状态

坑：
- 别用 except Exception 兜底——这里只需要接住 OSError 这一族
- 返回 False 前一定要 print 具体错误，不然调用方不知道发生了什么
- save_results_checked 写成功后要真的能读回（自测会验证）
"""
from __future__ import annotations
import csv
import os


def load_cities_safe(path: str) -> list[dict]:
    # 你的实现：读 CSV（表头 city,latitude,longitude），文件不存在打印提示返回 []
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


def save_results_checked(rows: list[dict], path: str) -> bool:
    # 你的实现：csv.DictWriter 写 weather.csv 风格文件
    # 成功 → True；OSError（目录不存在/磁盘满等）→ print 具体错误 → False
    try:
        with open(path,'w',encoding='utf-8',newline="") as f:
            w = csv.DictWriter(f,fieldnames=["city","temperature","weathercode"])
            w.writeheader()
            for row in rows:
                w.writerow(row)
    except OSError as e:
        print(f"写入错误：{e}")
        return False
    else:
        return True


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    rows = [{"city": "北京", "temperature": 25.6, "weathercode": 0},
            {"city": "上海", "temperature": 28.5, "weathercode": 2}]

    # ① 读不存在的文件 → 软失败
    assert load_cities_safe("no_such_file.csv") == []

    # ② 写不存在的目录 → 返回 False，且不抛异常、程序继续
    ok = save_results_checked(rows, "no_such_dir/weather.csv")
    assert ok is False, "目录不存在应该返回 False"
    print("写不存在的目录 → 返回 False，程序继续跑")

    # ③ 正常写入 → True，且能原样读回
    # 注意：DictReader 读回的全是字符串（"25.6" 不是 25.6）——这正是 Day 8 预习第 4 条讲的坑，
    # 所以这里用字符串版本的 rows 来比，不用转类型
    out = "submissions/2026-08/2026-W33/week1-review/weather.csv"
    assert save_results_checked(rows, out) is True
    with open(out, encoding="utf-8") as f:
        read_back = list(csv.DictReader(f))
    expected = [
        {"city": "北京", "temperature": "25.6", "weathercode": "0"},
        {"city": "上海", "temperature": "28.5", "weathercode": "2"},
    ]
    assert read_back == expected, f"读回不匹配: {read_back}"
    os.remove(out)  # 清理测试产物

    print("Q3 全过")
