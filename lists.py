# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from collections.abc import Iterable, MutableSequence
from numbers import Integral

# representations of objects
from reprlib import repr as reprlib_repr


class LinkedList(MutableSequence):
    """Class that implements (singly) linked lists."""

    class Node:
        """Internal node class for (singly) linked lists."""

        def __init__(self, value, successor=None):
            self.value = value
            self.successor = successor

        def __repr__(self):
            return repr(self.value)

        def __str__(self):
            return str(self.value)

    def __init__(self, values=None):
        self._len = 0
        if values:
            iterator = iter(values)

            self.head = self.Node(next(iterator))
            self._len += 1

            current_node = self.head
            for value in iterator:
                current_node.successor = self.Node(value, None)
                current_node = current_node.successor
                self._len += 1
        else:
            self.head = None

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        # traverse instance, meanwhile yield values
        current_node = self.head
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __reversed__(self):
        if self.is_empty():
            return

        # reverse instance
        self.reverse()

        # reverse reversed instance, while traversing, yield values
        yield self.head.value

        previous_node = self.head
        current_node = self.head.successor
        previous_node.successor = None

        while current_node:
            yield current_node.value
            next_node = current_node.successor
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node

        self.head = previous_node

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._get_node(key).value
        elif isinstance(key, slice):
            # replace this by an efficient implementation
            # return self.__class__(self[idx]
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
                raise IndexError('Can\'t delete from empty linked list.')

            node, predecessor = self._get_node_with_predecessor(key)

            # delete node
            if predecessor is None:  # ie node is self.head
                self.head = self.head.successor
            else:
                predecessor.successor = node.successor
        elif isinstance(key, slice):
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __len__(self):
        return self._len

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        # traverse instance and other linked list in parallel while
        # checking for equality
        current_node_self = self.head
        current_node_other = other.head
        while (current_node_self and current_node_other
               and current_node_self.value == current_node_other.value):
            current_node_self = current_node_self.successor
            current_node_other = current_node_other.successor

        return current_node_self == current_node_other

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only concatenate linked list to linked '
                            'list.')

        result = self.__class__(self)
        result += other

        return result

    def __iadd__(self, other):
        return self.extend_at_tail(other)

    def __mul__(self, other):
        result = self.__class__(self)
        result *= other

        return result

    def __imul__(self, other):
        if not isinstance(other, Integral):
            raise TypeError('Can\'t multiply linked list by non-integer of '
                            'type \'{}\'.'.format(type(other).__name__))

        if other < 0:
            raise ValueError('Can\'t multiply linked list by negative '
                             'integer.')

        if other == 0:
            self.head = None
        else:
            copy = self.__class__(self)
            self *= other - 1
            self += copy

        return self

    def __rmul__(self, other):
        return self*other

    def __repr__(self):
        # determine values of first seven nodes (at most)
        first_values = []
        current_node = self.head
        count = 0
        while count < 7 and current_node:
            first_values.append(current_node.value)
            current_node = current_node.successor
            count += 1

        return '{}({})'.format(self.__class__.__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        return ' \u2192 '.join(str(value) for value in self)

    def _get_node(self, key):  # assume key is an integer
        """Returns node at index."""
        if key < 0:
            length = len(self)
            if key < -length:
                raise IndexError('Index out of range.')
            else:
                key += length

        # traverse instance, return current node if item at index is
        # reached
        current_node = self.head
        while current_node:
            if key == 0:
                return current_node
            key -= 1
            current_node = current_node.successor

        raise IndexError('Index out of range.')

    def _get_node_with_predecessor(self, key):
        """Returns node at index together with predecessor."""
        if key < 0:
            length = len(self)
            if key < -length:
                raise IndexError('Index out of range.')
            else:
                key += length

        # traverse instance, return current node and predecessor if item
        # at index is reached
        previous_node = None
        current_node = self.head
        while current_node:
            if key == 0:
                return current_node, previous_node
            key -= 1
            previous_node = current_node
            current_node = current_node.successor

        raise IndexError('Index out of range.')

    def _get_tail(self):
        """Returns tail."""
        if self.is_empty():
            return

        # traverse instance until the successor of the current node
        # becomes None
        current_node = self.head
        while current_node.successor:
            current_node = current_node.successor

        return current_node

    def is_empty(self):
        """Checks whether this instance is the empty linked list."""
        return self.head is None

    def index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if start < 0 or stop and stop < 0:
            length = len(self)
            if start < 0:
                start = max(start + length, 0)
            if stop and stop < 0:
                stop += length

        # traverse instance, beginning from node at index start, when
        # value is reached, return index
        current_node = self._get_node(start)
        idx = start
        while current_node and (stop is None or idx < stop):
            if current_node.value is value or current_node.value == value:
                return idx
            current_node = current_node.successor
            idx += 1

        raise ValueError('{} is not in linked list.'.format(repr(value)))

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        node.successor = self.Node(value, successor=node.successor)
        self._len += 1

    def insert_before(self, index, value):
        """Inserts value before index."""
        node, predecessor = self._get_node_with_predecessor(index)
        if node is self.head:
            self.head = self.Node(value, self.head)
        else:
            predecessor.successor = self.Node(value, node)
        self._len += 1

    insert = insert_before

    def prepend(self, value):
        """Prepends an item to this instance."""
        self.head = self.Node(value, self.head)

    def append(self, value):
        """Appends an item to this instance."""
        tail = self._get_tail()
        tail.successor = self.Node(value)

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        # traverse list, meanwhile set successors to former predecessors
        previous_node = self.head
        current_node = self.head.successor
        previous_node.successor = None
        while current_node:
            next_node = current_node.successor
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node

        # reset head
        self.head = previous_node

    def extend_at_head(self, other):
        """Extends instance by prepending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        # define the new head/successor of tail of other linked list to
        # be the head of the instance
        if self.is_empty():
            other.head = self.head
        else:
            other._get_tail().successor = self.head

        # reset head
        self.head = other.head

        return self

    def extend_at_tail(self, other):
        """Extends instance by appending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        # define the new head/successor of tail to be the head of the
        # other linked list
        if self.is_empty():
            self.head = other.head
        else:
            self._get_tail().successor = other.head

        return self

    extend = extend_at_tail

    def pop(self, index=0):
        """Removes and returns item at index (default 0)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty linked list.')

        node, predecessor = self._get_node_with_predecessor(index)

        # remove node
        if predecessor is None:
            self.head = self.head.successor
        else:
            predecessor.successor = node.successor

        return node.value

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty linked list.')

        # traverse instance until value is found, then remove node
        previous_node = None
        current_node = self.head
        while current_node:
            if current_node.value == value:
                if previous_node is None:
                    self.head = self.head.successor
                else:
                    previous_node.successor = current_node.successor
                return

            previous_node = current_node
            current_node = current_node.successor

        raise ValueError('{} is not in linked list.'.format(repr(value)))

    remove = remove_first
