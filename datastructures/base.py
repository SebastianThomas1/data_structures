# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod, ABCMeta
from collections.abc import Iterable, Collection as PyCollection

# representations of objects
from reprlib import repr as reprlib_repr


__all__ = ['Collection']


class Collection(PyCollection, metaclass=ABCMeta):
    """Abstract base class for the abstract data type collection.

    Concrete subclasses must provide: __new__ or __init__, __iter__."""

    def __bool__(self):
        return not self.is_empty()

    def __repr__(self):
        # determine first seven values (at most)
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
        return ' '.join(str(value) for value in self)

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, value):
        for entry in self:
            if entry is value or entry == value:
                return True

        return False

    def is_empty(self):
        """Checks whether this instance is empty."""
        return len(self) == 0


class OrderedCollection(Collection, metaclass=ABCMeta):
    """Abstract base class for the abstract data type ordered collection.

    Concrete subclasses must provide: __new__ or __init__ and predictable
    __iter__."""

    def __eq__(self, other):
        if self is other:
            return True

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
