"""
   Defines stage group which allows grouping stages and sepecifying execution style
"""

from typing import List

from pydantic import Field

from dynapipeline.execution.base import CycleStrategy, ExecutionStrategy
from dynapipeline.pipelines.component import PipelineComponent
from dynapipeline.pipelines.stage import Stage


class StageGroup(PipelineComponent):
    """A pipeline stage group that can execute stages in dfiirent execution modes"""

    stages: List[Stage] = Field(
        ..., description="List of stages to be executed in the group"
    )
    cycle_strategy: CycleStrategy = Field(
        ...,
        description="Strategy to determine how the cycle of stages will be executed",
    )
    execution_strategy: ExecutionStrategy = Field(
        ..., description="Strategy to determine how each stage is executed"
    )

    async def execute(self, *args, **kwargs):
        """Executes the stage group using the provided cycle strategy and execution strategy"""
        results = await self.cycle_strategy.run(
            self.execution_strategy.execute, self.stages, *args, **kwargs
        )
        return results
