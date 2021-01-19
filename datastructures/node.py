# Sebastian Thomas (datascience at sebastianthomas dot de)


class LinkedNode:
    """Node class for eg (singly) linked lists, linked stacks, ..."""

    def __init__(self, value, successor=None):
        self.value = value
        self.successor = successor

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class LinkedNodeWithKey(LinkedNode):
    """Node class with a key field, eg for linked dictionaries."""

    def __init__(self, key, value, successor=None):
        super().__init__(value, successor=successor)
        self.key = key

    def __repr__(self):
        return '{}(key={}, value={})'.format(type(self).__name__,
                                             repr(self.key), repr(self.value))

    def __str__(self):
        return '({}: {})'.format(type(self).__name__, str(self.key),
                                 str(self.value))


class DoublyLinkedNode(LinkedNode):
    """Node class for eg doubly linked lists, ..."""

    def __init__(self, value, predecessor=None, successor=None):
        super().__init__(value, successor=successor)
        self.predecessor = predecessor
