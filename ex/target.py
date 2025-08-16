from collections import deque
def solution(numbers, target):
    q = deque()
    q.extend([[0, numbers[0]], [0, -numbers[0]]])
    l = len(numbers)-1
    while q:
        cur = q.popleft()
        print(cur)
        if cur[0]==l:
            break
        q.extend([[cur[0]+1, cur[1]+numbers[cur[0]+1]], \
                [cur[0]+1, cur[1]-numbers[cur[0]+1]]])
    print(q)
    return len(list(filter(lambda x: x[1]==target, q)))
print(solution([1,1,1,1,1], 3))