"""
    This module provides enumeration for stage types
"""
from enum import Enum


class StageType(Enum):
    """
    Enum representing the different types of stages in a pipeline.
    """

    INIT = "init"
    RUN = "run"
    LOOP = "loop"
    STOP = "stop"
    CLEANUP = "cleanup"
