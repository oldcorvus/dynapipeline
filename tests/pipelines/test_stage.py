"""
        Contains tests for Stage
"""
import asyncio

import pytest

from dynapipeline.pipelines.stage import Stage


class TestStage(Stage):
    """
    A test subclass of Stage for testing purposes
    """

    __test__ = False

    async def execute(self, *args, **kwargs):
        """test execute method"""
        await asyncio.sleep(2)
        return "result"


@pytest.fixture
def test_stage():
    """
    Fixture to create a TestStage
    """
    return TestStage(name="dummy_stage")


@pytest.mark.asyncio
async def test_stage_without_timeout(test_stage):
    """Test stage execution without any timeout"""
    test_stage.timeout = None

    result = await test_stage.run()
    assert result == "result"


@pytest.mark.asyncio
async def test_stage_with_timeout_success(test_stage):
    """Test  stage execution finishes within  timeout"""
    test_stage.timeout = 3
    result = await test_stage.run()
    assert result == "result"


@pytest.mark.asyncio
async def test_stage_with_timeout_failure(test_stage):
    """Test  stage execution  exceeds the specified timeout"""
    test_stage.timeout = 1

    with pytest.raises(asyncio.TimeoutError):
        await test_stage.run()


@pytest.mark.asyncio
async def test_stage_with_zero_timeout(test_stage):
    """Test  stage execution when timeout is set to zero"""
    test_stage.timeout = 0

    result = await test_stage.run()
    assert result == "result"


@pytest.mark.asyncio
async def test_stage_with_negative_timeout(test_stage):
    """Test  stage execution when timeout is set to a negative value"""
    test_stage.timeout = -1

    result = await test_stage.run()
    assert result == "result"
