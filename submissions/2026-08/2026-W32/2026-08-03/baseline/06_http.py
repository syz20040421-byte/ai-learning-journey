# 文件顶部用注释写出：
#   - HTTP 请求至少包含的两部分
#   - HTTP 响应至少包含的两部分


def describe_response(status_code: int) -> str:
    # 200-299 -> "success"；400-499 -> "client_error"；500-599 -> "server_error"；其他 -> "unknown"
    pass


# 在这里写断言，覆盖 200、201、404、500、999
