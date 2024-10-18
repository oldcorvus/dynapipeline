"""Example demonstrating the use of SemaphoreExecutionStrategy to implement rate limiting

This example simulates making API calls with a rate limit achieved using the
`SemaphoreExecutionStrategy` which allows controlling the maximum number of concurrent tasks
"""
import asyncio
import random

from pydantic import Field

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import (
    SemaphoreExecutionStrategy,
    SequentialExecutionStrategy,
)
from dynapipeline.execution.cycle_strategies import OnceCycleStrategy


class RateLimitedAPICallStage(Stage):
    """Simulates an API call with rate limiting, suitable for SemaphoreExecutionStrategy."""

    url: str = Field(..., description="API endpoint to call")

    async def execute(self, *args, **kwargs):
        print(f"Executing {self.name}: Calling {self.url}")
        simulated_latency = random.uniform(
            1, 3
        )  # Simulate network latency between 1 and 3 seconds
        await asyncio.sleep(simulated_latency)  # Simulate async API call
        print(
            f"{self.name}: Response from {self.url} after {simulated_latency:.2f} seconds."
        )
        return f"{self.name}: Response from {self.url} after {simulated_latency:.2f} seconds."


async def main():
    stage1 = RateLimitedAPICallStage(
        name="API Call 1", url="http://example.com/endpoint1"
    )
    stage2 = RateLimitedAPICallStage(
        name="API Call 2", url="http://example.com/endpoint2"
    )
    stage3 = RateLimitedAPICallStage(
        name="API Call 3", url="http://example.com/endpoint3"
    )
    stage4 = RateLimitedAPICallStage(
        name="API Call 4", url="http://example.com/endpoint4"
    )
    stage5 = RateLimitedAPICallStage(
        name="API Call 5", url="http://example.com/endpoint5"
    )

    factory = PipelineFactory()

    # stage group with the semaphore strategy (limit to 2 concurrent tasks)
    stage_group = StageGroup(
        name="RateLimited StageGroup",
        stages=[stage1, stage2, stage3, stage4, stage5],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SemaphoreExecutionStrategy(max_concurrent=2),
    )

    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="RateLimited Pipeline",
        groups=[stage_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    print("Executing Rate-Limited Pipeline:")
    results = await pipeline.run()
    print(f"results: {results}")
    print(f"Execution time for StageGroup: {stage_group.execution_time}")
    print(f"Execution time for Pipeline: {pipeline.execution_time}")


if __name__ == "__main__":
    asyncio.run(main())
