def fizzbuzz(n: int) -> list[str]:
    # 在这里写你的实现：
    # 3 的倍数 -> "Fizz"，5 的倍数 -> "Buzz"，同时是 3 和 5 的倍数 -> "FizzBuzz"
    # 其他 -> 数字的字符串；n <= 0 返回空列表
    if n <= 0:
        return []
    lst = []
    for i in range(1,n+1):
        if i%3 == 0 and i%5 == 0:
            lst.append("FizzBuzz")
        elif i%3 == 0:
            lst.append("Fizz")
        elif i%5 == 0:
            lst.append("Buzz")
        else:
            lst.append(str(i))
    return lst

# 在这里写至少 3 个 assert，覆盖 1、15、0 三种情况
# 例：assert fizzbuzz(1) == ["1"]
assert fizzbuzz(1) == ["1"]
assert fizzbuzz(0) == []
assert fizzbuzz(15) == ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]


print("01_syntax.py 跑通了")
