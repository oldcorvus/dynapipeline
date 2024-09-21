"""
Contains tests for ErrorRegistry class
"""

import logging
from typing import Optional

import pytest

from dynapipeline.core.base_context import BaseContext
from dynapipeline.core.base_middleware import BaseMiddleware
from dynapipeline.errors.base import BaseError
from dynapipeline.errors.manager import ErrorManager


@pytest.fixture
def context():
    """
    Fixture to provide a mock BaseContext
    """
    return BaseContext()


@pytest.fixture
def error_manager():
    """
    Fixture to provide ErrorManager instance
    """
    return ErrorManager()


class MockMiddleware(BaseMiddleware[BaseError]):
    """
    Mock middleware class for testing
    """

    async def _handle(self, error: BaseError) -> BaseError:
        """
        Simple middleware that passes the error without handling it
        """
        return error


@pytest.mark.asyncio
async def test_add_middleware(context, error_manager):
    """
    Test that middlewares can be added
    """
    mdw1 = MockMiddleware(context=context)
    mdw2 = MockMiddleware(context=context)

    error_manager.add_middleware(mdw1)
    error_manager.add_middleware(mdw2)

    assert len(error_manager._middleware) == 2


@pytest.mark.asyncio
async def test_remove_middleware(context, error_manager):
    """
    Test that middlewares can be removed
    """
    mdw1 = MockMiddleware(context=context)
    mdw2 = MockMiddleware(context=context)

    error_manager.add_middleware(mdw1)
    error_manager.add_middleware(mdw2)

    error_manager.remove_middleware(mdw1)

    assert len(error_manager._middleware) == 1

    with pytest.raises(ValueError):
        error_manager.remove_middleware(MockMiddleware(context=context))


@pytest.mark.asyncio
async def test_handle_middleware(caplog, context, error_manager):
    """
    Test that middleware handles errors
    """

    class TestMiddleware(BaseMiddleware):
        """
        Mock middleware class for testing
        """

        async def _handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that logs the error message
            """
            logging.info(f"Handling error: {error.message}")
            return error

    mdw1 = TestMiddleware(context=context)
    error_manager.add_middleware(mdw1)

    error = BaseError("Test error", "TestErrorType", "high")
    with caplog.at_level(logging.INFO):
        await error_manager.add(error)

    assert len(error_manager.list_all_errors()) == 1
    assert "Handling error: Test error" in caplog.text


@pytest.mark.asyncio
async def test_middleware_handles_error(context, error_manager):
    """
    Test that middleware stops error chain if it handles the error
    """

    class TestMiddleware(BaseMiddleware):
        """
        Mock middleware class for testing
        """

        async def _handle(self, error: BaseError) -> Optional[BaseError]:
            """
            Simple method that just returns None to simulate handling the error
            """
            return None

    mdw1 = TestMiddleware(context=context)
    error_manager.add_middleware(mdw1)

    error = BaseError("Test error", "TestErrorType", "high")
    await error_manager.add(error)

    assert len(error_manager.list_all_errors()) == 0


@pytest.mark.asyncio
async def test_add_and_get_error(error_manager):
    """
    Test adding an error to the registry and retrieving it with context
    """
    error = BaseError("Test error", "TestErrorType", "high")
    await error_manager.add(error, context="stage1")

    errors = error_manager.get("stage1")
    assert len(errors) == 1
    assert errors[0] == error


@pytest.mark.asyncio
async def test_add_to_default_context(error_manager):
    """
    Test adding an error with default context
    """
    error = BaseError("Default error", "DefaultErrorType", "low")
    await error_manager.add(error)

    errors = error_manager.get()
    assert len(errors) == 1
    assert errors[0] == error


@pytest.mark.asyncio
async def test_add_multiple_errors_to_context(error_manager):
    """
    Test adding multiple errors to a single context.
    """
    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")
    error3 = BaseError("Error 3", "ErrorType1", "low")

    await error_manager.add(error1, context="stage1")
    await error_manager.add(error2, context="stage1")
    await error_manager.add(error3, context="stage1")

    errors = error_manager.get("stage1")
    assert len(errors) == 3
    assert errors[0] == error1
    assert errors[1] == error2
    assert errors[2] == error3


@pytest.mark.asyncio
async def test_clear_errors_in_context(error_manager):
    """
    Test clearing errors from a specific context
    """
    error = BaseError("Clear test error", "ClearErrorType", "medium")
    await error_manager.add(error, context="stage2")

    assert len(error_manager.get("stage2")) == 1

    error_manager.clear("stage2")

    assert len(error_manager.get("stage2")) == 0


@pytest.mark.asyncio
async def test_list_all_errors(error_manager):
    """
    Test listing all errors from multiple contexts
    """
    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")

    await error_manager.add(error1, context="stage1")
    await error_manager.add(error2, context="stage2")

    all_errors = error_manager.list_all_errors()

    assert len(all_errors) == 2
    assert error1 in all_errors
    assert error2 in all_errors


@pytest.mark.asyncio
async def test_clear_all_errors(error_manager):
    """
    Test clearing all errors from the registry
    """
    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")

    await error_manager.add(error1, context="stage1")
    await error_manager.add(error2, context="stage2")

    assert len(error_manager.list_items()) == 2

    error_manager.clear()

    assert len(error_manager.list_items()) == 0
