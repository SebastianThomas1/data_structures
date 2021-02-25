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


__all__ = ['ArrayStack', 'LinkedStack', 'Stack', 'TOP']


TOP = 'top'


class Stack(PredictableIterable, Collection, CollectionWithReferences):
    """Abstract base class for the abstract data type stack.

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, peek, push and delete."""

    __slots__ = ()

    @classmethod
    def from_iterable(cls, values: Iterable) -> Stack:
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()

        for value in values:
            self.push(value)

        return self

    def __copy__(self) -> Stack:
        """Returns a (shallow) copy of this instance."""
        reverse_copy_of_self = type(self).from_iterable(self)
        copy_of_self = type(self).from_iterable(reverse_copy_of_self)
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

    def __getitem__(self, key: type(TOP)) -> Any:
        """Returns the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)

        return self.peek()

    def __setitem__(self, key: type(TOP), value: Any) -> NoReturn:
        """Updates the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)

        self.replace(value)

    def __delitem__(self, key: type(TOP)) -> NoReturn:
        """Deletes the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)

        self.delete()

    @staticmethod
    def _validate_key(key: type(TOP)):
        """Validates that key is TOP."""
        if key is not TOP:
            raise KeyError('key must be TOP')

    def get(self) -> Any:
        """Returns the value at the top of this instance."""
        return self.peek()

    @abstractmethod
    def peek(self) -> Any:
        """Alias to get: returns the value at the top of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def insert(self, key: type(TOP), value: Any) -> NoReturn:
        """Inserts the value at the key.

        The parameter key must be TOP."""
        self._validate_key(key)
        self.push(value)

    def post(self, value: Any) -> NoReturn:
        """Posts the value to this instance and places it on the top."""
        self.push(value)

    @abstractmethod
    def push(self, value: Any) -> NoReturn:
        """Alias to post: pushes the value on the top of this instance."""
        raise NotImplementedError

    def replace(self, value: Any) -> NoReturn:
        """Updates the value on the top of this instance."""
        self.delete()
        self.push(value)

    @abstractmethod
    def delete(self) -> NoReturn:
        """Deletes the value on the top of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def pop(self, key: type(TOP) = TOP) -> Any:
        """Removes and returns the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)

        return super().pop(key)


class ArrayStack(Stack):
    """Class that implements a stack based on an internal dynamic array (python
    list)."""

    __slots__ = '_values',

    @classmethod
    def from_iterable(cls, values: Iterable) -> ArrayStack:
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        return self

    def __init__(self) -> NoReturn:
        """Initializes instance."""
        self._values = []

    def __copy__(self) -> ArrayStack:
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self) -> Iterator:
        """Returns an iterator version of this instance."""
        return reversed(self._values)

    def __len__(self) -> int:
        """Returns the number of values in this instance."""
        return len(self._values)

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        return f'{type(self).__name__}({repr(self._values[::-1])})'

    def __contains__(self, value: Any) -> bool:
        """Checks whether the given value is contained in this instance."""
        return value in self._values

    def __iadd__(self, values: Iterable) -> ArrayStack:
        """Pushes values on top of this instance."""
        self._validate_iterability(values)

        self._values += values

        return self

    def is_empty(self) -> bool:
        """Checks whether this instance is empty."""
        return not bool(self._values)

    def peek(self) -> Any:
        """Alias to get: returns the value at the top of this instance."""
        self._validate_non_emptiness()

        return self._values[-1]

    def push(self, value: Any) -> NoReturn:
        """Alias to post: pushes the value on the top of this instance."""
        self._values.append(value)

    def replace(self, value: Any) -> NoReturn:
        """Updates the value on the top of this instance."""
        self._validate_non_emptiness()

        self._values[-1] = value

    def delete(self) -> NoReturn:
        """Deletes the value on the top of this instance."""
        self._validate_non_emptiness()

        del self._values[-1]

    def clear(self) -> NoReturn:
        """Removes all values."""
        self._values.clear()

    def pop(self, key: type(TOP) = TOP) -> Any:
        """Removes and returns the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)
        self._validate_non_emptiness()

        return self._values.pop()


class LinkedStack(Stack):
    """Class that implements a stack based on linked nodes."""

    __slots__ = '_top', '_len'

    class Node(LinkedNode):
        """Internal node class for linked stacks."""
        pass

    def __init__(self) -> NoReturn:
        """Initializes instance."""
        self._top = None
        self._len = 0

    def __copy__(self) -> LinkedStack:
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()

        if self:
            iterator = iter(self)

            copy_of_self._top = copy_of_self.Node(next(iterator))

            current_node = copy_of_self._top
            for value in iterator:
                current_node.successor = copy_of_self.Node(value)
                current_node = current_node.successor

        copy_of_self._len = len(self)

        return copy_of_self

    def __iter__(self) -> Iterator:
        """Returns an iterator version of this instance."""
        current_node = self._top
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self) -> int:
        """Returns the number of values in this instance."""
        return self._len

    def is_empty(self) -> bool:
        """Checks whether this instance is empty."""
        return self._top is None

    def peek(self) -> Any:
        """Alias to __getitem__(TOP): returns the value at the top of this
        instance."""
        self._validate_non_emptiness()

        return self._top.value

    def push(self, value: Any) -> NoReturn:
        """Alias to insert(TOP, value): pushes the value on the top of this
        instance."""
        self._top = self.Node(value, successor=self._top)

        self._len += 1

    def replace(self, value: Any) -> NoReturn:
        """Updates the value on the top of this instance."""
        self._validate_non_emptiness()

        self._top.value = value

    def delete(self) -> NoReturn:
        """Deletes the value on the top of this instance."""
        self._validate_non_emptiness()

        self._top = self._top.successor

        self._len -= 1

    def clear(self) -> NoReturn:
        """Removes all values."""
        self._top = None
        self._len = 0

    def pop(self, key: type(TOP) = TOP) -> Any:
        """Removes and returns the value on the top of this instance.

        The parameter key must be TOP."""
        self._validate_key(key)
        self._validate_non_emptiness()

        value = self._top.value
        self._top = self._top.successor

        self._len -= 1

        return value
