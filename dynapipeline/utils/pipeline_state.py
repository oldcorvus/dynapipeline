"""
This module provides enumeration for pipline state"""
from enum import Enum


class PiplineState(Enum):
    """Enumeration for pipeline state"""

    NOT_STARTED = "not_started"
    INITIALIZED = "initialized"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
