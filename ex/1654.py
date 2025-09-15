import sys
input = sys.stdin.readline

k, n = map(int, input().split())
a = []
ans = 1
for _ in range(k):
    a.append(int(input()))
lo, hi = 1, max(a) + 1

while lo <= hi:
    mid = (lo + hi) // 2
    cnt = sum(list(map(lambda x: x // mid, a)))
    #print(mid, cnt)
    if cnt >= n:
        lo = mid + 1
        ans = mid
    else:
        hi = mid - 1
print(ans)