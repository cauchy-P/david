import sys
input = sys.stdin.readline
n, m = map(int, input().split())
passwords = {}
for _ in range(n):
    website, password = input().split()
    passwords[website] = password
for __ in range(m):
    print(passwords[input().strip()])
