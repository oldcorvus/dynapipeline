"""Defines enumeration for PipelineType"""
from enum import Enum


class PipeLineType(Enum):
    """Enum for Pipeline type"""

    SIMPLE = "simple"
    ADVANCED = "advanced"
    CUSTOM = "custom"
