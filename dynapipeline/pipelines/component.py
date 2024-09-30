"""
    Contains base class for components of dynapipeline 
"""
import uuid
from abc import abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dynapipeline.core.component import AbstractComponent
from dynapipeline.core.context import AbstractContext
from dynapipeline.core.handler_registry import AbstractHandlerRegistry
from dynapipeline.handlers.handler_registry import HandlerRegistry
from dynapipeline.utils.handler_types import HandlerType


class PipelineComponent(BaseModel, AbstractComponent):
    """
    Base class for pipeline components such as stages and stage groups pipeline
    """

    name: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), init=False)
    context: Optional[AbstractContext] = None
    handlers: AbstractHandlerRegistry = Field(default_factory=HandlerRegistry)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("name")
    def validate_name(cls, value):
        """Check that the name is non-empty string"""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("The 'name' must be non-empty string")
        return value

    async def run(self, *args, **kwargs):
        """Run component"""
        try:
            await self.handlers.notify(HandlerType.BEFORE, self, *args, **kwargs)
            if self.handlers.get(HandlerType.AROUND):
                result = await self.handlers.notify(
                    HandlerType.AROUND, self, self.execute, *args, **kwargs
                )
            else:
                result = await self.execute(*args, **kwargs)
            await self.handlers.notify(HandlerType.AFTER, self, result, *args, **kwargs)
            return result

        except Exception as e:
            await self.handlers.notify(HandlerType.ON_ERROR, self, e, *args, **kwargs)

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Abstract method that must be implemented by subclasses"""
        raise NotImplementedError("subclasses must implement 'execute' method")
