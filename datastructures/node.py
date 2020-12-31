# Sebastian Thomas (datascience at sebastianthomas dot de)


class LinkedNode:
    """Node class for e.g. (singly) linked lists, linked stacks, ..."""

    def __init__(self, value, successor=None):
        self.value = value
        self.successor = successor

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class DoublyLinkedNode(LinkedNode):
    """Node class for e.g. doubly linked lists, ..."""

    def __init__(self, value, predecessor=None, successor=None):
        super().__init__(value, successor=successor)
        self.predecessor = predecessor
