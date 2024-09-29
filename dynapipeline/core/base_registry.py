"""
This module contains the BaseRegistry class that is responsible for managing items of any type"""

from collections import defaultdict
from collections.abc import MutableMapping
from typing import Callable, Dict, Generic, Optional, Union

from dynapipeline.exceptions.registry import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)
from dynapipeline.utils.types import T


class BaseRegistry(MutableMapping, Generic[T]):
    """
    A registry class that stores and manages items
    """

    def __init__(self, default_factory: Optional[Callable[[], T]] = None):
        self._items: Union[Dict[str, T], defaultdict[str, T]] = (
            defaultdict(default_factory) if default_factory else {}
        )
        self._default_factory = default_factory

    def register(self, name: str, item: T) -> None:
        """
        User-friendly method to add an item to the registry
        Calls __setitem__ internally
        """
        self.__setitem__(name, item)

    def unregister(self, name: str) -> None:
        """
        User-friendly method to remove an item from the registry
        Calls __delitem__ internally
        """
        self.__delitem__(name)

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __setitem__(self, name: str, item: T) -> None:
        """
        Adds an item to the registry
        Raises ItemAlreadyRegisteredError if name is missing
        """
        if name in self._items:
            raise ItemAlreadyRegisteredError(name)
        self._items[name] = item

    def __delitem__(self, name: str) -> None:
        """
        Removes an item from the registry by name
        Raises ItemNotFoundError if name is missing
        """
        if name not in self._items:
            raise ItemNotFoundError(name)
        del self._items[name]

    def __getitem__(self, name: str) -> T:
        """
        Retrieves an item by its name
        Raises ItemNotFoundError if name is missing and default_factory is not set
        """

        if name not in self._items and self._default_factory is None:
            raise ItemNotFoundError(name)

        return self._items[name]
