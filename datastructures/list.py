# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable, MutableSequence
from numbers import Integral

# copying objects
from copy import copy

# representations of objects
from reprlib import repr

# custom modules
from datastructures.base import PredictableIterable
from datastructures.node import LinkedNode, DoublyLinkedNode


__all__ = ['List', 'ArrayList', 'BasicLinkedList', 'LinkedList',
           'CircularLinkedList', 'DoublyLinkedList',
           'CircularDoublyLinkedList']


class List(PredictableIterable, MutableSequence):
    """Abstract base class for the abstract data type list.

    Concrete subclasses must provide: __new__ or __init__, __getitem__,
    __setitem__, __delitem__, __len__, insert_before and insert_after."""

    __slots__ = ()

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()
        self.extend_by_appending(values)

        return self

    def __copy__(self):
        return type(self).from_iterable(self)

    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        return sum(1 for _ in self)

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError('Can only concatenate instances of the same type.')

        result = copy(self)
        result += other

        return result

    def __iadd__(self, values):
        self.extend_by_appending(values)
        return self

    def __mul__(self, other):
        result = copy(self)
        result *= other

        return result

    def __rmul__(self, other):
        return self * other

    # noinspection PyMethodFirstArgAssignment
    def __imul__(self, other):
        if not isinstance(other, Integral):
            raise TypeError('Can\'t multiply list by non-integer of '
                            'type \'{}\'.'.format(type(other).__name__))

        if other < 0:
            raise ValueError('Can\'t multiply list by negative '
                             'integer.')

        if other == 0:
            self.clear()
        else:
            copy_of_self = copy(self)
            self *= other - 1
            self += copy_of_self

        return self

    @staticmethod
    def _validate_iterability(values):
        if not isinstance(values, Iterable):
            raise TypeError('\'{}\' object is not '
                            'iterable.'.format(type(values).__name__))

    def _validate_and_adjust_key(self, key):
        """Validates and adjusts integral key."""
        length = len(self)
        if key < -length or key >= length:
            raise IndexError('Index out of range.')
        elif key < 0:
            key += length

        return key

    def _validate_and_adjust_slice(self, start, stop):
        """Validates and adjusts slice."""
        start, stop, _ = slice(start, stop, 1).indices(len(self))

        if start > stop:
            raise ValueError('Slice is empty.')

        return start, stop

    def is_empty(self):
        """Checks whether this instance is an empty list."""
        return len(self) == 0

    def first_index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # check entries until value is found, then return index
        for idx in range(start, stop):
            entry = self[idx]
            if entry == value:
                return idx

        raise ValueError('{} is not in list resp. slice.'.format(repr(value)))

    def last_index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # check entries; if value is found, remember index
        remembered = None

        for idx in range(start, stop):
            entry = self[idx]
            if entry == value:
                remembered = idx

        # if value was found, return remembered index
        if remembered is not None:
            return remembered
        else:
            raise ValueError('{} is not in list resp. '
                             'slice.'.format(repr(value)))

    def index(self, value, start=0, stop=None):
        """Alias to first_index: returns first index of value."""
        return self.first_index(value, start=start, stop=stop)

    @abstractmethod
    def insert_before(self, index, value):
        """Inserts value before index."""
        raise IndexError

    @abstractmethod
    def insert_after(self, index, value):
        """Inserts value after index."""
        raise IndexError

    def insert(self, index, value):
        """Alias to insert_before: inserts value before index."""
        self.insert_before(index, value)

    def prepend(self, value):
        """Prepends value to this instance."""
        self.insert(0, value)

    def extend_by_prepending(self, values):
        """Extends this instance by prepending values."""
        self._validate_iterability(values)

        for value in values:
            self.prepend(value)

    def extend_by_appending(self, values):
        """Extends this instance by appending values."""
        self._validate_iterability(values)

        for value in values:
            self.append(value)

    def extend(self, values):
        """Alias to extend_by_appending: extends this instance by appending
        values."""
        self.extend_by_appending(values)

    def pop_first(self):
        """Removes and returns first value."""
        return self.pop(0)

    def pop_last(self):
        """Removes and returns last value."""
        return self.pop(-1)

    def remove_first(self, value):
        """Removes first occurrence of value."""
        del self[self.first_index(value)]

    def remove_last(self, value):
        """Removes last occurrence of value."""
        del self[self.last_index(value)]

    def remove(self, value):
        """Alias to remove_first: removes first occurrence of value."""
        self.remove_first(value)


class ArrayList(List):
    """Class that implement an array list (dynamic array).

    It is essentially a wrapper for Python's builtin lists."""

    __slots__ = '_values',

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            self._values = list(values)

        return self

    def __init__(self):
        self._values = []

    def __iter__(self):
        return iter(self._values)

    def __reversed__(self):
        return reversed(self._values)

    def __bool__(self):
        return bool(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self._values))

    def __str__(self):
        return str(self._values)

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._values[int(key)]
        elif isinstance(key, slice):
            return ArrayList.from_iterable(self._values[key])
        else:
            raise TypeError('Indices must be integers or slices.')

    def __setitem__(self, key, value):
        if isinstance(key, Integral):
            self._values[int(key)] = value
        elif isinstance(key, slice):
            if isinstance(value, Iterable):
                self._values[key] = value
            else:
                raise TypeError('Can only assign an iterable.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __delitem__(self, key):
        if isinstance(key, Integral):
            del self._values[int(key)]
        elif isinstance(key, slice):
            del self._values[key]
        else:
            raise TypeError('Indices must be integers or slices.')

    def is_empty(self):
        return not bool(self)

    def first_index(self, value, start=0, stop=None):
        start, stop = self._validate_and_adjust_slice(start, stop)
        return self._values.index(value, start, stop)

    def insert_before(self, index, value):
        if self.is_empty():
            raise IndexError('Can\'t access index in empty list.')

        index = self._validate_and_adjust_key(index)
        self._values.insert(index, value)

    def insert_after(self, index, value):
        if self.is_empty():
            raise IndexError('Can\'t access index in empty list.')

        index = self._validate_and_adjust_key(index)
        self._values.insert(index + 1, value)

    def prepend(self, value):
        self._values = [value] + self._values

    def append(self, value):
        self._values.append(value)

    def extend_by_prepending(self, values):
        self._values = list(values) + self._values

    def extend_by_appending(self, values):
        self._values.extend(values)

    def pop(self, index=-1):
        self._values.pop(index)

    def clear(self):
        """Removes all items."""
        self._values.clear()

    def remove_first(self, value):
        self._values.remove(value)

    def reverse(self):
        self._values.reverse()


class BasicLinkedList(List):
    """Class that implements a (singly) linked list in a very basic fashion,
    saving only a reference to the head node.

    This implementation is more inefficient than necessary from a runtime point
    of view."""

    __slots__ = '_head',

    class Node(LinkedNode):
        """Internal node class for (singly) linked lists."""
        pass

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._head = self.Node(next(iterator))

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value)
                current_node = current_node.successor

        return self

    def __init__(self):
        self._head = None

    def __copy__(self):
        return type(self).from_iterable(self)

    def __iter__(self):
        for node in self._traversal():
            yield node.value

    def __len__(self):
        return sum(1 for _ in self._traversal())

    def __repr__(self):
        # determine values of first seven nodes (at most)
        first_values = []
        for value in self:
            first_values.append(value)
            if len(first_values) == 7:
                break

        return '{}({})'.format(type(self).__name__, repr(first_values))

    def __str__(self):
        return ' \u2192 '.join(str(value) for value in self)

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._get_node(key).value
        elif isinstance(key, slice):
            # replace this by an efficient implementation
            # return type(self)(self[idx]
            #                       for idx in range(*key.indices(len(self))))
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __setitem__(self, key, value):
        if isinstance(key, Integral):
            self._get_node(key).value = value
        elif isinstance(key, slice):
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __delitem__(self, key):
        if isinstance(key, Integral):
            if self.is_empty():
                raise IndexError('Can\'t delete from empty list.')

            node, predecessor = self._get_node_with_predecessor(key)
            self._remove_node(node, predecessor)
        elif isinstance(key, slice):
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        if self.is_empty():
            return

        # traverse instance until the successor of the current node
        # becomes None
        for node in self._traversal():
            if node.successor is None:
                return node

    def _traversal(self, start_node=None):
        """Traverses instance, beginning with start_node (default: head)."""
        if start_node is None:
            start_node = self.head

        current_node = start_node
        while current_node:
            yield current_node
            current_node = current_node.successor

    def _validate_and_adjust_key(self, key):
        """Validates and adjusts integral key."""
        if key < 0:
            length = len(self)
            if key < -length:
                raise IndexError('Index out of range.')
            else:
                key += length

        return key

    def _validate_and_adjust_slice(self, start, stop):
        """Validates and adjusts slice."""
        if start is None:
            start = 0

        if start < 0 or stop is not None and stop < 0:
            start, stop, _ = slice(start, stop, 1).indices(len(self))

        if stop is not None and start > stop:
            raise ValueError('Slice is empty.')

        return start, stop

    def _get_node(self, key):  # assume key is an integer
        """Returns node at index."""
        if self.is_empty():
            raise IndexError('Can\'t access index in empty list.')

        key = self._validate_and_adjust_key(key)

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
            raise IndexError('Can\'t access index in empty list.')

        key = self._validate_and_adjust_key(key)

        # traverse instance, return current node and predecessor if item
        # at index is reached
        predecessor = None
        for node in self._traversal():
            if key == 0:
                return node, predecessor
            key -= 1
            predecessor = node

        raise IndexError('Index out of range.')

    def _insert_as_predecessor(self, node, value, current_predecessor):
        """Inserts value before node by reconnecting current predecessor."""
        if current_predecessor:
            current_predecessor.successor = self.Node(value, successor=node)
        else:  # ie node is self.head
            self._head = self.Node(value, successor=node)

    def _insert_as_successor(self, node, value):
        """Inserts value after node by reconnecting current successor."""
        node.successor = self.Node(value, successor=node.successor)

    def _extend_by_prepending(self, other):
        """Extends this instance by prepending values from instance other."""
        assert isinstance(other, type(self))

        if other.is_empty():
            return

        # extend
        other.tail.successor = self.head

        self._head = other.head

    def _extend_by_appending(self, other):
        """Extends this instance by appending values from instance other."""
        assert isinstance(other, type(self))

        if self.is_empty():
            self._head = other.head
        else:
            self.tail.successor = other.head

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        if predecessor:
            predecessor.successor = node.successor
        else:  # ie node is self.head
            self._head = self.head.successor

    def is_empty(self):
        """Checks whether this instance is the empty linked list."""
        return self.head is None

    def first_index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # traverse instance, beginning from node at index start, when
        # value is reached, return index
        idx = 0
        for node in self._traversal():
            if idx >= start and (node.value is value or node.value == value):
                return idx
            idx += 1
            if stop is not None and idx == stop:
                break

        raise ValueError('{} is not in list resp. slice.'.format(repr(value)))

    def last_index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # traverse instance, beginning from node at index start, when
        # value is found, remember index
        remembered = None

        idx = 0
        for node in self._traversal():
            if idx >= start and (node.value == value):
                remembered = idx
            idx += 1
            if stop is not None and idx == stop:
                break

        # if value was found, return remembered index
        if remembered is not None:
            return remembered
        else:
            raise ValueError('{} is not in list resp. '
                             'slice.'.format(repr(value)))

    def insert_before(self, index, value):
        """Inserts value before index."""
        node, predecessor = self._get_node_with_predecessor(index)
        self._insert_as_predecessor(node, value, predecessor)

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        self._insert_as_successor(node, value)

    def prepend(self, value):
        """Prepends an item to this instance."""
        self._head = self.Node(value, successor=self.head)

    def append(self, value):
        """Appends an item to this instance."""
        if self.is_empty():
            self._head = self.Node(value)
        else:
            self.tail.successor = self.Node(value)

    def extend_by_prepending(self, values):
        """Extends this instance by prepending values."""
        self._validate_iterability(values)

        # convert/copy other to linked list
        other = type(self).from_iterable(values)

        self._extend_by_prepending(other)

    def extend_by_appending(self, values):
        """Extends this instance by appending values."""
        self._validate_iterability(values)

        # convert/copy other to linked list
        other = type(self).from_iterable(values)

        self._extend_by_appending(other)

    def pop(self, index=-1):
        """Removes and returns item at index (default -1)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty list.')

        node, predecessor = self._get_node_with_predecessor(index)
        self._remove_node(node, predecessor)

        return node.value

    def clear(self):
        """Removes all items."""
        self._head = None

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance until value is found, then remove node
        predecessor = None
        for node in self._traversal():
            if node.value == value:
                self._remove_node(node, predecessor)
                return

            predecessor = node

        raise ValueError('{} is not in list.'.format(repr(value)))

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance, beginning from node at index start, when
        # value is found, remember node and predecessor
        remembered_predecessor = None
        remembered_node = None

        predecessor = None
        for node in self._traversal():
            if node.value == value:
                remembered_predecessor = predecessor
                remembered_node = node

            predecessor = node

        # if value was found, remove remembered node
        if remembered_node:
            self._remove_node(remembered_node, remembered_predecessor)
        else:
            raise ValueError('{} is not in list.'.format(repr(value)))

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        # traverse list, meanwhile set successors to former predecessors
        previous_node = None
        current_node = self.head
        while current_node:
            next_node = current_node.successor
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node

        self._head = previous_node


class LinkedList(BasicLinkedList):
    """Class that implements a (singly) linked list.

    In contrast to the class BasicLinkedList, in this implementation we save a
    reference to the tail node as well as the length. This speeds up some of
    the methods."""

    __slots__ = '_tail', '_len'

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._head = self.Node(next(iterator))
            self._len += 1

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value)
                current_node = current_node.successor
                self._len += 1

            self._tail = current_node

        return self

    def __init__(self):
        super().__init__()
        self._tail = None
        self._len = 0

    def __len__(self):
        return self._len

    @property
    def tail(self):
        return self._tail

    def _validate_and_adjust_key(self, key):
        """Validates and adjusts integral key."""
        return List._validate_and_adjust_key(self, key)

    def _validate_and_adjust_slice(self, start, stop):
        """Validates and adjusts slice."""
        return List._validate_and_adjust_slice(self, start, stop)

    def _insert_as_predecessor(self, node, value, current_predecessor):
        """Inserts value before node by reconnecting current predecessor."""
        super()._insert_as_predecessor(node, value, current_predecessor)

        self._len += 1

    def _insert_as_successor(self, node, value):
        """Inserts value after node by reconnecting current successor."""
        super()._insert_as_successor(node, value)

        if self.tail.successor:  # ie node was self.tail
            self._tail = self.tail.successor

        self._len += 1

    def _extend_by_prepending(self, other):
        """Extends this instance by prepending values from instance other."""
        assert isinstance(other, type(self))

        super()._extend_by_prepending(other)

        if self.tail is None:
            self._tail = other.tail

        self._len += len(other)

    def _extend_by_appending(self, other):
        """Extends this instance by appending values from instance other."""
        assert isinstance(other, type(self))

        super()._extend_by_appending(other)

        self._tail = other.tail

        self._len += len(other)

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        super()._remove_node(node, predecessor)

        if node.successor is None:  # ie node is self.tail
            self._tail = predecessor

        self._len -= 1

    def prepend(self, value):
        """Prepends an item to this instance."""
        super().prepend(value)

        if self.tail is None:
            self._tail = self.head

        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        super().append(value)

        if self.tail:
            self._tail = self.tail.successor
        else:  # length 1
            self._tail = self.head

        self._len += 1

    def clear(self):
        """Removes all items."""
        super().clear()
        self._tail = None
        self._len = 0

    def reverse(self):
        """Reverses this instance."""
        self._tail = self.head

        super().reverse()


class CircularLinkedList(BasicLinkedList):
    """Class that implements a (singly) circular linked list."""

    __slots__ = '_len',

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._head = self.Node(next(iterator))
            self._len += 1

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value)
                current_node = current_node.successor
                self._len += 1

            current_node.successor = self.head

        return self

    def __init__(self):
        super().__init__()
        self._len = 0

    def __len__(self):
        return self._len

    def __str__(self):
        if self.is_empty():
            return ''
        else:
            return ' \u2192 '.join(str(value) for value in self) + ' \u2192'

    @property
    def tail(self):
        if self.is_empty():
            return

        # traverse instance until the successor of the current node
        # becomes the head
        for node in self._traversal():
            if node.successor is self.head:
                return node

    def _traversal(self, start_node=None):
        """Traverses instance, beginning with start_node (default: head)."""
        if not self.is_empty():
            if start_node is None:
                start_node = self.head

            current_node = start_node
            while True:
                yield current_node
                current_node = current_node.successor
                if current_node is self.head:
                    break

    def _validate_and_adjust_key(self, key):
        """Validates and adjusts integral key."""
        return List._validate_and_adjust_key(self, key)

    def _validate_and_adjust_slice(self, start, stop):
        """Validates and adjusts slice."""
        return List._validate_and_adjust_slice(self, start, stop)

    def _get_node_with_predecessor(self, key):
        """Returns node at index together with predecessor."""
        if self.is_empty():
            raise IndexError('Can\'t access index in empty list.')

        key = self._validate_and_adjust_key(key)

        if key == 0:
            return self.head, self.tail

        # traverse instance, return current node and predecessor if item
        # at index is reached
        predecessor = None
        for node in self._traversal():
            if key == 0:
                return node, predecessor
            key -= 1
            predecessor = node

        raise IndexError('Index out of range.')

    def _insert_as_predecessor(self, node, value, current_predecessor):
        """Inserts value before node by reconnecting current predecessor."""
        current_predecessor.successor = self.Node(value, successor=node)

        if node is self.head:
            self._head = current_predecessor.successor

        self._len += 1

    def _insert_as_successor(self, node, value):
        """Inserts value after node by reconnecting current successor."""
        super()._insert_as_successor(node, value)

        self._len += 1

    def _extend_by_prepending(self, other):
        """Extends this instance by prepending values from instance other."""
        assert isinstance(other, type(self))

        if other.is_empty():
            return

        # extend
        if not self.is_empty():
            other.tail.successor = self.head
            self.tail.successor = other.head

        self._head = other.head
        self._len += len(other)

        return

    def _extend_by_appending(self, other):
        """Extends this instance by appending values from instance other."""
        if other.is_empty():
            return

        super()._extend_by_appending(other)

        other.tail.successor = self.head

        self._len += len(other)

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        if node is predecessor:  # length 1
            self._head = None
        else:
            predecessor.successor = node.successor

            if node is self.head:
                self._head = self.head.successor

        self._len -= 1

    def prepend(self, value):
        """Prepends an item to this instance."""
        if self.is_empty():
            super().prepend(value)
            self.head.successor = self.head
        else:
            tail = self.tail
            super().prepend(value)
            tail.successor = self.head

        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        if self.is_empty():
            self._head = self.Node(value)
            self.head.successor = self.head
        else:
            self.tail.successor = self.Node(value, self.head)

        self._len += 1

    def clear(self):
        """Removes all items."""
        super().clear()
        self._len = 0

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty circular list.')

        # traverse instance until value is found, then remove node
        predecessor = None
        for node in self._traversal():
            if node.value == value:
                if predecessor is None:  # ie node is self.head
                    predecessor = self.tail

                self._remove_node(node, predecessor)
                return

            predecessor = node

        raise ValueError('{} is not in list.'.format(repr(value)))

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance, beginning from node at index start, when
        # value is found, remember node and predecessor
        remembered_predecessor = None
        remembered_node = None

        predecessor = None
        for node in self._traversal():
            if node.value == value:
                remembered_predecessor = predecessor
                remembered_node = node

            predecessor = node

        if remembered_node:
            if remembered_predecessor is None:
                # ie remembered_node is self.head
                remembered_predecessor = self.tail
            self._remove_node(remembered_node, remembered_predecessor)
        else:
            raise ValueError('{} is not in list.'.format(repr(value)))

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        # traverse list, meanwhile set successors to former predecessors
        previous_node = None
        current_node = self.head
        while True:
            next_node = current_node.successor
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node
            if current_node is self.head:
                break

        self.head.successor = previous_node  # former tail
        self._head = previous_node


class DoublyLinkedList(LinkedList):
    """Class that implements a doubly linked list."""

    __slots__ = ()

    class Node(DoublyLinkedNode):
        """Internal node class for doubly linked lists."""
        pass

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._head = self.Node(next(iterator))
            self._len += 1

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value,
                                                   predecessor=current_node)
                current_node = current_node.successor
                self._len += 1

            self._tail = current_node

        return self

    def __reversed__(self):
        # traverse instance backwards, meanwhile yield values
        for node in self._reversed_traversal():
            yield node.value

    def __str__(self):
        return ' \u21c4 '.join(str(value) for value in self)

    def _reversed_traversal(self, start_node=None):
        """Traverses instance in reverse order, beginning with start_node
        (default: tail)."""
        if start_node is None:
            start_node = self.tail

        current_node = start_node
        while current_node:
            yield current_node
            current_node = current_node.predecessor

    def _validate_and_adjust_key(self, key):
        """Validates and adjusts integral key."""
        # cast key from Integral to int (so that >=, etc. are defined)
        key = int(key)

        length = len(self)
        if key < -length or key >= length:
            raise IndexError('Index out of range.')

        # prepare key for efficient traverse
        if key >= length // 2:
            key -= length
        if key < -length // 2:
            key += length

        return key

    def _get_node(self, key):
        """Returns node at index."""
        key = self._validate_and_adjust_key(key)

        # traverse instance, return current node if item at index is
        # reached
        if key >= 0:
            # traverse instance forwards
            for node in self._traversal():
                if key == 0:
                    return node
                key -= 1
        else:
            # traverse instance backwards
            for node in self._reversed_traversal():
                if key == -1:
                    return node
                key += 1

    def _get_node_with_predecessor(self, key):
        node = self._get_node(key)
        return node, node.predecessor

    def _insert_as_predecessor(self, node, value, current_predecessor):
        """Inserts value before node by reconnecting current predecessor."""
        assert node.predecessor == current_predecessor

        super()._insert_as_predecessor(node, value, current_predecessor)

        if current_predecessor:
            current_predecessor.successor.predecessor = current_predecessor
            node.predecessor = current_predecessor.successor
        else:  # ie node was self.head
            node.predecessor = self.head

    def _insert_as_successor(self, node, value):
        """Inserts value after node by reconnecting current successor."""
        super()._insert_as_successor(node, value)

        node.successor.predecessor = node
        if node.successor.successor:
            node.successor.successor.predecessor = node.successor

    def _extend_by_prepending(self, other):
        """Extends this instance by prepending values from instance other."""
        head = self.head  # save old head

        super()._extend_by_prepending(other)

        if head:  # ie self was not empty
            head.predecessor = other.tail

    def _extend_by_appending(self, other):
        """Extends this instance by appending values from instance other."""
        tail = self.tail  # save old tail

        super()._extend_by_appending(other)

        if other:
            other.head.predecessor = tail

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        assert node.predecessor == predecessor

        super()._remove_node(node, predecessor)

        if node.successor:
            node.successor.predecessor = predecessor

    def last_index(self, value, start=0, stop=None):
        """Returns last index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # traverse instance in reverse order, beginning from node at
        # index before stop, when value is reached, return index
        idx = len(self) - 1
        for node in self._reversed_traversal():
            if idx < stop and node.value == value:
                return idx
            idx -= 1
            if idx < start:
                break

        raise ValueError('{} is not in list resp. slice.'.format(repr(value)))

    def prepend(self, value):
        """Prepends an item to this instance."""
        super().prepend(value)

        if self.head.successor:
            self.head.successor.predecessor = self.head

    def append(self, value):
        """Appends an item to this instance."""
        tail = self.tail  # save old tail

        super().append(value)

        if tail:
            tail.predecessor = tail

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance until value is found, then remove node
        for node in self._traversal():
            if node.value == value:
                self._remove_node(node, node.predecessor)
                return

        raise ValueError('{} is not in list.'.format(repr(value)))

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance in reverse order until value is found, then
        # remove node
        for node in self._reversed_traversal():
            if node.value == value:
                self._remove_node(node, node.predecessor)
                return

        raise ValueError('{} is not in list.'.format(repr(value)))

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        # traverse list, meanwhile swap successors and predecessors
        current_node = self.head
        while current_node:
            current_node.predecessor, current_node.successor \
                = current_node.successor, current_node.predecessor
            current_node = current_node.predecessor  # former successor

        self._head, self._tail = self.tail, self.head


class CircularDoublyLinkedList(CircularLinkedList):
    """Class that implements a circular doubly linked list."""

    __slots__ = ()

    class Node(DoublyLinkedList.Node):
        """Internal node class for doubly linked lists."""
        pass

    @classmethod
    def from_iterable(cls, values):
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._head = self.Node(next(iterator))
            self._len += 1

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value,
                                                   predecessor=current_node)
                current_node = current_node.successor
                self._len += 1

            current_node.successor = self.head
            self.head.predecessor = current_node

        return self

    def __reversed__(self):
        # traverse instance backwards, meanwhile yield values
        for node in self._reversed_traversal():
            yield node.value

    def __str__(self):
        if self.is_empty():
            return ''
        else:
            return ' \u21c4 '.join(str(value) for value in self) + ' \u21c4'

    @property
    def tail(self):
        if self.is_empty():
            return
        else:
            return self.head.predecessor

    def _reversed_traversal(self, start_node=None):
        """Traverses instance in reverse order, beginning with start_node
        (default: tail)."""
        if not self.is_empty():
            if start_node is None:
                start_node = self.tail

            current_node = start_node
            while True:
                yield current_node
                current_node = current_node.predecessor
                if current_node is self.tail:
                    break

    def _validate_and_adjust_key(self, key):
        key = int(key)

        length = len(self)
        if key < -length or key >= length:
            raise IndexError('Index out of range.')

        # prepare key for efficient traverse
        if key >= length // 2:
            key -= length
        if key < -length // 2:
            key += length

        return key

    def _get_node(self, key):
        """Returns node at index."""
        key = self._validate_and_adjust_key(key)

        # traverse instance, return current node if item at index is
        # reached
        if key >= 0:
            # traverse instance forwards
            for node in self._traversal():
                if key == 0:
                    return node
                key -= 1
        else:
            # traverse instance backwards
            for node in self._reversed_traversal():
                if key == -1:
                    return node
                key += 1

    def _get_node_with_predecessor(self, key):
        """Returns node at index."""
        node = self._get_node(key)
        return node, node.predecessor

    def _insert_as_predecessor(self, node, value, current_predecessor):
        """Inserts value before node by reconnecting current predecessor."""
        assert node.predecessor == current_predecessor

        super()._insert_as_predecessor(node, value, current_predecessor)

        current_predecessor.successor.predecessor = current_predecessor
        node.predecessor = current_predecessor.successor

    def _insert_as_successor(self, node, value):
        """Inserts value after node by reconnecting current successor."""
        super()._insert_as_successor(node, value)

        node.successor.predecessor = node
        node.successor.successor.predecessor = node.successor

    def _extend_by_prepending(self, other):
        """Extends this instance by prepending values from instance other."""
        # save old head and tail
        head = self.head
        tail = self.tail

        super()._extend_by_prepending(other)

        if head:  # ie self was not empty
            head.predecessor = other.tail
            self.head.predecessor = tail

    def _extend_by_appending(self, other):
        """Extends this instance by appending values from instance other."""
        # save tails of self and other
        tail_of_self = self.tail
        tail_of_other = other.tail

        super()._extend_by_appending(other)

        if other:
            other.head.predecessor = tail_of_self
            self.head.predecessor = tail_of_other

    def _remove_node(self, node, predecessor):
        """Removes node by connecting predecessor with successor."""
        assert node.predecessor == predecessor

        super()._remove_node(node, predecessor)

        node.successor.predecessor = predecessor

    def last_index(self, value, start=0, stop=None):
        """Returns last index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty list.')

        start, stop = self._validate_and_adjust_slice(start, stop)

        # traverse instance in reverse order, beginning from node at
        # index before stop, when value is reached, return index
        idx = len(self) - 1
        for node in self._reversed_traversal():
            if idx < stop and node.value == value:
                return idx
            idx -= 1
            if idx < start:
                break

        raise ValueError('{} is not in list resp. slice.'.format(repr(value)))

    def prepend(self, value):
        """Prepends an item to this instance."""
        tail = self.tail  # save old tail

        super().prepend(value)

        # ie self was not empty
        self.head.predecessor = tail if tail else self.head

        if self.head.successor:
            self.head.successor.predecessor = self.head

    def append(self, value):
        """Appends an item to this instance."""
        self.prepend(value)
        self._head = self.head.successor

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance until value is found, then remove node
        for node in self._traversal():
            if node.value == value:
                self._remove_node(node, node.predecessor)
                return

        raise ValueError('{} is not in list.'.format(repr(value)))

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty list.')

        # traverse instance in reverse order until value is found, then
        # remove node
        for node in self._reversed_traversal():
            if node.value == value:
                self._remove_node(node, node.predecessor)
                return

        raise ValueError('{} is not in list.'.format(repr(value)))

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        # traverse list, meanwhile swap successors and predecessors
        current_node = self.head
        while True:
            current_node.predecessor, current_node.successor \
                = current_node.successor, current_node.predecessor
            current_node = current_node.predecessor  # former successor
            if current_node is self.head:
                break

        self._head = self.head.successor
