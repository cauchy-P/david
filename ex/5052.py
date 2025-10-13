import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    phonebook = [input().strip() for __ in range(n)]
    phonebook.sort()
    for i in range(n-1):
        if phonebook[i+1].startswith(phonebook[i]):
            print("NO")
            break
    else:
        print("YES")
