"""Contains Strategies for specifying how often a component should run"""
import asyncio
from typing import Any, Callable, List, Optional

from dynapipeline.execution.base import CycleStrategy
from dynapipeline.pipelines.component import PipelineComponent


class OnceCycleStrategy(CycleStrategy):
    """Executes the list of components once"""

    async def run(
        self,
        execute_fn: Callable[[List[PipelineComponent], Any], Any],
        components: List[PipelineComponent],
        *args: Any,
        **kwargs: Any
    ) -> None:
        result = await execute_fn(components, *args, **kwargs)
        return result


class InfinitLoopStrategy(CycleStrategy):
    """Executes the group of components in a loop until event is set or pipeline stops"""

    def __init__(self, event: Optional[asyncio.Event] = None) -> None:
        self.event = event

    async def run(
        self,
        execute_fn: Callable[[List[PipelineComponent], Any], Any],
        components: List[PipelineComponent],
        *args: Any,
        **kwargs: Any
    ) -> None:
        if self.event is None:
            while True:
                await execute_fn(components, *args, **kwargs)

        # If an event is provided loop until the event is set
        else:
            while not self.event.is_set():
                await execute_fn(components, *args, **kwargs)


class LoopCycleStrategy(CycleStrategy):
    """Executes the group of components in a specified cycles"""

    def __init__(self, cycles: int) -> None:
        self.cycles = cycles

    async def run(
        self,
        execute_fn: Callable[[List[PipelineComponent], Any], Any],
        components: List[PipelineComponent],
        *args: Any,
        **kwargs: Any
    ) -> Any:
        results = []
        for _ in range(self.cycles):
            result = await execute_fn(components, *args, **kwargs)
            results.append(result)
        return results
