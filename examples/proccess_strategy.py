"""
Example comparing the execution time of SequentialExecutionStrategy and MultiprocessExecutionStrategy for CPU-bound tasks like prime number calculation in dynapipeline
This example defines a `PrimeStage` that calculates prime numbers within a given range. The example showcases the performance difference between two strategies:
1. SequentialExecutionStrategy: Executes stages one by one, demonstrating longer execution time for CPU-heavy tasks
2. MultiprocessExecutionStrategy: Runs stages concurrently in separate processes leading to improved performance for CPU-bound tasks by utilizing parallelism
"""
import asyncio

from pydantic import Field

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import (
    MultiprocessExecutionStrategy,
    SequentialExecutionStrategy,
)
from dynapipeline.execution.cycle_strategies import OnceCycleStrategy


def find_primes(start, end):
    primes = []
    for num in range(start, end):
        is_prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes


class PrimeStage(Stage):
    start: int = Field(..., description="Start of the range for prime number search")
    end: int = Field(..., description="End of the range for prime number search")

    async def execute(self, *args, **kwargs):
        print(f"Executing {self.name} to find primes from {self.start} to {self.end}")

        result = find_primes(self.start, self.end)
        print(f"{self.name}: Found {len(result)} primes.")
        return f"Result of {self.name}: {len(result)} primes found."


async def main():
    stage1 = PrimeStage(name="Stage 1", start=2, end=500000)

    stage_group1 = StageGroup(
        name="StageGroup 1",
        stages=[stage1],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    factory = PipelineFactory()

    # Create a SIMPLE pipeline (will use AsyncLockableContext by default)
    simple_pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Simple Pipeline",
        groups=[stage_group1],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    print("Executing SIMPLE Pipeline:")
    await simple_pipeline.run()
    print(f"execution time for Stage1: {stage1.execution_time}")
    print(f"execution time for Stagegroup1 :{stage_group1.execution_time}")
    print(f"execution time for pipeline: { simple_pipeline.execution_time}")

    stage2 = PrimeStage(name="Stage 2", start=2, end=250000)
    stage3 = PrimeStage(name="Stage 3", start=250001, end=500000)

    # stage group containing two stages that should run parell
    stage_group2 = StageGroup(
        name="StageGroup 2",
        stages=[stage2, stage3],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=MultiprocessExecutionStrategy(),
    )

    # to use (MultiprocessExecutionStrategy, or MultithreadsExecutionStrategy) pipeline type should be Advanced
    # when pipeline type is Advanced context is locked when pipeline runs preventing any modification
    advanced_pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.ADVANCED,
        name="Advanced Pipeline",
        groups=[stage_group2],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    print("Executing ADVANCED Pipeline:")
    await advanced_pipeline.run()
    print(f"execution time for Stagegroup2 :{stage_group2.execution_time}")
    print(f"execution time for pipeline: { advanced_pipeline.execution_time}")


if __name__ == "__main__":
    asyncio.run(main())
