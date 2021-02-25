# Sebastian Thomas (datascience at sebastianthomas dot de)

from __future__ import annotations

# type hints
from typing import NoReturn, Any

# abstract base classes
from abc import abstractmethod
from collections import Iterable, Iterator

# copying objects
from copy import copy

# representations of objects
from reprlib import repr

# custom modules
from datastructures.base import Collection, CollectionWithReferences, \
    PredictableIterable
from datastructures.node import LinkedNode


__all__ = ['ArrayQueue', 'FRONT', 'LinkedQueue', 'Queue', 'REAR']


REAR = 'rear'
FRONT = 'front'


class Queue(PredictableIterable, Collection, CollectionWithReferences):
    """Abstract base class for the abstract data type queue.

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, peek, enqueue and dequeue."""

    __slots__ = ()

    @classmethod
    def from_iterable(cls, values: Iterable) -> Queue:
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()

        for value in values:
            self.enqueue(value)

        return self

    def __copy__(self) -> Queue:
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self).from_iterable(self)
        return copy_of_self

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        # determine values of first seven values (at most)
        first_values = []
        for value in self:
            first_values.append(value)
            if len(first_values) == 7:
                break

        return f'{type(self).__name__}({repr(first_values)})'

    def __str__(self) -> str:
        """Returns a user-friendly string representation of this instance,
        which may be used for printing."""
        return ' '.join(str(value) for value in self)

    def __contains__(self, value: Any) -> bool:
        """Checks whether the given value is contained in this instance."""
        return Collection.__contains__(self, value)

    def __getitem__(self, key: type(FRONT)) -> Any:
        """Returns the value on the front of this instance.

        The parameter key must be FRONT."""
        self._validate_key_front(key)

        return self.peek()

    def __setitem__(self, key, value: Any) -> NoReturn:
        """Raises TypeError."""
        raise TypeError(f'\'{type(self).__name__}\' object does not support '
                        f'item assignment')

    def __delitem__(self, key: type(FRONT)) -> NoReturn:
        """Deletes the value on the front of this instance.

        The parameter key must be FRONT."""
        self._validate_key_front(key)

        self.delete()

    @staticmethod
    def _validate_key_rear(key: type(REAR)) -> NoReturn:
        """Validates that key is REAR."""
        if key is not REAR:
            raise KeyError('key must be REAR')

    @staticmethod
    def _validate_key_front(key: type(FRONT)) -> NoReturn:
        """Validates that key is FRONT."""
        if key is not FRONT:
            raise KeyError('key must be FRONT')

    def get(self) -> Any:
        """Returns the value at the front of this instance."""
        return self.peek()

    @abstractmethod
    def peek(self) -> Any:
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def insert(self, key: type(REAR), value: Any) -> NoReturn:
        """Inserts the value at the key.

        The parameter key must be REAR."""
        self._validate_key_rear(key)
        self.enqueue(value)

    def post(self, value: Any) -> NoReturn:
        """Posts the value to this instance and places it on the rear."""
        self.enqueue(value)

    @abstractmethod
    def enqueue(self, value: Any) -> NoReturn:
        """Alias to post: enqueues the value to this instance."""
        raise NotImplementedError

    def delete(self) -> Any:
        """Deletes the value on the front of this instance."""
        self.dequeue()

    def pop(self, key: type(FRONT) = FRONT) -> Any:
        """Removes and returns the value on the front of this instance.

        The parameter key must be FRONT (default)."""
        self._validate_key_front(key)

        return self.dequeue()

    @abstractmethod
    def dequeue(self) -> Any:
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class ArrayQueue(Queue):
    """Class that implements a queue based on an internal dynamic array (python
    list)."""

    __slots__ = '_values'

    @classmethod
    def from_iterable(cls, values: Iterable) -> ArrayQueue:
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        return self

    def __init__(self) -> NoReturn:
        """Initializes instance."""
        self._values = []

    def __copy__(self) -> ArrayQueue:
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self) -> Iterator:
        """Returns an iterator version of this instance."""
        return iter(self._values)

    def __len__(self) -> int:
        """Returns the number of values in this instance."""
        return len(self._values)

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        return f'{type(self).__name__}({repr(self._values)})'

    def __contains__(self, value: Any) -> bool:
        """Checks whether the given value is contained in this instance."""
        return value in self._values

    def __iadd__(self, values: Iterable) -> ArrayQueue:
        """Enqueues values to this instance."""
        self._validate_iterability(values)

        self._values += values

        return self

    def is_empty(self) -> bool:
        """Checks whether this instance is empty."""
        return not bool(self._values)

    def peek(self) -> Any:
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._values[0]

    def enqueue(self, value: Any) -> NoReturn:
        """Alias to post: enqueues the value to this instance."""
        self._values.append(value)

    def delete(self) -> NoReturn:
        """Deletes the value on the front of this instance."""
        self._validate_non_emptiness()

        del self._values[0]

    def clear(self) -> NoReturn:
        """Removes all values."""
        self._values.clear()

    def dequeue(self) -> Any:
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._values.pop(0)


class LinkedQueue(Queue):
    """Class that implements a queue based on linked nodes."""

    __slots__ = '_front', '_rear', '_len'

    class Node(LinkedNode):
        """Internal node class for linked queues."""
        pass

    @classmethod
    def from_iterable(cls, values: Iterable) -> LinkedQueue:
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._front = self.Node(next(iterator))
            self._len += 1

            current_node = self._front
            for value in iterator:
                current_node.successor = self.Node(value)
                current_node = current_node.successor
                self._len += 1

            self._rear = current_node

        return self

    def __init__(self) -> NoReturn:
        """Initializes instance."""
        self._front = None
        self._rear = None
        self._len = 0

    def __copy__(self) -> LinkedQueue:
        """Returns a (shallow) copy of this instance."""
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

    def __iter__(self) -> Iterator:
        """Returns an iterator version of this instance."""
        current_node = self._front
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self) -> int:
        """Returns the number of values in this instance."""
        return self._len

    def is_empty(self) -> bool:
        """Checks whether this instance is empty."""
        return self._front is None

    def peek(self) -> Any:
        """Alias to get: returns the value at the front of this instance."""
        self._validate_non_emptiness()

        return self._front.value

    def enqueue(self, value: Any) -> NoReturn:
        """Alias to post: enqueues the value to this instance."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._rear.successor = self.Node(value)
            self._rear = self._rear.successor

        self._len += 1

    def delete(self) -> NoReturn:
        """Deletes the value on the front of this instance."""
        self._validate_non_emptiness()

        self._front = self._front.successor

        self._len -= 1

    def clear(self) -> NoReturn:
        """Removes all values."""
        self._front = None
        self._rear = None
        self._len = 0

    def dequeue(self) -> Any:
        """Alias to pop: dequeues the value at the front of this instance."""
        self._validate_non_emptiness()

        value = self._front.value
        self._front = self._front.successor

        self._len -= 1

        return value
