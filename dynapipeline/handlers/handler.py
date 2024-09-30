"""
    Contains Handler abstract class 
"""
from typing import Any, Awaitable, Callable, Optional

from pydantic import BaseModel, ConfigDict

from dynapipeline.core.handler import AbstractHandler
from dynapipeline.pipelines.component import PipelineComponent


class Handler(BaseModel, AbstractHandler[PipelineComponent]):
    """
    Concrete class for handlers, specifically for `PipelineComponent`
    Handlers can override only the methods they need which can be  synchronous or asynchronous
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def before(
        self, component: PipelineComponent, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        """
        Called before the component's execution
        Can be overridden
        """
        return None

    async def around(
        self,
        component: PipelineComponent,
        execute: Callable[..., Awaitable[Any]],
        *args,
        **kwargs
    ) -> Any:
        """
        Wraps around the component's execution
        Must be asynchronous
        Can be overridden
        """
        return await execute(*args, **kwargs)

    async def after(
        self, component: PipelineComponent, result: Any, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        """
        Called after the component's execution
        Can be overridden
        """
        return None

    def on_error(
        self, component: PipelineComponent, error: Exception, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        """
        Called when an error occurs during the component's execution
        Can be overridden
        """
        return None
