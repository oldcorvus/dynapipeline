"""
    Defines the base abstract class for error middleware in the pipeline.
"""

from dynapipeline.core.base_middleware import BaseMiddleware
from dynapipeline.exceptions.base_error import BaseError


class ErrorMiddleware(BaseMiddleware[BaseError]):
    """
    Abstract base class for processing errors in the pipeline.
    """

    def handle(self, error: BaseError) -> BaseError:
        """
        Handle the given error.
        """
        return error
