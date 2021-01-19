# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod

# copying objects
from copy import copy

# representations of objects
from reprlib import repr

# sorting
from bisect import insort

# custom modules
from datastructures.base import Collection


__all__ = ['ArrayMaxPriorityQueue', 'ArrayMinPriorityQueue',
           'ArrayPriorityQueue', 'HeapMaxPriorityQueue',
           'HeapMinPriorityQueue', 'HeapPriorityQueue', 'MAX', 'MIN',
           'OrderedArrayPriorityQueue', 'OrderedArrayMaxPriorityQueue',
           'OrderedArrayMinPriorityQueue', 'PriorityQueue']


MIN = 'min'
MAX = 'max'


# Source: https://github.com/python/cpython/blob/master/Lib/bisect.py,
# https://stackoverflow.com/a/2247433/10816965
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

    @classmethod
    def from_iterable(cls, values, extreme_key):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls(extreme_key)

        for value in values:
            self.post(value)

        return self

    @abstractmethod
    def __init__(self, extreme_key):
        """Initializes instance."""
        self._validate_extreme_key(extreme_key)

        self._extreme_key = extreme_key

    def __eq__(self, other):
        """Checks whether this instance is equal to the other object."""
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
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self).from_iterable(self, self._extreme_key)
        return copy_of_self

    def __str__(self):
        """Returns a user-friendly string representation of this instance,
        which may be used for printing."""
        return ' '.join(str(value) for value in self)

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
        """Validates that value is comparable to the values in the instance."""
        if not self.is_empty():
            _ = self.peek() < value

    @staticmethod
    def _validate_extreme_key(extreme_key):
        """Validates that extreme_key is MAX or MIN."""
        if extreme_key is not MAX and extreme_key is not MIN:
            raise KeyError('extreme_key must be MAX or MIN')

    def _validate_key(self, key):
        """Validates that key is the extreme key."""
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

    @classmethod
    def from_iterable(cls, values, extreme_key):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls(extreme_key)
        self._values += values

        return self

    def __init__(self, extreme_key):
        """Initializes instance."""
        super().__init__(extreme_key)
        self._values = []

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)(self._extreme_key)
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        return iter(sorted(self._values, reverse=self._extreme_key == MAX))

    def __len__(self):
        """Returns the number of values in this instance."""
        return len(self._values)

    def __repr__(self):
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
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

        return '{}({})'.format(type(self).__name__, repr(extreme_values))

    def __contains__(self, value):
        """Checks whether the given value is contained in this instance."""
        return value in self._values

    def __iadd__(self, values):
        """Enqueues values to this instance."""
        self._validate_iterability(values)

        for value in values:
            self._validate_comparability(value)

        self._values += values

        return self

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the extreme value of this instance."""
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
        self._validate_non_emptiness()

        del self._values[self._idx_of_extreme_value]

    def clear(self):
        """Removes all items."""
        self._values.clear()

    def dequeue(self):
        """Alias to pop(extreme_key): dequeues the extreme value of this
        instance."""
        self._validate_non_emptiness()

        idx_of_extreme_value = self._idx_of_extreme_value
        value = self._values[idx_of_extreme_value]
        del self._values[idx_of_extreme_value]

        return value


class ArrayMinPriorityQueue(ArrayPriorityQueue):
    """Class that implements a min priority queue based on an internal dynamic
    array (python list)."""

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MIN)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        return iter(sorted(self._values, reverse=False))

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the minimal value of this instance."""
        return min(range(len(self._values)), key=self._values.__getitem__)

    def peek(self):
        """Alias to get: returns the minimal value of this instance."""
        self._validate_non_emptiness()

        return min(self._values)


class ArrayMaxPriorityQueue(ArrayPriorityQueue):
    """Class that implements a max priority queue based on an internal dynamic
    array (python list)."""

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MAX)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        return iter(sorted(self._values, reverse=True))

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the maximal value of this instance."""
        return max(range(len(self._values)), key=self._values.__getitem__)

    def peek(self):
        """Alias to get: returns the maximal value of this instance."""
        self._validate_non_emptiness()

        return max(self._values)


class OrderedArrayPriorityQueue(ArrayPriorityQueue):
    """Class that implements a priority queue based on an ordered internal
    dynamic array (python list)."""

    @classmethod
    def from_iterable(cls, values, extreme_key):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls(extreme_key)
        self._values += sorted(values, reverse=extreme_key == MIN)

        return self

    def __iter__(self):
        """Returns an iterator version of this instance."""
        return reversed(self._values)

    def __repr__(self):
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        # determine seven most extreme values (at most)
        extreme_values = self._values[-7:]
        extreme_values.reverse()

        return '{}({})'.format(type(self).__name__, repr(extreme_values))

    def __iadd__(self, other):
        """Enqueues values to this instance."""
        return PriorityQueue.__iadd__(self, other)

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the extreme value of this instance."""
        return -1

    def peek(self):
        """Alias to get: returns the extreme value of this instance."""
        self._validate_non_emptiness()

        return self._values[self._idx_of_extreme_value]

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

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += sorted(values, reverse=True)

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MIN)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        reverse_insort(self._values, value)


class OrderedArrayMaxPriorityQueue(OrderedArrayPriorityQueue):
    """Class that implements a max priority queue based on an ordered internal
    dynamic array (python list)."""

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += sorted(values, reverse=False)

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MAX)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        self._validate_comparability(value)

        insort(self._values, value)


class HeapPriorityQueue(ArrayPriorityQueue):
    """Class that implements a priority queue based on a heap, which is
    realised by a dynamic array (python list)."""

    @classmethod
    def from_iterable(cls, values, extreme_key):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls(extreme_key)
        self._values += values

        for idx in range(len(self) // 2, 0, -1):
            self._sink(idx)

        return self

    def __init__(self, extreme_key):
        """Initializes instance."""
        super().__init__(extreme_key)
        self._values = [None]

    def __iter__(self):
        """Returns an iterator version of this instance."""
        copy_of_self = copy(self)

        while copy_of_self:
            yield copy_of_self.dequeue()

    def __len__(self):
        """Returns the number of values in this instance."""
        return len(self._values) - 1

    def __repr__(self):
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        # determine seven most extreme values (at most)
        extreme_values = []
        for value in self._values[1:8]:
            insort(extreme_values, value)

        if self._extreme_key == MAX:
            extreme_values.reverse()

        return '{}({})'.format(type(self).__name__, repr(extreme_values))

    def __contains__(self, value):
        """Checks whether the given value is contained in this instance."""
        return value in self._values[1:]

    def __iadd__(self, other):
        """Enqueues values to this instance."""
        return PriorityQueue.__iadd__(self, other)

    @property
    def _idx_of_extreme_value(self):
        """Returns the index of the extreme value of this instance."""
        return 1

    @staticmethod
    def _parent_idx(idx):
        """Returns index of parent value."""
        return idx >> 1  # idx // 2

    def _child_idx(self, idx):
        """Returns index of more extreme child value."""
        child_idx = idx << 1  # child_idx = 2*idx
        if child_idx < len(self) \
                and (self._extreme_key == MAX
                     and self._values[child_idx] < self._values[child_idx + 1]
                     or self._extreme_key == MIN
                     and self._values[child_idx]
                     > self._values[child_idx + 1]):
            child_idx += 1

        return child_idx

    def _swim(self, idx):
        """Swims value at given index (upwards) such that heap order is
        restored."""
        value = self._values[idx]

        parent_idx = self._parent_idx(idx)
        while parent_idx > 0:
            parent_value = self._values[parent_idx]
            if (self._extreme_key == MAX and parent_value < value
                    or self._extreme_key == MIN and parent_value > value):
                self._values[idx] = parent_value
                idx = parent_idx
                parent_idx = self._parent_idx(idx)
            else:
                break

        self._values[idx] = value

    def _sink(self, idx):
        """Sinks value at given index (downwards) such that heap order is
        restored."""
        value = self._values[idx]

        child_idx = self._child_idx(idx)
        while child_idx <= len(self):
            child_value = self._values[child_idx]
            if (self._extreme_key == MAX and value < child_value
                    or self._extreme_key == MIN and value > child_value):
                self._values[idx] = child_value
                idx = child_idx
                child_idx = self._child_idx(idx)
            else:
                break

        self._values[idx] = value

    def is_empty(self):
        """Checks whether this instance is an empty heap priority queue."""
        return len(self._values) == 1

    def peek(self):
        """Alias to get: returns the extreme value of this instance."""
        self._validate_non_emptiness()

        return self._values[1]

    def enqueue(self, value):
        """Alias to post: enqueues the value to this instance."""
        super().enqueue(value)
        self._swim(len(self))

    def delete(self):
        """Deletes the extreme value of this instance."""
        self._validate_non_emptiness()

        self._values[1], self._values[len(self)] \
            = self._values[len(self)], self._values[1]
        del self._values[-1]

        if self:
            self._sink(1)

    def clear(self):
        """Removes all items."""
        self._values.clear()
        self._values.append(None)

    def dequeue(self):
        """Alias to pop(extreme_key): dequeues the extreme value of this
        instance."""
        self._validate_non_emptiness()

        self._values[1], self._values[len(self)] \
            = self._values[len(self)], self._values[1]
        extreme_value = self._values.pop()

        if self:
            self._sink(1)

        return extreme_value


class HeapMinPriorityQueue(HeapPriorityQueue):
    """Class that implements a min priority queue based on a heap, which is
    realised by a dynamic array (python list)."""

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        for idx in range(len(self) // 2, 0, -1):
            self._sink(idx)

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MIN)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def _child_idx(self, idx):
        """Returns index of smaller child value."""
        child_idx = idx << 1  # child_idx = 2*idx
        if child_idx < len(self) \
                and self._values[child_idx] > self._values[child_idx + 1]:
            child_idx += 1

        return child_idx

    def _swim(self, idx):
        """Swims value at given index (upwards) such that heap order is
        restored."""
        value = self._values[idx]

        parent_idx = self._parent_idx(idx)
        while parent_idx > 0:
            parent_value = self._values[parent_idx]
            if parent_value > value:
                self._values[idx] = parent_value
                idx = parent_idx
                parent_idx = self._parent_idx(idx)
            else:
                break

        self._values[idx] = value

    def _sink(self, idx):
        """Sinks value at given index (downwards) such that heap order is
         restored."""
        value = self._values[idx]

        child_idx = self._child_idx(idx)
        while child_idx <= len(self):
            child_value = self._values[child_idx]
            if value > child_value:
                self._values[idx] = child_value
                idx = child_idx
                child_idx = self._child_idx(idx)
            else:
                break

        self._values[idx] = value


class HeapMaxPriorityQueue(HeapPriorityQueue):
    """Class that implements a max priority queue based on a heap, which is
    realised by a dynamic array (python list)."""

    # noinspection PyMethodOverriding
    @classmethod
    def from_iterable(cls, values):
        """Constructs instance from iterable values."""
        cls._validate_iterability(values)

        self = cls()
        self._values += values

        for idx in range(len(self) // 2, 0, -1):
            self._sink(idx)

        return self

    def __init__(self):
        """Initializes instance."""
        super().__init__(MAX)

    def __copy__(self):
        """Returns a (shallow) copy of this instance."""
        copy_of_self = type(self)()
        copy_of_self._values = copy(self._values)
        return copy_of_self

    def _child_idx(self, idx):
        """Returns index of larger child value."""
        child_idx = idx << 1  # child_idx = 2*idx
        if child_idx < len(self) \
                and self._values[child_idx] < self._values[child_idx + 1]:
            child_idx += 1

        return child_idx

    def _swim(self, idx):
        """Swims value at given index (upwards) such that heap order is
        restored."""
        value = self._values[idx]

        parent_idx = self._parent_idx(idx)
        while parent_idx > 0:
            parent_value = self._values[parent_idx]
            if parent_value < value:
                self._values[idx] = parent_value
                idx = parent_idx
                parent_idx = self._parent_idx(idx)
            else:
                break

        self._values[idx] = value

    def _sink(self, idx):
        """Sinks value at given index (downwards) such that heap order is
         restored."""
        value = self._values[idx]

        child_idx = self._child_idx(idx)
        while child_idx <= len(self):
            child_value = self._values[child_idx]
            if value < child_value:
                self._values[idx] = child_value
                idx = child_idx
                child_idx = self._child_idx(idx)
            else:
                break

        self._values[idx] = value
