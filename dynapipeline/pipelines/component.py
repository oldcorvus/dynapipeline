"""
    Contains base class for components of dynapipeline 
"""
import uuid
from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dynapipeline.core.component import AbstractComponent
from dynapipeline.core.context import AbstractContext


class PipelineComponent(BaseModel, AbstractComponent):
    """
    Base class for pipeline components such as stages and stage groups pipeline
    """

    name: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), init=False)
    context: Optional[AbstractContext] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("name")
    def validate_name(cls, value):
        """Check that the name is non-empty string"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The 'name' must be non-empty string")
        return value

    async def run(self, *args, **kwargs):
        """Run component"""

        return super().run(self, *args, **kwargs)

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Abstract method that must be implemented by subclasses"""
        raise NotImplementedError("subclasses must implement 'execute' method")
