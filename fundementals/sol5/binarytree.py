'''Binary search tree implementation without external dependencies.'''


class BinarySearchTree:
    '''Binary search tree that supports insert, find, and delete operations.'''

    class _Node:
        '''Single node in the binary search tree.'''

        __slots__ = ('value', 'left', 'right')

        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self._root = None
        self._size = 0

    def insert(self, value):
        '''Insert value into the tree. Returns True when insertion succeeds.'''
        if self._root is None:
            self._root = self._Node(value)
            self._size = 1
            return True

        parent = None
        current = self._root
        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return False

        new_node = self._Node(value)
        if value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1
        return True

    def find(self, value):
        '''Return True when value exists in the tree.'''
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
        parent = None
        current = self._root

        while current is not None and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if current is None:
            return False

        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.value = successor.value
            parent = successor_parent
            current = successor

        replacement = current.left if current.left is not None else current.right

        if parent is None:
            self._root = replacement
        elif parent.left is current:
            parent.left = replacement
        else:
            parent.right = replacement

        self._size -= 1
        return True

    def __contains__(self, value):
        return self.find(value)

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0


binarytree = BinarySearchTree()


def _parse_value(raw_value):
    try:
        return int(raw_value)
    except ValueError:
        try:
            return float(raw_value)
        except ValueError:
            return raw_value


def _inorder(node):
    if node is None:
        return []
    return _inorder(node.left) + [node.value] + _inorder(node.right)


if __name__ == '__main__':
    tree = BinarySearchTree()
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
            print(_inorder(tree._root))
            continue

        if action == 'size':
            print(len(tree))
            continue

        if len(parts) != 2:
            print('Invalid command. Provide exactly one value.')
            continue

        value = _parse_value(parts[1])

        if action == 'insert':
            if tree.insert(value):
                print(f'Inserted {value}.')
            else:
                print(f'{value} already exists.')
        elif action == 'find':
            print('Found.' if tree.find(value) else 'Not found.')
        elif action == 'delete':
            if tree.delete(value):
                print(f'Deleted {value}.')
            else:
                print(f'{value} not present.')
        else:
            print('Unknown command.')
