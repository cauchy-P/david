from collections import deque
n, m, v = map(int, input().split())
adj = [[False]*(n+1) for _ in range(n+1)]
chkd = [False]*(n+1)
chkb = chkd.copy()
for _ in range(m):
    v1, v2 = map(int, input().split())
    adj[v1][v2] = adj[v2][v1] = True

def dfs(v):
    chkd[v] = True
    print(v, end=' ')
    for vc in range(1, n+1):
        if adj[v][vc] and not chkd[vc]:
            dfs(vc)

def bfs(v):
    chkb[v] = True
    q = deque([v])
    while q:
        vc = q.popleft()
        print(vc, end=' ')
        for vd in range(1, n+1):
            if adj[vc][vd] and not chkb[vd]:
                q.append(vd)
                chkb[vd] = True

dfs(v)
print()
bfs(v)