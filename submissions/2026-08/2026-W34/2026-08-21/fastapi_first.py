"""Day 15 · 第一个 FastAPI 服务：路由 + 参数 + Pydantic 校验

先读任务书「今日知识点预习」再动手。每个函数正上方都有它自己的要求（行为 + 边界 + 坑），
写哪部分看哪部分，不用回翻顶部。填空后运行（在仓库根）：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-21/fastapi_first.py
预期输出：全部 assert 通过，最后打印 Day 15 全过

数据结构约定（全文统一）：
- STUDENTS = 元素是 {"name": str, "age": int, "score": float} dict 的列表（预置数据，文件顶部定义）
- Student = Pydantic 模型（Day 14 学过的写法），POST 请求体用它校验

启动真实服务（自测之外体验用，见任务书第 4 项）：
    cd submissions/2026-08/2026-W34/2026-08-21
    ".venv/Scripts/python.exe" -m uvicorn fastapi_first:app --reload
    然后浏览器打开 http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Day 15 学员成绩 API")


# ═══════════ 1. Student 模型 ═══════════
# 要求：
#   - class Student(BaseModel)：三个字段
#       name: str
#       age: int
#       score: float = Field(ge=0, le=100)
#   - 和 Day 14 完全一样——FastAPI 的请求体校验就是 Pydantic 在干活
# 坑：POST 收到坏数据（age="abc" / score=150）时 FastAPI 自动返回 422，
#     你不需要写 try/except——框架替你捕获了 ValidationError 并转成 HTTP 响应
class Student(BaseModel):
    # 你的实现：
    name: str
    age: int
    score: float = Field(ge=0, le=100)


# ═══════════ 2. 预置数据 ═══════════
# 要求：
#   - STUDENTS = 3 个学生的 dict 列表（张三 20 岁 88.5 分 / 李四 21 岁 55.0 分 / 王五 22 岁 72.5 分）
# 坑：score 写浮点数不要写整数，和模型字段类型保持一致（写 88 也会被宽松转换，但养成好习惯）
STUDENTS = [
    {"name": "张三", "age": 20, "score": 88.5},
    {"name": "李四", "age": 21, "score": 55.0},
    {"name": "王五", "age": 22, "score": 72.5}
]


# ═══════════ 3. GET / ═══════════
# 要求：
#   - 装饰器 @app.get("/") 挂在函数上，函数返回 {"message": "hello"}
#   - FastAPI 会自动把 dict 转成 JSON 响应（响应头 Content-Type: application/json）
# 坑：返回的是 dict 不是字符串；路由路径 "/" 是根路径
@app.get("/")
def root():
    # 你的实现：
    return {"message": "hello"}


# ═══════════ 4. GET /students（查询参数过滤） ═══════════
# 要求：
#   - 装饰器 @app.get("/students")，查询参数 min_score: float = Query(0, ge=0, le=100)
#   - 返回 STUDENTS 中 score >= min_score 的学生列表（推导式一行）
#   - Query(0, ge=0, le=100)：默认 0、范围 0~100，越界/非数字自动 422
# 坑：Query 要 from fastapi import Query；参数名 min_score 会出现在 URL 里
#     即 GET /students?min_score=70；不带参数时用默认值 0（返回全部）
@app.get("/students")
def list_students(min_score: float = Query(0, ge=0, le=100)):
    # 你的实现：
    return [s for s in STUDENTS if s.get('score',0) >= min_score]


# ═══════════ 5. GET /students/{name}（路径参数） ═══════════
# 要求：
#   - 装饰器 @app.get("/students/{name}")，路径参数 name: str
#   - 在 STUDENTS 里找 name 匹配的学生：找到返回该学生 dict，找不到 raise
#     HTTPException(status_code=404, detail="not found")（响应体自动变 {"detail": "not found"}）
#   - 返回单个学生时要带上查询参数过滤逻辑吗？不用——本函数只管按名字查
# 坑：路径参数名必须和 {name} 占位符一致；用 next((s for s in STUDENTS if s["name"] == name), None)
#     是「找第一个匹配，找不到给默认值」的惯用写法；路由顺序：/students/{name} 只匹配
#     /students/ + 一段非空内容，**不会**吞掉 /students（查询参数不参与路由匹配）；
#     真正要小心的是和 /students/stats 这种固定子路径撞车——固定路径要声明在 {name} 前面
@app.get("/students/{name}")
def get_student(name: str):
    # 你的实现：
    student = next((s for s in STUDENTS if s["name"] == name),None)
    if student is None:
        raise HTTPException(status_code=404,detail="not found")
    return student


# ═══════════ 6. POST /students（请求体校验） ═══════════
# 要求：
#   - 装饰器 @app.post("/students", status_code=201)——创建成功返回 201 而不是默认 200
#   - 请求体参数 student: Student
#   - 把 student 转成 dict 追加进 STUDENTS（STUDENTS.append(student.model_dump())），返回新建的学生 dict
#   - 校验失败（缺字段/类型错/分数越界）FastAPI 自动 422，函数体不写 try/except
# 坑：Pydantic v2 用 .model_dump() 转 dict（不是 .dict()，那是 v1 的旧写法）；
#     201 要写在装饰器 status_code= 上，不是 return 里——「创建资源」和「查询资源」的语义分开，面试常考
@app.post("/students", status_code=201)
def add_student(student: Student):
    # 你的实现：
    STUDENTS.append(student.model_dump())
    return student.model_dump()


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # 1. GET / → 200 + JSON
    r = client.get("/")
    assert r.status_code == 200 and r.json() == {"message": "hello"}, r.text

    # 2. GET /students（无参数）→ 3 个预置学生
    r = client.get("/students")
    assert r.status_code == 200 and len(r.json()) == 3, f"应 3 个学生，实际 {r.text}"

    # 3. GET /students?min_score=70 → 只剩 >=70 的（张三 88.5、王五 72.5）
    r = client.get("/students", params={"min_score": 70})
    assert r.status_code == 200, r.text
    names = [s["name"] for s in r.json()]
    assert "张三" in names and "王五" in names and "李四" not in names, f"过滤失败: {names}"

    # 4. GET /students?min_score=abc → 422（查询参数校验失败也是 422）
    r = client.get("/students", params={"min_score": "abc"})
    assert r.status_code == 422, f"应 422，实际 {r.status_code}"

    # 5. GET /students/张三 → 找到
    r = client.get("/students/张三")
    assert r.status_code == 200 and r.json()["name"] == "张三", r.text

    # 6. GET /students/不存在的人 → 404 + detail
    r = client.get("/students/不存在的人")
    assert r.status_code == 404, f"应 404，实际 {r.status_code}"
    assert r.json() == {"detail": "not found"}, r.text

    # 7. POST 合法数据 → 201 + 返回新建的学生
    r = client.post("/students", json={"name": "赵六", "age": 23, "score": 66.0})
    assert r.status_code == 201, f"应 201，实际 {r.status_code}: {r.text}"
    assert r.json()["name"] == "赵六" and r.json()["score"] == 66.0, r.text
    # 再查一次列表，确认真的写进去了（4 个）
    assert len(client.get("/students").json()) == 4, "POST 后列表应变为 4 个"

    # 8. POST 坏数据（age 是字符串）→ 422，且错误信息能定位字段
    r = client.post("/students", json={"name": "钱七", "age": "abc", "score": 70})
    assert r.status_code == 422, f"应 422，实际 {r.status_code}"
    err = r.json()["detail"][0]
    assert "loc" in err and "age" in str(err["loc"]), f"错误应定位到 age 字段: {err}"

    print("Day 15 全过")
