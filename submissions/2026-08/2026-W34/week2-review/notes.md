# Week 2 周检 · 文字概念题

> 代码题在 `q1_comprehension.py` / `q2_decorators.py` / `q3_dataclass_async.py`。
> 这里是文字题：每题 3–5 句，答「为什么」不答「怎么写」，直接写在题目下方。

## 1. 列表推导式 vs for 循环 vs 生成器表达式

你 Day 9 写了列表推导式——同样功能 for 循环也能写，为什么推导式更简洁？`[...]` 和 `(...)` 生成器表达式在**内存**上差在哪（假设有 10 万元素，哪个先爆内存）？

答：

## 2. 装饰器语法糖与三层嵌套

你 Day 10 写了装饰器——为什么说 `@timer` 只是 `timer(func)` 的语法糖？如果装饰器本身要带参数（比如 `@retry(3)`），为什么要三层嵌套？

答：

## 3. dict vs dataclass

你 Day 11 写了 dataclass——dict 也能存学生数据，为什么还要定义 `Student` 类？在「访问字段 / 拼错 key / 加方法」三个维度上，dict 和 dataclass 差在哪？

答：
