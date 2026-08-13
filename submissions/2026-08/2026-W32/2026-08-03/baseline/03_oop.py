class BankAccount:
    # 构造函数接收 owner: str 与 balance: float = 0
    # deposit(amount): 只接受大于 0 的金额，返回新余额
    # withdraw(amount): 金额不合法或余额不足时抛 ValueError，成功时返回新余额
    def __init__  (self, owner:str, balance: float = 0):
        self.owner=owner
        self.balance=balance

    def deposit(self, amount: float = 0) -> float:
        self.amount = amount
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float = 0) ->float:
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        elif amount > self.balance:
            raise ValueError("存款金额不足")
        else:
            self.balance -= amount
        return self.balance

acc = BankAccount("syz", 666)
print(f"初始账户：{acc.owner}，余额：{acc.balance}")

# 1. 成功存款
try:
    new_balance = acc.deposit(5211314)
    print(f"存款成功，新余额：{new_balance}")
except ValueError as e:
    print(f"存款失败：{e}")

# 2. 成功取款（取款金额 ≤ 余额）
try:
    new_balance = acc.withdraw(666)
    print(f"取款成功，新余额：{new_balance}")
except ValueError as e:
    print(f"取款失败：{e}")

# 3. 余额不足取款（取款金额 > 余额）
try:
    new_balance = acc.withdraw(99999999999999)
    print(f"取款成功，新余额：{new_balance}")
except ValueError as e:
    print(f"取款失败（余额不足）：{e}")




# 创建一个实例，覆盖：成功存款、成功取款、余额不足 三种情况
