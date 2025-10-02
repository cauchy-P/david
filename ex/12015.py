import sys
input = sys.stdin.readline
n = int(input())
a = list(map(int, input().split()))
ans = [a[0]]
def find(x, arr):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            hi = mid - 1
        else:
            lo = mid + 1
    return lo
for i in range(n):
    if ans[-1] >= a[i]:
        ans[find(a[i], ans)] = a[i]
    else:
        ans.append(a[i])
print(len(ans))
