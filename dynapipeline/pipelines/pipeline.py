""" Contains Pipeline component which allows grouping GroupStages and specifiying execution style"""
import asyncio
from typing import List, Optional

from pydantic import Field, ValidationInfo, field_validator

from dynapipeline.execution.base import CycleStrategy, ExecutionStrategy
from dynapipeline.execution.strategies import (
    MultiprocessExecutionStrategy,
    MultithreadExecutionStrategy,
)
from dynapipeline.pipelines.component import PipelineComponent
from dynapipeline.pipelines.stage_group import StageGroup
from dynapipeline.utils.pipeline_types import PipeLineType


class Pipeline(PipelineComponent):
    """
    A pipeline class that can execute stage groups in different execution modes
    """

    pipeline_type: PipeLineType = Field(
        ..., description="The type of the pipeline (SIMPLE, ADVANCED, CUSTOM)"
    )

    stage_groups: List[StageGroup] = Field(
        ..., description="List of stage groups to be executed in the pipeline"
    )
    cycle_strategy: CycleStrategy = Field(
        ...,
        description="Strategy to determine how the cycle of stages will be executed",
    )
    execution_strategy: ExecutionStrategy = Field(
        ..., description="Strategy to determine how each stage group is executed"
    )
    pipeline_task: Optional[asyncio.Task] = None

    @field_validator("execution_strategy")
    @classmethod
    def validate_execution_strategy(cls, execution_strategy, values: ValidationInfo):
        """
        Validate the execution strategies of pipeline
        For SIMPLE pipelines, pipeline cannot use Multithread or Multiprocess strategies
        """
        pipeline_type = values.data.get("pipeline_type")
        if pipeline_type == PipeLineType.SIMPLE:
            if isinstance(
                execution_strategy,
                (MultithreadExecutionStrategy, MultiprocessExecutionStrategy),
            ):
                raise ValueError(
                    "Multithread and Multiprocess strategies are not allowed for SIMPLE pipelines."
                )
        return execution_strategy

    @field_validator("stage_groups")
    @classmethod
    def validate_stage_groups(cls, stage_groups, values: ValidationInfo):
        """
        Validate the execution strategies of all stage groups in the pipeline
        For SIMPLE pipelines, stage groups cannot use Multithread or Multiprocess strategies
        """
        pipeline_type = values.data.get("pipeline_type")
        if pipeline_type == PipeLineType.SIMPLE:
            for group in stage_groups:
                if isinstance(
                    group.execution_strategy,
                    (MultithreadExecutionStrategy, MultiprocessExecutionStrategy),
                ):
                    raise ValueError(
                        f"Stage group '{group.name}' uses Multithread or Multiprocess strategy, which is not allowed for SIMPLE pipelines."
                    )
        return stage_groups

    async def execute(self, *args, **kwargs):
        """
        Executes the stage groups using the provided cycle strategy and execution strategy
        """
        if self.pipeline_type == PipeLineType.ADVANCED:
            self.context.lock()
        if not self.pipeline_task or self.pipeline_task.done():
            self.pipeline_task = asyncio.create_task(
                self.cycle_strategy.run(
                    self.execution_strategy.execute, self.stage_groups, *args, **kwargs
                )
            )
            results = await self.pipeline_task
            return results
        else:
            raise RuntimeError("Pipeline is already running")

    def stop(self):
        """
        Cancels the pipeline task if it's running
        """
        if self.pipeline_task and not self.pipeline_task.done():
            self.pipeline_task.cancel()
