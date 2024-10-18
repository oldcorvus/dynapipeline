"""
Contains PipelineFactory for creating and managing pipelines within  dynapipeline framework
"""
from typing import Any, Dict, List, Optional

from dynapipeline.contexts.async_ctx import AsyncLockableContext
from dynapipeline.contexts.protected import ProtectedContext
from dynapipeline.core.context import AbstractContext
from dynapipeline.execution.base import CycleStrategy, ExecutionStrategy
from dynapipeline.pipelines.pipeline import Pipeline
from dynapipeline.pipelines.stage_group import StageGroup
from dynapipeline.utils.pipeline_types import PipeLineType


class PipelineFactory:
    """
    A factory class for creating and configuring pipelines"""

    def create_pipeline(
        self,
        pipeline_type: PipeLineType,
        name: str,
        groups: List[StageGroup],
        cycle_strategy: CycleStrategy,
        execution_strategy: ExecutionStrategy,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> Pipeline:
        """
        Method to create and return a Pipeline instance
        """
        pipeline = Pipeline(
            name=name,
            pipeline_type=pipeline_type,
            stage_groups=groups,
            cycle_strategy=cycle_strategy,
            execution_strategy=execution_strategy,
        )
        context = self.get_context(pipeline_type, context_data)
        self.inject_context(context, pipeline)
        return pipeline

    def get_context(
        self, pipeline_type: PipeLineType, context_data: Optional[Dict[str, Any]] = None
    ):
        """Determines and returns the appropriate context for the given pipeline type"""
        match pipeline_type:
            case PipeLineType.SIMPLE:
                return AsyncLockableContext(context_data)
            case PipeLineType.ADVANCED:
                return ProtectedContext(context_data)

            case _:
                raise ValueError("Invalid pipeline type")

    def inject_context(self, context: AbstractContext, pipeline: Pipeline):
        """
        Injects the context into the pipeline, its stage groups, and individual stages
        """
        pipeline.set_context(context)

        for stage_group in pipeline.stage_groups:
            stage_group.set_context(context)

            for stage in stage_group.stages:
                stage.set_context(context)
