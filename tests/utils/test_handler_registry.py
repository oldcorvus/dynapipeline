"""
    Contains tests for HandlerRegistry
"""
from typing import Any, Awaitable, Callable

import pytest

from dynapipeline.handlers.handler_registry import HandlerRegistry


class TestHandlerOne:
    """First test handler"""

    __test__ = False

    def __init__(self, component):
        self.component = component
        self.reset_flags()

    def before(self, *args, **kwargs):
        """test implimentation for before method"""
        self.before_called = True

    async def after(self, result, *args, **kwargs):
        """test implimentation for after method"""

        self.after_called = True
        self.after_result = result

    def on_error(self, error: Exception, *args, **kwargs):
        """test implimentation for on errror method"""

        self.error_called = True
        self.error_message = str(error)

    def reset_flags(self):
        """to rest falgs"""

        self.before_called = False
        self.after_called = False
        self.error_called = False


class TestHandlerTwo:
    """Second test handler"""

    __test__ = False

    def __init__(self, component):
        self.component = component
        self.reset_flags()

    async def around(
        self, execute: Callable[..., Awaitable[Any]], *args, **kwargs
    ) -> Any:
        """test implimentation for around method"""

        self.around_called = True
        return await execute(*args, **kwargs)

    def reset_flags(self):
        """to rest falgs"""

        self.around_called = False
        self.before_called = False


class TestHandlerThree:
    """Third test handler"""

    __test__ = False

    def __init__(self, component):
        self.component = component
        self.reset_flags()

    def before(self, *args, **kwargs):
        """test implimentation for before method"""

        self.before_called = True

    def on_error(self, error: Exception, *args, **kwargs):
        """test implimentation for on error method"""

        self.error_called = True
        self.error_message = str(error)

    def reset_flags(self):
        """to reset flags"""

        self.before_called = False
        self.error_called = False


class Component:
    """test compoenent"""

    def __init__(self, name):
        self.name = name


@pytest.fixture
def test_component():
    """Fixture to create TestComponent"""
    return Component(name="test")


@pytest.fixture
def handler_registry():
    """Fixture to create HandlerRegistry"""
    return HandlerRegistry()


@pytest.fixture
def test_handler_one(test_component):
    """Fixture to create TestHandlerOne"""
    handler = TestHandlerOne(component=test_component)
    handler.reset_flags()
    return handler


@pytest.fixture
def test_handler_two(test_component):
    """Fixture to create a TestHandlerTwo"""
    handler = TestHandlerTwo(component=test_component)
    handler.reset_flags()
    return handler


@pytest.fixture
def test_handler_three(test_component):
    """Fixture to create a TestHandlerThree"""
    handler = TestHandlerThree(component=test_component)
    handler.reset_flags()
    return handler


@pytest.mark.asyncio
async def test_no_methods_registered(
    handler_registry,
    test_handler_one,
    test_handler_two,
    test_handler_three,
    test_component,
):
    """Test notifying a non-registered method does nothing"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])

    await handler_registry.notify("non_existent_method", test_component)

    assert test_handler_one.before_called is False
    assert test_handler_one.after_called is False
    assert test_handler_one.error_called is False
    assert test_handler_two.around_called is False
    assert test_handler_three.before_called is False
    assert test_handler_three.error_called is False


@pytest.mark.asyncio
async def test_notify_on_error(
    handler_registry,
    test_handler_one,
    test_handler_two,
    test_handler_three,
    test_component,
):
    """Test notifying the 'on_error' event calls the correct handler"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])
    await handler_registry.notify("on_error", Exception("Test error"))

    assert test_handler_one.error_called is True
    assert test_handler_one.error_message == "Test error"
    assert test_handler_three.error_called is True
    assert test_handler_three.error_message == "Test error"


@pytest.mark.asyncio
async def test_register_methods(
    handler_registry, test_handler_one, test_handler_two, test_handler_three
):
    """Test that handler methods are correctly registered"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])

    assert "before" in handler_registry._items
    assert "after" in handler_registry._items
    assert "on_error" in handler_registry._items
    assert "around" in handler_registry._items


@pytest.mark.asyncio
async def test_notify_before_run(
    handler_registry,
    test_handler_one,
    test_handler_two,
    test_handler_three,
    test_component,
):
    """Test notifying the 'before' event calls the correct handler"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])
    await handler_registry.notify("before", test_component)

    assert test_handler_one.before_called is True
    assert test_handler_three.before_called is True
    assert test_handler_two.before_called is False


@pytest.mark.asyncio
async def test_notify_after_run(
    handler_registry,
    test_handler_one,
    test_handler_two,
    test_handler_three,
    test_component,
):
    """Test notifying the 'after' event calls the correct handler"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])
    await handler_registry.notify("after", "result_value")

    assert test_handler_one.after_called is True
    assert test_handler_one.after_result == "result_value"


@pytest.mark.asyncio
async def test_notify_around(
    handler_registry,
    test_handler_one,
    test_handler_two,
    test_handler_three,
    test_component,
):
    """Test notifying the 'around' event calls the correct handler"""
    handler_registry.attach([test_handler_one, test_handler_two, test_handler_three])

    async def mock_execute(*args, **kwargs):
        return "executed"

    await handler_registry.notify("around", mock_execute)

    assert test_handler_two.around_called is True
