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


class SemaphoreExecutionStrategy(ExecutionStrategy):
    """
    A concrete execution strategy that uses a semaphore to limit the number of concurrent executions of pipeline components
    """

    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def execute(self, components: List[PipelineComponent], *args, **kwargs):
        """
        Executes the pipeline components concurrently but limits the number of concurrent executions

        """
        tasks = [
            self._run_with_semaphore(component, *args, **kwargs)
            for component in components
        ]
        results = await asyncio.gather(*tasks)
        return results

    async def _run_with_semaphore(self, component: PipelineComponent, *args, **kwargs):
        """
        Wraps the execution of a component with a semaphore to limit concurrency

        """
        async with self.semaphore:
            return await component.run(*args, **kwargs)
