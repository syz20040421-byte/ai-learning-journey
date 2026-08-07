"""Day 5 练习：从文件读成绩 load_scores（摸底遗留 04 题）。

任务要求（验收标准）：
- load_scores(path) 读取文件，每行格式 "姓名,分数"
- 忽略空行；坏行（无逗号/分数非整数）跳过并打印 "第 N 行跳过：<原因>"
- 文件不存在 → 打印清晰提示，返回 {}（不能有 traceback 冒出来）
- 用 with open(...) 读，encoding="utf-8"，for line in f 逐行迭代
- 解析逻辑复制昨天的 parse_score_line（含两个 raise）
- 写 assert 覆盖：正常文件全解析、文件不存在返回 {}
- 末尾加「文件不存在」演示：load_scores("不存在的文件.txt")
"""
from typing import Tuple


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


def load_scores(path: str) -> dict[str, int]:
    # 你的实现：with open + try/except FileNotFoundError + 逐行解析
    file_line = []
    return_dict = dict()
    try:
        with open(path,'r',encoding='utf-8') as f:
            file_line = f.readlines()
    except FileNotFoundError:
        print("文件不存在")
    for i,line in enumerate(file_line,start=1):
        line1 = line.strip()
        if not line1:
            print(f"第{i}行跳过：空行")          # 跳过空行（可选，因为空行也会被解析异常捕获）
            continue
        try:
            name,score = parse_score_line(line)
        except ValueError as e:
            print(f"第{i}行跳过：{e}")
            #将报错写进e中并打印
        else:
            return_dict[name] = score
            #写入返回的字典中
    return return_dict 



# 你的 assert 写在这里（正常文件全解析 / 文件不存在返回 {}）
# 注意：测试用的 scores.txt 要自己造，放在本目录
assert load_scores("submissions/2026-08-07/scores.txt") == {"张三": 100,"里斯": 90,"英超": 85,"法甲": 89}
# 文件不存在演示（打印提示、返回 {}、无 traceback）：
assert load_scores("submissions/2026-08-07/scor.txt") == {}
# print(load_scores("不存在的文件.txt"))
print(load_scores("submissions/2026-08-07/scor.txt"))