import sys
sys.setrecursionlimit(1000000)
input = sys.stdin.readline
ans = 0
r, c = map(int, input().split())
g = []
for _ in range(r):
    g.append(list(input().strip()))
#print(g)
def search(i, j):
    global ans
    if not(0<=i<r): 
        return False
    

    if j == c - 1:
        if g[i][j] == 'x':
            return False
        g[i][j] = 'x'
        ans += 1
        return True
    g[i][j] = 'x'
    
    if search(i-1, j+1):
        return True
    elif search(i, j+1):

        return True
    elif search(i+1, j+1):
  
        return True
    
    
    return False

for i in range(r):
    search(i, 0)
    #print("\n".join(["".join(g[i]) for i in range(r)]))
print(ans)
