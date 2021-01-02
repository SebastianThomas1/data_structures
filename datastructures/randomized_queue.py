# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# representations of objects
from reprlib import repr as reprlib_repr

# randomization
from random import choice, randrange, seed
from numpy.random import permutation, seed as np_seed

# custom modules
from datastructures.base import Collection
from datastructures.node import LinkedNode


__all__ = ['RandomizedQueue', 'ArrayRandomizedQueue', 'LinkedRandomizedQueue',
           'EmptyRandomizedQueueException']


class RandomizedQueue(Collection):
    """Abstract base class for the abstract data type randomized queue.

    Concrete subclasses must provide: __new__ or __init__, __iter__, sample,
    enqueue, dequeue."""

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.enqueue(value)

        return self

    @abstractmethod
    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        pass

    @abstractmethod
    def enqueue(self, value):
        """Enqueues an item on the randomized_queue."""
        pass

    @abstractmethod
    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        pass


class ArrayRandomizedQueue(RandomizedQueue):
    """Class that implements randomized queues based on an internal dynamic
    array (python list)."""

    def __init__(self, random_state=None):
        self._values = []
        self._random_state = random_state

    def __iter__(self):
        seed(self._random_state)
        np_seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        for idx in permutation(len(self)):
            yield self._values[idx]

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(self._values))

    def __str__(self):
        return ' '.join(str(value) for value in self._values)

    def __contains__(self, value):
        return value in self._values

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        self._values += other

        return self

    def is_empty(self):
        """Checks whether this instance is an empty queue."""
        return not bool(self._values)

    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        if self.is_empty():
            raise EmptyRandomizedQueueException('Can\'t access entries of '
                                                'empty randomized queue.')

        seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        return choice(self._values)

    def enqueue(self, value):
        """Enqueues an item on the randomized queue."""
        self._values.append(value)

    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        if self.is_empty():
            raise EmptyRandomizedQueueException('Can\'t dequeue from empty '
                                                'randomized queue.')

        seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        return self._values.pop(randrange(len(self)))


class LinkedRandomizedQueue(RandomizedQueue):
    """Class that implements randomized queues based on linked nodes."""

    class Node(LinkedNode):
        """Internal node class for linked randomized queues."""
        pass

    def __init__(self, random_state=None):
        self._front = None
        self._len = 0
        self._random_state = random_state

    def __iter__(self):
        seed(self._random_state)
        np_seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        for idx in permutation(len(self)):
            yield self._get_node(idx).value

    def __repr__(self):
        # determine first seven values (at most)
        first_values = []
        count = 0
        for node in self._traversal():
            first_values.append(node.value)
            count += 1
            if count == 7:
                break

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        return ' '.join(str(node.value) for node in self._traversal())

    def __len__(self):
        return self._len

    def _traversal(self, start_node=None):
        """Traverses instance, beginning with start_node (default: front)."""
        if start_node is None:
            start_node = self._front

        current_node = start_node
        while current_node:
            yield current_node
            current_node = current_node.successor

    def _get_node(self, key):  # assume key is an integer
        """Returns node at index."""
        if self.is_empty():
            raise IndexError('Can\'t access index in empty randomized queue.')

        # traverse instance, return current node if item at index is
        # reached
        for node in self._traversal():
            if key == 0:
                return node
            key -= 1

        raise IndexError('Index out of range.')

    def _get_node_with_predecessor(self, key):
        """Returns node at index together with predecessor."""
        if self.is_empty():
            raise IndexError('Can\'t access index in empty randomized queue.')

        # traverse instance, return current node and predecessor if item
        # at index is reached
        predecessor = None
        for node in self._traversal():
            if key == 0:
                return node, predecessor
            key -= 1
            predecessor = node

        raise IndexError('Index out of range.')

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        if predecessor:
            predecessor.successor = node.successor
        else:  # ie node is self._front
            self._front = self._front.successor

        self._len -= 1

    def is_empty(self):
        """Checks whether this instance is an empty queue."""
        return self._front is None

    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        if self.is_empty():
            raise EmptyRandomizedQueueException('Can\'t access entries of '
                                                'empty randomized queue.')

        seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        return self._get_node(randrange(len(self))).value

    def enqueue(self, value):
        """Enqueues an item on the randomized queue."""
        self._front = self.Node(value, self._front)
        self._len += 1

    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        if self.is_empty():
            raise EmptyRandomizedQueueException('Can\'t dequeue from empty '
                                                'randomized queue.')

        seed(self._random_state)
        if self._random_state:
            self._random_state += randrange(-1000000, 1000000)

        node, predecessor = \
            self._get_node_with_predecessor(randrange(len(self)))
        self._remove_node(node, predecessor)

        return node.value


# noch DoublyLinked machen? für schnelleren access?


class EmptyRandomizedQueueException(Exception):
    pass
