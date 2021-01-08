# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# copying objects
from copy import copy

# representations of objects
from reprlib import repr as reprlib_repr

# randomization
from random import shuffle, choice, randrange, seed
from numpy.random import permutation, seed as np_seed

# custom modules
from datastructures.base import Collection, EmptyCollectionException
from datastructures.node import LinkedNode, DoublyLinkedNode


__all__ = ['ArrayRandomizedQueue', 'DoublyLinkedRandomizedQueue',
           'LinkedRandomizedQueue', 'RandomizedQueue']


class RandomizedQueue(Collection):
    """Abstract base class for the abstract data type randomized queue.

    Concrete subclasses must provide: __new__ or __init__, __iter__, choice,
    enqueue, dequeue."""

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __getitem__(self, key):
        raise TypeError('\'{}\' object is not subscriptable'
                        .format(type(self).__name__))

    def __setitem__(self, key, value):
        raise TypeError('\'{}\' object does not support item assignment'
                        .format(type(self).__name__))

    def __delitem__(self, key):
        raise TypeError('\'{}\' object doesn\'t support item deletion'
                        .format(type(self).__name__))

    def get(self):
        """Returns a random value of this instance."""
        return self.choice()

    @abstractmethod
    def choice(self):
        """Alias to get: returns a random value of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def post(self, value):
        """Posts the value to this instance."""
        self.enqueue(value)

    @abstractmethod
    def enqueue(self, value):
        """Alias to post: enqueues the value on this instance."""
        raise NotImplementedError

    def delete(self):
        """Deletes the value on the front of this instance."""
        self.dequeue()

    @abstractmethod
    def dequeue(self):
        """Dequeues a random value from this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class ArrayRandomizedQueue(RandomizedQueue):
    """Class that implements a randomized queue based on an internal dynamic
    array (python list)."""

    def __init__(self, random_state=None):
        self._values = []
        self._random_state = random_state

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self):
        seed(self._random_state)
        np_seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        shuffle(self._values)

        return iter(self._values)

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
        """Checks whether this instance is empty."""
        return not bool(self._values)

    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        return choice(self._values)

    def enqueue(self, value):
        """Enqueues an item on the randomized queue."""
        self._values.append(value)

    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        return self._values.pop(randrange(len(self)))

    def clear(self):
        """Removes all items."""
        self._values.clear()


class LinkedRandomizedQueue(RandomizedQueue):
    """Class that implements a randomized queue based on linked nodes."""

    class Node(LinkedNode):
        """Internal node class for linked randomized queues."""
        pass

    def __init__(self, random_state=None):
        self._front = None
        self._current_node = None
        self._current_idx = None
        self._len = 0
        self._random_state = random_state

    def __iter__(self):
        seed(self._random_state)
        np_seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        for idx in permutation(len(self)):
            yield self._get_node(idx).value

    def __repr__(self):
        self._reset_current_node()

        # determine first seven values (at most)
        first_values = []
        for node in self._traversal():
            first_values.append(node.value)
            if len(first_values) == 7:
                break

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        self._reset_current_node()
        return ' '.join(str(node.value) for node in self._traversal())

    def __len__(self):
        return self._len

    def _reset_current_node(self):
        if self:
            self._current_idx = 0
            self._current_node = self._front
        else:
            self._current_idx = None
            self._current_node = None

    def _traversal(self):
        """Traverses instance, beginning at current node."""
        while self._current_node:
            yield self._current_node
            self._current_idx += 1
            self._current_node = self._current_node.successor

    def _get_node(self, key):  # assume key is an integer
        """Returns node at index."""
        self._validate_non_emptiness()

        if key < self._current_idx:
            self._reset_current_node()

        # traverse instance, return current node if item at index is
        # reached
        key -= self._current_idx
        for node in self._traversal():
            if key == 0:
                return node
            key -= 1

        raise IndexError('Index out of range.')

    def _get_node_with_predecessor(self, key):
        """Returns node at index together with predecessor."""
        self._validate_non_emptiness()

        if key <= self._current_idx:
            self._reset_current_node()

        # traverse instance, return current node and predecessor if item
        # at index is reached
        key -= self._current_idx
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

        if self:
            if self._current_node is node:
                self._current_idx += 1
                self._current_node = self._current_node.successor
        else:
            self._current_idx = None
            self._current_node = None

    def is_empty(self):
        """Checks whether this instance is an empty queue."""
        return self._front is None

    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        return self._get_node(randrange(len(self))).value

    def enqueue(self, value):
        """Enqueues an item on the randomized queue."""
        self._front = self.Node(value, successor=self._front)
        self._len += 1
        if self._len == 1:
            self._current_idx = 0
            self._current_node = self._front
        else:
            self._current_idx += 1

    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        node, predecessor = \
            self._get_node_with_predecessor(randrange(len(self)))
        self._remove_node(node, predecessor)

        return node.value

    def clear(self):
        """Removes all items."""
        self._front = None
        self._len = 0
        self._current_idx = None
        self._current_node = None


class DoublyLinkedRandomizedQueue(RandomizedQueue):
    """Class that implements a randomized queue based on doubly linked
    nodes."""

    class Node(DoublyLinkedNode):
        """Internal node class for linked randomized queues."""
        pass

    def __init__(self, random_state=None):
        # self._front = None
        self._current_node = None
        self._len = 0
        self._random_state = random_state

    def __iter__(self):
        seed(self._random_state)
        np_seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        moves = permutation(len(self))
        for idx in range(len(self) - 1, 0, - 1):
            moves[idx] = moves[idx] - moves[idx - 1]

        for idx, steps in enumerate(moves):
            if steps > len(self) // 2:
                moves[idx] -= len(self)
            elif steps < -(len(self) // 2):
                moves[idx] += len(self)

        for steps in moves:
            self._move_to_node(steps)
            yield self._current_node.value

    def __repr__(self):
        # determine first seven values (at most)
        first_values = []
        for _ in range(len(self)):
            first_values.append(self._current_node.value)
            self._current_node = self._current_node.successor
            if len(first_values) == 7:
                break

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        values = []
        for _ in range(len(self)):
            values.append(self._current_node.value)
            self._current_node = self._current_node.successor
        return ' '.join(str(value) for value in values)

    def __len__(self):
        return self._len

    def _move_to_node(self, steps):
        # assume key is an integer, count of steps to make
        """Returns node at index."""
        self._validate_non_emptiness()

        # traverse instance, return current node if item at index is
        # reached
        if steps >= 0:
            # traverse instance forwards
            for _ in range(len(self)):
                if steps == 0:
                    return
                steps -= 1
                self._current_node = self._current_node.successor
        else:
            # traverse instance backwards
            for _ in range(len(self)):
                if steps == 0:
                    return
                steps += 1
                self._current_node = self._current_node.predecessor

        raise IndexError('Index out of range.')

    def _insert_as_predecessor(self, value):
        """Inserts value before current node by reconnecting predecessor."""
        self._current_node.predecessor.successor \
            = self.Node(value, predecessor=self._current_node.predecessor,
                        successor=self._current_node)
        self._current_node.predecessor \
            = self._current_node.predecessor.successor

        self._current_node = self._current_node.predecessor

        self._len += 1

    def _remove_current_node(self):
        """Removes current node by connecting predecessor with successor."""
        if self._current_node.successor == self._current_node:  # length 1
            self._current_node = None
        else:
            self._current_node.predecessor.successor \
                = self._current_node.successor
            self._current_node.successor.predecessor \
                = self._current_node.predecessor
            self._current_node = self._current_node.successor

        self._len -= 1

    def is_empty(self):
        """Checks whether this instance is an empty queue."""
        return self._current_node is None

    def choice(self):
        """Returns a random item of the randomized queue (but does not remove
        it)."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        move = randrange(len(self))  # count of steps to make
        if move > len(self) // 2:
            move -= len(self)

        self._move_to_node(randrange(len(self)))

        return self._current_node.value

    def enqueue(self, value):
        """Enqueues an item on the randomized queue."""
        if self.is_empty():
            self._current_node = self.Node(value)
            self._current_node.predecessor = self._current_node
            self._current_node.successor = self._current_node
            self._len += 1
        else:
            self._insert_as_predecessor(value)

    def dequeue(self):
        """Dequeues a random item from the randomized queue."""
        self._validate_non_emptiness()

        seed(self._random_state)
        if self._random_state is not None:
            self._random_state = randrange(2**32)

        self._move_to_node(randrange(len(self)))

        value = self._current_node.value
        self._remove_current_node()

        return value

    def clear(self):
        """Removes all items."""
        self._current_node = None
        self._len = 0
