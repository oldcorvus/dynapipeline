"""
    Contains tests for ErrorRegistry class
"""

from dynapipeline.exceptions.base_error import BaseError
from dynapipeline.exceptions.error_registry import ErrorRegistry


def test_add_and_get_error():
    """
    Test adding an error to the registry and retrieving it with context
    """
    error_registry = ErrorRegistry()

    error = BaseError("Test error", "TestErrorType", "high")
    error_registry.add(error, context="stage1")

    errors = error_registry.get("stage1")
    assert len(errors) == 1
    assert errors[0] == error


def test_add_to_default_context():
    """
    Test adding an error with default context
    """
    error_registry = ErrorRegistry()

    error = BaseError("Default error", "DefaultErrorType", "low")
    error_registry.add(error)

    errors = error_registry.get()
    assert len(errors) == 1
    assert errors[0] == error


def test_add_multiple_errors_to_context():
    """
    Test adding multiple errors to a single context.
    """
    error_registry = ErrorRegistry()

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
    error_registry = ErrorRegistry()

    error = BaseError("Clear test error", "ClearErrorType", "medium")
    error_registry.add(error, context="stage2")

    assert len(error_registry.get("stage2")) == 1

    error_registry.clear("stage2")

    assert len(error_registry.get("stage2")) == 0


def test_list_all_errors():
    """
    Test listing all errors from multiple contexts
    """
    error_registry = ErrorRegistry()

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
    error_registry = ErrorRegistry()

    error1 = BaseError("Error 1", "ErrorType1", "high")
    error2 = BaseError("Error 2", "ErrorType2", "medium")

    error_registry.add(error1, context="stage1")
    error_registry.add(error2, context="stage2")

    assert len(error_registry.list_items()) == 2

    error_registry.clear()

    assert len(error_registry.list_items()) == 0
