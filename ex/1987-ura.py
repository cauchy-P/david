from collections import deque
r, c = map(int, input().split())
g = [list(input()) for _ in range(r)]
q = deque([(0,0,set([g[0][0]]))])
dirs = ((1,0),(0,1),(-1,0),(0,-1))
ans = 1
while q:
    i, j, used = q.pop()
    ans = max(ans, len(used))
    
    for di, dj in dirs:
        ni, nj = i+di, j+dj
        if 0<=ni<r and 0<=nj<c and \
            g[ni][nj] not in used:
            q.append((ni, nj, used|{g[ni][nj]}))
print(ans)