"""
        Contains abstratc  component  class 
"""
from abc import ABC, abstractmethod


class AbstractComponent(ABC):
    """
    Abstract class for all pipeline components
    """

    def __init__(self, name: str):
        self.name = name

    async def run(self, *args, **kwargs):
        """
        Run the component
        """
        return await self.execute(*args, **kwargs)

    @abstractmethod
    async def execute(self, *args, **kwargs):
        """
        This is where the core logic of the component should do
        """
        raise NotImplementedError("Subclasses must implement the `execute` method")
