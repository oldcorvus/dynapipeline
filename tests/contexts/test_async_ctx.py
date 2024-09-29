"""This module provides tests for AsyncLockableContext"""

import pytest

from dynapipeline.contexts.async_ctx import AsyncLockableContext
from dynapipeline.exceptions.context import ContextKeyError


@pytest.mark.asyncio
async def test_initial_lock_state():
    """
    Test context is initially unlocked
    """
    context = AsyncLockableContext()
    assert not context.is_locked, "Context should initially be unlocked"


@pytest.mark.asyncio
async def test_lock_and_unlock():
    """
    Test locking and unlocking behavior of context"""
    context = AsyncLockableContext()

    await context.lock()
    assert context.is_locked, "Context should be locked after calling lock()"

    await context.unlock()
    assert not context.is_locked, "Context should be unlocked after calling unlock()"


@pytest.mark.asyncio
async def test_lock_allows_modification():
    """
    Test context allows modification while locked
    """
    context = AsyncLockableContext()

    await context.lock()

    context["key1"] = "value1"
    assert context["key1"] == "value1"

    await context.unlock()


@pytest.mark.asyncio
async def test_async_with_locks_and_allows_modification():
    """Test context can be locked and modified inside with block"""
    context = AsyncLockableContext()

    async with context:
        assert context.is_locked, "Context should be locked within async with block"

        context["a"] = 1
        assert context["a"] == 1

    assert not context.is_locked, "Context should be unlocked after async with block"


@pytest.mark.asyncio
async def test_iteration_with_lock():
    """Test that asynchronous iteration works while the context is locked"""
    context = AsyncLockableContext()
    context["key1"] = "value1"
    context["key2"] = "value2"

    async with context:
        items = [(key, value) async for key, value in context]
        assert items == [("key1", "value1"), ("key2", "value2")]


@pytest.mark.asyncio
async def test_key_error_on_non_existent_key():
    """Test that accessing a non-existent key raises a ContextKeyError"""
    context = AsyncLockableContext()

    with pytest.raises(ContextKeyError):
        _ = context["non_existent"]

    context["existing_key"] = "value"
    assert context["existing_key"] == "value"


@pytest.mark.asyncio
async def test_lock_releases_properly_on_error_in_async_with():
    """Test that the lock is properly released if an exception occurs in with  block"""
    context = AsyncLockableContext()

    try:
        async with context:
            assert context.is_locked
            raise ValueError("Simulate an error inside the async with block")
    except ValueError:
        pass

    assert not context.is_locked
