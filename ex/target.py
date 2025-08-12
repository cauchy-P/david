from itertools import *
def solution(numbers, target):
    shot = 0
    for lhs in product(*[(x, -x) for x in numbers]):
        if(sum(lhs) == target):
            shot += 1
    return shot
print(solution([1,1,1,1,1],5))