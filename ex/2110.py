import sys
input = sys.stdin.readline
n, c = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(int(input()))
arr.sort()
lo = arr[1] - arr[0]
hi = arr[-1] - arr[0]
res = 0
while lo <= hi:
    mid = (lo + hi) // 2
    cnt = 1
    cur = arr[0]
    for i in range(1, n):
        if arr[i] >= cur + mid:
            cur = arr[i]
            cnt += 1
    if cnt >= c:
        res = mid
        lo = mid + 1
    else:
        hi = mid - 1
print(res)