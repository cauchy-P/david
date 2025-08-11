def solution(n, wires):
    adj = [[] for _ in range(n+1)]
    ans = n - 2
    for u, v in wires:
        adj[u].append(v)
        adj[v].append(u)
    def dfs(node, parent):
        
        size = 1
        for child in adj[node]:
            if child != parent:
                sub = dfs(child, node)
                size += sub
                other = n - sub
                ans = min(ans, abs(size - other))
        return size
    dfs(wires[0][0], -1)
    return ans
print(solution(9,[[1,3],[2,3],[3,4],[4,5],[4,6],[4,7],[7,8],[7,9]]))