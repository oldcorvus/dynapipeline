"""
Contains tests for LoggerMiddleware
"""
import logging

import pytest

from dynapipeline.core.base_context import BaseContext
from dynapipeline.errors.base import BaseError
from dynapipeline.middlewares.logger import LoggerMiddleware
from dynapipeline.utils.error_levels import SeverityLevel


@pytest.fixture
def context():
    """
    Fixture to provide a mock BaseContext
    """
    return BaseContext()


@pytest.mark.asyncio
async def test_default_behavior_logs_error(caplog, context):
    """
    Test that the default logger logs the error when the middleware is enabled
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware(context=context, log_level=logging.ERROR)
        await middleware.handle(error)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
    assert "Test error" in caplog.text


@pytest.mark.asyncio
async def test_custom_logger(caplog, context):
    """
    Test that the custom logger logs the error correctly.
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    custom_logger = logging.getLogger("custom_logger")
    with caplog.at_level(logging.ERROR, logger="custom_logger"):
        middleware = LoggerMiddleware(
            context=context, log_level=logging.ERROR, logger=custom_logger
        )
        await middleware.handle(error)

    assert len(caplog.records) == 1
    assert caplog.records[0].name == "custom_logger"
    assert "Test error" in caplog.text


@pytest.mark.asyncio
async def test_disabled_middleware_does_not_log(caplog, context):
    """
    Test that the middleware doesn't log the error when disabled
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware(context=context, enabled=False)
        await middleware.handle(error)

    assert len(caplog.records) == 0


@pytest.mark.asyncio
async def test_toggle_middleware(caplog, context):
    """
    Test toggling the middleware on and off controls whether the error is logged.
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware(context=context, log_level=logging.ERROR)

        await middleware.handle(error)
        assert len(caplog.records) == 1

        middleware.toggle(False)
        await middleware.handle(error)

        assert len(caplog.records) == 1
