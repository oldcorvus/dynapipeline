"""
This module defines the StateRegistry class, which is used to manage pipeline states
"""
from dynapipeline.core.base_registry import BaseRegistry
from dynapipeline.utils.pipeline_state import PiplineState


class StateRegistry(BaseRegistry[str]):
    """StateRegistry is a registry designed to manage the different states"""

    def __init__(self, set_default=True) -> None:
        super().__init__()
        if set_default:
            for state in PiplineState:
                self.register(state.name, state.value)

    def reset_to_default(self) -> None:
        """
        Resets the registry to contain only the default pipeline states.
        """
        self.clear()
        for state in PiplineState:
            self.register(state.name, state.value)
