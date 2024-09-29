"""
    Conatins execptions realted to context 
"""
from typing import Optional

from dynapipeline.exceptions.base import DynaPipelineException


class ContextLockedError(DynaPipelineException):
    """Raised when an attempt is made to modify a locked context"""

    def __init__(self, message: str = "The context is locked and cannot be modified"):
        super().__init__(message)


class ContextKeyError(DynaPipelineException):
    """Raised when there is an issue with a key in the context"""

    def __init__(self, key: str, message: Optional[str] = None):
        if message is None:
            message = f"Key '{key}' not found in the context"
        super().__init__(message)
