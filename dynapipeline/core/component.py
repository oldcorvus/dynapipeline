"""
        Contains pipeline component abstract class 
"""
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from dynapipeline.core.context import AbstractContext


@dataclass
class PipelineComponent(BaseModel, ABC):
    """
    Base class for pipeline components such as stages and stage groups, pipeline
    """

    name: str
    context: Optional[AbstractContext] = None
    _id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="id", init=False)

    @field_validator("name")
    def validate_name(cls, value):
        """Ensure that the name is a non-empty string"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The 'name' must be a non-empty string.")
        return value

    class Config:
        """Pydantic configuration"""

        allow_mutation = False
        arbitrary_types_allowed = True

    @property
    def id(self) -> str:
        """Read-only property for the unique ID"""
        return self._id

    async def run(self, *args, **kwargs):
        """Run the component with handler support"""

        return await self.execute(*args, **kwargs)

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Abstract method that must be implemented by subclasses"""
        raise NotImplementedError("subclasses must implement 'execute' method")
