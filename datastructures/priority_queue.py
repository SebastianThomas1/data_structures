# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod, ABCMeta
from collections.abc import Iterable

# representations of objects
from reprlib import repr as reprlib_repr

# sorting
from bisect import insort

# custom modules
from datastructures.base import Collection


__all__ = ['MAX', 'MaxPriorityQueue', 'ArrayMaxPriorityQueue']


MAX = 'max'


class PriorityQueue(Collection):
    """Abstract base class for the abstract data type priority queue.

    Concrete subclasses must provide: __new__ or __init__,
    predictable __iter__, peek, enqueue, delete."""

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __getitem__(self, key):
        """Returns the optimal value of this instance."""
        self._validate_key(key)

        return self.peek()

    def __delitem__(self, key):
        """Deletes the largest value of this instance.

        The parameter key must be MAX."""
        self._validate_key(key)

        self.delete()

    def _validate_comparability(self, value):
        if not self.is_empty():
            _ = self.peek() < value

    @staticmethod
    @abstractmethod
    def _validate_key(key):
        raise NotImplementedError

    def get(self):
        """Returns the optimal value of this instance."""
        return self.peek()

    @abstractmethod
    def peek(self):
        """Alias to get: returns the optimal value of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def post(self, value):
        """Posts the value to this instance."""
        self.enqueue(value)

    @abstractmethod
    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """Deletes the optimal value of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def pop(self, key):
        """Removes and returns the optimal value of this instance."""
        self._validate_key(key)

        return self.dequeue()

    def dequeue(self):
        """Alias to pop(MAX): dequeues the optimal value of this instance."""
        value = self.peek()
        self.delete()

        return value


class MaxPriorityQueue(PriorityQueue, metaclass=ABCMeta):
    """Abstract base class for the abstract data type max priority queue.

    Concrete subclasses must provide: __new__ or __init__,
    predictable __iter__, peek, enqueue, delete."""  # XXX ok?

    def __getitem__(self, key):
        """Returns the largest value of this instance.

        The parameter key must be MAX."""
        return super().__getitem__(key)

    def __delitem__(self, key):
        """Deletes the largest value of this instance.

        The parameter key must be MAX."""
        super().__delitem__(key)

    @staticmethod
    def _validate_key(key):
        """Checks whether key is MAX."""
        if key is not MAX:
            raise KeyError('key must be MAX')

    def pop(self, key=MAX):
        """Removes and returns the largest value of this instance.

        The parameter key must be MAX (default)."""
        return super().pop(key)


class ArrayMaxPriorityQueue(MaxPriorityQueue):
    """Class that implements a max priority queue based on an internal dynamic
    array (python list)."""

    def __init__(self):
        self._values = []

    def __iter__(self):
        return iter(sorted(self._values, reverse=True))

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        # determine seven largest values (at most)
        largest_values = []
        for value in self._values[:7]:
            insort(largest_values, value)

        for value in self._values[7:]:
            if value > largest_values[0]:
                insort(largest_values, value)
                del largest_values[0]

        largest_values.reverse()

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(largest_values))

    def __contains__(self, value):
        return value in self._values

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self._validate_comparability(value)

        self._values += other

        return self

    def is_empty(self):
        """Checks whether this instance is an empty max priority queue."""
        return not bool(self._values)

    def peek(self):
        """Alias to get: returns the largest value of this instance."""
        self._validate_non_emptiness()

        return max(self._values)

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        self._values.append(value)

    def delete(self):
        """Deletes the largest value of this instance."""
        self._validate_non_emptiness()

        idx_of_max = max(range(len(self._values)),
                         key=self._values.__getitem__)

        del self._values[idx_of_max]

    def clear(self):
        """Removes all items."""
        self._values.clear()

    def dequeue(self):
        """Alias to pop(MAX): dequeues the maximal value of this instance."""
        self._validate_non_emptiness()

        idx_of_max = max(range(len(self._values)),
                         key=self._values.__getitem__)
        value = self._values[idx_of_max]
        del self._values[idx_of_max]

        return value
