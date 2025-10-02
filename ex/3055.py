from collections import deque
r, c = map(int, input().split())
visited = [[-1]*c for _ in range(r)]
g = [list(input()) for _ in range(r)]
q = deque()
for i in range(r):
    for j in range(c):
        if g[i][j]=='*':
            q.appendleft((i,j))
        if g[i][j]=='S':
            q.append((i,j))
            visited[i][j] = 0
while q:
    i, j = q.popleft()
    cur = g[i][j]
    dirs = ((1,0),(0,1),(-1,0),(0,-1))
    for di, dj in dirs:
        ni, nj = i+di, j+dj
        if not(0<=ni<r and 0<=nj<c) or \
            visited[ni][nj] != -1 or \
            g[ni][nj] == '*' or \
            g[ni][nj] == 'X' or \
            cur == '*' and g[ni][nj]=='D':
            continue
        if cur=='S':
            if g[ni][nj]=='D':
                print(visited[i][j] + 1)
                break
            visited[ni][nj] = visited[i][j] + 1
            
        g[ni][nj] = cur
        q.append((ni, nj))
    else:
        continue
    break
else:
    print("KAKTUS")