"""Day 15 · HTTP 解剖：用 requests 拆开真实请求/响应

先读任务书「今日知识点预习」再动手。每个函数正上方都有它自己的要求（行为 + 边界 + 坑），
写哪部分看哪部分，不用回翻顶部。填空后运行（在仓库根）：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-21/http_probe.py
预期输出：全部 assert 通过，最后打印 HTTP probe 全过

数据结构约定（全文统一）：
- 本文件没有跨函数共享的数据结构；每个函数只返回自己的字典/数值
- 注意：httpbingo.org 返回的 args/headers 值是**数组**形式（如 {"name": ["alice"]}），
  取字段要带 [0]，这是它和 httpbin 的一个差异
"""
import requests


# ═══════════ 1. probe_status ═══════════
# 要求：
#   - probe_status(url) -> int：GET 请求并返回状态码（不调 raise_for_status）
#   - 必须带 timeout=10——真实网络请求不设超时，服务器卡住你的脚本就永远挂起
# 坑：requests.get 对 4xx/5xx **默认不抛异常**，resp.status_code 还是能拿到；
#     想让它抛异常必须手动 resp.raise_for_status()（这是 Day 8 学过的）
def probe_status(url: str) -> int:
    # 你的实现：
    ...


# ═══════════ 2. probe_headers ═══════════
# 要求：
#   - probe_headers(url) -> dict：返回 {"content_type": ..., "server": ...}
#   - content_type 取 resp.headers.get("Content-Type")，server 取 resp.headers.get("Server")
#   - header 名大小写不敏感：resp.headers["content-type"] 和 ["Content-Type"] 都能取到
# 坑：headers.get() 取不到时返回 None，不要用 resp.headers["..."] 直接索引（可能 KeyError）
def probe_headers(url: str) -> dict:
    # 你的实现：
    ...


# ═══════════ 3. probe_args ═══════════
# 要求：
#   - probe_args(url, params: dict) -> dict：GET 请求带查询参数，返回 resp.json()["args"]
#   - 即服务器回显收到的查询参数（httpbingo 会把 query string 原样回显）
# 坑：httpbingo 的 args 值全是数组，如 {"name": ["alice"]}——取出时要带 [0]
def probe_args(url: str, params: dict) -> dict:
    # 你的实现：
    ...


# ═══════════ 4. probe_404 ═══════════
# 要求：
#   - probe_404() -> tuple[int, bool]：请求 httpbingo.org/status/404，
#     返回 (状态码, ok 布尔值)；resp.ok 在 4xx/5xx 时为 False
#   - 不 try/except、不 raise_for_status——就用默认行为观察
# 坑：resp.ok 才是「请求是否成功」的正确判断；status_code == 404 但 ok == False
def probe_404():
    # 你的实现：
    ...


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    BASE = "https://httpbingo.org"

    # 1. probe_status：真实请求 200
    st = probe_status(f"{BASE}/get?name=alice")
    assert st == 200, f"应 200，实际 {st}"

    # 2. probe_headers：Content-Type 含 json
    hd = probe_headers(f"{BASE}/get")
    assert hd["content_type"] and "json" in hd["content_type"].lower(), f"content_type 异常: {hd}"

    # 3. probe_args：查询参数回显（注意 httpbingo 值是数组）
    args = probe_args(f"{BASE}/get", {"name": "alice", "score": "88.5"})
    assert args["name"][0] == "alice", f"name 回显异常: {args}"
    assert args["score"][0] == "88.5", f"score 回显异常: {args}"

    # 4. probe_404：状态码 404 且 ok=False
    code, ok = probe_404()
    assert code == 404 and ok is False, f"应 (404, False)，实际 {(code, ok)}"

    print("HTTP probe 全过")
