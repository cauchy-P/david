from math import *
from itertools import *

def isprime(n):
    if n<2: return False
    for i in range(2, floor(n**.5)):
        if not n%i: return False
    return True
def solution(numbers):
    candidates = set()
    for k in range(1, len(numbers)+1):
        for n in permutations(numbers, k):
            candidates.add(int("".join(n)))
    return list(map(isprime, candidates)).count(True))