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
                current_node.successor = self.Node(value)
                current_node = current_node.successor
                self._len += 1

            self.tail = current_node
        else:
            self.head = None
            self.tail = None

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

        self.head, self.tail = self.tail, self.head

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

            if node.successor is None:  # ie node is self.tail
                self.tail = predecessor
            self._len -= 1
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
               and  # current_node_self.value is current_node_other.value
               # or
               current_node_self.value == current_node_other.value):
            current_node_self = current_node_self.successor
            current_node_other = current_node_other.successor

        return (current_node_self is current_node_other
                or current_node_self == current_node_other)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only concatenate linked list to linked '
                            'list.')

        result = self.__class__(self)
        result += other

        return result

    def __iadd__(self, other):
        return self.extend_by_appending(other)

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
        return self * other

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

    def is_empty(self):
        """Checks whether this instance is the empty linked list."""
        return self.head is None

    def index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty linked list.')

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

        raise ValueError('{} is not in linked list resp. '
                         'slice.'.format(repr(value)))

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        node.successor = self.Node(value, successor=node.successor)

        if node is self.tail:
            self.tail = self.tail.successor
        self._len += 1

    def insert_before(self, index, value):
        """Inserts value before index."""
        node, predecessor = self._get_node_with_predecessor(index)

        if node is self.head:
            self.head = self.Node(value, successor=self.head)
        else:
            predecessor.successor = self.Node(value, successor=node)

        self._len += 1

    insert = insert_before

    def prepend(self, value):
        """Prepends an item to this instance."""
        self.head = self.Node(value, successor=self.head)

        if self.tail is None:
            self.tail = self.head
        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.tail = self.head
        else:
            self.tail.successor = self.Node(value)
            self.tail = self.tail.successor

        self._len += 1

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

        self.head, self.tail = self.tail, self.head

    def extend_by_prepending(self, other):
        """Extends instance by prepending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        if self.is_empty():
            self.tail = other.tail

        # extend
        other.tail.successor = self.head

        self.head = other.head
        self._len += len(other)

        return self

    def extend_by_appending(self, other):
        """Extends instance by appending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        # extend
        if self.is_empty():
            self.head = other.head
        else:
            self.tail.successor = other.head

        self.tail = other.tail
        self._len += len(other)

        return self

    extend = extend_by_appending

    def pop(self, index=0):
        """Removes and returns item at index (default 0)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty linked list.')

        node, predecessor = self._get_node_with_predecessor(index)

        # remove node
        if predecessor is None:  # ie node is self.head
            self.head = self.head.successor
        else:
            predecessor.successor = node.successor

        if node is self.tail:
            self.tail = predecessor

        self._len -= 1

        return node.value

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty linked list.')

        # traverse instance until value is found, then remove node
        previous_node = None
        current_node = self.head
        while current_node:
            if current_node.value is value or current_node.value == value:
                if previous_node is None:  # ie node is self.head
                    self.head = self.head.successor
                else:
                    previous_node.successor = current_node.successor

                if current_node is self.tail:
                    self.tail = previous_node
                self._len -= 1

                return

            previous_node = current_node
            current_node = current_node.successor

        raise ValueError('{} is not in linked list.'.format(repr(value)))

    remove = remove_first

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty linked list.')

        # traverse instance until value is found, remember node and
        # predecessor, after traversal remove remembered node
        predecessor = None
        node = None

        previous_node = None
        current_node = self.head
        while current_node:
            if current_node.value is value or current_node.value == value:
                predecessor = previous_node
                node = current_node

            previous_node = current_node
            current_node = current_node.successor

        if node:
            if predecessor is None:  # ie node is self.head
                self.head = self.head.successor
            else:
                predecessor.successor = node.successor

            if node is self.tail:
                self.tail = predecessor
            self._len -= 1
        else:
            raise ValueError('{} is not in linked list.'.format(repr(value)))


class CircularLinkedList(MutableSequence):
    """Class that implements (singly) circular linked lists."""

    class Node:
        """Internal node class for (singly) circular linked lists."""

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
                current_node.successor = self.Node(value)
                current_node = current_node.successor
                self._len += 1

            current_node.successor = self.head
        else:
            self.head = None

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        # traverse instance, meanwhile yield values
        if self.head:
            current_node = self.head
            while True:
                yield current_node.value
                current_node = current_node.successor
                if current_node is self.head:
                    break

    def __reversed__(self):
        if self.is_empty():
            return

        # reverse instance
        self.reverse()

        # reverse reversed instance, while traversing, yield values
        yield self.head.value

        predecessor_of_head = None

        previous_node = self.head
        current_node = self.head.successor
        previous_node.successor = None

        while current_node is not self.head:
            yield current_node.value
            next_node = current_node.successor
            if next_node is self.head:
                predecessor_of_head = current_node
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node

        self.head.successor = predecessor_of_head
        self.head = predecessor_of_head

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._get_node(key).value
        elif isinstance(key, slice):
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
                raise IndexError('Can\'t delete from empty circular linked '
                                 'list.')

            # delete node
            if self.head.successor is self.head:  # length 1
                self.head = None
            else:
                node, predecessor = self._get_node_with_predecessor(key)

                predecessor.successor = node.successor
                if node is self.head:
                    self.head = self.head.successor

            self._len -= 1
        elif isinstance(key, slice):
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __len__(self):
        return self._len

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.is_empty():
            return other.is_empty()
        if other.is_empty():
            return False  # self.is_empty() is False

        # traverse instance and other linked list in parallel while
        # checking for equality
        current_node_self = self.head
        current_node_other = other.head
        while True:
            if (current_node_self.value is current_node_other.value
                    or current_node_self.value == current_node_other.value):
                current_node_self = current_node_self.successor
                current_node_other = current_node_other.successor
            else:
                return False
            if current_node_self is self.head:
                return current_node_other is other.head
            if current_node_other is other.head:
                return False  # current_node_self is not self.head

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only concatenate circular linked list to '
                            'circular linked list.')

        result = self.__class__(self)
        result += other

        return result

    def __iadd__(self, other):
        return self.extend_by_appending(other)

    def __mul__(self, other):
        result = self.__class__(self)
        result *= other

        return result

    def __imul__(self, other):
        if not isinstance(other, Integral):
            raise TypeError('Can\'t multiply circular linked list by '
                            'non-integer of type \'{}\'.'
                            .format(type(other).__name__))

        if other < 0:
            raise ValueError('Can\'t multiply circular linked list by '
                             'negative integer.')

        if other == 0:
            self.head = None
        else:
            copy = self.__class__(self)
            self *= other - 1
            self += copy

        return self

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        if self.is_empty():
            return '{}([])'.format(self.__class__.__name__)

        # determine values of first seven nodes (at most)
        first_values = []
        current_node = self.head
        count = 0
        while count < 7:
            first_values.append(current_node.value)
            current_node = current_node.successor
            count += 1
            if current_node is self.head:
                break

        return '{}({})'.format(self.__class__.__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        if self.is_empty():
            return ''
        else:
            return ' \u2192 '.join(str(value) for value in self) + ' \u2192'

    def _get_node(self, key):  # assume key is an integer
        """Returns node at index."""
        length = len(self)
        if length == 0:
            raise IndexError('Can\'t access node in empty circular linked '
                             'list.')

        key %= length

        # traverse instance, return current node if item at index is
        # reached
        current_node = self.head
        while True:
            if key == 0:
                return current_node
            key -= 1
            current_node = current_node.successor

    def _get_node_with_predecessor(self, key):
        """Returns node at index together with predecessor."""
        length = len(self)
        if length == 0:
            raise IndexError('Can\'t access node in empty circular linked '
                             'list.')

        key %= length
        if key == 0:
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

    @property
    def _predecessor_of_head(self):
        """Returns predecessor of instance's head."""
        if self.head is None:
            raise IndexError('Can\'t access node in empty circular linked '
                             'list.')

        # traverse instance until the next successor is the head
        current_node = self.head
        while current_node.successor is not self.head:
            current_node = current_node.successor

        return current_node

    def is_empty(self):
        """Checks whether this instance is the empty linked list."""
        return self.head is None

    def index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty circular linked '
                             'list.')

        length = len(self)
        start %= length
        if stop:
            stop %= length

        # traverse instance, beginning from node at index start, when
        # value is reached, return index
        current_node = self._get_node(start)
        idx = start
        while stop is None or idx < stop:
            if current_node.value is value or current_node.value == value:
                return idx
            current_node = current_node.successor
            idx += 1
            if current_node is self.head:
                break

        raise ValueError('{} is not in circular linked list resp. slice.'
                         .format(repr(value)))

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        node.successor = self.Node(value, successor=node.successor)

        self._len += 1

    def insert_before(self, index, value):
        """Inserts value before index."""
        node, predecessor = self._get_node_with_predecessor(index)

        predecessor.successor = self.Node(value, successor=node)
        if node is self.head:
            self.head = predecessor.successor

        self._len += 1

    insert = insert_before

    def prepend(self, value):
        """Prepends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.head.successor = self.head
        else:
            predecessor_of_head = self._predecessor_of_head
            self.head = self.Node(value, successor=self.head)
            predecessor_of_head.successor = self.head

        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.head.successor = self.head
        else:
            self._predecessor_of_head.successor = self.Node(value, self.head)

        self._len += 1

    def reverse(self):
        """Reverses this instance."""
        if self.is_empty():
            return

        if self.head.successor is self.head:  # length 1
            return

        predecessor_of_head = None

        # traverse list, meanwhile set successors to former predecessors
        previous_node = self.head
        current_node = self.head.successor
        previous_node.successor = None
        while current_node is not self.head:
            next_node = current_node.successor
            if next_node is self.head:
                predecessor_of_head = current_node
            current_node.successor = previous_node
            previous_node = current_node
            current_node = next_node

        self.head.successor = predecessor_of_head
        self.head = predecessor_of_head

    def extend_by_prepending(self, other):
        """Extends instance by prepending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # extend
        if not self.is_empty():
            other._predecessor_of_head.successor = self.head
            self._predecessor_of_head.successor = other.head

        self.head = other.head
        self._len += len(other)

        return self

    def extend_by_appending(self, other):
        """Extends instance by appending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # extend
        if self.is_empty():
            self.head = other.head
        else:
            self._predecessor_of_head.successor = other.head

        other._predecessor_of_head.successor = self.head

        self._len += len(other)

        return self

    extend = extend_by_appending

    def pop(self, index=0):
        """Removes and returns item at index (default 0)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty circular linked list.')

        node, predecessor = self._get_node_with_predecessor(index)

        # remove node
        predecessor.successor = node.successor
        if self.head.successor is self.head:  # length 1
            self.head = None
        elif node is self.head:
            self.head = self.head.successor

        self._len -= 1

        return node.value

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty circular linked list.')

        # traverse instance until value is found, then remove node
        previous_node = None
        current_node = self.head
        while True:
            if current_node.value is value or current_node.value == value:
                if self.head.successor is self.head:  # length 1
                    self.head = None
                else:
                    if previous_node is None:  # ie node is self.head
                        previous_node = self._predecessor_of_head
                        self.head = self.head.successor
                    previous_node.successor = current_node.successor

                self._len -= 1

                return

            previous_node = current_node
            current_node = current_node.successor

            if current_node is self.head:
                break

        raise ValueError('{} is not in circular linked list.'.format(repr(value)))

    remove = remove_first

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty circular linked list.')

        # traverse instance until value is found, remember node and
        # predecessor, after traversal remove remembered node
        predecessor = None
        node = None

        previous_node = None
        current_node = self.head
        while True:
            if current_node.value is value or current_node.value == value:
                if previous_node is None:  # ie current_node is self.head
                    predecessor = self._predecessor_of_head
                else:
                    predecessor = previous_node
                node = current_node

            previous_node = current_node
            current_node = current_node.successor

            if current_node is self.head:
                break

        if node:
            predecessor.successor = node.successor

            if self.head.successor is self.head:  # length 1
                self.head = None
            elif node is self.head:
                self.head = self.head.successor

            self._len -= 1
        else:
            raise ValueError('{} is not in circular linked list.'.format(repr(value)))


class DoublyLinkedList(MutableSequence):
    """Class that implements doubly linked lists."""

    class Node:
        """Internal node class for doubly linked lists."""

        def __init__(self, value, predecessor=None, successor=None):
            self.value = value
            self.predecessor = predecessor
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
                current_node.successor = self.Node(value,
                                                   predecessor=current_node)
                current_node = current_node.successor
                self._len += 1

            self.tail = current_node
        else:
            self.head = None
            self.tail = None

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        # traverse instance, meanwhile yield values
        current_node = self.head
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __reversed__(self):
        # traverse instance backwards, meanwhile yield values
        current_node = self.tail
        while current_node:
            yield current_node.value
            current_node = current_node.predecessor

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._get_node(key).value
        elif isinstance(key, slice):
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
                raise IndexError('Can\'t delete from empty doubly linked list.')

            node = self._get_node(key)

            # delete node
            if node is self.head and node is self.tail:  # length 1
                self.head = None
                self.tail = None
            elif node is self.head:
                self.head = self.head.successor
                if self.head:
                    self.head.predecessor = None
            elif node is self.tail:
                self.tail = self.tail.predecessor
                if self.tail:
                    self.tail.successor = None
            else:
                predecessor = node.predecessor
                successor = node.successor
                predecessor.successor, successor.predecessor \
                    = successor, predecessor

            self._len -= 1
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
               and  # current_node_self.value is current_node_other.value
               # or
               current_node_self.value == current_node_other.value):
            current_node_self = current_node_self.successor
            current_node_other = current_node_other.successor

        return (current_node_self is current_node_other
                or current_node_self == current_node_other)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only concatenate doubly linked list to '
                            'doubly linked list.')

        result = self.__class__(self)
        result += other

        return result

    def __iadd__(self, other):
        return self.extend(other)

    def __mul__(self, other):
        result = self.__class__(self)
        result *= other

        return result

    def __imul__(self, other):
        if not isinstance(other, Integral):
            raise TypeError(
                'Can\'t multiply doubly linked list by non-integer of '
                'type \'{}\'.'.format(type(other).__name__))

        if other < 0:
            raise ValueError('Can\'t multiply doubly linked list by negative '
                             'integer.')

        if other == 0:
            self.head = None
        else:
            copy = self.__class__(self)
            self *= other - 1
            self += copy

        return self

    def __rmul__(self, other):
        return self * other

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
        return ' \u21c4 '.join(str(value) for value in self)

    def _get_node(self, key):
        """Returns node at index."""
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

        # traverse instance, return current node if item at index is
        # reached
        if key >= 0:
            # traverse instance forwards, beginning from head
            current_node = self.head
            while current_node:
                if key == 0:
                    return current_node
                key -= 1
                current_node = current_node.successor
        else:
            # traverse instance backwards, beginning from tail
            current_node = self.tail
            while current_node:
                if key == -1:
                    return current_node
                key += 1
                current_node = current_node.predecessor

    def is_empty(self):
        """Checks whether this instance is the empty doubly linked list."""
        return self.head is None

    def index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty doubly linked list.')

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

        raise ValueError(
            '{} is not in doubly linked list.'.format(repr(value)))

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        node.successor = self.Node(value, predecessor=node,
                                   successor=node.successor)
        if node.successor.successor:
            node.successor.successor.predecessor = node.successor
        if node is self.tail:
            self.tail = node.successor
        self._len += 1

    def insert_before(self, index, value):
        """Inserts value before index."""
        node = self._get_node(index)
        node.predecessor = self.Node(value, predecessor=node.predecessor,
                                     successor=node)
        if node.predecessor.predecessor:
            node.predecessor.predecessor.successor = node.predecessor
        if node is self.head:
            self.head = node.predecessor
        self._len += 1

    insert = insert_before

    def prepend(self, value):
        """Prepends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.tail = self.head
        else:
            self.head = self.Node(value, predecessor=None, successor=self.head)
            self.head.successor.predecessor = self.head

        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.tail = self.head
        else:
            self.tail = self.Node(value, predecessor=self.tail, successor=None)
            self.tail.predecessor.successor = self.tail

        self._len += 1

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

        self.head, self.tail = self.tail, self.head

    def extend_by_prepending(self, other):
        """Extends instance by prepending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to doubly linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # define the new tail/predecessor of head to be the tail of the
        # other doubly linked list
        if self.is_empty():
            self.tail = other.tail
        else:
            self.head.predecessor = other.tail
            other.tail.successor = self.head

        self.head = other.head

        self._len += len(other)

        return self

    def extend_by_appending(self, other):
        """Extends instance by appending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to doubly linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # define the new head/successor of tail to be the head of the
        # other doubly linked list
        if self.is_empty():
            self.head = other.head
        else:
            self.tail.successor = other.head
            other.head.predecessor = self.tail

        self.tail = other.tail

        self._len += len(other)

        return self

    extend = extend_by_appending

    def pop(self, index=-1):
        """Removes and returns item at index (default -1)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty doubly linked list.')

        node = self._get_node(index)

        # remove node
        if node is self.head and node is self.tail:
            self.head = None
            self.tail = None
        elif node is self.head:
            self.head = self.head.successor
            self.head.predecessor = None
        elif node is self.tail:
            self.tail = self.tail.predecessor
            self.tail.successor = None
        else:
            predecessor = node.predecessor
            successor = node.successor
            predecessor.successor, successor.predecessor \
                = successor, predecessor

        self._len -= 1

        return node.value

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty doubly linked list.')

        # traverse instance until value is found, then remove node
        current_node = self.head
        while current_node:
            if current_node.value is value or current_node.value == value:
                if current_node is self.head and current_node is self.tail:
                    self.head = None
                    self.tail = None
                elif current_node is self.head:
                    self.head = self.head.successor
                    if self.head:
                        self.head.predecessor = None
                elif current_node is self.tail:
                    self.tail = self.tail.predecessor
                    if self.tail:
                        self.tail.successor = None
                else:
                    predecessor = current_node.predecessor
                    successor = current_node.successor
                    predecessor.successor, successor.predecessor \
                        = successor, predecessor

                self._len -= 1

                return

            current_node = current_node.successor

        raise ValueError(
            '{} is not in doubly linked list.'.format(repr(value)))

    remove = remove_first

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty doubly linked list.')

        # traverse instance backwards until value is found, then remove node
        current_node = self.tail
        while current_node:
            if current_node.value is value or current_node.value == value:
                if current_node is self.head and current_node is self.tail:
                    self.head = None
                    self.tail = None
                elif current_node is self.tail:
                    self.tail = self.tail.predecessor
                    if self.tail:
                        self.tail.successor = None
                elif current_node is self.head:
                    self.head = self.head.successor
                    if self.head:
                        self.head.predecessor = None
                else:
                    predecessor = current_node.predecessor
                    successor = current_node.successor
                    predecessor.successor, successor.predecessor \
                        = successor, predecessor

                self._len -= 1

                return

            current_node = current_node.predecessor

        raise ValueError(
            '{} is not in doubly linked list.'.format(repr(value)))


class CircularDoublyLinkedList(MutableSequence):
    """Class that implements circular doubly linked lists."""

    class Node:
        """Internal node class for circular doubly linked lists."""

        def __init__(self, value, predecessor=None, successor=None):
            self.value = value
            self.predecessor = predecessor
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
                current_node.successor = self.Node(value,
                                                   predecessor=current_node)
                current_node = current_node.successor
                self._len += 1

            current_node.successor = self.head
            self.head.predecessor = current_node
        else:
            self.head = None

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        # traverse instance, meanwhile yield values
        if self.head:
            current_node = self.head
            while True:
                yield current_node.value
                current_node = current_node.successor
                if current_node is self.head:
                    break

    def __reversed__(self):
        # traverse instance backwards, meanwhile yield values
        if self.head:
            current_node = self.head.predecessor
            while True:
                yield current_node.value
                current_node = current_node.predecessor
                if current_node is self.head.predecessor:
                    break

    def __getitem__(self, key):
        if isinstance(key, Integral):
            return self._get_node(key).value
        elif isinstance(key, slice):
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
                raise IndexError('Can\'t delete from empty circular doubly '
                                 'linked list.')

            # delete node
            if self.head.successor is self.head:  # length 1
                self.head = None
            else:
                node = self._get_node(key)

                predecessor = node.predecessor
                successor = node.successor
                predecessor.successor, successor.predecessor \
                    = successor, predecessor
                if node is self.head:
                    self.head = self.head.successor

            self._len -= 1
        elif isinstance(key, slice):
            raise NotImplementedError('Access by slices not yet implemented.')
        else:
            raise TypeError('Indices must be integers or slices.')

    def __len__(self):
        return self._len

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.is_empty():
            return other.is_empty()
        if other.is_empty():
            return False  # self.is_empty() is False

        # traverse instance and other linked list in parallel while
        # checking for equality
        current_node_self = self.head
        current_node_other = other.head
        while True:
            if (current_node_self.value is current_node_other.value
                    or current_node_self.value == current_node_other.value):
                current_node_self = current_node_self.successor
                current_node_other = current_node_other.successor
            else:
                return False
            if current_node_self is self.head:
                return current_node_other is other.head
            if current_node_other is other.head:
                return False  # current_node_self is not self.head

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only concatenate circular doubly linked list '
                            'to circular doubly linked list.')

        result = self.__class__(self)
        result += other

        return result

    def __iadd__(self, other):
        return self.extend(other)

    def __mul__(self, other):
        result = self.__class__(self)
        result *= other

        return result

    def __imul__(self, other):
        if not isinstance(other, Integral):
            raise TypeError(
                'Can\'t multiply circular doubly linked list by non-integer '
                'of type \'{}\'.'.format(type(other).__name__))

        if other < 0:
            raise ValueError('Can\'t multiply circular doubly linked list by '
                             'negative integer.')

        if other == 0:
            self.head = None
        else:
            copy = self.__class__(self)
            self *= other - 1
            self += copy

        return self

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        if self.is_empty():
            return '{}([])'.format(self.__class__.__name__)

        # determine values of first seven nodes (at most)
        first_values = []
        current_node = self.head
        count = 0
        while count < 7:
            first_values.append(current_node.value)
            current_node = current_node.successor
            count += 1
            if current_node is self.head:
                break

        return '{}({})'.format(self.__class__.__name__,
                               reprlib_repr(first_values))

    def __str__(self):
        if self.is_empty():
            return ''
        else:
            return ' \u21c4 '.join(str(value) for value in self) + ' \u21c4'

    def _get_node(self, key):
        """Returns node at index."""
        length = len(self)
        if length == 0:
            raise IndexError('Can\'t access node in empty circular doubly '
                             'linked list.')

        # cast key from Integral to int (so that >=, etc. are defined)
        key = int(key)

        key %= length

        # prepare key for efficient traverse
        if key >= length // 2:
            key -= length
        if key < -length // 2:
            key += length

        # traverse instance, return current node if item at index is
        # reached
        current_node = self.head
        while current_node:
            if key == 0:
                return current_node
            elif key > 0:
                # traverse instance forwards
                key -= 1
                current_node = current_node.successor
            else:
                # traverse instance backwards
                key += 1
                current_node = current_node.predecessor

    def is_empty(self):
        """Checks whether this instance is the empty doubly linked list."""
        return self.head is None

    def index(self, value, start=0, stop=None):
        """Returns first index of value."""
        if self.is_empty():
            raise ValueError('Can\'t find value in empty circular doubly '
                             'linked list.')

        length = len(self)
        start %= length
        if stop:
            stop %= length

        # traverse instance, beginning from node at index start, when
        # value is reached, return index
        current_node = self._get_node(start)
        idx = start
        while stop is None or idx < stop:
            if current_node.value is value or current_node.value == value:
                return idx
            current_node = current_node.successor
            idx += 1
            if current_node is self.head:
                break

        raise ValueError('{} is not in circular doubly linked list resp. '
                         'slice.'.format(repr(value)))

    def insert_after(self, index, value):
        """Inserts value after index."""
        node = self._get_node(index)
        node.successor = self.Node(value, predecessor=node,
                                   successor=node.successor)
        node.successor.successor.predecessor = node.successor
        self._len += 1

    def insert_before(self, index, value):
        """Inserts value before index."""
        node = self._get_node(index)
        node.predecessor = self.Node(value, predecessor=node.predecessor,
                                     successor=node)
        node.predecessor.predecessor.successor = node.predecessor
        if node is self.head:
            self.head = node.predecessor
        self._len += 1

    insert = insert_before

    def prepend(self, value):
        """Prepends an item to this instance."""
        if self.is_empty():
            self.head = self.Node(value)
            self.head.predecessor = self.head
            self.head.successor = self.head
        else:
            self.head = self.Node(value, predecessor=self.head.predecessor,
                                  successor=self.head)
            self.head.predecessor.successor = self.head
            self.head.successor.predecessor = self.head

        self._len += 1

    def append(self, value):
        """Appends an item to this instance."""
        self.prepend(value)
        self.head = self.head.successor

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

        self.head = self.head.successor

    def extend_by_prepending(self, other):
        """Extends instance by prepending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to doubly linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # define the new tail/predecessor of head to be the tail of the
        # other doubly linked list
        if not self.is_empty():
            other.head.predecessor.successor = self.head
            self.head.predecessor.successor = other.head
            self.head.predecessor, other.head.predecessor \
                = other.head.predecessor, self.head.predecessor

        self.head = other.head

        self._len += len(other)

        return self

    def extend_by_appending(self, other):
        """Extends instance by appending elements from iterable other."""
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        # convert/copy other to doubly linked list
        other = self.__class__(other)

        if other.is_empty():
            return self

        # define the new head/successor of tail to be the head of the
        # other doubly linked list
        if self.is_empty():
            self.head = other.head
        else:
            self.head.predecessor.successor = other.head
            other.head.predecessor.successor = self.head
            self.head.predecessor, other.head.predecessor \
                = other.head.predecessor, self.head.predecessor

        self._len += len(other)

        return self

    extend = extend_by_appending

    def pop(self, index=-1):
        """Removes and returns item at index (default -1)."""
        if self.is_empty():
            raise IndexError('Can\'t pop from empty doubly linked list.')

        node = self._get_node(index)

        # remove node
        if self.head.successor is self.head:  # length 1
            self.head = None
        else:
            if node is self.head:
                self.head = self.head.successor
            node.predecessor.successor = node.successor
            node.successor.predecessor = node.predecessor

        self._len -= 1

        return node.value

    def remove_first(self, value):
        """Removes first occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty circular doubly linked '
                             'list.')

        # traverse instance until value is found, then remove node
        current_node = self.head
        while True:
            if current_node.value is value or current_node.value == value:
                if self.head.successor is self.head: # length 1
                    self.head = None
                else:
                    predecessor = current_node.predecessor
                    successor = current_node.successor
                    predecessor.successor, successor.predecessor \
                        = successor, predecessor
                    if current_node is self.head:
                        self.head = successor

                self._len -= 1

                return

            current_node = current_node.successor

            if current_node is self.head:
                break

        raise ValueError(
            '{} is not in circular doubly linked list.'.format(repr(value)))

    remove = remove_first

    def remove_last(self, value):
        """Removes last occurrence of value."""
        if self.is_empty():
            raise ValueError('Can\'t remove from empty circular doubly linked '
                             'list.')

        # traverse instance until value is found, then remove node
        current_node = self.head.predecessor
        while True:
            if current_node.value is value or current_node.value == value:
                if self.head.successor is self.head:  # length 1
                    self.head = None
                else:
                    predecessor = current_node.predecessor
                    successor = current_node.successor
                    predecessor.successor, successor.predecessor \
                        = successor, predecessor
                    if current_node is self.head:
                        self.head = successor

                self._len -= 1

                return

            current_node = current_node.predecessor

            if current_node is self.head.predecessor:
                break

        raise ValueError(
            '{} is not in circular doubly linked list.'.format(repr(value)))
