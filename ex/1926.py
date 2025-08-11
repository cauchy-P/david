"""
그림 행렬 mp : int[][]
방문 행렬 chk : bool[][]
큐 q : deque
각 요소를 방문하면서 bfs
V+E=5V = 5*500*500 < 2억

"""


from collections import deque
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
mp = [list(map(int, input().split())) for _ in range(n)]
chk = [[False]*m for _ in range(n)]
dirs = ((1,0),(0,1),(-1,0),(0,-1))
pics = 0
area = 0

def bfs(x, y): #x행 y열
    A = 1
    q = deque()
    q.append((x, y))
    while q:
        cx, cy = q.popleft()
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < m and \
                not chk[nx][ny] and mp[nx][ny]:
                A += 1
                chk[nx][ny] = True
                q.append((nx, ny))
    return A

for i in range(n):
    for j in range(m):
        if not chk[i][j] and mp[i][j]:
            chk[i][j] = True
            pics += 1
            area = max(area, bfs(i, j))
print(pics)
print(area)
