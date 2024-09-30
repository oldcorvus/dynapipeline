"""
        Defines  interface for handlers
        
"""
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable

from dynapipeline.core.component import AbstractComponent


class AbstractHandler(ABC):
    """
    Abstract base class for all handlers
    """

    component: AbstractComponent

    @abstractmethod
    def before(self, *args, **kwargs):
        """Method is called before the component's execution"""
        pass

    @abstractmethod
    async def around(
        self, execute: Callable[..., Awaitable[Any]], *args, **kwargs
    ) -> Any:
        """
        Wraps around the component's execution
        default implementation calls `execute()`
        """
        pass

    @abstractmethod
    async def after(self, result, *args, **kwargs):
        """Method is called after the component's execution"""
        pass

    @abstractmethod
    def on_error(self, error: Exception, *args, **kwargs):
        """Method is called when an error occurs"""
        pass
