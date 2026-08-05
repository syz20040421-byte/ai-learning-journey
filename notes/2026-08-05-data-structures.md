# 技术英语
1. 词汇：dictionary 词典（dict）  set：集合  collection：收藏，集合  unordered：无序的  union：合集，联合  intersection：交集，相交  symmetric difference：对称差集  data structure：数据结构  sequence：序列  index：索引  tuple：元组  assignment：赋值
2. 摘抄：
- 原文：Performing list(d) on a dictionary returns a list of all the keys used in the dictionary, in insertion order (if you want it sorted, just use sorted(d) instead). To check whether a single key is in the dictionary, use the in keyword.
- 译文：对字典执行 list(d) 操作，返回该字典中所有键的列表，按插入次序排列 (如需排序，请使用 sorted(d))。 检查字典里是否存在某个键，使用关键字 in。
3. 总结：
- 5.4 集合介绍了Python中的集合数据类型，集合是由不重复元素组成的无序多项集，支持成员检测和数学运算（如合集、交集等）。创建集合可以使用花括号或set()函数，注意空集合只能用set()创建。示例展示了如何去除重复元素及进行集合运算。
- 5.5 字典则讲解了字典这一数据类型，它是以键值对的形式存储数据的集合，键必须唯一且不可变。字典支持通过键存取值，使用get()方法避免访问不存在的键时引发错误。示例展示了字典的基本操作，包括添加、删除键值对及使用字典推导式创建字典。
- 在程序编写过程中有以下错误点：首先是致命的缩进问题，return被误放在第一层循环内部，导致程序只处理了第一个键就直接返回了；其次是逻辑覆盖不全，你只用双层 if 判断处理了同时在 a 和 b 中出现的重叠键，而完全遗漏了“只在a存在”或“只在b存在”的库存数据；最后是方法低效且绕远，试图用嵌套循环去遍历字典的键来寻找匹配，不仅导致时间复杂度变为 O(n*m)，也忽视了字典最核心的O(1)直接取值特性——这种场景其实完全不需要写双层循环，利用in判断键是否存在或用get方法设默认值，就能简洁高效地一步到位。总结成一句话就是：“缩进错了会中断流程，逻辑不全会漏数据，而用嵌套循环遍历字典找键，就是把哈希表当数组用，绕了远路且没发挥字典的优势。”

# 问题（没查资料）
1. 为什么 `["a","b","a"]` 里查「b 出现几次」用 list 要 O(n)，用 dict 只要 O(1)？
- 因为 list 中要遍历一遍列表，而 dict 中可以直接将出现次数转化为键值，只需要找key为b键值即可，即dict[b] 

2. 什么场景用 dict，什么场景用 set，什么场景继续用 list？各举一个例子
- dict 对两个元素需要建立关联时用，dict中的键和键值可以满足这一要求。场景：需要统计相应元素出现次数时
- set 对元素需要交，并，差等操作时。场景：将两组人的姓名放到同一集合下时
- list 只对元素进行排列。场景：列出水果的名称

3. 你昨天 `first_unique` 是 O(n²)，今天改成多少了？怎么证明（描述你脑子里怎么验证，不用写基准测试）
- O(n) 两个for循环，分别将items遍历一遍，O(n)+O(n)=O(n)