"""Day 7 练习：第 1 周综合验收 — 读 CSV → 调 API → 处理 → 写回文件。

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


def load_cities(path: str) -> list[dict]:
    # 读 CSV：跳过表头，坏行打印原因（复用 Day 5 逐行模式）
    # 文件不存在 → 打印提示，返回 []
    pass  # 删掉这句，写你的实现


def fetch_weather(lat: float, lon: float) -> dict | None:
    # requests.get(..., timeout=10) 必须设
    # 成功 → {"temperature": ..., "weathercode": ...}
    # 失败（超时/断网/非 200）→ 打印错误，返回 None，不抛异常
    pass  # 删掉这句，写你的实现


def save_results(rows: list[dict], path: str) -> None:
    # 写 weather.csv：表头 city,temperature,weathercode，encoding="utf-8"
    pass  # 删掉这句，写你的实现


# ============ 主流程 ============
# 读 cities.csv → 逐个 fetch_weather → 跳过 None → 打印 "城市 温度" → save_results


# ============ assert / 自测 ============
# ① load_cities：正常解析 3 行 + 坏行跳过 + 文件不存在返回 []
# ② fetch_weather：真调一次（北京 39.9042,116.4074），确认 temperature 是数字
# ③ save_results：写完后读回 weather.csv，确认表头与内容
