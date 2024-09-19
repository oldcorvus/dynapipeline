"""
    defines the ErrorRegistryWithMiddleware class that extends ErrorRegistry to include middlewares 
"""

from typing import List, Type

from dynapipeline.exceptions.base_error import BaseError
from dynapipeline.exceptions.error_registry import ErrorRegistry
from dynapipeline.exceptions.middleware.base import ErrorMiddleware


class MiddlewareErrorRegistry(ErrorRegistry):
    """
    enhanced version of ErrorRegistry that has middleware support
    """

    def __init__(self) -> None:
        super().__init__()
        self.middleware: List[ErrorMiddleware] = []

    def add(self, error: BaseError, context: str = "default") -> None:
        """
        Adds an error to the registry after processing it through the middleware chain.
        """
        for middleware in self.middleware:
            error = middleware.handle(error)
            if error is None:
                return  # Middleware handled the error

        super().add(error, context)

    def add_middleware(self, middleware: ErrorMiddleware) -> None:
        """
        Adds an error middleware to the processing chain.


        """
        self.middleware.append(middleware)

    def remove_middleware(self, middleware: ErrorMiddleware) -> None:
        """
        Removes an error middleware from the processing chain.
        """
        self.middleware.remove(middleware)

    def toggle_middleware(
        self, middleware_type: Type[ErrorMiddleware], enable: bool
    ) -> None:
        """
        Enable or disable a specific middleware type in the chain.
        """
        for mw in self.middleware:
            if isinstance(mw, middleware_type):
                mw.toggle(enable)
