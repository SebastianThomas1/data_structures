# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# representations of objects
from reprlib import repr as reprlib_repr

# custom modules
from datastructures.base import Collection
from datastructures.node import LinkedNode


__all__ = ['Queue', 'ArrayQueue', 'LinkedQueue', 'EmptyQueueException']


class Queue(Collection):
    """Abstract base class for the abstract data type queue.

    Concrete subclasses must provide: __new__ or __init__, __iter__, enqueue,
    dequeue."""

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.enqueue(value)

        return self

    @abstractmethod
    def peek(self):
        """Returns item at front of the queue."""
        pass

    @abstractmethod
    def enqueue(self, value):
        """Enqueues an item on the queue."""
        pass

    @abstractmethod
    def dequeue(self):
        """Dequeues an item from the queue."""
        pass


class ArrayQueue(Queue):
    """Class that implements queues based on an internal dynamic array (python
    list)."""

    def __init__(self):
        self._values = []

    def __iter__(self):
        return iter(self._values)

    def __bool__(self):
        return bool(self._values)

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

    def peek(self):
        """Returns item at front of the queue."""
        if self.is_empty():
            raise EmptyQueueException('Can\'t peek at empty queue.')

        return self._values[0]

    def enqueue(self, value):
        """Enqueues an item on the queue."""
        self._values.append(value)

    def dequeue(self):
        """Dequeues an item from the queue."""
        if self.is_empty():
            raise EmptyQueueException('Can\'t dequeue from empty queue.')

        return self._values.pop(0)


class LinkedQueue(Queue):
    """Class that implements queues based on linked nodes."""

    class Node(LinkedNode):
        """Internal node class for linked queues."""
        pass

    def __init__(self):
        self._back = None
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

    def peek(self):
        """Returns item at front of the queue."""
        if self.is_empty():
            raise EmptyQueueException('Can\'t peek at empty queue.')

        return self._front.value

    def enqueue(self, value):
        """Enqueues an item on the queue."""
        if self.is_empty():
            self._back = self.Node(value)
            self._front = self._back
        else:
            self._back.successor = self.Node(value)
            self._back = self._back.successor

        self._len += 1

    def dequeue(self):
        """Dequeus an item from the queue."""
        if self.is_empty():
            raise EmptyQueueException('Can\'t dequeue from empty queue.')

        value = self._front.value
        self._front = self._front.successor

        self._len -= 1

        return value


class EmptyQueueException(Exception):
    pass
