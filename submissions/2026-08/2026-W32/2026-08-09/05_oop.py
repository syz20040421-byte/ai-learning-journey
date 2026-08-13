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
from typing import Tuple


class Student:
    school = "AI 学习营"  # 类属性：所有实例共享

    def __init__(self, name: str, scores: list[int] | None = None):
        # 不能写 scores=[] 当默认值（为什么？见预习第 9 条）
        self.name = name
        if scores is None:
            self.scores = []
        else:
            self.scores = scores

    def add_score(self, score: int) -> None:
        self.scores.append(score)
        return self.scores

    def average(self) -> float | None:    # 返回平均分；scores 为空时返回 0.0（不能崩）
        e = 0.0
        if len(self.scores) == 0:
            return 0.0
        else:
            for i in range(len(self.scores)):
                if self.scores[i] < 0:
                    print(f"{self.name}的第{i+1}个分数输入错误")
                    return None
                else:
                    e += self.scores[i]
        return e/len(self.scores)

    def __str__(self) -> str:
        scores_str = ", ".join(f"{s}分" for s in self.scores)
        return f"{self.name}({scores_str}) - {self.school}"  # 返回 "张三(90分, 85分) - AI 学习营" 这样的描述


# ============ ② 类属性 vs 实例属性实验 ============
# 1. 创建两个学生 stu1 / stu2，打印 stu1.school 和 stu2.school（应该都是 "AI 学习营"）
stu1 = Student("mesi",[91])
stu2 = Student("c罗",[89])
print(stu1.school)
print(stu2.school)
# 2. Student.school = "AI 学院"  —— 通过类名改，再打印两个实例（都变了？为什么？）
Student.school = "AI 学院"
print(stu1.school)
print(stu2.school)
# 3. stu1.school = "隔壁班"      —— 通过实例改，再打印 stu1.school 和 stu2.school
#    （stu1 变了、stu2 没变？为什么？这叫什么？——预习第 5 条）
stu1.school = "隔壁班"
print(stu1.school)
print(stu2.school)
# 4. 写 3 条 assert 验证第 2、3 步的行为：类属性全体生效、实例赋值只改自己
assert(stu2.school) == "AI 学院"
assert(stu1.school) == "隔壁班"
assert Student.school == "AI 学院"
# ============ ③ 串起来：文件 → 对象 → 文件 ============
# 1. 把昨天 submissions/2026-08-07/04_file_io.py 里的两个函数都复制过来：
#    - parse_score_line(line)（含两个 raise：缺逗号 / 分数非整数）
#    - load_scores(path)（它内部调用 parse_score_line，所以两个都要带过来）
#    复制时改掉昨天的一个小毛病：load_scores 读文件要用 for line in f 逐行迭代，
#    不要用 f.readlines() 一次性全读（昨天的批改提过）
# 2. 用它读本目录的 scores.txt（自己造测试数据：至少 4 行有效、1 空行、2 坏行）
# 3. 把每个 姓名->分数 变成 Student 实例，装进列表
# 4. 打印每个学生的 "姓名 平均分"
# 5. 把所有学生的 "姓名,平均分" 写进 summary.txt（含表头，encoding="utf-8"）


def parse_score_line(line: str) -> Tuple[str, int]:
    return_tuple = tuple()
    parts = line.split(",") 
    #将字符串以','作为分割界限分割，并写入到列表parts中
    if len(parts) < 2:
        raise ValueError("缺少逗号")
    #判断列表长度，如果小于2说明分割前字符串中没有','，即缺少成绩
    try:
        name = parts[0].strip()
        score = int(parts[1].strip())
    except ValueError:
        raise ValueError("分数不是整数")
    #parts中的元素都是字符串，如果要进行整数强转不确定是否成功，用try进行尝试，如果parts[1]不是整数，就会报错
    return_tuple = (name,score)
    return return_tuple


def load_scores(path: str) -> dict[str, list[int]]:
    return_dict = dict()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):   # 逐行迭代，无需readlines()
                line1 = line.strip()
                if not line1:
                    print(f"第{i}行跳过：空行")
                    continue
                try:
                    name, score = parse_score_line(line)
                except ValueError as e:
                    print(f"第{i}行跳过：{e}")
                else:
                    if name not in return_dict:
                        return_dict[name] = []
                    return_dict[name].append(score)
    except FileNotFoundError:
        print("文件不存在")
    return return_dict 

dict_student = load_scores("submissions/2026-08-09/scores.txt")
list_student = []

for key,vaule in dict_student.items():
    stu = Student(key,vaule)
    list_student.append(stu)

#打印平均成绩
for stu in list_student:
    print (stu.name,stu.average())

#文件写入
# 写入 summary.txt
with open("submissions/2026-08-09/summary.txt", "w", encoding="utf-8") as f:
    f.write("姓名,平均分\n")
    for stu in list_student:
        avg = stu.average()
        # 如果你没有简化 average，avg 可能为 None，这里转为 0.0 避免写入 None
        # 但按任务要求，avg 应为浮点数，所以最好简化 average
        f.write(f"{stu.name},{stu.average()}\n")   # 保留一位小数，更美观


# ============ assert 写在这里 ============
# ① Student 类：add_score / average（空列表返回 0.0）/ __str__ 格式
assert stu1.add_score(92) == [91,92]
assert stu1.average() == 91.5
stu3 = Student("mubap")
stu4 = Student("dbl",[-99])
assert stu3.average() == 0.0
assert stu4.average() is None
assert stu1.__str__() == "mesi(91分, 92分) - 隔壁班"
# ② 类属性/实例属性：类属性全体生效、实例赋值只改自己（至少 3 条）
assert Student.school == "AI 学院"
assert(stu1.school) == "隔壁班"
assert(stu2.school) == "AI 学院"
# ③ 综合：load_scores 正常解析 + 文件不存在返回 {} + summary.txt 内容与打印一致
# 正常解析
#assert load_scores("submissions/2026-08-09/scores.txt") == {"张三": 100,"里斯": 90,"英超": 85,"法甲": 89}
# 文件不存在演示（打印提示、返回 {}、无 traceback）：
assert load_scores("submissions/2026-08-09/scor.txt") == {}
# print(load_scores("不存在的文件.txt"))
print(load_scores("submissions/2026-08-09/scor.txt"))
print(stu4.average())
# ============ 主流程演示 ============
# 创建学生 → 打印 → 写 summary.txt（放在文件末尾，python 05_oop.py 直接可跑）
