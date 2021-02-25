# Sebastian Thomas (datascience at sebastianthomas dot de)

from __future__ import annotations

# type hints
from typing import NoReturn, Optional, Any


class LinkedNode:
    """Node class for eg (singly) linked lists, linked stacks, ..."""

    __slots__ = 'value', 'successor'

    def __init__(self, value: Any, successor: Optional[LinkedNode] = None) \
            -> NoReturn:
        self.value = value
        self.successor = successor

    def __repr__(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        return str(self.value)


class LinkedNodeWithKey(LinkedNode):
    """Node class with a key field, eg for linked dictionaries."""

    __slots__ = 'key', 'value', 'successor'

    def __init__(self, key: Any, value: Any,
                 successor: Optional[LinkedNodeWithKey] = None) -> NoReturn:
        super().__init__(value, successor=successor)
        self.key = key

    def __repr__(self) -> str:
        return f'{type(self).__name__}(key={repr(self.key)}, ' \
               f'value={repr(self.value)})'

    def __str__(self) -> str:
        return f'({str(self.key)}: {str(self.value)})'


class DoublyLinkedNode(LinkedNode):
    """Node class for eg doubly linked lists, ..."""

    __slots__ = 'value', 'predecessor', 'successor'

    def __init__(self, value: Any,
                 predecessor: Optional[DoublyLinkedNode] = None,
                 successor: Optional[DoublyLinkedNode] = None) -> NoReturn:
        super().__init__(value, successor=successor)
        self.predecessor = predecessor
