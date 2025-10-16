class TrieNode:
    def __init__(self):
        self.children = {}
        self.isend = False
class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isend = True
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.isend
    def isprefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return bool(node.children)
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.isend:
                    return False
                node.isend = False
                return len(node.children) == 0
            char = word[depth]
            if char not in node.children:
                return False
            canabort = _delete(node.children[char], word, depth + 1)
            if canabort:
                del node.children[char]
                return len(node.children) == 0 and not node.isend
            return False
        _delete(self.root, word, 0)
import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    trie = Trie()
    phonebook = [input().strip() for __ in range(n)]
    for i in range(n):
        trie.insert(phonebook[i])
    for phonenum in phonebook:
        if trie.isprefix(phonenum):
            print("NO")
            break
    else:
        print("YES")