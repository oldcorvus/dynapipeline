"""
    Contains ListRegistry to store and manage lists of items
"""
from typing import Iterable, List, Optional

from dynapipeline.exceptions.registry import ItemNotFoundError
from dynapipeline.utils.base_registry import BaseRegistry
from dynapipeline.utils.types import T


class ListRegistry(BaseRegistry[List[T]]):
    """
    A registry class that stores and manages lists of items
    Uses BaseRegistry with a default_factory to manage lists automatically
    """

    def __init__(self):
        super().__init__(default_factory=list)

    def register(self, name: str, items: Iterable[T]) -> None:
        """
        Adds an item to the list for the given name
        Automatically creates a new list if one does not exist for the name
        """
        self._items[name].extend(items)

    def unregister(self, name: str, item: Optional[T] = None) -> None:
        """
        Removes a specific item from the list of items registered under the given name
        Raises ItemNotFoundError if the name or the item is not found
        """
        try:
            if item:
                self._items[name].remove(item)
                if not self._items[name]:
                    del self._items[name]
            else:
                super().unregister(name)
        except ValueError:
            raise ItemNotFoundError(f"Item '{item}' not found under '{name}'")
        except KeyError:
            raise ItemNotFoundError(f"No list found under '{name}'")

    def clear(self, name: Optional[str] = None) -> None:
        """
        Clears the list of items for the given name or entire items
        """
        if name:
            self._items[name].clear()
        else:
            super().clear()
