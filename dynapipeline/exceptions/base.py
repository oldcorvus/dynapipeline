"""Contains Base Exception for dynapipline"""
from typing import Optional


class DynaPipelineException(Exception):
    """Base exception for all custom errors in the Dynapipeline system"""

    def __init__(self, message: str, context: Optional[str] = None):
        self.context = context
        super().__init__(message)
