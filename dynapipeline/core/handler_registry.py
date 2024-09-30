"""
    Defines abstract hander registry 

"""
from abc import ABC, abstractmethod
from typing import Any


class AbstractHandlerRegistry(ABC):
    """
    Abstract base class for a handler registry
    """

    @abstractmethod
    def register(self, handler: Any) -> None:
        """
        Registers a handler in the registry
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    async def notify(self, method_name: str, *args, **kwargs) -> None:
        """
        Notifies (calls) all handlers registered under a specific method name
        """
        raise NotImplementedError("Subclasses must implement this method")
