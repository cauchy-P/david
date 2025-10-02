n, k = int(input()), int(input())
lo, hi = 0, k
ans = 0
while lo <= hi:
    mid = (lo + hi) // 2
    s = sum([min(n, mid//i) for i in range(1,n+1)])
    #print(s)
    if s >= k:
        ans = mid
        hi = mid - 1
    else:
        lo = mid + 1
print(ans)