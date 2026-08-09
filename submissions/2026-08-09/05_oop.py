"""Day 6 练习：类与实例（OOP 补漏）。

任务要求（验收标准）：
- Student 类：类属性 school = "AI 学习营"，实例属性 name / scores
- __init__ 必须用 scores=None + 判空，不能写 scores=[]（可变默认参数陷阱）
- add_score(score) 追加一个分数
- average() 返回平均分；scores 为空时返回 0.0（不抛异常）
- __str__ 返回 "张三(90分, 85分) - AI 学习营" 这样的描述
- 类属性 vs 实例属性实验：3 条 assert + 注释解释每步输出
- 综合部分：复用 load_scores 读 scores.txt → 生成 Student 列表 → 写 summary.txt
  （含表头 "姓名,平均分"，encoding="utf-8"）
"""
from __future__ import annotations


class Student:
    school = "AI 学习营"  # 类属性：所有实例共享

    def __init__(self, name: str, scores: list[int] | None = None):
        # 不能写 scores=[] 当默认值（为什么？见预习第 9 条）
        pass  # 删掉这句，写你的实现

    def add_score(self, score: int) -> None:
        pass  # 追加一个分数到 self.scores

    def average(self) -> float:
        pass  # 返回平均分；scores 为空时返回 0.0（不能崩）

    def __str__(self) -> str:
        pass  # 返回 "张三(90分, 85分) - AI 学习营" 这样的描述


# ============ ② 类属性 vs 实例属性实验 ============
# 1. 创建两个学生 stu1 / stu2，打印 stu1.school 和 stu2.school（应该都是 "AI 学习营"）
# 2. Student.school = "AI 学院"  —— 通过类名改，再打印两个实例（都变了？为什么？）
# 3. stu1.school = "隔壁班"      —— 通过实例改，再打印 stu1.school 和 stu2.school
#    （stu1 变了、stu2 没变？为什么？这叫什么？——预习第 5 条）
# 4. 写 3 条 assert 验证第 2、3 步的行为：类属性全体生效、实例赋值只改自己

# ============ ③ 串起来：文件 → 对象 → 文件 ============
# 1. 把昨天 04_file_io.py 里的 load_scores 复制到下面（含两个 raise 的 parse_score_line）
# 2. 用它读本目录的 scores.txt（自己造测试数据：至少 4 行有效、1 空行、2 坏行）
# 3. 把每个 姓名->分数 变成 Student 实例，装进列表
# 4. 打印每个学生的 "姓名 平均分"
# 5. 把所有学生的 "姓名,平均分" 写进 summary.txt（含表头，encoding="utf-8"）


def load_scores(path: str) -> dict[str, int]:
    # 复制昨天 04_file_io.py 里的实现（文件不存在返回 {}，无 traceback）
    pass  # 删掉这句，写你的实现


# ============ assert 写在这里 ============
# ① Student 类：add_score / average（空列表返回 0.0）/ __str__ 格式
# ② 类属性/实例属性：类属性全体生效、实例赋值只改自己（至少 3 条）
# ③ 综合：load_scores 正常解析 + 文件不存在返回 {} + summary.txt 内容与打印一致

# ============ 主流程演示 ============
# 创建学生 → 打印 → 写 summary.txt（放在文件末尾，python 05_oop.py 直接可跑）
