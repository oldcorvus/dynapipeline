"""
This module defines the ErrorManager class, responsible for managing error handling middleware 
and storing pipeline errors by stage.
"""

from typing import Dict, List, Optional, Type

from dynapipeline.exceptions.base_error import BaseError
from dynapipeline.exceptions.middleware.base_middleware import ErrorMiddleware


class ErrorManager:
    """
    Manages the error middleware chain and stores errors.
    """

    def __init__(self) -> None:
        self.errors: Dict[str, List[BaseError]] = {}
        self.middleware: List[ErrorMiddleware] = []

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

    def add_error(self, stage: str, error: BaseError) -> None:
        """
        Adds an error for a given stage and processes it through the middleware chain.


        """
        for mw in self.middleware:
            if mw.enabled:
                error = mw.handle(error)

        self.errors.setdefault(stage, []).append(error)

    def get_errors(self, stage: Optional[str] = None) -> List[BaseError]:
        """
        Retrieves errors for a specific stage or all stages.

        """
        if stage:
            return self.errors.get(stage, [])
        return [
            error for stage_errors in self.errors.values() for error in stage_errors
        ]

    def clear_errors(self, stage: Optional[str] = None) -> None:
        """
        Clears all errors or errors for a specific stage.
        """
        if stage:
            self.errors.pop(stage, None)
        else:
            self.errors.clear()

    def toggle_middleware(
        self, middleware_type: Type[ErrorMiddleware], enable: bool
    ) -> None:
        """
        Enable or disable a specific middleware type in the chain.
        """
        for mw in self.middleware:
            if isinstance(mw, middleware_type):
                mw.toggle(enable)
