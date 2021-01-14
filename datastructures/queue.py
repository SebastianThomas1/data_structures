# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# copying objects
from copy import copy

# representations of objects
from reprlib import repr as reprlib_repr

# custom modules
from datastructures.base import Collection, PredictableIterMixin, \
    EmptyCollectionException
from datastructures.node import LinkedNode


__all__ = ['ArrayQueue', 'FRONT', 'LinkedQueue', 'Queue', 'REAR']


REAR = 'rear'
FRONT = 'front'


class Queue(PredictableIterMixin, Collection):
    """Abstract base class for the abstract data type queue.

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, peek, enqueue and dequeue."""

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __getitem__(self, key):
        """Returns the value on the front of this instance.

        The parameter key must be FRONT."""
        self._validate_key_front(key)

        return self.peek()

    def __delitem__(self, key):
        """Deletes the value on the front of this instance.

        The parameter key must be FRONT."""
        self._validate_key_front(key)

        self.delete()

    @staticmethod
    def _validate_key_rear(key):
        """Checks whether key is REAR."""
        if key is not REAR:
            raise KeyError('key must be REAR')

    @staticmethod
    def _validate_key_front(key):
        """Checks whether key is FRONT."""
        if key is not FRONT:
            raise KeyError('key must be FRONT')

    def get(self):
        """Returns the value at the front of this instance."""
        return self.peek()

    @abstractmethod
    def peek(self):
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def insert(self, key, value):
        """Inserts the value at the key.

        The parameter key must be REAR."""
        self._validate_key_rear(key)
        self.enqueue(value)

    def post(self, value):
        """Posts the value to this instance and places it on the rear."""
        self.enqueue(value)

    @abstractmethod
    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        raise NotImplementedError

    def delete(self):
        """Deletes the value on the front of this instance."""
        self.dequeue()

    def pop(self, key=FRONT):
        """Removes and returns the value on the front of this instance.

        The parameter key must be FRONT (default)."""
        self._validate_key_front(key)

        return self.dequeue()

    @abstractmethod
    def dequeue(self):
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class ArrayQueue(Queue):
    """Class that implements a queue based on an internal dynamic array (python
    list)."""

    def __init__(self):
        self._values = []

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

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
        """Checks whether this instance is empty."""
        return not bool(self._values)

    def peek(self):
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._values[0]

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._values.append(value)

    def delete(self):
        """Deletes the value on the front of this instance."""
        self._validate_non_emptiness()

        del self._values[0]

    def clear(self):
        """Removes all values."""
        self._values.clear()

    def dequeue(self):
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._values.pop(0)


class LinkedQueue(Queue):
    """Class that implements a queue based on linked nodes."""

    class Node(LinkedNode):
        """Internal node class for linked queues."""
        pass

    def __init__(self):
        self._front = None
        self._rear = None
        self._len = 0

    def __copy__(self):
        copy_of_self = type(self)()

        if self:
            iterator = iter(self)

            copy_of_self._front = copy_of_self.Node(next(iterator))

            current_node = copy_of_self._front
            for value in iterator:
                current_node.successor = copy_of_self.Node(value)
                current_node = current_node.successor

            copy_of_self._rear = current_node

        copy_of_self._len = len(self)

        return copy_of_self

    def __iter__(self):
        current_node = self._front
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self):
        return self._len

    def __repr__(self):
        # determine values of first seven nodes (at most)
        first_values = []
        for value in self:
            first_values.append(value)
            if len(first_values) == 7:
                break

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(first_values))

    def is_empty(self):
        """Checks whether this instance is empty."""
        return self._front is None

    def peek(self):
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._front.value

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._rear.successor = self.Node(value)
            self._rear = self._rear.successor

        self._len += 1

    def delete(self):
        """Deletes the value on the front of this instance."""
        self._validate_non_emptiness()

        self._front = self._front.successor

        self._len -= 1

    def clear(self):
        """Removes all values."""
        self._front = None
        self._rear = None
        self._len = 0

    def dequeue(self):
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        value = self._front.value
        self._front = self._front.successor

        self._len -= 1

        return value
