from collections import deque

def solution(priorities, location):
    q = deque(enumerate(priorities)) 
    cnt = 0
    
    while q:
        process = q.popleft()  
        if any(process[1] < other[1] for other in q):
            q.append(process) 
        else:
            cnt += 1  
            if process[0] == location: 
                return cnt
    
    return cnt

print(solution([2, 1, 3, 2], 2))  # Should print 1
print(solution([1, 1, 9, 1, 1, 1], 0))