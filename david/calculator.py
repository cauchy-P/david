import re
# The easy way
# eval(input())

add = lambda x, y: x + y
subtract = lambda x, y: x - y
multiply = lambda x, y: x * y
divide = lambda x, y: x / y if y != 0 else 'Error: Division by zero'


if __name__ == "__main__":

    # The hard way
    istr = input()
    tokens = re.findall(r'\d+|[+\-*/]', istr)
    values = list(map(int, tokens[::2]))
    operators = tokens[1::2]
    result = values[0]
    for i, op in enumerate(operators):
        if op == '+':
            result = add(result, values[i + 1])
        elif op == '-':
            result = subtract(result, values[i + 1])
        elif op == '*':
            result = multiply(result, values[i + 1])
        elif op == '/':
            result = divide(result, values[i + 1])

    print(result)
