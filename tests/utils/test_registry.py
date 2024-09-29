"""Contains tests for Base Registry"""
import pytest

from dynapipeline.exceptions.registry import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)
from dynapipeline.utils.base_registry import BaseRegistry


def test_register_item():
    """Test that items can be registered successfully"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    assert registry["item1"] == "value1"


def test_unregister_item():
    """Test that items can be unregistered successfully"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    registry.unregister("item1")
    with pytest.raises(ItemNotFoundError):
        registry["item1"]


def test_register_duplicate_item():
    """Test that registering an already registered item raises an error"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    with pytest.raises(ItemAlreadyRegisteredError):
        registry.register("item1", "value2")


def test_unregister_non_existent_item():
    """Test that trying to unregister a non-existent item raises an error"""
    registry = BaseRegistry()
    with pytest.raises(ItemNotFoundError):
        registry.unregister("non_existent_item")


def test_get_item_not_found():
    """Test that retrieving a non-existent item raises an error."""
    registry = BaseRegistry()
    with pytest.raises(ItemNotFoundError):
        registry["item1"]


def test_get_item_with_default_factory():
    """Test that retrieving a non-existent item returns a default value if default_factory is set"""
    registry = BaseRegistry(default_factory=lambda: "default_value")
    assert registry["non_existent"] == "default_value"


def test_len_registry():
    """Test that the length of the registry is correct."""
    registry = BaseRegistry()
    assert len(registry) == 0
    registry.register("item1", "value1")
    registry.register("item2", "value2")
    assert len(registry) == 2
    registry.unregister("item1")
    assert len(registry) == 1


def test_iterate_registry():
    """Test that the registry can be iterated over"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    registry.register("item2", "value2")

    items = {key: registry[key] for key in registry}

    assert items == {"item1": "value1", "item2": "value2"}


def test_clear_registry():
    """Test that the clear method removes all items from the registry"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    registry.register("item2", "value2")

    assert len(registry) == 2

    registry.clear()

    assert len(registry) == 0
    with pytest.raises(ItemNotFoundError):
        registry["item1"]


def test_items_method():
    """Test that the items method returns all key-value pairs in the registry"""
    registry = BaseRegistry()
    registry.register("item1", "value1")
    registry.register("item2", "value2")

    expected_items = {"item1": "value1", "item2": "value2"}

    assert dict(registry.items()) == expected_items
