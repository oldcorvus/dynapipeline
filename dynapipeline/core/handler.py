"""
        Defines  interface for handlers
        
"""
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Generic, TypeVar

from dynapipeline.core.component import AbstractComponent

T_Component = TypeVar("T_Component", bound="AbstractComponent")


class AbstractHandler(ABC, Generic[T_Component]):
    """
    Abstract base class for all handlers
    """

    @abstractmethod
    def before(self, component: T_Component, *args, **kwargs):
        """Method is called before the component's execution"""
        pass

    @abstractmethod
    async def around(
        self,
        component: T_Component,
        execute: Callable[..., Awaitable[Any]],
        *args,
        **kwargs
    ) -> Any:
        """
        Wraps around the component's execution The default implementation calls `execute()`
        """
        pass

    @abstractmethod
    async def after(self, component: T_Component, result: Any, *args, **kwargs) -> Any:
        """Method is called after the component's execution"""
        pass

    @abstractmethod
    def on_error(self, component: T_Component, error: Exception, *args, **kwargs):
        """Method is called when an error occurs"""
        pass
