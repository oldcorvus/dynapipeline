"""
Contains tests for MiddlewareErrorRegistry
"""
import logging
from typing import Optional

import pytest

from dynapipeline.exceptions.base_error import BaseError
from dynapipeline.exceptions.middleware.base import BaseMiddleware
from dynapipeline.exceptions.middleware_registry import MiddlewareErrorRegistry


class MockMiddleware(BaseMiddleware):
    """
    Mock middleware class for testing
    """

    def handle(self, error: BaseError) -> BaseError:
        """
        Simple middleware that passes the error without handling it
        """
        return error


def test_add_middleware():
    """
    Test that middlewares can be added
    """
    mdw1 = MockMiddleware()
    mdw2 = MockMiddleware()

    registry = MiddlewareErrorRegistry()

    registry.add_middleware(mdw1)
    registry.add_middleware(mdw2)

    assert len(registry.middleware) == 2


def test_remove_middleware():
    """
    Test that middlewares can be removed
    """
    mdw1 = MockMiddleware()
    mdw2 = MockMiddleware()

    registry = MiddlewareErrorRegistry()

    registry.add_middleware(mdw1)
    registry.add_middleware(mdw2)

    registry.remove_middleware(mdw1)

    assert len(registry.middleware) == 1

    with pytest.raises(ValueError):
        registry.remove_middleware(MockMiddleware())


def test_handle_middleware(caplog):
    """
    Test that middleware handles errors
    """

    class TestMiddleware(BaseMiddleware):
        """
        Mock middleware class for testing
        """

        def handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that logs the error message
            """
            logging.info(f"Handling error: {error.message}")
            return error

    mdw1 = TestMiddleware()
    registry = MiddlewareErrorRegistry()

    registry.add_middleware(mdw1)

    error = BaseError("Test error", "TestErrorType", "high")
    with caplog.at_level(logging.INFO):
        registry.add(error)

    assert len(registry.list_all_errors()) == 1
    assert "Handling error: Test error" in caplog.text


def test_middleware_handles_error():
    """
    Test that middleware stops error chain if it handles the error
    """

    class TestMiddleware(BaseMiddleware):
        """
        Mock middleware class for testing
        """

        def handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that just returns error
            """
            # returning None simulates handling the error
            return None

    mdw1 = TestMiddleware()
    registry = MiddlewareErrorRegistry()

    registry.add_middleware(mdw1)

    error = BaseError("Test error", "TestErrorType", "high")
    registry.add(error)

    # middleware should handled it
    assert len(registry.list_all_errors()) == 0
