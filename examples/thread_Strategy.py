"""
Example demonstrating the use of MultithreadExecutionStrategy in dynapipeline for handling blocking I/O tasks

This example defines an `APICallStage` that simulates a blocking I/O operation using `time.sleep()` which represents a typical API call that may block an asyncio event loop
The example compares the performance of executing these stages with two different strategies:
1. MultithreadExecutionStrategy: Suitable for handling blocking I/O tasks preventing the event loop from being blocked
2. ConcurrentExecutionStrategy: Demonstrates the inefficiency of using a sequential execution strategy for blocking I/O tasks
"""
import asyncio
import random
import time

from pydantic import Field

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import (
    ConcurrentExecutionStrategy,
    MultithreadExecutionStrategy,
    SequentialExecutionStrategy,
)
from dynapipeline.execution.cycle_strategies import OnceCycleStrategy


class APICallStage(Stage):
    """
    Simulates Blocking I/O call (using time.sleep())
    If run in an asyncio event loop, it will block the loop
    Suitable to run with MultithreadExecutionStrategy to prevnt blocking the event loop
    """

    url: str = Field(..., description="API endpoint to call")

    async def execute(self, *args, **kwargs):
        print(f"Executing {self.name}: Calling {self.url}")
        simulated_latency = random.uniform(
            1, 3
        )  # Simulate network latency between 1 and 3 seconds
        time.sleep(simulated_latency)  # Simulating a blocking API call
        return f"{self.name}: Response from {self.url} after {simulated_latency:.2f} seconds."


async def main():
    stage1 = APICallStage(name="API Call 1", url="http://example.com/endpoint1")
    stage2 = APICallStage(name="API Call 2", url="http://example.com/endpoint2")
    stage3 = APICallStage(name="API Call 3", url="http://example.com/endpoint3")

    factory = PipelineFactory()

    # Create a stage group with the multithreading strategy suitable for Blocking IO bound calls
    stage_group = StageGroup(
        name="StageGroup 1",
        stages=[stage1, stage2, stage3],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=MultithreadExecutionStrategy(),
    )

    # Create an ADVANCED pipeline to allow multithreading or multiprocessing
    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.ADVANCED,
        name="Multithreaded Pipeline",
        groups=[stage_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    print("Executing Advanced Pipeline:")
    await pipeline.run()
    print(f"execution time for Stagegroup :{stage_group.execution_time}")
    print(f"execution time for advanced pipeline: {pipeline.execution_time}")

    # Running same stages as asyncio tasks since tasks are blocking multi threading is better
    stage_group2 = StageGroup(
        name="StageGroup 2",
        stages=[stage1, stage2, stage3],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )
    simple_pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Multithreaded Pipeline",
        groups=[stage_group2],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    print("Executing Simple Pipeline:")
    await simple_pipeline.run()
    print(f"execution time for Stagegroup2 :{stage_group2.execution_time}")
    print(f"execution time for simple pipeline: {simple_pipeline.execution_time}")


if __name__ == "__main__":
    asyncio.run(main())
