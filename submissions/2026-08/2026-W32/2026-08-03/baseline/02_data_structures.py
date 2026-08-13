def first_unique(items: list[str]) -> str | None:
    # 返回列表中第一个只出现一次的字符串；没有则返回 None
    # 不得修改 items
    for s in items:
        a = items.count(s)
        if a == 1:
            return s
    return None
   
assert(first_unique(["a","b","a"])) == "b"
assert(first_unique([])) == None
assert(first_unique(["x","x"])) == None
 

print("完成")