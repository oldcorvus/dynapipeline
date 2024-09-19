"""
    Defines BaseContext class to  manage attributes dynamically
"""
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")


class BaseContext(Generic[T]):
    """
    A flexible context class that allows users to dynamically manage attributes
    """

    def __init__(self, raise_on_missing: bool = False):
        self._data: Dict[str, T] = {}
        self.raise_on_missing = raise_on_missing

    def set(self, key: str, value: T) -> None:
        """Sets a value in the context"""
        self._data[key] = value

    def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
        """Retrieves a value from the context returns default if key is not found
        or raises an error based on flag"""
        if key not in self._data:
            if self.raise_on_missing:
                raise KeyError(f"Key '{key}' not found in the context")
            return default
        return self._data.get(key)

    def remove(self, key: str) -> None:
        """Removes a key from the context"""
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in the context")

    def contains(self, key: str) -> bool:
        """Checks if the key exists in the context"""
        return key in self._data

    def clear(self) -> None:
        """Clears all values from the context"""
        self._data.clear()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
