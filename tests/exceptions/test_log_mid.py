"""
Contains tests for LoggerMiddleware
"""

import logging

from dynapipeline.exceptions.base_error import BaseError, SeverityLevel
from dynapipeline.exceptions.middleware.logging import LoggerMiddleware


def test_default_behavior_logs_error(caplog):
    """
    Test  default logger logs the error when the middleware is enabled
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware()
        middleware.handle(error)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
    assert "Test error" in caplog.text


def test_custom_logger(caplog):
    """
    Test custom logger logs the error correctly.
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    custom_logger = logging.getLogger("custom_logger")
    with caplog.at_level(logging.ERROR, logger="custom_logger"):
        middleware = LoggerMiddleware(logger=custom_logger)
        middleware.handle(error)

    assert len(caplog.records) == 1
    assert caplog.records[0].name == "custom_logger"
    assert "Test error" in caplog.text


def test_disabled_middleware_does_not_log(caplog):
    """
    Test  the middleware doesnt log the error when disabled
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware(enabled=False)
        middleware.handle(error)

    assert len(caplog.records) == 0


def test_toggle_middleware(caplog):
    """
    Test  toggling the middleware on and off controls whether the error is logged.
    """
    error = BaseError("Test error", "TestErrorType", SeverityLevel.ERROR)

    with caplog.at_level(logging.ERROR):
        middleware = LoggerMiddleware()

        middleware.handle(error)
        assert len(caplog.records) == 1

        middleware.toggle(False)
        middleware.handle(error)

        assert len(caplog.records) == 1
