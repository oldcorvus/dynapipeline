""" Contains tests for ProtectedContext"""
import pytest

from dynapipeline.contexts.protected import ProtectedContext
from dynapipeline.exceptions.context import ContextKeyError, ContextLockedError


@pytest.fixture
def context():
    """Fixture that provides a ProtectedContext"""
    return ProtectedContext()


def test_lock_functionality(context):
    """Test that the lock() method locks context"""
    context.lock()
    assert context.is_locked


def test_unlock_functionality(context):
    """Test that the unlock() method unlocks context"""
    context.lock()
    context.unlock()
    assert not context.is_locked


def test_is_locked_property_when_unlocked(context):
    """Test the is_locked property when  context is unlocked"""
    assert not context.is_locked


def test_is_locked_property_when_locked(context):
    """Test the is_locked property when context is locked"""
    context.lock()
    assert context.is_locked


def test_set_item_when_unlocked(context):
    """Test that an item can be set when context is unlocked"""
    context["key1"] = "value1"
    assert context._data["key1"] == "value1"


def test_set_item_when_locked(context):
    """Test that setting an item raises ContextLockedError when locked"""
    context.lock()
    with pytest.raises(ContextLockedError):
        context["key1"] = "value1"


def test_delete_item_when_unlocked(context):
    """Test that an item can be deleted when context is unlocked"""
    context._data["key1"] = "value1"
    del context["key1"]
    assert "key1" not in context._data


def test_delete_item_when_locked(context):
    """Test that deleting an item raises ContextLockedError when locked"""
    context._data["key1"] = "value1"
    context.lock()
    with pytest.raises(ContextLockedError):
        del context["key1"]


def test_delete_non_existent_key(context):
    """Test that deleting a non-existent key raises ContextKeyError"""
    with pytest.raises(ContextKeyError):
        del context["non_existent_key"]
