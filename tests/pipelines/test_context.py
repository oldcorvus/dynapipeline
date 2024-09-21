"""
Contains tests for PiplineContext
"""

import pytest

from dynapipeline.errors.base import BaseError
from dynapipeline.pipelines.context import PipelineContext


@pytest.fixture
def pipeline_context():
    """Fixture to initialize PipelineContext"""
    return PipelineContext()


def test_set_and_get_data(pipeline_context):
    """Test setting and getting value in the contex"""
    pipeline_context.set("key_1", "value_1")
    assert pipeline_context.get("key_1") == "value_1"


def test_clear_context(pipeline_context):
    """Test clearing all items from the context"""
    pipeline_context.set("key_1", "value_1")
    pipeline_context.set("key_2", "value_2")
    pipeline_context.clear()
    assert pipeline_context.get("key_1") is None
    assert pipeline_context.get("key_2") is None


def test_remove_item(pipeline_context):
    """Test removing an item from the context"""
    pipeline_context.set("key_1", "value_1")
    pipeline_context.remove("key_1")

    assert pipeline_context.get("key_1") is None


def test_contains_key(pipeline_context):
    """Test checking if a key exists in the context"""
    pipeline_context.set("key_1", "value_1")
    assert pipeline_context.contains("key_1") is True
    assert pipeline_context.contains("non_existent_key") is False


def test_get_data_with_default(pipeline_context):
    """Test retrieving a non-existent key with a default value"""
    assert pipeline_context.get("non_existent_key", "default_value") == "default_value"


@pytest.mark.asyncio
async def test_add_and_get_errors(pipeline_context):
    """Test  errors can be added to the error registry and retrieved"""
    error = BaseError("Test error", "TestErrorType", "HIGH")
    await pipeline_context.add_error(error, context="stage_1")

    errors = pipeline_context.get_errors("stage_1")
    assert len(errors) == 1
    assert errors[0].message == "Test error"


@pytest.mark.asyncio
async def test_get_errors_without_context(pipeline_context):
    """Test getting errors without specifying a context uses 'default'"""
    error = BaseError("Test default error", "TestErrorType", "LOW")
    await pipeline_context.add_error(error)

    errors = pipeline_context.get_errors()
    assert len(errors) == 1
    assert errors[0].message == "Test default error"


@pytest.mark.asyncio
async def test_list_all_errors(pipeline_context):
    """Test listing all errors for all contexts"""
    error1 = BaseError("Test error 1", "TestErrorType", "HIGH")
    error2 = BaseError("Test error 2", "TestErrorType", "LOW")
    await pipeline_context.add_error(error1, context="stage_1")
    await pipeline_context.add_error(error2, context="stage_2")

    all_errors = pipeline_context.list_all_errors()
    assert len(all_errors) == 2
    assert all_errors[0].message == "Test error 1"
    assert all_errors[1].message == "Test error 2"


@pytest.mark.asyncio
async def test_clear_errors(pipeline_context):
    """Test clearing errors for a specific context"""
    error = BaseError("Test error", "TestErrorType", "HIGH")
    await pipeline_context.add_error(error, context="stage_1")

    pipeline_context.clear_errors("stage_1")
    assert pipeline_context.get_errors("stage_1") == []


@pytest.mark.asyncio
async def test_clear_all_errors(pipeline_context):
    """Test clearing all errors for all contexts"""
    error1 = BaseError("Test error 1", "TestErrorType", "HIGH")
    error2 = BaseError("Test error 2", "TestErrorType", "LOW")

    await pipeline_context.add_error(error1, context="stage_1")
    await pipeline_context.add_error(error2, context="stage_2")

    pipeline_context.clear_errors()

    assert pipeline_context.list_all_errors() == []
