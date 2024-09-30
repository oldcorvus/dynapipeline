"""
    Defines enumeration for handler types
"""

from enum import Enum


class HandlerType(str, Enum):
    """
    Enum representing the types of handlers in the pipeline
    """

    BEFORE = "before"
    AROUND = "around"
    AFTER = "after"
    ON_ERROR = "on_error"
