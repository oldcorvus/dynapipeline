"""
    This module defines the BaseError class, which provides a foundation for handling error

"""
import datetime
import uuid
from typing import Any, Dict, Optional

from utils.error_levels import SeverityLevel


class BaseError:
    """
    Base class for all errors in the pipeline, containing common attributes.
    """

    def __init__(
        self,
        message: str,
        error_type: str,
        severity: SeverityLevel,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes the BaseError with relevant details.
        """
        self.error_id = str(uuid.uuid4())
        self.message = message
        self.error_type = error_type
        self.timestamp = datetime.datetime.now()
        self.severity = severity
        self.context = context or {}

    def __repr__(self) -> str:
        """
        Returns a string representation of the BaseError for debugging.
        """
        return f"{self.__class__.__name__}(id={self.error_id}, error_type={self.error_type}, message={self.message}, severity={self.severity}, timestamp={self.timestamp})"
