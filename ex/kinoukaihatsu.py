from math import *
def solution(progresses, speeds):
    days = list(map(lambda x: ceil((100-x[0])/x[1]), zip(progresses, speeds)))
    stack = []
    ans = []
    for d in days:
        if not stack:
            stack.append(d)
        elif stack[-1] > d:
            ans.append(len(stack))
            stack = [d]
        else:
            stack.append(d)
        print(stack)
    ans.append(len(stack))
    return ans[::-1]