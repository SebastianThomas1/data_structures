# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable, Collection

# representations of objects
from reprlib import repr as reprlib_repr

# custom modules
from node import LinkedNode


__all__ = ['Stack', 'ArrayStack', 'LinkedStack', 'EmptyStackException']


class Stack(Collection):
    """Abstract base class for the abstract data type stack.

    Concrete subclasses must provide: __new__ or __init__, __iter__."""

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        # iterate over instance and other in parallel while checking for
        # equality
        values_of_self = iter(self)
        values_of_other = iter(other)

        self_is_empty = False
        other_is_empty = False

        while True:
            try:
                value_of_self = next(values_of_self)
            except StopIteration:
                self_is_empty = True

            try:
                value_of_other = next(values_of_other)
            except StopIteration:
                other_is_empty = True

            if self_is_empty:
                return other_is_empty
            elif other_is_empty:
                return False  # self_is_empty is False
            elif value_of_self != value_of_other:
                return False

    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, value):
        for entry in self:
            if entry is value or entry == value:
                return True

        return False

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.push(value)

        return self

    @abstractmethod
    def push(self, value):
        """Pushs an item on top of the stack."""
        pass

    @abstractmethod
    def pop(self):
        """Removes and returns value on top of the stack."""
        pass

    def is_empty(self):
        """Checks whether this instance is an empty stack."""
        return len(self) == 0

    def peek(self):
        """Returns item on top of the stack."""
        if self.is_empty():
            raise EmptyStackException('Can\'t peek at empty stack.')

        value = self.pop()
        self.push(value)
        return value


class ArrayStack(Stack):
    """Class that implements stacks based on an internal dynamic array (python
    list)."""

    def __init__(self):
        self._values = []

    def __iter__(self):
        return reversed(self._values)

    def __bool__(self):
        return bool(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(self._values[::-1]))

    def __str__(self):
        return str(self._values[::-1])[1:-1]

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
        """Returns item on top of the stack."""
        if self.is_empty():
            raise EmptyStackException('Can\'t peek on top of empty stack.')

        return self._values[-1]

    def push(self, value):
        """Pushs an item on top of the stack."""
        self._values.append(value)

    def pop(self):
        """Removes and returns value on top of the stack."""
        if self.is_empty():
            raise EmptyStackException('Can\'t pop from top of empty stack.')

        return self._values.pop()


class LinkedStack(Stack):
    """Class that implements stacks based on linked nodes."""

    class Node(LinkedNode):
        """Internal node class for linked stacks."""
        pass

    def __init__(self):
        self._top = None
        self._len = 0

    def __iter__(self):
        current_node = self._top
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self):
        return self._len

    def __repr__(self):
        # determine values of first seven nodes (at most)
        first_values = []
        count = 0
        for value in self:
            first_values.append(value)
            count += 1
            if count == 7:
                break

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        return ' \u2192 '.join(str(value) for value in self)

    def peek(self):
        """Returns item on top of the stack."""
        if self.is_empty():
            raise EmptyStackException('Can\'t peek at empty stack.')

        return self._top.value

    def push(self, value):
        """Pushs an item on top of the stack."""
        self._top = self.Node(value, successor=self._top)

        self._len += 1

    def pop(self):
        """Removes and returns value on top of the stack."""
        if self.is_empty():
            raise EmptyStackException('Can\'t peek at empty stack.')

        value = self._top.value
        self._top = self._top.successor

        self._len -= 1

        return value


class EmptyStackException(Exception):
    pass
