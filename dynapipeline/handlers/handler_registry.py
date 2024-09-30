"""
    Defines HandlerRegistry for managing handlers
"""
import asyncio
import inspect
from typing import Any, Awaitable, Callable, Dict, List

from dynapipeline.core.handler import AbstractHandler
from dynapipeline.core.handler_registry import AbstractHandlerRegistry
from dynapipeline.utils.list_registry import ListRegistry


class HandlerRegistry(
    ListRegistry[Callable[..., Awaitable[Any]]], AbstractHandlerRegistry
):
    """
    Class for managing handlers
    """

    def attach(self, handlers: List[AbstractHandler]) -> None:
        """
        attaches handlers by registering all callable public methodsgrouping and storing each
        under its corresponding method name in the registry

        """
        method_dict: Dict[str, List[Callable[..., Awaitable[Any]]]] = {}

        for handler in handlers:
            for method_name, method in inspect.getmembers(
                handler, predicate=inspect.isroutine
            ):
                # Skip magic methods
                if method_name.startswith("__") and method_name.endswith("__"):
                    continue
                if method_name not in method_dict:
                    method_dict[method_name] = []
                method_dict[method_name].append(method)

        for name, methods in method_dict.items():
            super().register(name, methods)

    async def notify(self, method_name: str, *args, **kwargs):
        """
        Notifies (calls) all handlers registered under a specific method name
        """
        methods = self.get(method_name)
        result = None
        if methods:
            for method in methods:
                result = method(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    result = await result
        return result
