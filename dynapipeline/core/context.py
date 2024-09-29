"""
Contains AbstractContext class for managing key-value pairs within a pipeline context
"""

from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Any, Dict

from dynapipeline.exceptions.context import ContextKeyError


@dataclass
class AbstractContext(ABC, MutableMapping[str, Any]):
    """
    Abstract base class for context using dataclasses
    """

    _data: Dict[str, Any] = field(default_factory=dict)
    _is_locked: bool = field(default=False)

    @abstractmethod
    def lock(self):
        """Locks the context to prevent further modifications"""
        raise NotImplementedError("Subclasses must implement the lock method")

    @abstractmethod
    def unlock(self):
        """Unlocks the context to allow modifications"""
        raise NotImplementedError("Subclasses must implement the unlock method")

    @property
    def is_locked(self) -> bool:
        """Check if the context is locked"""
        return self._is_locked

    def __getitem__(self, key: str) -> Any:
        """Retrieve the value associated with the given key"""
        try:
            return self._data[key]
        except KeyError as e:
            raise ContextKeyError(key) from e

    def __setitem__(self, key: str, value: Any):
        """Assign a value to a specific key in the context"""
        self._data[key] = value

    def __delitem__(self, key: str):
        """Remove the value associated with the given key"""
        try:
            del self._data[key]
        except KeyError as e:
            raise ContextKeyError(key) from e

    def __iter__(self):
        """Return an iterator over the keys stored in the context"""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of key-value pairs stored in the context"""
        return len(self._data)
