# Sebastian Thomas (datascience at sebastianthomas dot de)

from __future__ import annotations

# type hints
from typing import Optional, Any, Generator

# abstract base classes
from abc import abstractmethod, ABCMeta
from collections import Iterable, Iterator

# representations of objects
from reprlib import repr

# custom modules
from datastructures.base import CollectionWithReferences, UntouchableCollection
from datastructures.node import LinkedNodeWithKey


__all__ = ['Dictionary', 'LinkedDictionary', 'DictionaryView', 'KeysView',
           'ItemsView', 'ValuesView']


class Dictionary(CollectionWithReferences):
    """Abstract base class for the abstract data type dictionary (aka symbol
    table aka associative array).

    Concrete subclasses must provide: __new__ or __init__, predictable
    __iter__, __getitem__, __setitem__, __delitem__ and insert."""

    __slots__ = ()

    @classmethod
    def from_dictionary(cls, other: Dictionary) -> Dictionary:
        """Constructs instance from dictionary other."""
        cls._validate_dictionary(other)

        self = cls()

        for key in other:
            self.insert(key, other[key])

        return self

    @classmethod
    def from_iterable(cls, pairs: Iterable[tuple[Any, Any]]) -> Dictionary:
        """Constructs instance from iterable pairs."""
        cls._validate_iterability(pairs)

        self = cls()

        for key, value in pairs:
            self.insert(key, value)

        return self

    def __copy__(self) -> Dictionary:
        return type(self).from_dictionary(self)

    def __repr__(self) -> str:
        """Returns a developer-friendly string representation of this instance,
        which may be used for debugging."""
        # determine first seven items (at most)
        first_items = []
        for item in self.items():
            first_items.append(item)
            if len(first_items) == 7:
                break

        return f'{type(self).__name__}({repr(dict(first_items))})'

    def __str__(self) -> str:
        """Returns a user-friendly string representation of this instance,
        which may be used for printing."""
        return ', '.join(f'{key}: {self[key]}' for key in self)

    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        """Returns the value of this instance at the given key."""
        self._validate_key(key)

        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key: Any, value: Any) -> None:
        """Updates the value of this instance at the given key."""
        self._validate_key(key)

        raise NotImplementedError

    @abstractmethod
    def __delitem__(self, key: Any) -> None:
        """Deletes the value of this instance at the given key."""
        self._validate_key(key)

        raise NotImplementedError

    @staticmethod
    def _validate_dictionary(other: Dictionary) -> None:
        """Validates that other is a dictionary."""
        if not isinstance(other, Dictionary):
            raise TypeError('\'{}\' object is not a '
                            'dictionary.'.format(type(other).__name__))

    def _validate_key(self, key: Any) -> None:
        """Validates that key is a key of this instance."""
        if key not in self:
            raise KeyError(f'{key} is not a key of this instance')

    def _validate_non_key(self, key: Any) -> None:
        """Validates that key is not a key of this instance."""
        if key in self:
            raise KeyError(f'{key} is already a key of this instance')

    @abstractmethod
    def insert(self, key: Any, value: Any) -> None:
        """Inserts the value into this instance at the given key."""
        self._validate_non_key(key)

        raise NotImplementedError

    def clear(self) -> None:
        """Removes all values."""
        for key in self:
            del self[key]

    def keys(self) -> KeysView:
        """Returns an untouchable collection providing a view on the keys of
        this instance."""
        return KeysView(self)

    def items(self) -> ItemsView:
        """Returns an untouchable collection providing a view on the items of
        this instance."""
        return ItemsView(self)

    def values(self) -> ValuesView:
        """Returns an untouchable collection providing a view on the values of
        this instance."""
        return ValuesView(self)


Dictionary.register(dict)


class DictionaryView(UntouchableCollection, metaclass=ABCMeta):
    """Abstract base class for an abstract data type providing a view on a
    dictionary."""

    __slots__ = '_dictionary',

    def __init__(self, dictionary: Dictionary):
        self._dictionary = dictionary

    def __len__(self) -> int:
        return len(self._dictionary)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({repr(self._dictionary)})'


class KeysView(DictionaryView):
    """Base class for a data type providing a view on the keys of a
    dictionary."""

    __slots__ = ()

    def __contains__(self, key: Any) -> bool:
        return key in self._dictionary

    def __iter__(self) -> Iterator:
        yield from self._dictionary


class ItemsView(DictionaryView):
    """Base class for a data type providing a view on the items of a
    dictionary."""

    __slots__ = ()

    def __contains__(self, item: Any) -> bool:
        key, value = item
        try:
            self._dictionary[key] == value
        except KeyError:
            return False
        else:
            return True

    def __iter__(self) -> Iterator:
        for key in self._dictionary:
            yield key, self._dictionary[key]


class ValuesView(DictionaryView):
    """Base class for a data type providing a view on the values of a
    dictionary."""

    __slots__ = ()

    def __iter__(self) -> Iterator:
        for key in self._dictionary:
            yield self._dictionary[key]


class LinkedDictionary(Dictionary):
    """Class that implements a dictionary based on linked nodes."""

    __slots__ = '_head', '_len'

    class Node(LinkedNodeWithKey):
        """Internal node class for linked dictionaries."""
        pass

    @classmethod
    def from_iterable(cls, pairs: Iterable[tuple[Any, Any]]) \
            -> LinkedDictionary:
        """Constructs instance from iterable pairs."""
        cls._validate_iterability(pairs)

        self = cls()

        if pairs:
            iterator = iter(pairs)

            self._head = self.Node(*next(iterator))
            self._len += 1

            current_node = self._head
            for key, value in iterator:
                current_node.successor = self.Node(key, value)
                current_node = current_node.successor
                self._len += 1

        return self

    def __init__(self) -> None:
        """Initializes instance."""
        self._head = None
        self._len = 0

    def __iter__(self) -> Iterator:
        """Returns an iterator of the keys of this instance."""
        for node in self._traversal():
            yield node.key

    def __len__(self) -> int:
        return self._len

    def __contains__(self, key: Any) -> bool:
        return UntouchableCollection.__contains__(self, key)

    def __getitem__(self, key: Any) -> Any:
        """Returns the value of this instance at the given key."""
        return self._get_node(key).value

    def __setitem__(self, key: Any, value: Any) -> None:
        """Updates the value of this instance at the given key."""
        self._get_node(key).value = value

    def __delitem__(self, key: Any) -> None:
        """Deletes the value of this instance at the given key."""
        node, predecessor = self._get_node_with_predecessor(key)
        self._remove_node(node, predecessor)

    def _traversal(self, start_node: Optional[LinkedDictionary.Node] = None) \
            -> Generator[LinkedDictionary.Node]:
        """Traverses instance, beginning with start_node (default: head)."""
        if start_node is None:
            start_node = self._head

        current_node = start_node
        while current_node:
            yield current_node
            current_node = current_node.successor

    def _get_node(self, key: Any) -> LinkedDictionary.Node:
        """Returns node with given key."""
        self._validate_key(key)

        # traverse instance, return current node if its key is the given
        # key
        for node in self._traversal():
            if node.key == key:
                return node

    def _get_node_with_predecessor(self, key: Any) \
            -> tuple[LinkedDictionary.Node, Optional[LinkedDictionary.Node]]:
        """Returns node with given key together with predecessor."""
        self._validate_key(key)

        # traverse instance, return current node and predecessor if its
        # key is the given key
        predecessor = None
        for node in self._traversal():
            if node.key == key:
                return node, predecessor
            predecessor = node

    def _remove_node(self, node: LinkedDictionary.Node,
                     predecessor: Optional[LinkedDictionary.Node]) -> None:
        """Removes node by connecting predecessor with successor."""
        if predecessor:
            predecessor.successor = node.successor
        else:  # ie node is self.head
            self._head = self._head.successor

        self._len -= 1

    def insert(self, key: Any, value: Any) -> None:
        """Inserts the value into this instance at the given key."""
        self._validate_non_key(key)

        self._head = self.Node(key, value, successor=self._head)

        self._len += 1
