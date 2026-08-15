"""Day 7 练习：第 1 周综合验收 — 读 CSV → 调 API → 处理 → 写回文件。
昨天没写完卡在：昨天没空写
任务要求（验收标准）：
- load_cities(path) -> list[dict]：读 CSV（表头 city,latitude,longitude），坏行打印原因跳过；
  文件不存在打印提示、返回空列表（复用 Day 5 的逐行模式）
- fetch_weather(lat, lon) -> dict | None：GET open-meteo API，timeout=10 必须设，
  返回 {"temperature": ..., "weathercode": ...}；失败打印错误、返回 None，不抛异常
- save_results(rows, path)：把 [{"city","temperature","weathercode"}, ...] 写进 weather.csv
  （表头 city,temperature,weathercode，encoding="utf-8"）
- 主流程（文件末尾）：读 cities.csv → 逐个 fetch_weather → 跳过 None → 打印 "城市 温度"
  → save_results 写 weather.csv
- 每个城市一个 try/except，单个失败不影响其他城市
- 全程自己 debug：可以问 AI「为什么报这个错」，禁止让 AI 写完整代码
"""
from __future__ import annotations
import requests, csv, json
from pathlib import Path

# 基础目录：当前脚本所在目录
BASE_DIR = Path(__file__).parent

def load_cities(path: str) -> list[dict]:
    # 读 CSV：跳过表头，坏行打印原因（复用 Day 5 逐行模式）
    # 文件不存在 → 打印提示，返回 []
    return_list = list()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            next(f)  # 跳过表头
            for i, line in enumerate(f, start=1):
                lines = line.strip()
                return_dict = dict()
                if not lines:
                    print(f"第{i}行跳过：空行666")
                    continue
                list1 = lines.split(",")
                try:
                    list1[1] = float(list1[1])
                    list1[2] = float(list1[2])
                except (ValueError, TypeError):
                    print(f"{list1[0]}的数据异常")
                    continue
                return_dict["city"] = list1[0]
                return_dict["latitude"] = list1[1]
                return_dict["longitude"] = list1[2]
                return_list.append(return_dict)
    except FileNotFoundError:
        print("文件不存在")
        return []
    return return_list

def fetch_weather(lat: float, lon: float) -> dict | None:
    # requests.get(..., timeout=10) 必须设
    # 成功 → {"temperature": ..., "weathercode": ...}
    # 失败（超时/断网/非 200）→ 打印错误，返回 None，不抛异常
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()  # 非 2xx 状态码会抛出 HTTPError（是 RequestException 的子类）
        data = resp.json()
        # 使用 .get() 或直接访问，若缺失则触发 KeyError，由外层捕获
        return {
            "temperature": data["current_weather"]["temperature"],
            "weathercode": data["current_weather"]["weathercode"],
        }
    except requests.exceptions.RequestException as e:
        # 捕获超时、连接错误、HTTP 错误等
        print(f"请求异常: {e}")
        return None
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # 捕获 JSON 解析失败或数据结构不符
        print(f"数据解析异常: {e}")
        return None
    except Exception as e:
        # 兜底，捕获任何未预料的异常（保证永不抛出）
        print(f"未知异常: {e}")
        return None

WEATHER = {
    0: "晴", 1: "晴间多云", 2: "多云", 3: "阴", 45: "雾", 48: "雾凇",
    51: "毛毛雨", 53: "小毛毛雨", 55: "毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "阵雨", 81: "强阵雨", 82: "暴雨",
    95: "雷暴", 96: "雷暴伴冰雹", 99: "雷暴伴冰雹",
}

def save_results(rows: list[dict], path: str) -> None:
    # 写 weather.csv：表头 city,temperature,weathercode，encoding="utf-8"
    with open(path, 'w', encoding='utf-8', newline="") as f:
        w = csv.DictWriter(f, fieldnames=["city", "temperature", "weathercode"])
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return None

# ============ 主流程 ============
# 读 cities.csv → 逐个 fetch_weather → 跳过 None → 打印 "城市 温度" → save_results
read_list = load_cities(str((BASE_DIR / "../../2026-08-10/cities.csv").resolve()))   # 改用相对路径
print(read_list)

re_list = list()
for i in range(len(read_list)):
    re_dict = dict()

    tem = fetch_weather(read_list[i]["latitude"],read_list[i]["longitude"])

    if tem is not None:
        desc = WEATHER.get(tem["weathercode"], f"未知代码{tem['weathercode']}")
        print(f"{read_list[i]['city']}，{tem['temperature']}℃ ，{desc}")
        re_dict["city"] = read_list[i]["city"]
        re_dict["temperature"] = tem["temperature"]
        re_dict["weathercode"] = tem["weathercode"]
        re_list.append(re_dict)

print(re_list)
save_results(re_list, str(BASE_DIR / "weather.csv"))   # 直接使用当前目录


# ============ assert / 自测 ============
# ① load_cities：正常解析 3 行 + 坏行跳过 + 文件不存在返回 []
#正常解析 3 行 + 坏行跳过
assert load_cities(str(BASE_DIR / "cities.csv")) == [{'city': '北京', 'latitude': 39.9042, 'longitude': 116.4074}, {'city': '上海', 'latitude': 31.2304, 'longitude': 121.4737}, {'city': '广州', 'latitude': 23.1291, 'longitude': 113.2644}]
#文件不存在返回 []
assert load_cities(str((BASE_DIR / "../../2026-08-10/citie.csv").resolve())) == []
# ② fetch_weather：真调一次（北京 39.9042,116.4074），确认 temperature 是数字
tem_bj = fetch_weather(39.9042,116.4074)["temperature"]
if type(tem_bj) in (int,float):
    print("是数字")
else:
    print("不是数字")
# ③ save_results：写完后读回 weather.csv，确认表头与内容
with open(str(BASE_DIR / "weather.csv"),'r',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # 检查表头
    assert reader.fieldnames == ["city","temperature","weathercode"]
    # 检查内容
    # 检查内容
    read_back = list(reader)
    for row in read_back:
        t = float(row["temperature"])   # 转数字失败会抛 ValueError，本身就是检查
        assert -50 < t < 60             # 地球温度范围
        w = int(row["weathercode"])
        assert 0 <= w <= 99             # WMO 标准码范围