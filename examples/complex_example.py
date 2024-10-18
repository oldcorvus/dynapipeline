"""
Example demonstrating a multi-stage sensor data pipeline with event handling and monitoring

This example simulates a data pipeline that includes:

1. Sensor Stages (`TemperatureSensorStage`, `PressureSensorStage`, `HumiditySensorStage`):
   These stages simulate reading data from sensors and publish success (flow) events to the `EventBus`
   Each sensor stage uses an `asyncio.Queue` (flow queue) to publish these events

2. ThresholdMonitoringStage:
   Checks sensor values against predefined threshold values from the `config`
   If a sensor value exceeds the threshold it raises an error event and publishes it to the error queue (a thread-safe `queue.Queue`)

3. WatchdogStage:
   Continuously monitors the error queue for any error events depending on the error level it takes appropriate action (logging, sending alerts,...).

4. EventBus:
   A shared communication mechanism with two types of queues:
   - An `asyncio.Queue` for flow (success) events
   - A thread-safe `queue.Queue` for error events

The pipeline demonstrates:
- InfinitLoopStrategy for continuously reading sensor data 
- MultithreadExecutionStrategy for running the watchdog independently from the sensor stages allowing it to handle errors in parallel
- ConcurrentExecutionStrategy for simultaneous sensor data collection 

"""

import asyncio
import queue
import random
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from pydantic import Field

from dynapipeline import PipelineFactory, PipeLineType, Stage, StageGroup
from dynapipeline.execution import (
    ConcurrentExecutionStrategy,
    MultithreadExecutionStrategy,
    SequentialExecutionStrategy,
)
from dynapipeline.execution.cycle_strategies import (
    InfinitLoopStrategy,
    OnceCycleStrategy,
)


class EventType(Enum):
    FLOW = "flow"
    ERROR = "error"


class ErrorLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Event:
    event_type: EventType
    payload: dict
    error_level: ErrorLevel = ErrorLevel.INFO


class EventBus:
    def __init__(self):
        self.flow_queue = asyncio.Queue()  # Asyncio queue for flow events
        self.error_queue = queue.Queue()  # Thread-safe queue for error events

    async def publish_flow_event(self, event: Event):
        """Publish flow events to the asyncio flow queue."""
        await self.flow_queue.put(event)

    def publish_error_event(self, event: Event):
        """Publish error events to the thread-safe error queue."""
        self.error_queue.put(event)

    async def get_flow_event(self):
        """Get the next flow event from the flow queue."""
        return await self.flow_queue.get()


class TemperatureSensorStage(Stage):
    """Simulates work for a temperature sensor."""

    event_bus: Optional[EventBus] = None

    async def execute(self, *args, **kwargs):
        try:
            await asyncio.sleep(2)
            temperature = random.uniform(20.0, 35.0)  # Simulate temperature data
            print(f"{self.name}: Read temperature: {temperature:.2f}°C")

            # Publish a flow event with the temperature data
            flow_event = Event(
                event_type=EventType.FLOW,
                payload={"sensor_type": "temperature", "value": temperature},
            )
            await self.event_bus.publish_flow_event(flow_event)
        except Exception as e:
            error_event = Event(
                event_type=EventType.ERROR,
                payload={"message": str(e)},
                error_level=ErrorLevel.CRITICAL,
            )
            self.event_bus.publish_error_event(error_event)


class PressureSensorStage(Stage):
    """Simulates work for a pressure sensor."""

    event_bus: Optional[EventBus] = None

    async def execute(self, *args, **kwargs):
        try:
            await asyncio.sleep(3)
            pressure = random.uniform(950.0, 1100.0)  # Simulate pressure data
            print(f"{self.name}: Read pressure: {pressure:.2f} hPa")

            # Publish a flow event with the pressure data
            flow_event = Event(
                event_type=EventType.FLOW,
                payload={"sensor_type": "pressure", "value": pressure},
            )
            await self.event_bus.publish_flow_event(flow_event)
        except Exception as e:
            error_event = Event(
                event_type=EventType.ERROR,
                payload={"message": str(e)},
                error_level=ErrorLevel.WARNING,
            )
            self.event_bus.publish_error_event(error_event)


class HumiditySensorStage(Stage):
    """Simulates work for a humidity sensor."""

    event_bus: Optional[EventBus] = None

    async def execute(self, event_bus=None, *args, **kwargs):
        try:
            await asyncio.sleep(1.5)
            humidity = random.uniform(30.0, 70.0)  # Simulate humidity data
            print(f"{self.name}: Read humidity: {humidity:.2f}%")

            # Publish a flow event with the humidity data
            flow_event = Event(
                event_type=EventType.FLOW,
                payload={"sensor_type": "humidity", "value": humidity},
            )
            await self.event_bus.publish_flow_event(flow_event)
        except Exception as e:
            error_event = Event(
                event_type=EventType.ERROR,
                payload={"message": str(e)},
                error_level=ErrorLevel.INFO,
            )
            self.event_bus.publish_error_event(error_event)


class ThresholdMonitoringStage(Stage):
    """Monitors sensor data and checks it against predefined thresholds"""

    config: Dict[str, tuple] = Field(
        ..., description="Threshold values for each sensor"
    )
    event_queue: queue.Queue = Field(..., description="Queue for error events")
    event_bus: Optional[EventBus] = None

    async def execute(self, *args, **kwargs):
        try:
            event = await self.event_bus.get_flow_event()
            sensor_type = event.payload.get("sensor_type")
            value = event.payload.get("value")

            if sensor_type and value:
                threshold = self.config.get(sensor_type)
                if threshold:
                    min_val, max_val = threshold
                    if value < min_val or value > max_val:
                        print(
                            f"{self.name}: {sensor_type.capitalize()} reading {value:.2f} exceeds threshold [{min_val}, {max_val}]"
                        )

                        # Raise an error event if the threshold is violated
                        error_event = Event(
                            event_type=EventType.ERROR,
                            payload={
                                "message": f"{sensor_type.capitalize()} value out of range: {value:.2f}"
                            },
                            error_level=ErrorLevel.WARNING
                            if value < max_val
                            else ErrorLevel.CRITICAL,
                        )
                        self.event_queue.put(error_event)

        except Exception as e:
            error_event = Event(
                event_type=EventType.ERROR,
                payload={"message": f"Monitoring error: {str(e)}"},
                error_level=ErrorLevel.CRITICAL,
            )
            self.event_queue.put(error_event)


class WatchdogStage(Stage):
    """Watchdog that monitors the error queue and takes action based on the error level."""

    event_queue: queue.Queue = Field(..., description="Queue for error events")

    async def execute(self, *args, **kwargs):
        while True:
            try:
                event = self.event_queue.get(timeout=1)
                print(
                    f"{self.name}: Watchdog received error event: {event.payload['message']}"
                )

                if event.error_level == ErrorLevel.CRITICAL:
                    print(
                        f"{self.name}: CRITICAL ERROR! Simulating sending SMS to admin..."
                    )
                elif event.error_level == ErrorLevel.WARNING:
                    print(
                        f"{self.name}: WARNING: Simulating sending Email to admin...."
                    )
                elif event.error_level == ErrorLevel.INFO:
                    print(f"{self.name}: INFO: No critical action needed, logging.")
            except queue.Empty:
                continue
            except asyncio.CancelledError:
                print(f"{self.name}: Watchdog stage cancelled, shutting down.")
                break  # Break out of the infinite loop to stop execution


async def run_pipeline():
    event_bus = EventBus()

    sensor_thresholds = {
        "temperature": (20.0, 30.0),
        "pressure": (950.0, 1050.0),
        "humidity": (40.0, 70.0),
    }

    # Sensor stages that simulate collecting data from sensors
    temp_stage = TemperatureSensorStage(name="Temperature Sensor", event_bus=event_bus)
    pressure_stage = PressureSensorStage(name="Pressure Sensor", event_bus=event_bus)
    humidity_stage = HumiditySensorStage(name="Humidity Sensor", event_bus=event_bus)

    # Threshold checker stage that checks values retrived
    # by sensors against threahsold value defined in config
    threshold_monitor_stage = ThresholdMonitoringStage(
        name="Threshold Monitor",
        config=sensor_thresholds,
        event_queue=event_bus.error_queue,
        event_bus=event_bus,
    )

    # Watchdog stage that checks for errors and based on error type takes actions
    watchdog_stage = WatchdogStage(name="Watchdog", event_queue=event_bus.error_queue)

    sensor_group = StageGroup(
        name="Sensor Data Group",
        stages=[temp_stage, pressure_stage, humidity_stage],
        cycle_strategy=InfinitLoopStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    monitor_group = StageGroup(
        name="Threshold Monitor Group",
        stages=[threshold_monitor_stage],
        cycle_strategy=InfinitLoopStrategy(),
        execution_strategy=SequentialExecutionStrategy(),
    )

    # Create the watchdog stage group (runs independently)
    watchdog_group = StageGroup(
        name="Watchdog Group",
        stages=[watchdog_stage],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=MultithreadExecutionStrategy(),
    )

    factory = PipelineFactory()

    pipeline = factory.create_pipeline(
        pipeline_type=PipeLineType.ADVANCED,
        name="Sensor Pipeline with Watchdog",
        groups=[sensor_group, monitor_group, watchdog_group],
        cycle_strategy=OnceCycleStrategy(),
        execution_strategy=ConcurrentExecutionStrategy(),
    )

    await pipeline.run()


if __name__ == "__main__":
    asyncio.run(run_pipeline())
