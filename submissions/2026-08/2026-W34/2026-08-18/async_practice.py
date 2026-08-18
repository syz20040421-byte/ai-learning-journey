"""Day 12 · async/await 入门（Week 2）

先读任务书「今日知识点预习」再动手。每个函数正上方都有它自己的要求（行为 + 边界 + 坑），
写哪部分看哪部分，不用回翻顶部。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-18/async_practice.py
预期输出：全部 assert 通过，最后打印 Day 12 全过
"""
import asyncio
import time


# ═══════════ 1. async def fetch_one ═══════════
# 要求：
#   - async def fetch_one(name: str, delay: float = 0.05) -> str
#   - await asyncio.sleep(delay) 模拟一次耗时的网络请求（等的时候让出控制权）
#   - 返回 f"{name} 完成"
# 坑：用 asyncio.sleep（假装睡觉、让出事件循环），别用 time.sleep（真阻塞，会堵死整个循环）
async def fetch_one(name: str, delay: float = 0.05) -> str:
    # 你的实现：
    ...


# ═══════════ 2. async def fetch_all ═══════════
# 要求：
#   - async def fetch_all(names: list) -> list：对每个名字并发发起 fetch_one（delay 用默认 0.05）
#   - 用 asyncio.gather 一次性并发跑，返回结果列表
#   - 结果顺序必须和 names 输入顺序一致（gather 保序，不用自己排序）
# 坑：for 循环里逐个 await 是串行（等完 A 才跑 B）；gather(*tasks) 别忘了星号展开列表
async def fetch_all(names: list) -> list:
    # 你的实现：
    ...


# ═══════════ 3. async def tick_tock ═══════════
# 要求：
#   - async def tick_tock() -> list：两个 worker 协程交替干活，证明事件循环是「协作式切换」
#   - 在函数内部定义 async def worker(name: str) -> None：
#     循环 3 次（i = 1,2,3），每次往共享列表 events append f"{name}{i}"，然后 await asyncio.sleep(0) 让出
#   - 用 asyncio.gather(worker("A"), worker("B")) 同时跑，返回 events
#   - 预期结果：["A1", "B1", "A2", "B2", "A3", "B3"]（A/B 严格交替！）
# 坑：不写 await asyncio.sleep(0) 的话，worker A 会一口气跑完 3 次，根本不会交替
async def tick_tock() -> list:
    events = []
    # 你的实现：定义内部 worker 并 gather
    ...


# ═══════════ 4. async def compare_times ═══════════
# 要求：
#   - async def compare_times(names: list) -> dict
#   - 用 time.perf_counter（Day 10 学的）分别测两种跑法的总耗时：
#     ① 串行：for 循环逐个 await fetch_one(n, 0.15)
#     ② 并发：asyncio.gather 同时跑 3 个 fetch_one(n, 0.15)
#   - 返回 {"sequential": 串行耗时, "concurrent": 并发耗时}（浮点秒）
# 坑：两次计时都要包住完整的跑法；delay 固定 0.15，串行≈0.45s vs 并发≈0.15s，差距才明显
async def compare_times(names: list) -> dict:
    # 你的实现：
    ...


# ═══════════ 5. def call_async_from_sync ═══════════
# 要求：
#   - def call_async_from_sync() -> str：普通同步函数（没有 async 前缀！）
#   - 里面用 asyncio.run(fetch_one("桥", 0.01)) 调用协程，返回它的结果
# 坑：同步函数里直接 await 是 SyntaxError（'await' outside async function）；asyncio.run 是同步↔异步的桥
def call_async_from_sync() -> str:
    # 你的实现：
    ...


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    # 1. 协程「不 await 不执行」：调用只得到 coroutine 对象，函数体还没跑
    c = fetch_one("测试", 0.01)
    assert asyncio.iscoroutine(c), "fetch_one(...) 返回的必须是 coroutine 对象"
    c.close()  # 不执行就释放

    assert asyncio.run(fetch_one("A", 0.01)) == "A 完成"

    # 2. gather 并发 + 保序
    res = asyncio.run(fetch_all(["A", "B", "C"]))
    assert res == ["A 完成", "B 完成", "C 完成"], f"保序失败，实际 {res}"

    # 3. 协作式切换：A/B 严格交替，而不是 A 跑完再 B
    events = asyncio.run(tick_tock())
    assert len(events) == 6, f"事件数不对，实际 {events}"
    assert all(events[i][0] != events[i + 1][0] for i in range(5)), f"没有交替，实际 {events}"

    # 4. 并发 < 串行
    t = asyncio.run(compare_times(["A", "B", "C"]))
    print(f"串行 {t['sequential']:.3f}s / 并发 {t['concurrent']:.3f}s")
    assert t["concurrent"] < t["sequential"], "并发应该比串行快"

    # 5. 同步函数里调协程
    assert call_async_from_sync() == "桥 完成"

    print("Day 12 全过")
