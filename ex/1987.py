r, c = map(int, input().split())
g = [list(input()) for _ in range(r)]
dirs = ((1,0),(0,1),(-1,0),(0,-1))
used = set(g[0][0])
ans = 1
def dfs(i, j):
    global used, ans
    ans = max(ans, len(used))
    for di, dj in dirs:
        ni, nj = i+di, j+dj
        if 0<=ni<r and 0<=nj<c and g[ni][nj] not in used:
            used.add(g[ni][nj])
            dfs(ni, nj)
            used.remove(g[ni][nj])
    #print(used)
    
dfs(0,0)
print(ans)