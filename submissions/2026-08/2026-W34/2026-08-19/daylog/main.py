"""daylog.main · 主流程 + 自测（Day 13 · 模块与包实战）

先读任务书「今日知识点预习」再动手。先 cd 进任务目录再运行（venv 在仓库根）：
    cd "D:/work-coding/Knowledge base/AI_KnowledgeBase/submissions/2026-08/2026-W34/2026-08-19"
    "D:/work-coding/Knowledge base/AI_KnowledgeBase/.venv/Scripts/python.exe" -m daylog.main
预期输出：logging 的 INFO 记录（带时间戳）+ 统计结果 + Day 13 全过
"""
import json
import logging
from pathlib import Path

from daylog import add_entry, load_entries, most_studied, total_minutes

LOG_FILE = Path(__file__).parent / "study_log.json"


# ═══════════ 1. run ═══════════
# 要求：
#   - run() -> str：完整主流程，做 5 件事：
#     ① logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
#        （asctime 就是预习 4 说的「时间戳」，logging 自动带上，不用手拼）
#     ② entries = load_entries(LOG_FILE) 读已有日志（第一次跑是空列表，别炸）
#     ③ add_entry(entries, "模块与包", 120) 追加今天这条
#     ④ logging.info 打一条（例：f"记录: 模块与包 120 分钟"）
#     ⑤ 用 json.dump 写回 LOG_FILE，必须 ensure_ascii=False + indent=2 + encoding="utf-8"
#     ⑥ total = total_minutes(entries)；top = most_studied(entries)
#     ⑦ logging.info 打统计（例：f"统计: 共 {total} 分钟，学得最多的是 {top}"）
#     ⑧ return f"{top} 共 {total} 分钟"
# 坑：json.dump 忘 ensure_ascii=False 中文会变 \uXXXX；logging 的 level 不设 INFO 就看不到 info 记录
def run() -> str:
    # 你的实现：
    ...


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    from datetime import date

    # 1. add_entry：原地追加 + 返回原列表 + 字段齐全
    base = []
    ret = add_entry(base, "语法", 30)
    assert ret is base, "add_entry 必须返回原列表（原地修改）"
    assert len(base) == 1 and base[0]["topic"] == "语法" and base[0]["minutes"] == 30
    assert base[0]["date"] == date.today().isoformat(), f"日期应为今天，实际 {base[0]['date']}"

    # 2. load_entries：文件不存在 → []；空文件 → []；正常文件 → 内容
    import tempfile
    tmp = Path(tempfile.mkdtemp())
    assert load_entries(tmp / "nope.json") == [], "文件不存在应返回 []"
    empty = tmp / "empty.json"
    empty.write_text("", encoding="utf-8")
    assert load_entries(empty) == [], "空文件应返回 []"
    good = tmp / "good.json"
    good.write_text('[{"date": "2026-08-01", "topic": "推导式", "minutes": 90}]', encoding="utf-8")
    assert load_entries(good) == [{"date": "2026-08-01", "topic": "推导式", "minutes": 90}]

    # 3. total_minutes：求和 + 空列表 0
    sample = [
        {"date": "2026-08-01", "topic": "推导式", "minutes": 60},
        {"date": "2026-08-02", "topic": "装饰器", "minutes": 90},
        {"date": "2026-08-03", "topic": "推导式", "minutes": 120},
    ]
    assert total_minutes(sample) == 270, f"应 270，实际 {total_minutes(sample)}"
    assert total_minutes([]) == 0, "空列表应返回 0"

    # 4. most_studied：看【累计】分钟数，不是单条最多
    assert most_studied(sample) == "推导式", f"推导式累计 180 最多，实际 {most_studied(sample)}"
    assert most_studied([]) == "", "空列表应返回空字符串"

    # 5. run：完整主流程（logging + 读写 json + 统计）
    if LOG_FILE.exists():
        LOG_FILE.unlink()  # 重跑前清掉上次的日志，保证断言确定
    result = run()
    assert "模块与包" in result and "120" in result, f"返回应含统计结果，实际 {result}"
    assert LOG_FILE.exists(), "run 后 study_log.json 应已生成"

    print("Day 13 全过")
