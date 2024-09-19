"""
This module contains the BaseRegistry class, which is responsible for managing items of any type.
"""
from typing import Dict, Generic, Optional

from dynapipeline.exceptions.registry_exceptions import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)
from dynapipeline.utils.types import T


class BaseRegistry(Generic[T]):
    """
    A registry class that stores and manages items.
    """

    def __init__(self):
        self._items: Dict[str, T] = {}

    def register(self, name: str, item: T) -> None:
        """
        Adds an item to the registry. Raises an error if the item already exists.
        """
        if name in self._items:
            raise ItemAlreadyRegisteredError(name)
        self._items[name] = item

    def get(self, name: str) -> Optional[T]:
        """
        Retrieves an item by its name. Raises an error if not found.
        """
        if name not in self._items:
            raise ItemNotFoundError(name)
        return self._items.get(name)

    def unregister(self, name: str) -> None:
        """
        Removes an item from the registry by name. Raises an error if the item doesn't exist.
        """
        if name not in self._items:
            raise ItemNotFoundError(name)
        del self._items[name]

    def is_registered(self, name: str) -> bool:
        """Checks if an item is already registered."""
        return name in self._items

    def count(self) -> int:
        """Returns the number of items in the registry."""
        return len(self._items)

    def clear(self) -> None:
        """Clears all items from the registry."""
        self._items.clear()

    def list_items(self) -> Dict[str, T]:
        """Returns a dictionary of all registered items."""
        return self._items
