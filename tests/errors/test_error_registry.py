"""
    Contains tests for ErrorRegistry class
"""


import logging
from typing import Optional

import pytest

from dynapipeline.core.base_middleware import BaseMiddleware
from dynapipeline.errors.base import BaseError
from dynapipeline.errors.manager import ErrorManager


class MockMiddleware(BaseMiddleware[BaseError]):
    """
    Mock middleware class for testing
    """

    def _handle(self, error: BaseError) -> BaseError:
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

    registry = ErrorManager()

    registry.add_middleware(mdw1)
    registry.add_middleware(mdw2)

    assert len(registry._middleware) == 2


def test_remove_middleware():
    """
    Test that middlewares can be removed
    """
    mdw1 = MockMiddleware()
    mdw2 = MockMiddleware()

    registry = ErrorManager()

    registry.add_middleware(mdw1)
    registry.add_middleware(mdw2)

    registry.remove_middleware(mdw1)

    assert len(registry._middleware) == 1

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

        def _handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that logs the error message
            """
            logging.info(f"Handling error: {error.message}")
            return error

    mdw1 = TestMiddleware()
    registry = ErrorManager()

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

        def _handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that just returns error
            """
            # returning None simulates handling the error
            return None

    mdw1 = TestMiddleware()
    registry = ErrorManager()

    registry.add_middleware(mdw1)

    error = BaseError("Test error", "TestErrorType", "high")
    registry.add(error)

    # middleware should handled it
    assert len(registry.list_all_errors()) == 0


def test_add_and_get_error():
    """
    Test adding an error to the registry and retrieving it with context
    """
    error_registry = ErrorManager()

    error = BaseError("Test error", "TestErrorType", "high")
    error_registry.add(error, context="stage1")

    errors = error_registry.get("stage1")
    assert len(errors) == 1
    assert errors[0] == error


def test_add_to_default_context():
    """
    Test adding an error with default context
    """
    error_registry = ErrorManager()

    error = BaseError("Default error", "DefaultErrorType", "low")
    error_registry.add(error)

    errors = error_registry.get()
    assert len(errors) == 1
    assert errors[0] == error


def test_add_multiple_errors_to_context():
    """
    Test adding multiple errors to a single context.
    """
    error_registry = ErrorManager()

    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")
    error3 = BaseError("Error 3", "ErrorType1", "low")

    error_registry.add(error1, context="stage1")
    error_registry.add(error2, context="stage1")
    error_registry.add(error3, context="stage1")

    errors = error_registry.get("stage1")
    assert len(errors) == 3
    assert errors[0] == error1
    assert errors[1] == error2
    assert errors[2] == error3


def test_clear_errors_in_context():
    """
    Test clearing errors from a specific context
    """
    error_registry = ErrorManager()

    error = BaseError("Clear test error", "ClearErrorType", "medium")
    error_registry.add(error, context="stage2")

    assert len(error_registry.get("stage2")) == 1

    error_registry.clear("stage2")

    assert len(error_registry.get("stage2")) == 0


def test_list_all_errors():
    """
    Test listing all errors from multiple contexts
    """
    error_registry = ErrorManager()

    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")

    error_registry.add(error1, context="stage1")
    error_registry.add(error2, context="stage2")

    all_errors = error_registry.list_all_errors()

    assert len(all_errors) == 2
    assert error1 in all_errors
    assert error2 in all_errors


def test_clear_all_errors():
    """
    Test clearing all errors from the registry
    """
    error_registry = ErrorManager()

    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")

    error_registry.add(error1, context="stage1")
    error_registry.add(error2, context="stage2")

    assert len(error_registry.list_items()) == 2

    error_registry.clear()

    assert len(error_registry.list_items()) == 0
