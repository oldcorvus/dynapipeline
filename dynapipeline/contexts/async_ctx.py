"""
    Contains AsyncLockableContext that extends AsyncLockableContext with asyncio.Lock
"""
import asyncio
from typing import Any, Dict, Optional

from dynapipeline.core.context import AbstractContext


class AsyncLockableContext(AbstractContext):
    """
    Extends AbstractContext with an asyncio.Lock
    """

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        super().__init__()
        if initial_data:
            self._data.update(initial_data)
        self._async_lock = asyncio.Lock()

    async def lock(self):
        """Locks the context to prevent further modifications"""
        await self._async_lock.acquire()

    async def unlock(self):
        """Unlocks the context to allow modifications"""
        if self.is_locked:
            self._async_lock.release()

    @property
    def is_locked(self) -> bool:
        """Returns True if the context is locked"""
        return self._async_lock.locked()

    async def __aenter__(self):
        """Asynchronous context manager entry method

        Acquires the asyncio lock when entering"""
        await self._async_lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronous context manager exit method
        releases the asyncio lock when exiting"""

        if self.is_locked:
            self._async_lock.release()
        return False

    async def __aiter__(self):
        """Asynchronous iterator to iterate over context's data"""
        for key, value in self._data.items():
            yield key, value
