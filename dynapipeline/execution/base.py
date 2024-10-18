""" Contains Base Strategy classes"""
from abc import ABC, abstractmethod
from typing import Any, Callable, List

from dynapipeline.pipelines.component import PipelineComponent


class CycleStrategy(ABC):
    """
    Abstract base class for defining how often a group of pipeline components should run
    """

    @abstractmethod
    async def run(
        self,
        execute_fn: Callable[[List[PipelineComponent], Any], None],
        components: List[PipelineComponent],
        *args,
        **kwargs
    ):
        """
        Defines how often to run the pipeline components.

        """
        raise NotImplementedError("Cycle strategy is not implemented")


class ExecutionStrategy(ABC):
    """
    Abstract base class for execution mode strategies for pipeline components"""

    @abstractmethod
    async def execute(self, components: List[PipelineComponent], *args, **kwargs):
        """
        Executes the list of pipeline components according to strategy
        """
        raise NotImplementedError("Execution strategy is not implemented")
