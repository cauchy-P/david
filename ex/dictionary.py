from itertools import *
def solution(word):
    wordlist = []
    for k in range(1,6):
        wordlist.extend(list(map("".join, list(product("AEIOU",repeat=k)))))
    return sorted(wordlist).index(word)+1