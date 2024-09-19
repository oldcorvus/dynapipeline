"""
    Defines the base abstract class for middlewares
"""

from abc import ABC, abstractmethod
from typing import Generic

from dynapipeline.utils.types import T


class BaseMiddleware(ABC, Generic[T]):
    """
    Abstract base class for processing items
    """

    def __init__(self, enabled: bool = True, description: str = ""):
        self.enabled = enabled
        self.description = description

    @abstractmethod
    def handle(self, item: T) -> T:
        """
        Handle the given item
        """
        raise NotImplementedError("Subclasses must implement the `handle` method")

    def toggle(self, enable: bool) -> None:
        """
        Enable or disable the middleware.

        Args:
            enable (bool): Whether to enable or disable the middleware.
        """
        self.enabled = enable

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(enabled={self.enabled}, description={self.description})"
