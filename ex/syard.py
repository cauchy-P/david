def isnumber(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def to_postfix(expression: str) -> str:
    op: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2, "^":3}
    res: str = ""
    s: list[str] = []
    for exp in expression:
        if isnumber(exp):
            res += exp
        elif exp == "(":
            s.append(exp)
        elif exp == ")":
            while s[-1] != "(":
                res += s.pop()
            s.pop() # 불필요한 "(" 제거
        elif exp in op:
            if s and s[-1] != "(" and (op[exp] <= op[s[-1]]):
                res += s.pop()
            s.append(exp)
    while s:
        res += s.pop()
    return res


#테스트 코드
for expr in ("(3 + 5) * 2", "((1 + 2) * 3) / 4 + 5 * (6 - 7)"):
    print(f"{expr} -> {to_postfix2(expr)}")
