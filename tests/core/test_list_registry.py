"""
    Contains tests for ListRegistry
"""
import pytest

from dynapipeline.exceptions.registry import ItemNotFoundError
from dynapipeline.utils.list_registry import ListRegistry


def test_clear_specific_list():
    """Test that a specific list can be cleared"""
    registry = ListRegistry()
    registry.register("item1", ["value1", "value2"])
    registry.clear("item1")
    assert registry["item1"] == []


def test_clear_entire_registry():
    """Test that clearing the entire registry works correctly"""
    registry = ListRegistry()
    registry.register("item1", ["value1"])
    registry.register("item2", ["value2"])
    registry.clear()
    assert len(registry) == 0


def test_register_items_to_list():
    """Test that an iterable of items can be registered to a list successfully"""
    registry = ListRegistry()
    registry.register("item1", ["value1", "value2"])
    assert registry["item1"] == ["value1", "value2"]


def test_register_additional_items():
    """Test that additional items can be appended to an existing list"""
    registry = ListRegistry()
    registry.register("item1", ["value1"])
    registry.register("item1", ["value2", "value3"])
    assert registry["item1"] == ["value1", "value2", "value3"]


def test_unregister_specific_item_from_list():
    """Test that a specific item can be unregistered from the list"""
    registry = ListRegistry()
    registry.register("item1", ["value1", "value2", "value3"])
    registry.unregister("item1", "value2")
    assert registry["item1"] == ["value1", "value3"]


def test_unregister_last_item_removes_list():
    """Test that when the last item is removed list is removed from the registry"""
    registry = ListRegistry()
    registry.register("item1", ["value1"])
    registry.unregister("item1", "value1")
    assert registry["item1"] == []


def test_unregister_non_existent_item_raises_error():
    """Test that unregistering a non-existent item raises ItemNotFoundError"""
    registry = ListRegistry()
    registry.register("item1", ["value1", "value2"])
    with pytest.raises(ItemNotFoundError):
        registry.unregister("item1", "non_existent_item")


def test_len_registry_with_lists():
    """Test that the length of the registry is correct with multiple lists"""
    registry = ListRegistry()
    assert len(registry) == 0
    registry.register("item1", ["value1"])
    registry.register("item2", ["value2"])
    assert len(registry) == 2
    registry.clear("item1")
    assert len(registry) == 2
    registry.unregister("item2", "value2")
    assert len(registry) == 1
