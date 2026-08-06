# 技术英语
1. 词汇：Syntax Error：语法错误  Exception：异常  Handing Exception：异常处理  raise：触发  chaining：链接  user-define：自定义  finally：最终  parser：解析器  repeat：重复  correct：正确的  identifier：标识符
2. 摘抄：
- 原文：However, it is good practice to be as specific as possible with the types of exceptions that we intend to handle, and to allow any unexpected exceptions to propagate on.
- 译文：然而，好的做法是，尽可能具体地说明我们打算处理的异常类型，并允许任何意外的异常传播下去。
3. 总结
- 异常处理：try: 尝试的具体操作 ->1.异常 except _Error：报错处理 or ->2.无异常 else：下一步操作 or ->3.有无异常都进行 finally
- 触发异常：raise exception（异常类型）->直接触发异常 ->找except ->无 报错中断 ->有 执行
- 异常链（异常转换）：try：异常A  except _Error：异常B form exc（异常实例）or None -> exc：先报异常B，再链接异常A  -> None：只报异常B

# 问题
1. 你昨天用 return None 表示「没有找到」，今天用 raise 表示「输入非法」——什么情况该返回 None、什么情况该抛异常？你的判断标准
- 如果“没找到”是业务上允许的正常分支（调用方需自行处理），就返回 `None`；如果参数本身破坏了函数运行的前提条件（契约违规），就该立即抛出异常，把 Bug 暴露给调用方修复，而不是静默掩盖。

2. except Exception 能接住所有错误，为什么说它是反模式？（提示：会把什么不该吞的错误也吞掉？）
- `except Exception` 最大的问题在于它会吞掉 `KeyboardInterrupt`（Ctrl+C）和你代码中因拼写/逻辑错误引发的 `NameError` 等 Bug，让程序“死得不明不白”——正确的做法是只捕获你预期会发生的具体异常（如 `ValueError`），把意料之外的错误暴露出来以便及时修复。

3. 什么场景必须用 `finally`，用 `else`又省了什么？
- 无论执行`try`成功与否，都要进行的操作要用`finally`，比如关闭文件、关闭数据库连接等资源释放场景。执行`try`成功后，要进行接下来的操作时用`else`。

# 今日一问
`try/except` 里写了 `finally` 之后，如果 `try` 里 `return` 了，`finally` 还会执行吗？为什么？明天批改会追问。
- 会。无论try的结果怎么样，finally都会执行