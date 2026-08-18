"""Day 11 · dataclass 数据类（Week 2）

先读任务书「今日知识点预习」再动手。每个函数/类正上方都有它自己的要求（行为 + 边界 + 坑），
写哪部分看哪部分，不用回翻顶部。填空后运行：
    ".venv/Scripts/python.exe" submissions/2026-08/2026-W34/2026-08-17/dataclass_practice.py
预期输出：全部 assert 通过 + frozen 捕获打印，最后打印 Day 11 全过
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict


# ═══════════ 1. @dataclass class Student ═══════════
# 要求：
#   - 字段：name: str、scores: list[int] = field(default_factory=list)
#   - add_score(score: int) -> None：追加分数（只追加，不覆盖——Day 6 教训）
#   - average() -> float：平均分，空 scores 返回 0.0（Day 6 教训）
# 坑：可变默认值必须 field(default_factory=list)；写 scores: list = [] 会让所有实例共享同一个列表
@dataclass
class Student:
    name: str
    scores: list = field(default_factory=list)

    def add_score(self, score: int) -> None:
        # 你的实现：追加分数，不覆盖已有分数
        self.scores.append(score)
        return None

    def average(self) -> float:
        # 你的实现：空列表返回 0.0，否则返回平均分
        if len(self.scores) == 0:
            return 0.0
        else:
            return sum(self.scores)/len(self.scores)


# ═══════════ 2. @dataclass(frozen=True) class Point ═══════════
# 要求：字段 x: float, y: float（创建后不可改）
# 自测里会故意 p.x = 99，你要用 try/except（不能写到下面类中，写在自测里） 捕获 FrozenInstanceError 并打印「已冻结，改不了」
# 坑：frozen 只管字段绑定；p.x = 99 会抛 dataclasses.FrozenInstanceError，别让它崩
@dataclass(frozen=True)
class Point:
        x: float
        y: float

# ═══════════ 3. student_to_dict(s) ═══════════
# 要求：把 Student 转成普通 dict（用 asdict）
# 例：student_to_dict(Student("张三", [90])) == {"name": "张三", "scores": [90]}
def student_to_dict(s: Student) -> dict:
    # 你的实现：用 asdict
    s_dict = asdict(s)
    return s_dict

# ═══════════ 4. dict_to_student(d) ═══════════
# 要求：从 dict 还原 Student（Student(**d) 或手动构造）
# 坑：Student(**d) 要求 dict 的 key 和字段名完全一致，多一个 key 会 TypeError
def dict_to_student(d: dict) -> Student:
    # 你的实现：从 dict 还原 Student
    d_stu = Student(**d)
    return d_stu

# ═══════════ 5. top_student(students) ═══════════
# 要求：返回平均分最高的 Student；空列表返回 None
# 坑：max 可以带 key 参数（key=lambda s: s.average()）；空列表直接用 max 会 ValueError，先判空
def top_student(students: list) -> Student | None:
    # 你的实现：平均分最高者；空列表返回 None
    if not students:
        return None
    else:
        return max(students,key= lambda s: s.average())
        

# ============ 自测（别改这里） ============
if __name__ == "__main__":
    s1 = Student("张三")
    s1.add_score(90)
    s1.add_score(85)

    s2 = Student("李四")  # 不添加分数，验证 default_factory 隔离

    s3 = Student("王五")
    s3.add_score(60)
    s3.add_score(70)
    s3.add_score(80)

    assert s1.average() == 87.5, f"张三平均分，实际 {s1.average()}"
    assert s2.scores == [], "李四的列表必须是全新的（default_factory 隔离）"
    assert s2.average() == 0.0, "空列表平均分应为 0.0"
    assert s3.average() == 70.0, f"王五平均分，实际 {s3.average()}"

    d = student_to_dict(s1)
    assert d == {"name": "张三", "scores": [90, 85]}, f"asdict 结果，实际 {d}"

    s1_roundtrip = dict_to_student(d)
    assert s1_roundtrip == s1, "dict 往返后应相等（__eq__ 自动生成）"

    assert top_student([s1, s2, s3]) == s1, "平均分最高应为张三"
    assert top_student([]) is None, "空列表应返回 None"

    # frozen 实验：故意改 p.x，捕获 FrozenInstanceError
    p = Point(1.0, 2.0)
    try:
        p.x = 99.0
        print("frozen 实验失败：竟然改成功了")
    except Exception as e:
        print(f"已冻结，改不了：{type(e).__name__}")

    print("Day 11 全过")
