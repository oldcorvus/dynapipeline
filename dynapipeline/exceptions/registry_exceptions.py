"""
Contains custom exceptions related to registry operations.
"""


class RegistryError(Exception):
    """Base exception for registry-related errors."""

    pass


class ItemAlreadyRegisteredError(RegistryError):
    """Raised when an item is already registered in the registry."""

    def __init__(self, name: str):
        super().__init__(f"Item '{name}' is already registered in the registry.")


class ItemNotFoundError(RegistryError):
    """Raised when an item is not found in the registry."""

    def __init__(self, name: str):
        super().__init__(f"Item '{name}' not found in the registry.")
