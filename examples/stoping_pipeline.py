"""Example demonstrating pipeline stop functionality in dynapipeline

This example defines a `FibonacciStage` that generates Fibonacci numbers in an
infinite loop using the `InfinitLoopStrategy` 
The pipeline is set to run indefinitely but is stopped explicitly after a set duration (6 seconds) to show how the pipeline stop mechanism works

"""
import asyncio

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import ConcurrentExecutionStrategy
from dynapipeline.execution.cycle_strategies import (
    InfinitLoopStrategy,
    OnceCycleStrategy,
)


class FibonacciStage(Stage):
    """Stage that reads previous Fibonacci numbers from the context and generates the next one"""

    async def execute(self, *args, **kwargs):
        prev = self.context.get("prev", 0)
        current = self.context.get("current", 1)
        # Calculate the next Fibonacci number
        next_value = prev + current
        print(f"{self.name}: Generated Fibonacci number: {next_value}")

        self.context["prev"] = current
        self.context["current"] = next_value
        await asyncio.sleep(1)


async def main():
    fibo_stage = FibonacciStage(name="Fibonacci")

    factory = PipelineFactory()

    stage_group = StageGroup(
        name="infinit stage group",
        stages=[fibo_stage],
        cycle_strategy=InfinitLoopStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )
    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Fibonacci Pipeline",
        groups=[stage_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    print("Starting Fibonacci Pipeline")
    asyncio.create_task(pipeline.run())
    print("Pipeline execution complete.")
    await asyncio.sleep(6)
    # Stoping Pipeline after 6 seconds
    pipeline.stop()


if __name__ == "__main__":
    asyncio.run(main())
