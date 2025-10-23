import sys, heapq
input = sys.stdin.readline

n = int(input())
a = []
for i in range(n):
    x, y = map(int, input().split())
    a.append([x, y])
a.sort()
res = []
t = 1
for x, y in a:
    
    if t > x:
        heapq.heappop(res)
        t -= 1
        #print(res)
    heapq.heappush(res, y)
    t +=1 
    #print(res)

print(sum(list(res)))
    
    