# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# representations of objects
from reprlib import repr as reprlib_repr

# custom modules
from datastructures.base import OrderedCollection
from datastructures.node import DoublyLinkedNode


__all__ = ['Deque', 'ArrayDeque', 'LinkedDeque', 'EmptyDequeException']


class Deque(OrderedCollection):
    """Abstract base class for the abstract data type queue.

    Concrete subclasses must provide: __new__ or __init__, __iter__,
    enqueue_rear, enqueue_front, dequeue_rear, dequeue_front."""

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.enqueue_rear(value)

        return self

    @abstractmethod
    def enqueue_rear(self, value):
        """Enqueues an item on the rear of the deque."""
        pass

    @abstractmethod
    def enqueue_front(self, value):
        """Enqueues an item on the front of the deque."""
        pass

    @abstractmethod
    def dequeue_rear(self):
        """Dequeues an item from the rear of the deque."""
        pass

    @abstractmethod
    def dequeue_front(self):
        """Dequeues an item from the front of the deque."""
        pass

    def peek_rear(self):
        """Returns item at rear of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        value = self.dequeue_rear()
        self.enqueue_rear(value)
        return value

    def peek_front(self):
        """Returns item at front of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        value = self.dequeue_front()
        self.enqueue_front(value)
        return value


class ArrayDeque(Deque):
    """Class that implements deques based on an internal dynamic array (python
    list)."""

    def __init__(self):
        self._values = []

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(self._values))

    def __contains__(self, value):
        return value in self._values

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        self._values += other

        return self

    def is_empty(self):
        """Checks whether this instance is an empty stack."""
        return not bool(self._values)

    def peek_rear(self):
        """Returns item at rear of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        return self._values[-1]

    def peek_front(self):
        """Returns item at front of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        return self._values[0]

    def enqueue_rear(self, value):
        """Enqueues an item on the rear of the deque."""
        self._values.append(value)

    def enqueue_front(self, value):
        """Enqueues an item on the rear of the deque."""
        self._values.insert(0, value)

    def dequeue_rear(self):
        """Dequeues an item from the rear of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t dequeue from empty deque.')

        return self._values.pop()

    def dequeue_front(self):
        """Dequeues an item from the front of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t dequeue from empty deque.')

        return self._values.pop(0)


class LinkedDeque(Deque):
    """Class that implements deques based on linked nodes."""

    class Node(DoublyLinkedNode):
        """Internal node class for linked deques."""
        pass

    def __init__(self):
        self._rear = None
        self._front = None
        self._len = 0

    def __iter__(self):
        current_node = self._front
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self):
        return self._len

    def is_empty(self):
        return self._front is None

    def peek_rear(self):
        """Returns item at rear of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        return self._rear.value

    def peek_front(self):
        """Returns item at front of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t peek at empty deque.')

        return self._front.value

    def enqueue_rear(self, value):
        """Enqueues an item on the rear of the deque."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._rear.successor = self.Node(value, predecessor=self._rear)
            self._rear = self._rear.successor

        self._len += 1

    def enqueue_front(self, value):
        """Enqueues an item on the front of the deque."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._front.predecessor = self.Node(value, successor=self._front)
            self._front = self._front.predecessor

        self._len += 1

    def dequeue_rear(self):
        """Dequeues an item from the rear of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t dequeue from empty deque.')

        value = self._rear.value
        if self._rear.predecessor:
            self._rear = self._rear.predecessor
            self._rear.successor = None
        else:
            self._rear = None
            self._front = None

        self._len -= 1

        return value

    def dequeue_front(self):
        """Dequeues an item from the front of the deque."""
        if self.is_empty():
            raise EmptyDequeException('Can\'t dequeue from empty deque.')

        value = self._front.value
        if self._front.successor:
            self._front = self._front.successor
            self._front.predecessor = None
        else:
            self._rear = None
            self._front = None

        self._len -= 1

        return value


class EmptyDequeException(Exception):
    pass
