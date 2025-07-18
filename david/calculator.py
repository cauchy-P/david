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
    tokens = re.findall(r'\d+\.\d+|\.\d+|\d+|[^\d.]+', istr)
    # x.y | .z | 123 | op
    # 123.2392 
    #print(tokens)
    values = list(map(float, tokens[::2]))
    operators = tokens[1::2]
    result = values[0]
    for i, op in enumerate(operators):
        if op == '+':
            result = "Result: {0}".format(add(result, values[i + 1]))
        elif op == '-':
            result = "Result: {0}".format(subtract(result, values[i + 1]))
        elif op == '*':
            result = "Result: {0}".format(multiply(result, values[i + 1]))
        elif op == '/':
            result = "Result: {0}".format(divide(result, values[i + 1]))
        else:
            print('Invalid operator')
            exit(1)
    print(result)
