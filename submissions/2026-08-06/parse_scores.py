"""Day 4 练习 ②：带校验的分数解析 parse_scores。

任务要求（验收标准）：
- parse_score_line(line) 解析 "姓名,分数"（如 "张三,90"）
  - 没有逗号 → raise ValueError("缺少逗号")
  - 分数不是整数 → raise ValueError("分数不是整数")
  - 正常 → 返回 (姓名, 分数) 元组
- load_scores(lines) 逐行调用 parse_score_line
  - 某行抛 ValueError 时：打印 "第 N 行跳过：<原因>"，继续处理下一行（不能中断）
  - 正常行收进返回的 dict {姓名: 分数}
- 写 assert 覆盖：正常两行、坏行（无逗号）被跳过、坏行（分数非整数）被跳过、返回 dict 只含好行
"""
from typing import Tuple

def parse_score_line(line: str) -> Tuple[str, int]: #输入字符串返回元组，先定义一个空元组
    return_tuple = tuple()
    parts = line.split(",") 
    #将字符串以','作为分割界限分割，并写入到列表parts中
    if len(parts) < 2:
        raise ValueError("缺少逗号")
    #判断列表长度，如果小于2说明分割前字符串中没有','，即缺少成绩
    try:
        name,score = parts[0],int(parts[1])
    except ValueError:
        raise ValueError("分数不是整数")
    #parts中的元素都是字符串，如果要进行整数强转不确定是否成功，用try进行尝试，如果parts[1]不是整数，就会报错
    return_tuple = (name,score)
    return return_tuple

def load_scores(lines: list[str]) -> dict[str, int]: #输入列表，返回字典，先定义一个空字典
    return_dict = dict()
    for i,line in enumerate(lines,start=1):  
        #将列表中每一部分都遍历一遍 lines[i] = line，start = 1表示从lines[1]开始
        #enumerate表示同时取出lines中位置索引和对应的值
        try:
            name,score = parse_score_line(line)
        #将name和score分别对应到parse_score_line返回的元组("张三", 90) 
        except ValueError as e:
            print(f"第{i}行跳过：{e}")
            continue
        #将报错写进e中并打印
        else:
            return_dict[name] = score
        #写入返回的字典中
    return return_dict

# ========== assert 测试 ==========
lines = ["张三,90", "李四,abc", "王五", "赵六,85"]
result = load_scores(lines)

# 场景1：正常两行解析正确 + 场景4：dict 只含好行
assert result == {"张三": 90, "赵六": 85}
# 场景2：无逗号坏行（王五）被跳过
assert "王五" not in result
# 场景3：非整数坏行（李四,abc）被跳过
assert "李四" not in result

# 补充：parse_score_line 单测（正常路径）
assert parse_score_line("张三,90") == ("张三", 90)





