"""""
This module defines the StageTypeRegistry class, a specialized registry
for managing pipeline stage types.
"""
from dynapipeline.core.base_registry import BaseRegistry
from dynapipeline.utils.stage_types import StageType


class StageTypeRegistry(BaseRegistry[str]):
    """
    A registry for managing pipeline stage types.
    """

    def __init__(self, set_default=True) -> None:
        """
        Initializes the StageTypeRegistry with default stage types.
        """
        super().__init__()
        if set_default:
            for st_type in StageType:
                self.register(st_type.name, st_type.value)

    def reset_to_default(self) -> None:
        """
        Resets the registry to contain only the default stage types.
        """
        self.clear()
        for st_type in StageType:
            self.register(st_type.name, st_type.value)
