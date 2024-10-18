"""
Example demonstrating the use of the InfinitLoopStrategy with asyncio event-driven stopping condition in dynapipeline

This example defines two types of stages:
1. `DataProcessorStage`: Simulates data processing and sets a result upon completion. It uses an asyncio event to signal the watcher once the data processing is done
2. `WatcherStage`: Continuously checks for the asyncio event to be set indicating that the data processing has completed It waits for the event fetches the result and processes it

The pipeline utilizes the `InfinitLoopStrategy` running the stages continuously until the asyncio event is triggered which stops the pipeline
"""

import asyncio
import random
from typing import Optional

from pydantic import Field

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import ConcurrentExecutionStrategy
from dynapipeline.execution.cycle_strategies import (
    InfinitLoopStrategy,
    OnceCycleStrategy,
)


class WatcherStage(Stage):
    """Watches for the completion of data processing and reacts"""

    watch_interval: float = Field(
        ..., description="Interval (in seconds) to check for result"
    )
    result_event: asyncio.Event
    result: Optional[str] = None

    async def execute(self, *args, **kwargs):
        print(f"{self.name}: Watching for result...")
        while (
            not self.result_event.is_set()
        ):  # Check until the event is set by the data processor
            print(
                f"{self.name}: No result yet, checking again in {self.watch_interval} seconds..."
            )
            await asyncio.sleep(self.watch_interval)

        # Once the event is set fetch the result
        print(f"{self.name}: Result received! Processing result...")
        self.result = self.context["result"]
        print(f"{self.name}: Result processed: {self.result}")


class DataProcessorStage(Stage):
    """Simulates data processing and sets the result when done"""

    result_event: asyncio.Event
    result: Optional[str] = None

    async def execute(self, *args, **kwargs):
        print(f"{self.name}: Processing data...")
        process_time = random.uniform(1, 3)
        await asyncio.sleep(process_time)
        self.result = f"{self.name} Processed data after {process_time:.2f} seconds."
        print(f"{self.name}: Data processing complete. Result: {self.result}")
        self.context["result"] = self.result

        # Signal the watcher that processing is done by setting the event
        self.result_event.set()


async def main():
    result_event = asyncio.Event()

    data_processor = DataProcessorStage(name="DataProcessor", result_event=result_event)
    data_processor2 = DataProcessorStage(
        name="DataProcessor2", result_event=result_event
    )
    # Watcher checks for event set for the first DataProcessor that completes
    watcher = WatcherStage(name="Watcher", watch_interval=1, result_event=result_event)

    factory = PipelineFactory()

    stage_group = StageGroup(
        name="ConcurrentProcessing",
        stages=[data_processor, data_processor2, watcher],
        cycle_strategy=InfinitLoopStrategy(event=result_event),
        execution_strategy=ConcurrentExecutionStrategy(),  # Run both stages concurrently
    )
    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Concurrent Data Processing Pipeline",
        groups=[stage_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    print("Starting concurrent data processor and watcher...")
    await pipeline.run()
    print("Pipeline execution complete.")


if __name__ == "__main__":
    asyncio.run(main())
