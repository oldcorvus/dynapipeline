"""
    Defines abstract hander registry 

"""
from abc import ABC, abstractmethod
from typing import List

from dynapipeline.core.handler import AbstractHandler


class AbstractHandlerRegistry(ABC):
    """
    Abstract base class for a handler registry
    """

    @abstractmethod
    def attach(self, handler: List[AbstractHandler]) -> None:
        """
        attaches a handler to the registry
        """
        raise NotImplementedError("Subclasses must implement 'attach' method")

    @abstractmethod
    async def notify(self, method_name: str, *args, **kwargs) -> None:
        """
        Notifies (calls) all handlers registered under a specific method name
        """
        raise NotImplementedError("Subclasses must implement 'notify' method")
