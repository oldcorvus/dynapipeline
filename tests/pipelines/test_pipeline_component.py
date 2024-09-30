"""
    tests for PipelienComponent
"""
import asyncio
from typing import Any, Awaitable, Callable

import pytest

from dynapipeline.handlers.handler import Handler
from dynapipeline.handlers.handler_registry import HandlerRegistry
from dynapipeline.pipelines.component import PipelineComponent


class TestHandler(Handler):
    """test class for Handler"""

    __test__ = False

    def __init__(self):
        super().__init__()
        self.before_called = False
        self.around_called = False
        self.after_called = False
        self.error_called = False
        self.result = None

    def before(self, component: PipelineComponent, *args, **kwargs):
        """Test Method implimentation for before method"""
        self.before_called = True

    async def around(
        self,
        component: PipelineComponent,
        execute: Callable[..., Awaitable[Any]],
        *args,
        **kwargs
    ):
        """Test Method implimentation for around method"""

        self.around_called = True
        return await execute(*args, **kwargs)

    def after(self, component: PipelineComponent, result: Any, *args, **kwargs):
        """Test Method implimentation for after method"""

        self.after_called = True

    def on_error(self, component: PipelineComponent, error: Exception, *args, **kwargs):
        """Test Method implimentation for on_error method"""

        self.error_called = True


class TestPipelineComponent(PipelineComponent):
    """test class for piplinecomponent"""

    __test__ = False

    async def execute(self, *args, **kwargs) -> str:
        """Test Method implimentation for execute method"""

        if "fail" in args:
            raise Exception("test")
        await asyncio.sleep(1)
        return "execution_result"


@pytest.fixture
def test_handler():
    """Fixture to create TestHandler"""
    return TestHandler()


@pytest.fixture
def handler_registry(test_handler):
    """Fixture to create HandlerRegistry with TestHandler"""
    registry = HandlerRegistry()
    registry.attach([test_handler])
    return registry


@pytest.fixture
def test_component(handler_registry):
    """Fixture to create  TestPipelineComponent"""
    return TestPipelineComponent(name="test_component", handlers=handler_registry)


@pytest.mark.asyncio
async def test_name_validation():
    """Test name validation in PipelineComponent"""
    with pytest.raises(ValueError, match="The 'name' must be non-empty string"):
        TestPipelineComponent(name="").validate_name("")


@pytest.mark.asyncio
async def test_run_with_all_handlers(test_component, test_handler):
    """Test the component run method with all handler"""
    result = await test_component.run()

    assert result == "execution_result"
    assert test_handler.before_called is True
    assert test_handler.around_called is True
    assert test_handler.after_called is True
    assert test_handler.error_called is False


@pytest.mark.asyncio
async def test_run_with_error_handler(test_component, test_handler):
    """Test the component run method with error handling"""

    result = None
    try:
        result = await test_component.run("fail")
    except Exception:
        pass

    assert result is None
    assert test_handler.before_called is True
    assert test_handler.around_called is True
    assert test_handler.after_called is False
    assert test_handler.error_called is True


@pytest.mark.asyncio
async def test_run_without_around_handler(
    test_component, test_handler, handler_registry
):
    """Test the component run  without an 'around' handler"""
    handler_registry.unregister("around")

    result = await test_component.run()

    assert result == "execution_result"
    assert test_handler.before_called is True
    assert test_handler.around_called is False
    assert test_handler.after_called is True
    assert test_handler.error_called is False
