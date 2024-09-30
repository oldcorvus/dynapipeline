"""
    Contains Handler abstract class 
"""
from typing import Any, Awaitable, Callable, Optional

from pydantic import BaseModel, ConfigDict

from dynapipeline.core.handler import AbstractHandler
from dynapipeline.pipelines.component import PipelineComponent


class Handler(BaseModel, AbstractHandler):
    """
    Abstract class for all handlers providing default no-op implementations
    Handlers can override only the methods they need which can be either synchronous or asynchronous
    """

    component: PipelineComponent

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def before(self, *args, **kwargs) -> Optional[Awaitable[None]]:
        """
        Called before the component's execution
        Can be overridden to provide custom behavior

        """
        return None

    async def around(
        self, execute: Callable[..., Awaitable[Any]], *args, **kwargs
    ) -> Any:
        """
        Wraps around the component's execution Must be asynchronous
        Can be overridden to provide custom behavior

        """
        return await execute(*args, **kwargs)

    def after(self, result: Any, *args, **kwargs) -> Optional[Awaitable[None]]:
        """
        Called after the component's execution
        Can be overridden to provide custom behavior
        """
        return None

    def on_error(self, error: Exception, *args, **kwargs) -> Optional[Awaitable[None]]:
        """
        Called when an error occurs during the component's execution
        Can be overridden to provide custom behavior
        """
        return None
