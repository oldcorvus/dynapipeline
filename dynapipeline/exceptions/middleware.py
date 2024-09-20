""" Defines Exceptions for middleware"""
from typing import Optional

from dynapipeline.exceptions.base import BaseDynapipelineError


class MiddlewareError(BaseDynapipelineError):
    """Base exception for middleware-related errors"""

    pass


class MiddlewareProcessingError(MiddlewareError):
    """Exception for middleware processing failures"""

    def __init__(self, middleware_name: str, context: Optional[str] = None):
        super().__init__(f"Error processing middleware '{middleware_name}'.", context)
