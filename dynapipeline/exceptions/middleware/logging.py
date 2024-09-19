"""
Defines specialized middleware to log errors using Python's logging module
"""
import logging
from typing import Optional

from exceptions.middleware.base import ErrorMiddleware

from dynapipeline.exceptions.base_error import BaseError


class LoggerMiddleware(ErrorMiddleware):
    """
    Logs errors using Python's logging module with configurable log levels.
    """

    def __init__(
        self,
        enabled: bool = True,
        description: str = "",
        logger: Optional[logging.Logger] = None,
        log_level: int = logging.ERROR,
    ):
        super().__init__(enabled, description)
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def handle(self, error: BaseError) -> BaseError:
        """
        Logs the error using the provided logger
        """
        if self.enabled:
            self._log(error)

        return error

    def _log(self, error: BaseError) -> None:
        """
        Logs the error based on its severity and log level.


        """
        severity_level = error.severity.value.lower()
        log_method = getattr(self.logger, severity_level, self.logger.error)
        log_method(f"{severity_level}: {error}")
