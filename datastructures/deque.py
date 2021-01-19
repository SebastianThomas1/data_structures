# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod

# copying objects
from copy import copy

# representations of objects
from reprlib import repr

# custom modules
from datastructures.base import PredictableIterable, Collection, \
    CollectionWithReferences
from datastructures.node import DoublyLinkedNode


__all__ = ['ArrayDeque', 'Deque', 'FRONT', 'LinkedDeque', 'REAR']


REAR = 'rear'
FRONT = 'front'


class Deque(PredictableIterable, Collection, CollectionWithReferences):
    """Abstract base class for the abstract data type deque.

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, enqueue_rear, enqueue_front, dequeue_rear and dequeue_front."""

    __slots__ = ()

    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()

        for value in values:
            self.enqueue_rear(value)

        return self

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self).from_iterable(self)
        return copy_of_self

    def __repr__(self):
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        # determine values of first seven nodes (at most)
        first_values = []
        for value in self:
            first_values.append(value)
            if len(first_values) == 7:
                break

        return '{}({})'.format(type(self).__name__, repr(first_values))

    def __str__(self):
        """Returns a user-friendly string representation of this instance,
        which may be used for printing."""
        return ' '.join(str(value) for value in self)

    def __contains__(self, value):
        """Checks whether the given value is contained in this instance."""
        return Collection.__contains__(self, value)

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

    @staticmethod
    def _validate_key(key):
        """Validates that key is REAR or FRONT."""
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

    __slots__ = '_values',

    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        return self

    def __init__(self):
        """Initializes instance."""
        self._values = []

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        return iter(self._values)

    def __len__(self):
        """Returns the number of values in this instance."""
        return len(self._values)

    def __repr__(self):
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        return '{}({})'.format(type(self).__name__, repr(self._values))

    def __contains__(self, value):
        """Checks whether the given value is contained in this instance."""
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

    def __iadd__(self, values):
        """Enqueues values on the rear of this instance."""
        self._validate_iterability(values)

        self._values += values

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

    __slots__ = '_front', '_rear', '_len'

    class Node(DoublyLinkedNode):
        """Internal node class for a linked deque."""
        pass

    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()

        if values:
            iterator = iter(values)

            self._front = self.Node(next(iterator))
            self._len += 1

            current_node = self._front
            for value in iterator:
                current_node.successor = self.Node(value,
                                                   predecessor=current_node)
                current_node = current_node.successor
                self._len += 1

            self._rear = current_node

        return self

    def __init__(self):
        """Initializes instance."""
        self._front = None
        self._rear = None
        self._len = 0

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()

        if self:
            iterator = iter(self)

            copy_of_self._front = copy_of_self.Node(next(iterator))

            current_node = copy_of_self._front
            for value in iterator:
                current_node.successor \
                    = copy_of_self.Node(value, predecessor=current_node)
                current_node = current_node.successor

            copy_of_self._rear = current_node

        copy_of_self._len = len(self)

        return copy_of_self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        current_node = self._front
        while current_node:
            yield current_node.value
            current_node = current_node.successor

    def __len__(self):
        """Returns the number of values in this instance."""
        return self._len

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
        """Checks whether this instance is empty."""
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
