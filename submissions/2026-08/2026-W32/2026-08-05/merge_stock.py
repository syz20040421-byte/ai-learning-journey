"""Day 3 练习 ②：库存合并 merge_stock。

任务要求（验收标准）：
- 合并两家库存：相同 key 数量相加，只在 a 或只在 b 的 key 原样保留
- 返回【新】dict，不得修改 a 和 b 本身
- 写 3 个 assert 覆盖：空 dict 参与、key 重叠、key 完全不重叠
- 再加 1 个 assert 验证调用后 a、b 内容没变
- 加分项：用一行 dict 推导式实现（写得出就写，写不出明天教）
"""
from typing import Dict


def merge_stock(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    # 你的实现：
    result = dict(a)
    for k,v in b.items():
            if k in result:
                result[k] = a[k] + v
            else:
                result[k] = v
                
                
    return result

assert merge_stock({"a":1,"b":2,"c":3},{"a":1,"b":2,"c":3}) == {"a":2,"b":4,"c":6} #key 重叠
assert merge_stock({"a":1,"b":2},{"c":3}) == {"a":1,"b":2,"c":3} #key不重叠
assert merge_stock({},{}) == {} #key不重叠
a_orig = {"a": 1, "b": 2}
b_orig = {"c": 3}
merge_stock(a_orig, b_orig)
assert a_orig == {"a": 1, "b": 2}
assert b_orig == {"c": 3}  #调用后 a、b 内容没变



print("通过")



# 你的 3+1 个 assert 写在这里（空 dict / key 重叠 / key 不重叠 / a、b 未变）
