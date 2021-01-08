# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# copying objects
from copy import copy

# representations of objects
from reprlib import repr as reprlib_repr

# custom modules
from datastructures.base import PredictableIterMixin, Collection, \
    CollectionWithReferences
from datastructures.node import DoublyLinkedNode


__all__ = ['ArrayDeque', 'Deque', 'FRONT', 'LinkedDeque', 'REAR']


REAR = 'rear'
FRONT = 'front'


class Deque(PredictableIterMixin, CollectionWithReferences, Collection):
    """Abstract base class for the abstract data type deque.

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, enqueue_rear, enqueue_front, dequeue_rear and dequeue_front."""

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __getitem__(self, key):
        """Returns the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)

        return self.peek_rear() if key is REAR else self.peek_front()

    def __setitem__(self, key, value):
        """Updates the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)

        if key is REAR:
            self.dequeue_rear()
            self.enqueue_rear(value)
        else:  # key is FRONT
            self.dequeue_front()
            self.enqueue_front(value)

    def __delitem__(self, key):
        """Deletes the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self.pop(key)

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.enqueue_rear(value)

        return self

    @staticmethod
    def _validate_key(key):
        """Checks whether key is REAR or FRONT."""
        if key is not REAR and key is not FRONT:
            raise KeyError('key must be REAR or FRONT')

    def get(self):
        """Alias to __getitem__(FRONT): returns the value at the front of this
        instance."""
        return self.peek_front()

    def peek_rear(self):
        """Alias to __getitem__(REAR): returns the value at the rear of this
        instance."""
        self._validate_non_emptiness()

        value = self.dequeue_rear()
        self.enqueue_rear(value)

        return value

    def peek_front(self):
        """Alias to __getitem__(FRONT): returns the value at the front of this
        instance."""
        self._validate_non_emptiness()

        value = self.dequeue_front()
        self.enqueue_front(value)

        return value

    def insert(self, key, value):
        """Inserts the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)

        if key is REAR:
            self.enqueue_rear(value)
        else:  # key is FRONT
            self.enqueue_front(value)

    def post(self, value):
        """Alias to insert(REAR, value): posts the value to this instance
        and places it at the rear."""
        self.enqueue_rear(value)

    @abstractmethod
    def enqueue_rear(self, value):
        """Alias to insert(REAR, value): enqueues the value on the rear of
        this instance."""
        raise NotImplementedError

    @abstractmethod
    def enqueue_front(self, value):
        """Alias to insert(FRONT, value): enqueues the value on the front of
        this instance."""
        raise NotImplementedError

    def delete(self):
        """Alias to __delitem__(FRONT): deletes the value on the front of this
        instance."""
        self.dequeue_front()

    def pop(self, key):
        """Removes and returns the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)

        if key is REAR:
            return self.dequeue_rear()
        else:  # key is FRONT
            return self.dequeue_front()

    @abstractmethod
    def dequeue_rear(self):
        """Alias to pop(REAR): dequeues the value at the rear of this
        instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    @abstractmethod
    def dequeue_front(self):
        """Alias to pop(FRONT): dequeues the value at the front of this
        instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class ArrayDeque(Deque):
    """Class that implements a deque based on an internal dynamic array (python
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

    def __setitem__(self, key, value):
        """Updates the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)
        self._validate_non_emptiness()

        if key is REAR:
            self._values[-1] = value
        else:  # key is FRONT
            self._values[0] = value

    def __delitem__(self, key):
        """Deletes the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)
        self._validate_non_emptiness()

        if key is REAR:
            del self._values[-1]
        else:  # key is FRONT
            del self._values[0]

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        self._values += other

        return self

    def is_empty(self):
        """Checks whether this instance is empty."""
        return not bool(self._values)

    def peek_rear(self):
        """Returns item at rear of the deque."""
        self._validate_non_emptiness()

        return self._values[-1]

    def peek_front(self):
        """Returns item at front of the deque."""
        self._validate_non_emptiness()

        return self._values[0]

    def enqueue_rear(self, value):
        """Alias to insert(REAR, value): enqueues the value on the rear of
        this instance."""
        self._values.append(value)

    def enqueue_front(self, value):
        """Alias to insert(FRONT, value): enqueues the value on the front of
        this instance."""
        self._values.insert(0, value)

    def clear(self):
        """Removes all items."""
        self._values.clear()

    def dequeue_rear(self):
        """Alias to pop(REAR): dequeues the value at the rear of this
        instance."""
        self._validate_non_emptiness()

        return self._values.pop()

    def dequeue_front(self):
        """Alias to pop(FRONT): dequeues the value at the front of this
        instance."""
        self._validate_non_emptiness()

        return self._values.pop(0)


class LinkedDeque(Deque):
    """Class that implements a deque based on linked nodes."""

    class Node(DoublyLinkedNode):
        """Internal node class for a linked deque."""
        pass

    def __init__(self):
        self._front = None
        self._rear = None
        self._len = 0

    def __copy__(self):
        copy_of_self = type(self)()

        if self:
            iterator = iter(self)

            copy_of_self._front = self.Node(next(iterator))

            current_node = copy_of_self._front
            for value in iterator:
                current_node.successor \
                    = copy_of_self.Node(value, predecessor=current_node)
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

    def __setitem__(self, key, value):
        """Updates the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)

        del self[key]
        if key is REAR:
            self.enqueue_rear(value)
        else:  # key is FRONT
            self.enqueue_front(value)

    def __delitem__(self, key):
        """Deletes the value on one end of this instance.

        The parameter key must be REAR or FRONT."""
        self._validate_key(key)
        self._validate_non_emptiness()

        if self._rear is self._front:
            self._rear = None
            self._front = None
        elif key is REAR:
            self._rear = self._rear.predecessor
            self._rear.successor = None
        else:  # key is FRONT:
            self._front = self._front.successor
            self._front.predecessor = None

        self._len -= 1

    def is_empty(self):
        return self._front is None

    def peek_rear(self):
        """Alias to __getitem__(REAR): returns the value at the rear of this
        instance."""
        self._validate_non_emptiness()

        return self._rear.value

    def peek_front(self):
        """Alias to __getitem__(FRONT): returns the value at the front of this
        instance."""
        self._validate_non_emptiness()

        return self._front.value

    def enqueue_rear(self, value):
        """Alias to insert(REAR, value): enqueues the value on the rear of
        this instance."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._rear.successor = self.Node(value, predecessor=self._rear)
            self._rear = self._rear.successor

        self._len += 1

    def enqueue_front(self, value):
        """Alias to insert(FRONT, value): enqueues the value on the front of
        this instance."""
        if self.is_empty():
            self._rear = self.Node(value)
            self._front = self._rear
        else:
            self._front.predecessor = self.Node(value, successor=self._front)
            self._front = self._front.predecessor

        self._len += 1

    def clear(self):
        """Removes all values."""
        self._front = None
        self._rear = None
        self._len = 0

    def dequeue_rear(self):
        """Alias to pop(REAR): dequeues the value at the rear of this
        instance."""
        self._validate_non_emptiness()

        value = self._rear.value
        if self._rear.predecessor:
            self._rear = self._rear.predecessor
            self._rear.successor = None
        else:
            self._rear = None
            self._front = None

        self._len -= 1

        return value

    def dequeue_front(self):
        """Alias to pop(FRONT): dequeues the value at the front of this
        instance."""
        self._validate_non_emptiness()

        value = self._front.value
        if self._front.successor:
            self._front = self._front.successor
            self._front.predecessor = None
        else:
            self._rear = None
            self._front = None

        self._len -= 1

        return value
