from collections import deque
def solution(maps):
    n = len(maps)
    m = len(maps[0])
    chk = [[False]*m for _ in range(n)]
    directions = ((1,0),(0,1),(-1,0),(0,-1))
    def bfs():
        q = deque()
        q.append([0,0])
        while q:
            cx, cy = q.popleft()
            chk[cx][cy] = True
            for dx, dy in directions:
                ex = cx + dx
                ey = cy + dy
                if 0<=ex<n and 0<=ey<m and \
                    maps[ex][ey] and not chk[ex][ey]:
                    chk[ex][ey] = True
                    maps[ex][ey] = maps[cx][cy]+1
                    q.append((ex, ey))
        return -1 if maps[n-1][m-1] == 1 else maps[n-1][m-1]
    return bfs()
print(solution([[1,0,1,1,1],[1,0,1,0,1],[1,0,1,1,1],[1,1,1,0,1],[0,0,0,0,1]]))