"""
    Defines Exception for registry
"""
from typing import Optional

from dynapipeline.exceptions.base import DynaPipelineException


class RegistryError(DynaPipelineException):
    """Base exception for registry related errors"""

    pass


class ItemAlreadyRegisteredError(RegistryError):
    """Exception for already registered items in the registry"""

    def __init__(self, name: str, context: Optional[str] = None):
        super().__init__(
            f"Item '{name}' is already registered in the registry.", context
        )


class ItemNotFoundError(RegistryError):
    """Exception for missing items in the registry"""

    def __init__(self, name: str, context: Optional[str] = None):
        super().__init__(f"Item '{name}'is not found in the registry", context)
