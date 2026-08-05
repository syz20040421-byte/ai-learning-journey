"""Day 3 练习 ①：用 dict 把 first_unique 重写成 O(n)。

任务要求（验收标准）：
- 用 dict 数一遍每个元素出现次数，再遍历一次找第一个次数为 1 的
- 总体 O(n)，循环里不许再调用 items.count()
- 返回第一个只出现一次的字符串；没有则返回 None
- 写 3 个 assert 覆盖：空列表、有唯一元素、无唯一元素
  （参考：assert first_unique(["a", "b", "a"]) == "b"）
"""
from typing import Optional

def first_unique(items: list[str]) -> Optional[str]:
  # 你的实现：
  dict1 = {}
  for s in items:
    dict1[s] = dict1.get(s,0) + 1 
  for s in items:
    if dict1[s] == 1:
      return s

assert first_unique(["a", "b", "a"]) == "b" #有唯一元素
assert first_unique(["a", "a", "a"]) == None #无唯一元素
assert first_unique([]) is  None #空列表


print("通过")


  



# 你的 3 个 assert 写在这里（覆盖空列表 / 有唯一元素 / 无唯一元素）
