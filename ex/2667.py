"""
아이디어
이중 for문 돌면서 각 원소마다 dfs 탐색
지도행렬 int[][]
방문했는가? bool[][]

알고리즘
재귀함수 호출

시간복잡도
5*25*25 < 2억




"""
import sys
input = sys.stdin.readline

n = int(input())
mp = [list(map(int, input().strip())) for _ in range(n)]
chk = [[False]*n for _ in range(n)]
dirs = ((1,0),(0,1),(-1,0),(0,-1))
cnt = 0
lst = []
def dfs(x, y):
    size = 1
    for dx, dy in dirs:
        cx, cy = x+dx, y+dy
        if 0<=cx<n and 0<=cy<n and \
              not chk[cx][cy] and mp[cx][cy]:
            chk[cx][cy] = True
            size += dfs(cx,cy)

    return size
for i in range(n):
    for j in range(n):
        if not chk[i][j] and mp[i][j]:
            chk[i][j] = True
            cnt += 1
            lst.append(dfs(i, j))
lst.sort()

print(cnt)
for k in range(len(lst)):
    print(lst[k])