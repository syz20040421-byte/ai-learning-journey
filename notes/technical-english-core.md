# 高频技术英语核心词汇表（Python 文档篇）

> 用法：每天积累 10 个。先遮住中文回忆英文含义，再看中文核对。
> 技术文档的英语其实很窄——这 50 个词覆盖了官方文档 80% 的常见词。认全了再看原文，阻力会小一大半。

## 第一组：程序结构（Day 1）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| statement | 语句（一行代码） | "A `for` statement..." |
| expression | 表达式（有值的代码） | "any expression" |
| loop | 循环 | "the loop terminates" |
| iterate / iteration | 迭代 / 每一次循环 | "iterate over a list" |
| break | 跳出（循环） | "`break` out of the loop" |
| continue | 继续（跳过本次） | "`continue` to the next iteration" |
| block | 代码块（缩进的一段） | "the block of statements" |
| condition | 条件 | "if the condition is true" |
| body | 循环/函数体 | "the body of the loop" |
| clause | 子句（else 子句） | "the `else` clause" |

## 第二组：函数与数据（Day 2）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| function | 函数 | "define a function" |
| argument / parameter | 实参 / 形参 | "takes two arguments" |
| return | 返回 | "return a value" |
| call / invoke | 调用 | "call the function" |
| variable | 变量 | "assign to a variable" |
| assign / assignment | 赋值 | "variable assignment" |
| scope | 作用域 | "local scope" |
| global / local | 全局 / 局部 | "global variable" |
| string | 字符串 | "a string of text" |
| integer | 整数 | "an integer value" |
| float | 浮点数 | "floating point number" |
| boolean | 布尔值（True/False） | "a boolean value" |

## 第三组：数据结构（Day 3）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| list | 列表 | "a list of items" |
| dictionary / dict | 字典 | "dict keys" |
| set | 集合 | "set membership" |
| tuple | 元组 | "a tuple of values" |
| item / element | 元素 | "each item" |
| key / value | 键 / 值 | "key-value pairs" |
| index | 下标 | "index starts at 0" |
| slice | 切片 | "slice of a list" |
| sequence | 序列（list/str/tuple 的统称） | "any sequence type" |
| container | 容器 | "a container of items" |

## 第四组：类与错误（Day 4）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| class | 类 | "define a class" |
| method | 方法（类里的函数） | "call its methods" |
| attribute | 属性 | "instance attributes" |
| instance | 实例（对象） | "create an instance" |
| object | 对象 | "every object" |
| self | 自身（实例方法第一个参数） | "self.attr" |
| exception | 异常 | "raise an exception" |
| raise | 抛出 | "raise ValueError" |
| handle / catch | 处理 / 捕获 | "handle the error" |
| error | 错误 | "runtime error" |
| valid / invalid | 合法 / 不合法 | "invalid argument" |
| optional | 可选的 | "an optional argument" |

## 第五组：文件、命令行与网络（Day 5）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| file | 文件 | "open a file" |
| path | 路径 | "the file path" |
| open / close | 打开 / 关闭 | "open the file" |
| read / write | 读 / 写 | "read from a file" |
| command | 命令 | "command line" |
| flag / option | 选项 | "command-line options" |
| default | 默认值 | "default value" |
| request / response | 请求 / 响应 | "HTTP request" |
| status code | 状态码 | "status code 200" |
| server / client | 服务器 / 客户端 | "client error" |

## 第六组：面向对象（Day 6）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| define | 定义 | "define a class" |
| attribute | 属性 | "instance attributes" |
| instance | 实例（对象） | "create an instance" |
| class attribute | 类属性（属于类，全体共享） | "class attributes are shared" |
| shared | 共享的 | "shared by all instances" |
| bind / binding | 绑定（把名字绑到对象） | "the name is bound to the object" |
| assign | 赋值 | "assign an attribute" |
| lookup | 查找（按名字找值） | "attribute lookup" |
| override / shadow | 覆盖 / 遮蔽（实例属性盖住类属性） | "an instance attribute shadows the class attribute" |
| constructor | 构造方法（`__init__`） | "the constructor is called" |

## 第七组：HTTP 与 API（Day 7）

| 英文 | 中文 | 出现场景 |
|---|---|---|
| endpoint | 端点（API 的具体地址） | "the API endpoint" |
| query parameter | 查询参数（URL 问号后的 ?key=value） | "query parameters are passed in the URL" |
| JSON | 一种键值对数据格式 | "the response is in JSON format" |
| timeout | 超时（等待上限） | "set a timeout for the request" |
| header | 请求头 / 响应头 | "the request headers" |
| payload | 载荷（请求/响应里的数据体） | "the payload of the response" |
| API | 应用程序接口 | "call the API" |
| rate limit | 限流（单位时间请求次数上限） | "you hit the rate limit" |
| parse | 解析（把文本转成结构化数据） | "parse the JSON response" |
| fetch / retrieve | 获取（从远处取数据） | "fetch data from the server" |

---

## 三个高频句式（看文档先认句式）

1. **"To do X, you use Y."** → 要做 X，就用 Y。例：*To add an item, you use `list.append()`. *
2. **"This function returns ..."** → 这个函数返回……（读返回值时最关键）
3. **"If the condition is true, the block executes."** → 如果条件成立，就执行这个代码块。

> 技术文档用词窄、句式固定。词汇 + 句式过关后，剩下的就是术语查表，不需要系统学英语语法。
