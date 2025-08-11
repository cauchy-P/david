from itertools import *
def solution(k, dungeons):
    answer = 0
    for traverse in permutations(dungeons):
        print(traverse)
        level = 0
        hp = k
        for dungeon in traverse:
            if hp < dungeon[0]:
                continue
            else:
                hp -= dungeon[1]
                level += 1
            print(level)
        answer = max(answer, level)
    return answer
solution(80, [[80, 20], [50, 40], [30, 10]])