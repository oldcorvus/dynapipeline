"""
    Defines the base abstract class for middlewares
"""
from abc import ABC, abstractmethod
from typing import Generic

from dynapipeline.core.context import BaseContext
from dynapipeline.exceptions.middleware import MiddlewareProcessingError
from dynapipeline.utils.types import T


class BaseMiddleware(ABC, Generic[T]):
    """
    Abstract base class for processing items
    """

    def __init__(
        self, context: BaseContext, enabled: bool = True, description: str = ""
    ):
        self.enabled = enabled
        self.description = description
        self.context = context

    async def handle(self, item: T) -> T:
        """
        Handle the given item
        """

        if not self.enabled:
            return item
        try:
            return await self._handle(item)
        except Exception as e:
            raise MiddlewareProcessingError(f"{self.__class__.__name__}", str(e)) from e

    @abstractmethod
    async def _handle(self, item: T) -> T:
        """
        Handle the given item
        """
        raise NotImplementedError("Subclasses must implement the `handle` method")

    def toggle(self, enable: bool) -> None:
        """
        Enable or disable the middleware
        """
        self.enabled = enable

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(enabled={self.enabled}, description={self.description})"
