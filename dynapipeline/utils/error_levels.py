"""
This module provides enumeration for severity level
"""
from enum import Enum


class SeverityLevel(Enum):
    """
    Enum representing the severity levels for errors in the pipeline.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
