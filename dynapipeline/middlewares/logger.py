"""
Defines middleware to log with pythons logging package
"""

import logging
from typing import Any, Dict, Optional

from injector import inject

from dynapipeline.core.base_middleware import BaseMiddleware
from dynapipeline.core.context import BaseContext
from dynapipeline.utils.types import T


class LoggerMiddleware(BaseMiddleware[T]):
    """
    Middleware to log any item
    """

    @inject
    def __init__(
        self,
        context: BaseContext,
        enabled: bool = True,
        description: str = "",
        logger: Optional[logging.Logger] = None,
        log_level: int = logging.INFO,
        log_format: Optional[str] = None,
        extra_context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(context, enabled, description)
        self.logger = logger or logging.getLogger(__name__)
        self.log_level = log_level
        self.log_format = log_format or "{item}"
        self.extra_context = extra_context or {}

    async def _handle(self, item: T) -> T:
        """
        Logs the item using the provided logger with custom formating
        """
        if self.logger.isEnabledFor(self.log_level):
            log_message = self.log_format.format(item=str(item), **self.extra_context)
            self.logger.log(self.log_level, log_message)

        return item
