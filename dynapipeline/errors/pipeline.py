"""
    This module defines the StageError class which represent errors that occur during the execution of a specific stage in the pipeline
"""
from typing import Any, Dict, Optional

from dynapipeline.errors.base import BaseError
from dynapipeline.utils.error_levels import SeverityLevel


class PipelineError(BaseError):
    """
    Represents an error that affects the entire pipeline

    """

    def __init__(
        self,
        pipeline_id: str,
        pipeline_name: str,
        message: str,
        error_type: str,
        severity: SeverityLevel,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes the PipelineError with pipeline-specific information
        """
        super().__init__(
            message=message, error_type=error_type, severity=severity, context=context
        )
        self.pipeline_id = pipeline_id
        self.pipeline_name = pipeline_name

    def __repr__(self) -> str:
        """
        Returns a string representation of the PipelineError
        """
        return (
            f"{self.__class__.__name__}(id={self.error_id}, pipeline_id={self.pipeline_id}, error_type={self.error_type}, "
            f"message={self.message}, severity={self.severity}, timestamp={self.timestamp})"
        )
