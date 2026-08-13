# 用标准库 argparse 写一个 CLI（不要手动解析 sys.argv）：
#   python 05_cli.py --name Ada --times 3   -> 打印 3 行 "Hello, Ada"
#   --name 必填；--times 默认 1；times <= 0 时给出清晰错误并以非零状态退出
