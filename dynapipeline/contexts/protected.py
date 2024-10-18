"""Contains ProtectedContext that uses a boolean flag to make context immutable"""
from typing import Any, Dict, Optional

from dynapipeline.core.context import AbstractContext
from dynapipeline.exceptions.context import ContextKeyError, ContextLockedError

# for now i just lock the context before pipeline execution but it has some limitations
# and problems like context itself is locked, mutable objects inside
# can still be modified, leading to potential inconsistencies and
# simple boolean lock is not suffient so later i may add Versioning with vector clock or Snapshots for context to
# let users modify context safely


class ProtectedContext(AbstractContext):
    """
    A basic lockable context using a simple boolean  to make context immutable when locked
    """

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        super().__init__()
        if initial_data:
            self._data.update(initial_data)

    def lock(self):
        """Locks the context to make it immutable"""
        self._is_locked = True

    def unlock(self):
        """Unlocks the context to allow it to be modified"""
        self._is_locked = False

    @property
    def is_locked(self) -> bool:
        """Returns True if the context is locked an False when its unlocked"""
        return self._is_locked

    def __setitem__(self, key: str, value: Any):
        """
        Sets item in the context"""
        if self.is_locked:
            raise ContextLockedError()
        self._data[key] = value

    def __delitem__(self, key: str):
        """
        Deletes item from the context"""
        if self.is_locked:
            raise ContextLockedError()
        try:
            del self._data[key]
        except KeyError:
            raise ContextKeyError(key)
