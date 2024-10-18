""" 
Example demonstrating the timeout behavior of pipeline stages in dynapipeline
The pipeline is set to run in an infinite loop using the 
`InfinitLoopStrategy`, while the stage timeout behavior can be observed when a 
stage execution exceeds the specified limit
"""
import asyncio
import math
import random

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import SequentialExecutionStrategy
from dynapipeline.execution.cycle_strategies import (
    InfinitLoopStrategy,
    OnceCycleStrategy,
)


def catalan_number(n: int) -> int:
    """Utility function to calculate the nth Catalan number"""
    return math.comb(2 * n, n) // (n + 1)


class CatalanStage(Stage):
    """Stage that generates Catalan numbers with a timeout"""

    async def execute(self, *args, **kwargs):
        # Retrieve the last index n from the context defaulting to 0
        n = self.context.get("n", 0)

        # Calculate the next Catalan number
        next_catalan = catalan_number(n)
        print(f"{self.name}: Generated Catalan number C({n}) = {next_catalan}")

        self.context["n"] = n + 1

        delay = random.uniform(1, 6)
        await asyncio.sleep(delay)

        return next_catalan


async def main():
    # Change timeout and observe behavior
    catalan_stage = CatalanStage(name="Catalan", timeout=5)

    factory = PipelineFactory()

    stage_group = StageGroup(
        name="catalan stage group",
        stages=[catalan_stage],
        cycle_strategy=InfinitLoopStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Catalan Pipeline",
        groups=[stage_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    # Run the pipeline and observe timeout behavior
    try:
        await pipeline.run()
    except asyncio.TimeoutError:
        print("A stage timed out.")


if __name__ == "__main__":
    asyncio.run(main())
