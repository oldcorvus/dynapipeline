"""
Defines the PipelineContext class which allows dynamic key-value management and managing
errors
"""

from typing import Optional

from dynapipeline.core.context import BaseContext
from dynapipeline.errors.base import BaseError
from dynapipeline.errors.manager import ErrorManager
from dynapipeline.utils.types import T


class PipelineContext(BaseContext[T]):
    """
    Context class that manages both pipeline data and errors
    """

    def __init__(
        self,
        raise_on_missing: bool = False,
        error_registry: Optional[ErrorManager] = None,
    ) -> None:
        super().__init__(raise_on_missing)
        self._error_registry = error_registry or ErrorManager()

    async def add_error(self, error: BaseError, context: str = "default") -> None:
        """
        Adds an error to the error registry

        """
        await self._error_registry.add(error, context)

    def get_errors(self, context: str = "default") -> list[BaseError]:
        """
        Retrieves all errors from the error registry for a given context
        """
        return self._error_registry.get(context)

    def list_all_errors(self) -> list[BaseError]:
        """
        Lists all errors across all contexts in the error registry

        """
        return self._error_registry.list_all_errors()

    def clear_errors(self, context: Optional[str] = None) -> None:
        """
        Clears errors for a given context or clears all errors if no context is specified
        """
        self._error_registry.clear(context)
