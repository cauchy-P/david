import sys
import heapq
input = sys.stdin.readline
n, m = map(int, input().rstrip().split())
degree = [0 for _ in range(n+1)]
graph = [[] for _ in range(n+1)]
queue = []
answer = []

for i in range(m):
    first, second = map(int, input().rstrip().split())
    graph[first].append(second)
    degree[second] += 1

for i in range(1, n+1):
    if degree[i] == 0:
        heapq.heappush(queue, i)

while queue:
    tmp = heapq.heappop(queue)
    answer.append(tmp)
    for i in graph[tmp]:
        degree[i] -= 1
        if degree[i] == 0:
            heapq.heappush(queue, i)

print(" ".join(map(str, answer)))