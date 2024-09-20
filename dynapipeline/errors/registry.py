"""
Defines ErrorRegistry class for managing errors
"""

from collections import defaultdict
from typing import List, Optional

from dynapipeline.core.base_registry import BaseRegistry
from dynapipeline.errors.base import BaseError
from dynapipeline.middlewares.mixin import MiddlewareMixin


class ErrorRegistry(BaseRegistry[List[BaseError]], MiddlewareMixin[BaseError]):
    """
    A registry class for managing multiple errors in a system
    """

    def __init__(self):
        BaseRegistry.__init__(self)
        MiddlewareMixin.__init__(self)

        self._items = defaultdict(list)

    def add(self, error: BaseError, context: str = "default") -> None:
        """
        Adds an error to the registry for optional context
        """
        error = self.process_with_middleware(error)
        if error is not None:
            self._items[context].append(error)

    def get(self, context: str = "default") -> List[BaseError]:
        """
        Retrieves all errors for a given context or for the default context
        """
        return self._items[context]

    def list_all_errors(self) -> List[BaseError]:
        """
        Lists all errors across all contexts.
        """
        all_errors = []
        for error_list in self._items.values():
            all_errors.extend(error_list)
        return all_errors

    def clear(self, context: Optional[str] = None) -> None:
        """
        Clears all errors for a given context or all errors if no context is provided
        """
        if context:
            self._items.pop(context, None)
        else:
            self._items.clear()
