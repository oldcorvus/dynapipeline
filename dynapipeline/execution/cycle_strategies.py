"""Contains Strategies for specifying how often a component should run"""
from typing import Any, Callable, List

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
