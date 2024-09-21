"""
    Defines Mixin for middleware support
"""
from typing import Generic, List

from dynapipeline.core.base_middleware import BaseMiddleware
from dynapipeline.utils.types import T


class MiddlewareMixin(Generic[T]):
    """
    Mixin class to add middleware support for any type of data or object.
    """

    def __init__(self):
        self._middleware: List[BaseMiddleware[T]] = []

    def add_middleware(self, middleware: BaseMiddleware[T]) -> None:
        """
        Adds middleware to the processing chain
        """
        self._middleware.append(middleware)

    def remove_middleware(self, middleware: BaseMiddleware[T]) -> None:
        """
        Removes middleware from the processing chain
        """
        self._middleware.remove(middleware)

    async def process_with_middleware(self, item: T) -> T:
        """
        Processes the item through all registered middleware
        """
        for middleware in self._middleware:
            item = await middleware.handle(item)
            if item is None:
                break
        return item
