"""
This example demonstrates a simple pipeline workflow with two different strategies to run stages:
1. SequentialExecutionStrategy: Executes stages one by one.
2. ConcurrentExecutionStrategy: Executes stages concurrently.

It showcases the usage of a shared context (`AsyncLockableContext`), where a counter is incremented across 
multiple stages, ensuring safe access to the context data. The example also highlights the differences in 
execution time between the two strategies, as sequential execution typically takes longer compared to concurrent execution
"""
import asyncio

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import (
    ConcurrentExecutionStrategy,
    SequentialExecutionStrategy,
)
from dynapipeline.execution.cycle_strategies import OnceCycleStrategy


async def main():
    class CustomStage(Stage):
        async def execute(self, *args, **kwargs):
            print(f"Executing stage: {self.name} with {self.context['counter']}")
            async with self.context as ctx:  # Ensure race condition dosent accur by locking context
                ctx["counter"] += 1
            await asyncio.sleep(1)
            return f"Result of {self.name}"

    stage1 = CustomStage(name="Stage 1")
    stage2 = CustomStage(name="Stage 2")
    stage3 = CustomStage(name="Stage 3")
    stage4 = CustomStage(name="Stage 4")
    stage5 = CustomStage(name="Stage 5")
    stage6 = CustomStage(name="Stage 6")

    stage_group1 = StageGroup(
        name="StageGroup 1",
        stages=[stage1, stage2, stage3],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    stage_group2 = StageGroup(
        name="StageGroup 2",
        stages=[stage4, stage5, stage6],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    factory = PipelineFactory()

    # Create a SIMPLE pipeline (will use AsyncLockableContext by default)
    simple_pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Simple Pipeline",
        groups=[stage_group1, stage_group2],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
        context_data={"counter": 1},
    )

    print("Executing SIMPLE Pipeline:")
    await simple_pipeline.run()
    print(f"execution time for Stage1: {stage1.execution_time}")
    print(f"execution time for Stage2: {stage2.execution_time}")
    print(f"execution time for Stage3: {stage3.execution_time}")
    print(f"execution time for Stagegroup1 :{stage_group1.execution_time}")
    print(f"execution time for Stage4: {stage4.execution_time}")
    print(f"execution time for Stage5: {stage5.execution_time}")
    print(f"execution time for Stage6: {stage6.execution_time}")
    print(f"execution time for Stagegroup2: { stage_group2.execution_time}")
    print(f"execution time for pipeline: { simple_pipeline.execution_time}")


if __name__ == "__main__":
    asyncio.run(main())
