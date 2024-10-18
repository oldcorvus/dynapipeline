"""Contains Strategies for execution of components"""
import asyncio
from typing import List

from dynapipeline.execution.base import ExecutionStrategy
from dynapipeline.pipelines.component import PipelineComponent


class SequentialExecutionStrategy(ExecutionStrategy):
    """
    Executes pipeline components one by one sequentially
    """

    async def execute(self, components: List[PipelineComponent], *args, **kwargs):
        results = []
        for component in components:
            result = await component.run(*args, **kwargs)
            results.append(result)
        return results


class ConcurrentExecutionStrategy(ExecutionStrategy):
    """
    Executes pipeline components concurrently using asyncio.gather
    """

    async def execute(self, components: List[PipelineComponent], *args, **kwargs):
        tasks = [component.run(*args, **kwargs) for component in components]
        await asyncio.gather(*tasks)
