'''Binary search tree implementation without external dependencies.'''

# 이 모듈은 외부 라이브러리 없이 이진 탐색 트리(BST)를 구현한다.
# 과제 요구사항에 따라 insert, find, delete 연산을 제공하며,
# 모듈 전역에 사용할 수 있는 인스턴스 이름은 'binarytree' 이다.


class BinarySearchTree:
    '''Binary search tree that supports insert, find, and delete operations.'''

    # 내부 노드 구조. 값과 왼쪽/오른쪽 자식을 가진다.

    class _Node:
        '''Single node in the binary search tree.'''

        __slots__ = ('value', 'left', 'right')

        def __init__(self, value):
            # 노드에 저장될 값
            self.value = value
            # 왼쪽/오른쪽 자식 노드 레퍼런스
            self.left = None
            self.right = None

    def __init__(self):
        # 트리의 루트 노드와 현재 크기(원소 개수)
        self._root = None
        self._size = 0

    def insert(self, value):
        '''Insert value into the tree. Returns True when insertion succeeds.'''
        # 빈 트리라면 새 루트를 만든다.
        if self._root is None:
            self._root = self._Node(value)
            self._size = 1
            return True

        # 루트부터 내려가며 삽입 위치를 찾는다.
        parent = None
        current = self._root
        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                # 중복 값은 삽입하지 않는다.
                return False

        new_node = self._Node(value)
        # 부모 기준으로 왼쪽/오른쪽에 새 노드를 연결한다.
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1
        return True

    def find(self, value):
        '''Return True when value exists in the tree.'''
        # 이진 탐색으로 값 존재 여부를 확인한다.
        current = self._root
        while current is not None:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True
        return False

    def delete(self, value):
        '''Remove value from the tree. Returns True when removal succeeds.'''
        # 먼저 삭제할 노드(current)와 그 부모(parent)를 찾는다.
        parent = None
        current = self._root

        while current is not None and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if current is None:
            # 값이 존재하지 않음
            return False

        # 자식이 둘 다 있는 경우: 오른쪽 서브트리에서 후계자(가장 왼쪽)를 찾아 교체
        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.value = successor.value
            parent = successor_parent
            current = successor

        # 자식이 0개 또는 1개인 경우: 존재하는 자식을 올려 붙인다.
        replacement = current.left if current.left is not None else current.right

        if parent is None:
            # 루트를 삭제하는 경우
            print("루트 노드 삭제 시도")
            self._root = replacement
        elif parent.left is current:
            parent.left = replacement
        else:
            parent.right = replacement

        self._size -= 1
        return True

    def __contains__(self, value):
        # 'x in tree' 형태의 연산을 지원
        return self.find(value)

    def __len__(self):
        # len(tree) 를 지원
        return self._size

    def is_empty(self):
        # 트리가 비었는지 여부
        return self._size == 0


binarytree = BinarySearchTree()
# 모듈 전역 인스턴스. 과제 명세상의 이름 'binarytree' 를 사용한다.


def _parse_value(raw_value):
    # 입력 문자열을 int -> float -> str 순으로 파싱한다.
    try:
        return int(raw_value)
    except ValueError:
        try:
            return float(raw_value)
        except ValueError:
            return raw_value


def _inorder(node):
    # 중위 순회로 현재 트리의 정렬된 값 목록을 생성한다.
    if node is None:
        return []
    return _inorder(node.left) + [node.value] + _inorder(node.right)


if __name__ == '__main__':
    binarytree = BinarySearchTree()
    print('Binary Search Tree demo.')
    print('Commands: insert <value>, find <value>, delete <value>, list, size, exit')

    while True:
        try:
            command = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting.')
            break

        if not command:
            continue

        parts = command.split()
        action = parts[0].lower()

        if action == 'exit':
            print('Goodbye.')
            break

        if action == 'list':
            # 현재 트리의 값들을 정렬된 리스트로 출력
            print(_inorder(binarytree._root))
            continue

        if action == 'size':
            # 현재 트리의 원소 개수 출력
            print(len(binarytree))
            continue

        if len(parts) != 2:
            print('Invalid command. Provide exactly one value.')
            continue

        value = _parse_value(parts[1])

        if action == 'insert':
            # 이미 존재하면 False 를 반환해 중복 삽입을 방지
            if binarytree.insert(value):
                print(f'Inserted {value}.')
            else:
                print(f'{value} already exists.')
        elif action == 'find':
            print('Found.' if binarytree.find(value) else 'Not found.')
        elif action == 'delete':
            if binarytree.delete(value):
                print(f'Deleted {value}.')
            else:
                print(f'{value} not present.')
        else:
            print('Unknown command.')
