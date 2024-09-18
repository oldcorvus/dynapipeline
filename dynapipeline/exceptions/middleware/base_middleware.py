"""
This module defines the base abstract class for error middleware in the pipeline.
"""

from abc import ABC, abstractmethod
from typing import Optional

from dynapipeline.exceptions.base_error import BaseError


class ErrorMiddleware(ABC):
    """
    Abstract base class for processing errors in the pipeline.
    """

    def __init__(self, description: str = ""):
        self.enabled = True
        self.description = description

    @abstractmethod
    def handle(self, error: BaseError) -> Optional[BaseError]:
        """
        Handle the given error.
        """
        raise NotImplementedError("Subclasses must implement the `handle` method")

    def toggle(self, enable: bool) -> None:
        """
        Enable or disable the middleware.
        """
        self.enabled = enable

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(enabled={self.enabled}, description={self.description})"
