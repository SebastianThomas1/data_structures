# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod
from collections.abc import Iterable

# representations of objects
from reprlib import repr as reprlib_repr

# sorting
from bisect import insort

# custom modules
from datastructures.base import Collection


__all__ = ['ArrayMaxPriorityQueue', 'ArrayMinPriorityQueue',
           'ArrayPriorityQueue', 'MAX', 'MIN', 'OrderedArrayPriorityQueue',
           'OrderedArrayMaxPriorityQueue', 'OrderedArrayMinPriorityQueue',
           'PriorityQueue',
           ]


MIN = 'min'
MAX = 'max'


# Source: https://stackoverflow.com/a/2247433/10816965
def reverse_insort(a, x, lo=0, hi=None):
    """Insert item x in list a, and keep it reverse-sorted assuming a
    is reverse-sorted.
    If x is already in a, insert it to the right of the rightmost x.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched."""
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x > a[mid]:
            hi = mid
        else:
            lo = mid + 1
    a.insert(lo, x)


class PriorityQueue(Collection):
    """Abstract base class for the abstract data type priority queue.

    Concrete subclasses must call __init__ of super class and provide
    predictable __iter__, peek, enqueue, delete."""

    def __init__(self, extreme_key):
        self._validate_extreme_key(extreme_key)

        self._extreme_key = extreme_key

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, type(self)):
            return False

        if self._extreme_key != other._extreme_key:
            return False

        # iterate over instance and other in parallel while checking for
        # equality
        values_of_self = iter(self)
        values_of_other = iter(other)

        while True:
            try:
                value_of_self = next(values_of_self)
            except StopIteration:  # values_of_self exhausted
                try:
                    next(values_of_other)
                except StopIteration:  # values_of_other exhausted
                    return True
                else:  # values_of_other not exhausted
                    return False

            try:
                value_of_other = next(values_of_other)
            except StopIteration:  # values_of_other exhausted
                return False

            if value_of_self != value_of_other:
                return False

    def __copy__(self):
        copy_of_self = type(self)(self._extreme_key)
        copy_of_self += self
        return copy_of_self

    def __getitem__(self, key):
        """Returns the extreme value of this instance.

        The parameter key must be the chosen extreme key."""
        self._validate_key(key)

        return self.peek()

    def __delitem__(self, key):
        """Deletes the extreme value of this instance.

        The parameter key must be the chosen extreme key."""
        self._validate_key(key)

        self.delete()

    def _validate_comparability(self, value):
        if not self.is_empty():
            _ = self.peek() < value

    @staticmethod
    def _validate_extreme_key(extreme_key):
        """Checks whether extreme_key is MAX or MIN."""
        if extreme_key is not MAX and extreme_key is not MIN:
            raise KeyError('extreme_key must be MAX or MIN')

    def _validate_key(self, key):
        """Checks whether key is the extreme key."""
        if key is not self._extreme_key:
            raise KeyError('key must be the chosen extreme key')

    def get(self):
        """Returns the extreme value of this instance."""
        return self.peek()

    @abstractmethod
    def peek(self):
        """Alias to get: returns the extreme value of this instance."""
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
        """Deletes the extreme value of this instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def pop(self, key):
        """Removes and returns the extreme value of this instance.

        The parameter key must be the chosen extreme key."""
        self._validate_key(key)

        return self.dequeue()

    def dequeue(self):
        """Alias to pop(extreme_key): dequeues the extreme value of this
        instance."""
        value = self.peek()
        self.delete()

        return value


class ArrayPriorityQueue(PriorityQueue):
    """Class that implements a priority queue based on an internal dynamic
    array (python list)."""

    def __init__(self, extreme_key):
        super().__init__(extreme_key)
        self._values = []

    def __iter__(self):
        return iter(sorted(self._values, reverse=self._extreme_key == MAX))

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        # determine seven most extreme values (at most)
        extreme_values = []
        for value in self._values[:7]:
            insort(extreme_values, value)

        for value in self._values[7:]:
            if value > extreme_values[0]:
                insort(extreme_values, value)
                del extreme_values[0]

        if self._extreme_key == MAX:
            extreme_values.reverse()

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(extreme_values))

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

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the extreme value of this instance."""
        self._validate_non_emptiness()

        return (max(range(len(self._values)), key=self._values.__getitem__)
                if self._extreme_key == MAX
                else min(range(len(self._values)),
                         key=self._values.__getitem__))

    def is_empty(self):
        """Checks whether this instance is an empty array priority queue."""
        return not bool(self._values)

    def peek(self):
        """Alias to get: returns the extreme value of this instance."""
        self._validate_non_emptiness()

        return (max(self._values) if self._extreme_key == MAX
                else min(self._values))

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        self._values.append(value)

    def delete(self):
        """Deletes the extreme value of this instance."""
        del self._values[self._idx_of_extreme_value]

    def clear(self):
        """Removes all items."""
        self._values.clear()

    def dequeue(self):
        """Alias to pop(extreme_key): dequeues the extreme value of this
        instance."""
        idx_of_extreme_value = self._idx_of_extreme_value
        value = self._values[idx_of_extreme_value]
        del self._values[idx_of_extreme_value]

        return value


class ArrayMinPriorityQueue(ArrayPriorityQueue):
    """Class that implements a min priority queue based on an internal dynamic
    array (python list)."""

    def __init__(self):
        super().__init__(MIN)

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __iter__(self):
        return iter(sorted(self._values, reverse=False))

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the minimal value of this instance."""
        self._validate_non_emptiness()

        return min(range(len(self._values)), key=self._values.__getitem__)

    def peek(self):
        """Alias to get: returns the minimal value of this instance."""
        self._validate_non_emptiness()

        return min(self._values)


class ArrayMaxPriorityQueue(ArrayPriorityQueue):
    """Class that implements a max priority queue based on an internal dynamic
    array (python list)."""

    def __init__(self):
        super().__init__(MAX)

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def __iter__(self):
        return iter(sorted(self._values, reverse=True))

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the maximal value of this instance."""
        self._validate_non_emptiness()

        return max(range(len(self._values)), key=self._values.__getitem__)

    def peek(self):
        """Alias to get: returns the maximal value of this instance."""
        self._validate_non_emptiness()

        return max(self._values)


class OrderedArrayPriorityQueue(ArrayPriorityQueue):
    """Class that implements a priority queue based on an ordered internal
    dynamic array (python list)."""

    def __iter__(self):
        return reversed(self._values)

    def __repr__(self):
        # determine seven most extreme values (at most)
        extreme_values = self._values[-7:]
        extreme_values.reverse()

        return '{}({})'.format(type(self).__name__,
                               reprlib_repr(extreme_values))

    def __iadd__(self, other):
        return PriorityQueue.__iadd__(self, other)

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the extreme value of this instance."""
        self._validate_non_emptiness()

        return -1

    def peek(self):
        """Alias to get: returns the extreme value of this instance."""
        self._validate_non_emptiness()

        return self._values[-1]

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        if self._extreme_key == MAX:
            insort(self._values, value)
        else:
            reverse_insort(self._values, value)


class OrderedArrayMinPriorityQueue(OrderedArrayPriorityQueue):
    """Class that implements a min priority queue based on an ordered internal
    dynamic array (python list)."""

    def __init__(self):
        super().__init__(MIN)

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        reverse_insort(self._values, value)


class OrderedArrayMaxPriorityQueue(OrderedArrayPriorityQueue):
    """Class that implements a max priority queue based on an ordered internal
    dynamic array (python list)."""

    def __init__(self):
        super().__init__(MAX)

    def __copy__(self):
        copy_of_self = type(self)()
        copy_of_self += self
        return copy_of_self

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        insort(self._values, value)
