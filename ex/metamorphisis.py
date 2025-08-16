from collections import deque
similar = lambda x, y: list(map(lambda i: i[0]==i[1], zip(x, y))).count(False) == 1
def solution(begin, target, words):
    if target not in words:
        return 0
    dic = {}
    for word in [begin]+words:
        dic[word] = []
    for word1 in [begin]+words:
        for word2 in [begin]+words:
            if similar(word1, word2):
                dic[word1].append(word2)
                dic[word2].append(word1)
    q = deque()
    q.append([0, begin])
    while q:
        n, cword = q.popleft()
        if cword == target:
            return n
        if n > len(words):
            return 0
        q.extend(list(zip([n+1]*len(dic[cword]),dic[cword])))
        #print(q)
    return 0
print(solution("hit" ,"cog" ,["hot", "dot", "dog", "lot", "log"]))
