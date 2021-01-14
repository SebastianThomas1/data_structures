# Sebastian Thomas (datascience at sebastianthomas dot de)

# abstract base classes
from abc import abstractmethod, ABCMeta
from collections.abc import Iterable, Collection as PyCollection

# representations of objects
from reprlib import repr


__all__ = ['CollectionMixin', 'PredictableIterMixin',
           'StaticCollection', 'StaticCollectionWithReferences',
           'Collection', 'CollectionWithReferences',
           'EmptyCollectionException']


class CollectionMixin(PyCollection, metaclass=ABCMeta):
    def __eq__(self, other):
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

        return '{}({})'.format(type(self).__name__, repr(first_values))

    def __str__(self):
        return ' '.join(str(value) for value in self)

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, value):
        for entry in self:
            if entry is value or entry == value:
                return True

        return False

    def _validate_non_emptiness(self):
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


class PredictableIterMixin(Iterable, metaclass=ABCMeta):
    def __eq__(self, other):
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


class StaticCollection(CollectionMixin):
    """Abstract base class for the abstract data type static collection.

    Concrete subclasses must provide: __new__ or __init__, __iter__ and get."""

    @abstractmethod
    def get(self):
        """Returns a value of the instance."""
        self._validate_non_emptiness()

        raise NotImplementedError


class StaticCollectionWithReferences(CollectionMixin):
    """Abstract base class for the abstract data type static collection
    with references.

    Concrete subclasses must provide: __new__ or __init__, __iter__ and
    __getitem__."""

    @abstractmethod
    def __getitem__(self, key):
        self._validate_non_emptiness()

        raise NotImplementedError


class Collection(StaticCollection):
    """Abstract base class for the abstract data type collection.

    Concrete subclasses must provide: __new__ or __init__, __iter__,
    get, post and delete."""

    def __iadd__(self, other):
        if not isinstance(other, Iterable):
            raise TypeError('\'{}\' object is not iterable.'.format(type(other)
                                                                    .__name__))

        for value in other:
            self.post(value)

        return self

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

    @abstractmethod
    def __delitem__(self, key):
        """Deletes the value at the key."""
        self._validate_non_emptiness()

        raise NotImplementedError

    @abstractmethod
    def insert(self, key, value):
        """Inserts the value at the key."""
        pass

    def pop(self, key):
        """Removes and returns the value at the key."""
        value = self[key]
        del self[key]

        return value


class EmptyCollectionException(Exception):
    pass
