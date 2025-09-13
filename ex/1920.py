import sys
input = sys.stdin.readline
n = int(input())
a = sorted(list(map(int, input().split())))
m = int(input())
b = list(map(int, input().split()))
def exists(x):
    lo, hi = 0, n-1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return True
        elif a[mid] > x:
            hi = mid-1
        else:
            lo = mid+1
    return False
for i in b:
    if exists(i):
        print(1)
    else:
        print(0)
