import heapq
n = int(input())
q = [list(map(int, input().split())) for _ in range(n)]
q.sort(key = lambda x:(x[1],x[2]))
room = []
ans = [0]*(n+1)
rn = 1
heapq.heappush(room, [q[0][2], rn])
ans[q[0][0]] = rn
for i in range(1, n):
    if q[i][1] < room[0][0]:
        rn += 1
        ans[q[i][0]] = rn
        heapq.heappush(room, [q[i][2],rn])
    else:
        tmp = heapq.heappop(room)
        ans[q[i][0]] = tmp[1]
        heapq.heappush(room, [q[i][2],tmp[1]])
print(len(room))
for i in range(1, len(ans)):
    print(ans[i])