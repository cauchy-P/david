"""Linked list implementations written for the sol4 assignment."""


class _SinglyNode:
    """Node container for singly linked list values."""

    __slots__ = ('value', 'next')

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    """Singly linked list providing basic insertion and deletion."""

    def __init__(self):
        self.head = None
        self._length = 0

    def insert(self, value, position=None):
        """Insert value at the requested position or append when omitted."""
        new_node = _SinglyNode(value)

        if self.head is None:
            self.head = new_node
            self._length = 1
            return

        if position is None or position >= self._length:
            tail = self.head
            while tail.next is not None:
                tail = tail.next
            tail.next = new_node
        elif position <= 0:
            new_node.next = self.head
            self.head = new_node
        else:
            previous = self.head
            current_index = 0
            while current_index < position - 1 and previous.next is not None:
                previous = previous.next
                current_index += 1
            new_node.next = previous.next
            previous.next = new_node

        self._length += 1

    def delete(self, value):
        """Remove the first node containing value. Returns True on success."""
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._length -= 1
            return True

        previous = self.head
        current = previous.next

        while current is not None:
            if current.value == value:
                previous.next = current.next
                self._length -= 1
                return True
            previous = current
            current = current.next

        return False

    def get_list(self):
        """Return all values from head to tail as a Python list."""
        values = []
        node = self.head
        while node is not None:
            values.append(node.value)
            node = node.next
        return values

    def __len__(self):
        return self._length

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self):
        contents = ', '.join(repr(value) for value in self)
        return f'LinkedList([{contents}])'


class _CircularNode:
    """Node container for circular linked list values."""

    __slots__ = ('value', 'next')

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class CircularList:
    """Circular linked list supporting sequential iteration."""

    def __init__(self):
        self.tail = None
        self._length = 0
        self._current = None

    def insert(self, value):
        """Insert value at the logical end of the circular list."""
        new_node = _CircularNode(value)

        if self.tail is None:
            new_node.next = new_node
            self.tail = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

        self._length += 1

        if self._current is None:
            self._current = self.tail.next

    def delete(self, value):
        """Remove the first node containing value. Returns True on success."""
        if self.tail is None:
            return False

        previous = self.tail
        current = self.tail.next

        for _ in range(self._length):
            if current.value == value:
                if self._length == 1:
                    self.tail = None
                    self._current = None
                else:
                    previous.next = current.next
                    if current is self.tail:
                        self.tail = previous
                    if self._current is current:
                        self._current = current.next
                self._length -= 1
                return True

            previous = current
            current = current.next

        return False

    def get_next(self):
        """Return the next value in sequence, wrapping around automatically."""
        if self.tail is None:
            raise IndexError('The circular list is empty.')

        if self._current is None:
            self._current = self.tail.next

        value = self._current.value
        self._current = self._current.next
        return value

    def search(self, value):
        """Return True when value exists within the circular list."""
        if self.tail is None:
            return False

        current = self.tail.next
        for _ in range(self._length):
            if current.value == value:
                return True
            current = current.next
        return False

    def reset_iteration(self):
        """Reset the internal pointer used by get_next."""
        if self.tail is None:
            self._current = None
        else:
            self._current = self.tail.next

    def __len__(self):
        return self._length

    def __iter__(self):
        if self.tail is None:
            return

        current = self.tail.next
        for _ in range(self._length):
            yield current.value
            current = current.next

    def __repr__(self):
        contents = ', '.join(repr(value) for value in self)
        return f'CircularList([{contents}])'


linkedlist = LinkedList
circularlist = CircularList


def demo_music_playlists():
    """Demonstrate linked list behaviour with a small music collection."""
    tracks = [
        'Fly Me to the Moon',
        'Stairway to Heaven',
        'Levitating',
        'Bohemian Rhapsody',
        'Hotel California',
    ]

    play_queue = linkedlist()
    play_queue.insert('hello')
    for title in tracks:
        play_queue.insert(title)

    play_queue.insert('Billie Jean', position=0)
    play_queue.insert('Imagine', position=3)
    play_queue.delete('Levitating')

    print('Current queue:', play_queue.get_list())

    rotating_playlist = circularlist()
    for title in ['Blue in Green', 'Take Five', 'Autumn Leaves']:
        rotating_playlist.insert(title)

    print('Searching for "Take Five":', rotating_playlist.search('Take Five'))

    print('Rotating through the playlist:')
    for _ in range(10):
        print(rotating_playlist.get_next()) 


if __name__ == '__main__':
    demo_music_playlists()
