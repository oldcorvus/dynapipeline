
# Dynapipeline

`dynapipeline` is an **async-first** framework designed for building and managing data pipeline workflows. It provides flexible execution strategies and cycle strategies to run stages and stage groups in different environments, supporting a variety of execution styles. With its focus on modularity and extensibility, `dynapipeline` enables users to easily build, organize, and execute pipelines that fit their specific needs.

please check [examples folder](https://github.com/oldcorvus/dynapipeline/tree/master/examples) 

## Features

- **Async-first design**: Optimized for asyncio-based environments, allowing smooth integration of asynchronous tasks.
- **Execution Strategies**: Support for various execution styles such as sequential, concurrent, multithreading, and multiprocessing.
- **Cycle Strategies**: Control over how stages and stage groups are executed, including looping with condition, running once, or infinitely.
- **Customizable Pipelines**: Users can create their own stages and group them with different cycle and execution strategies.
- **Context Management**: Advanced context management to control shared state across pipeline components, preventing race conditions.
- **Event Handlers**: Handlers that allow users to add logic before, after, around, and on error during the execution of pipeline components.
- **Timeout Feature**: Users can specify timeouts for stages to control how long a stage should run before it times out.

## Key Components

`dynapipeline` has three primary components that work together to create flexible pipelines:

### 1. **Stage**
The basic unit of work in a pipeline. Users define their own stages by subclassing `Stage` and implementing the `execute()` method. Each stage can have custom logic and be part of a stage group. You can also specify a timeout for each stage, so it stops if it runs longer than the set limit.

### 2. **Stage Group**
A collection of stages that share a common execution strategy and cycle strategy. Stage groups allow you to group stages together and control their behavior as a single unit.

### 3. **Pipeline**
A pipeline is composed of one or more stage groups. It allows you to specify how each group of stages should be executed (using an execution strategy) and how often they should run (using a cycle strategy).

## Cycle Strategies

Control how often a group of stages is executed within a pipeline:

- **`OnceCycleStrategy`**: Executes the list of components once.
- **`LoopCycleStrategy`**: Executes the group of components for a predefined number of cycles.
- **`InfinitLoopStrategy`**: Continuously runs the group of components in a loop until an external event (such as a stop signal) is triggered.

## Execution Strategies

Control how components are executed (either concurrently, sequentially, or using multiple processes/threads):

- **`SequentialExecutionStrategy`**: Executes pipeline components one by one sequentially.
- **`ConcurrentExecutionStrategy`**: Executes pipeline components concurrently using `asyncio.gather()`.
- **`SemaphoreExecutionStrategy`**: Limits the number of concurrent executions using an asyncio semaphore.
- **`MultithreadExecutionStrategy`**: Executes pipeline components concurrently using multiple threads via `ThreadPoolExecutor`.
- **`MultiprocessExecutionStrategy`**: Executes pipeline components concurrently using multiple processes via `ProcessPoolExecutor`.

## Pipeline Types

- **`SimplePipeline`**: Uses an `AsyncLockableContext`, which prevents race conditions by utilizing asyncio locks. In the simple pipeline, execution strategies like multithread and multiprocess are restricted.
  
- **`AdvancedPipeline`**: Uses a `ProtectedContext`, which automatically locks the context before the pipeline starts and raises an error if there are any attempts to modify the context during execution. This type allows multithread and multiprocess execution strategies.

## Context Management

Each pipeline has a context shared across all components (stages, stage groups). Contexts store settings, configuration data, and other shared state:

- **`AsyncLockableContext`**: Prevents race conditions in a simple pipeline by allowing users to explicitly lock/unlock the context. You can use `async with self.context as context:` to safely modify shared state.
  
- **`ProtectedContext`**: Used in advanced pipelines, this context automatically locks during pipeline execution and prevents modifications, ensuring consistency.

## Handlers and Hooks

`dynapipeline` allows users to define custom event handlers to extend the pipeline's behavior. Handlers can be attached to stages to run at specific points during execution:

- **`before`**: Logic to execute before the stage runs.
- **`after`**: Logic to execute after the stage finishes.
- **`around`**: Logic to execute around the stage (e.g., as a wrapper around the main logic).
- **`on_error`**: Logic to execute if the stage raises an error.

Users can define their own handlers by subclassing the handler base class and attaching them to stages.

## Documentation and Tests

Documentation and tests for `dynapipeline` are **currently incomplete** but will be added soon. Stay tuned for upcoming improvements and additions.

## Examples

Please see the [examples folder](https://github.com/oldcorvus/dynapipeline/tree/master/examples) for detailed usage examples.

## Contribution

Contributions to `dynapipeline` are welcome! If you'd like to contribute, feel free to submit a pull request or report issues on GitHub.

## Installation

To install `dynapipeline`, you can use pip:

```bash
pip install dynapipeline
```

## Example Usage

```python
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
            async with self.context as ctx:
                ctx["counter"] += 1
            await asyncio.sleep(1)
            return f"Result of {self.name}"

    stage1 = CustomStage(name="Stage 1")
    stage2 = CustomStage(name="Stage 2")
    stage3 = CustomStage(name="Stage 3")
    stage4 = CustomStage(name="Stage 4")
    stage5 = CustomStage(name="Stage 5")
    stage6 = CustomStage(name="Stage 6")

    st_gp_sequential = StageGroup(
        name="StageGroup 1",
        stages=[stage1, stage2, stage3],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    st_gp_concurrent = StageGroup(
        name="StageGroup 2",
        stages=[stage4, stage5, stage6],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    factory = PipelineFactory()

    # Create a SIMPLE pipeline
    simple_pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.SIMPLE,
        name="Simple Pipeline",
        groups=[st_gp_sequential, st_gp_concurrent],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
        context_data={"counter": 1},
    )

    print("Executing SIMPLE Pipeline:")
    await simple_pipeline.run()
    print(
        f"execution time for Sequential stage group :{st_gp_sequential.execution_time}"
    )
    print(
        f"execution time for Concurrent stage group: { st_gp_concurrent.execution_time}"
    )
    print(f"execution time for pipeline: { simple_pipeline.execution_time}")


if __name__ == "__main__":
    asyncio.run(main())

```
