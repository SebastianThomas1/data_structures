# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod, ABCMeta
from collections.abc import Iterable, Collection as PyCollection

# representations of objects
from reprlib import repr


__all__ = ['UntouchableCollection', 'PredictableIterable',
           'StaticCollection',
           'StaticCollectionWithReferences',
           'Collection', 'CollectionWithReferences',
           'EmptyCollectionException']


def _validate_iterability(values):
    """Validates that values is iterable."""
    if not isinstance(values, Iterable):
        raise TypeError('\'{}\' object is not '
                        'iterable.'.format(type(values).__name__))


class PredictableIterable(Iterable, metaclass=ABCMeta):
    """Abstract base class for the abstract data type predictable iterable.

    Concrete subclasses must provide: __new__ or __init__, and
    predictable __iter__."""

    __slots__ = ()

    def __eq__(self, other):
        """Checks whether this instance is equal to the other object."""
        if self is other:
            return True

        if not isinstance(other, type(self)):
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


class UntouchableCollection(PyCollection, metaclass=ABCMeta):
    """Abstract base class for the abstract data type untouchable collection.

    Concrete subclasses must provide: __new__ or __init__ and __iter__."""

    __slots__ = ()

    def __eq__(self, other):
        """Checks whether this instance is equal to the other object."""
        if self is other:
            return True

        if not isinstance(other, type(self)):
            return False

        if len(self) != len(other):
            return False

        values_of_self = set(self)
        values_of_other = set(other)

        if len(values_of_self) != len(values_of_other):
            return False

        for value in values_of_self:
            if self.count(value) != other.count(value):
                return False

        return True

    def __bool__(self):
        """Returns boolean representation of this instance."""
        return not self.is_empty()

    def __len__(self):
        """Returns the number of values in this instance."""
        return sum(1 for _ in self)

    def __contains__(self, value):
        """Checks whether the given value is contained in this instance."""
        for entry in self:
            if entry == value:
                return True

        return False

    def _validate_non_emptiness(self):
        """Validates that this instance is not empty."""
        if self.is_empty():
            raise EmptyCollectionException('can\'t access entry in empty '
                                           'collection')

    def is_empty(self):
        """Checks whether this instance is empty."""
        try:
            next(iter(self))
        except StopIteration:
            return True
        else:
            return False

    def count(self, value):
        """Returns number of occurrences of value."""
        return sum(1 for entry in self if entry == value)


class StaticCollection(UntouchableCollection):
    """Abstract base class for the abstract data type static collection.

    Concrete subclasses must provide: __new__ or __init__, __iter__ and get."""

    __slots__ = ()

    @abstractmethod
    def get(self):
        """Returns a value of the instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class StaticCollectionWithReferences(UntouchableCollection):
    """Abstract base class for the abstract data type static collection
    with references.

    Concrete subclasses must provide: __new__ or __init__, __iter__ and
    __getitem__."""

    __slots__ = ()

    @abstractmethod
    def __getitem__(self, key):
        """Returns the value of this instance at the given key."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def __contains__(self, key):
        """Checks whether the given key is contained in this instance."""
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True


class Collection(StaticCollection):
    """Abstract base class for the abstract data type collection.

    Concrete subclasses must provide: __new__ or __init__, __iter__,
    get, post and delete."""

    def __iadd__(self, values):
        """Adds values to this instance."""
        self._validate_iterability(values)

        for value in values:
            self.post(value)

        return self

    @staticmethod
    def _validate_iterability(values):
        """Validates that values is iterable."""
        return _validate_iterability(values)

    @abstractmethod
    def post(self, value):
        """Posts the value to the instance."""
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        """Deletes a value from the instance."""
        self._validate_non_emptiness()

        raise NotImplementedError

    def clear(self):
        """Removes all values."""
        try:
            while True:
                self.delete()
        except EmptyCollectionException:
            pass


class CollectionWithReferences(StaticCollectionWithReferences):
    """Abstract base class for the abstract data type collection with
    references.

    Concrete subclasses must provide: __new__ or __init__, __iter__,
    __getitem__, __delitem__, insert."""

    __slots__ = ()

    @abstractmethod
    def __delitem__(self, key):
        """Deletes the value at the key."""
        self._validate_non_emptiness()

        raise NotImplementedError

    @staticmethod
    def _validate_iterability(values):
        """Validates that values is iterable."""
        return _validate_iterability(values)

    @abstractmethod
    def insert(self, key, value):
        """Inserts the value at the key."""
        raise NotImplementedError

    def pop(self, key):
        """Removes and returns the value at the key."""
        value = self[key]
        del self[key]

        return value


class EmptyCollectionException(Exception):

    __slots__ = ()
