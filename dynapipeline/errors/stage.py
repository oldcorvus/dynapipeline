"""
    This module defines the PipelineError class which represent errors that occur at the pipeline level

"""
from typing import Any, Dict, Optional

from dynapipeline.errors.base import BaseError
from dynapipeline.utils.error_levels import SeverityLevel


class StageError(BaseError):
    """
    Represents an error that occurs during the execution of a specific stage in the pipeline
    """

    def __init__(
        self,
        stage_id: str,
        stage_name: str,
        message: str,
        error_type: str,
        severity: SeverityLevel,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes the StageError with stage-specific information
        """
        super().__init__(
            message=message, error_type=error_type, severity=severity, context=context
        )
        self.stage_id = stage_id
        self.stage_name = stage_name

    def __repr__(self) -> str:
        """
        Returns a string representation of the StageError
        """
        return (
            f"{self.__class__.__name__}(id={self.error_id}, stage_id={self.stage_id}, stage_name={self.stage_name}, "
            f"error_type={self.error_type}, message={self.message}, severity={self.severity}, "
            f"timestamp={self.timestamp})"
        )
