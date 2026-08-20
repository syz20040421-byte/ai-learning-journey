"""Day 14 · Pydantic：数据校验自动化（Week 2 收官）

先读任务书「今日知识点预习」再动手。每个函数正上方都有它自己的要求（行为 + 边界 + 坑），
写哪部分看哪部分，不用回翻顶部。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-20/pydantic_practice.py
预期输出：全部 assert 通过，最后打印 Day 14 全过
"""
from pydantic import BaseModel, Field, ValidationError


# ═══════════ 1. 模型定义 ═══════════
# 要求：
#   - class Student(BaseModel)：三个字段
#       name: str
#       age: int
#       score: float = Field(ge=0, le=100)   # 分数 0~100，越界直接校验失败
#   - class ClassRoom(BaseModel)：一个字段 students: list[Student]（嵌套模型）
# 坑：Field 从 pydantic 导入（不是 dataclasses 的 field）；字段顺序就是报错里 loc 的顺序
class Student(BaseModel):
    # 你的实现：
    ...


class ClassRoom(BaseModel):
    # 你的实现：
    ...


# ═══════════ 2. make_student ═══════════
# 要求：
#   - make_student(name, age, score) -> Student：用三个参数构造 Student 并返回
#   - 不做任何手动校验——类型转换、越界检查全部交给 Pydantic
#   - 校验失败时 ValidationError 直接往外抛（不捕获，让调用方决定）
# 坑：别写 if score > 100: raise ...——Field 约束已经干了这事，重复检查就是不相信自己声明的规则
def make_student(name, age, score) -> Student:
    # 你的实现：
    ...


# ═══════════ 3. safe_score ═══════════
# 要求：
#   - safe_score(row: dict) -> tuple：接收一行成绩 dict（可能缺字段/类型错/分数越界）
#   - 成功：返回 (Student, "")；失败：返回 (None, 错误信息字符串)
#   - 错误信息格式："字段 age: Input should be a valid integer"——
#     从 e.errors()[0] 取 loc（可能是元组，如 ('age',)）和 msg 拼出来
# 坑：ValidationError 要 from pydantic import；e.errors() 是列表，可能有多条，取第一条即可；
#     loc 是元组不是字符串，拼信息时先取 [0]
def safe_score(row: dict):
    # 你的实现：
    ...


# ═══════════ 4. load_class ═══════════
# 要求：
#   - load_class(rows: list) -> ClassRoom：把一整份成绩单（dict 列表）整体交给 ClassRoom 校验
#   - 直接 return ClassRoom(students=rows)——dict 会自动转成 Student 实例
#   - 任何一条坏数据 → 整个构造失败，ValidationError 往外抛（不捕获）
# 坑：嵌套校验是递归的，坏行会让整份数据进不来；错误信息 loc 会带下标，如 ('students', 2, 'score')
def load_class(rows: list) -> ClassRoom:
    # 你的实现：
    ...


# ═══════════ 5. pass_rate ═══════════
# 要求：
#   - pass_rate(students: list) -> float：及格（score >= 60）人数占比
#   - 空列表返回 0.0
# 坑：先数及格人数再除总数；Python 3 里 / 已经是浮点除法，别写 //
def pass_rate(students: list) -> float:
    # 你的实现：
    ...


# ============ 自测（别改这里） ============
if __name__ == "__main__":
    # 1. make_student：合法数据 → 实例
    s = make_student("张三", 20, 88.5)
    assert isinstance(s, Student) and s.name == "张三" and s.age == 20 and s.score == 88.5

    # 2. 宽松转换："21" 自动转 int
    s2 = make_student("李四", "21", 90)
    assert s2.age == 21 and isinstance(s2.age, int), f"age 应为 int 21，实际 {s2.age!r}"

    # 3. 约束：分数越界 → ValidationError
    for bad_score in (150, -1):
        try:
            make_student("王五", 22, bad_score)
            raise AssertionError(f"score={bad_score} 应触发 ValidationError")
        except ValidationError:
            pass

    # 4. safe_score：好行 → (Student, "")
    ok, err = safe_score({"name": "赵六", "age": 23, "score": 59.5})
    assert isinstance(ok, Student) and err == "", f"好行应通过，实际 {err!r}"

    # 5. safe_score：坏行 → (None, 错误信息)，信息要能定位字段
    bad, msg = safe_score({"name": "钱七", "age": "abc", "score": 70})
    assert bad is None and "age" in msg, f"坏行应返回 None + 含字段名的错误，实际 {msg!r}"

    # 6. load_class：嵌套模型整体校验
    room = load_class([
        {"name": "A", "age": 20, "score": 100},
        {"name": "B", "age": 21, "score": 59},
    ])
    assert len(room.students) == 2 and all(isinstance(st, Student) for st in room.students)

    # 7. load_class：里面混一条坏数据 → 整个 ValidationError
    try:
        load_class([
            {"name": "A", "age": 20, "score": 100},
            {"name": "B", "age": 21},  # 缺 score
        ])
        raise AssertionError("缺字段应触发 ValidationError")
    except ValidationError:
        pass

    # 8. pass_rate：及格率 + 空列表
    three = [
        Student(name="甲", age=20, score=60),
        Student(name="乙", age=20, score=59),
        Student(name="丙", age=20, score=100),
    ]
    assert abs(pass_rate(three) - 2 / 3) < 1e-9, f"及格率应 2/3，实际 {pass_rate(three)}"
    assert pass_rate([]) == 0.0, "空列表及格率应为 0.0"

    print("Day 14 全过")
