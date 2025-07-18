import re

# 1) 연산자 정보: 우선순위, 함수 매핑
OPS = {
    '+': (1, lambda x, y: x + y),
    '-': (1, lambda x, y: x - y),
    '*': (2, lambda x, y: x * y),
    '/': (2, lambda x, y: x / y if y != 0 else (_ for _ in ()).throw(ZeroDivisionError("division by zero")))
}

def tokenize(expr: str):
    """
    문자열 expr을 토큰 리스트로 분리
    숫자(정수/소수), 연산자(+ - * /), 괄호
    """
    token_pattern = r'\d+\.\d+|\.\d+|\d+|[+\-*/()]'
    tokens = re.findall(token_pattern, expr.replace(' ', ''))
    return tokens

def infix_to_postfix(tokens: list[str]) -> list[str]:
    """
    shunting-yard 알고리즘으로 중위표기 → 후위표기 변환
    """
    output = []
    stack: list[str] = []
    for tok in tokens:
        if re.fullmatch(r'\d+\.\d+|\.\d+|\d+', tok):
            output.append(tok)
        elif tok in OPS:
            # 스택 꼭대기 연산자와 우선순위 비교
            while stack and stack[-1] in OPS and OPS[stack[-1]][0] >= OPS[tok][0]:
                output.append(stack.pop())
            stack.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            # '(' 만날 때까지 pop
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()  # '(' 제거
        else:
            raise ValueError(f"Unknown token: {tok}")
    # 남은 연산자들 모두 pop
    while stack:
        if stack[-1] in '()':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    return output

def eval_postfix(tokens: list[str]) -> float:
    """
    후위표기법 토큰을 스택으로 계산
    """
    stack: list[float] = []
    for tok in tokens:
        if re.fullmatch(r'\d+\.\d+|\.\d+|\d+', tok):
            stack.append(float(tok))
        elif tok in OPS:
            if len(stack) < 2:
                raise ValueError("Insufficient operands")
            b = stack.pop()
            a = stack.pop()
            result = OPS[tok][1](a, b)
            stack.append(result)
        else:
            raise ValueError(f"Unknown token in RPN: {tok}")
    if len(stack) != 1:
        raise ValueError("The user input has too many values")
    return stack[0]

def calculate(expr: str) -> float:
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    return eval_postfix(postfix)

if __name__ == "__main__":
    try:
        expr = input()
        res = calculate(expr)
        print(f"Result: {res}")
    except ZeroDivisionError as e:
        print("Error:", e)
    except Exception as e:
        print("Invalid input")
