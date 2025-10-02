n, m = map(int, input().split())
a = list(map(int,input().split()))
s = [a[0]]
for i in range(n):
    s[i+1] = s[i] + a[i+1]
i, f = 0, 0
while i <= n:
    if s[f] - s[i-1] 