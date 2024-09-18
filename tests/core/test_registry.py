"""
 This module provides tests for BaseRegistery class
"""
import pytest

from dynapipeline.core.base_registry import BaseRegistry
from dynapipeline.exceptions.registry_exceptions import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)


class MockPlugin:
    """
    Helper class for testing
    """

    def __init__(self, name):
        self.name = name


def test_register_and_get():
    """
    Test registering an item and retrieving it from the registry.
    """
    registry = BaseRegistry[MockPlugin]()
    plugin = MockPlugin("Plugin1")
    registry.register("plugin1", plugin)

    retrieved = registry.get("plugin1")
    assert retrieved == plugin
    assert retrieved.name == "Plugin1"


def test_register_existing_item_raises_error():
    """
    Test that registering an already registered item raises an ItemAlreadyRegisteredError.
    """
    registry = BaseRegistry[MockPlugin]()
    plugin = MockPlugin("Plugin1")
    registry.register("plugin1", plugin)

    with pytest.raises(ItemAlreadyRegisteredError):
        registry.register("plugin1", plugin)


def test_unregister_and_is_registered():
    """
    Test unregistering an item and verifying its removal from the registry.
    """
    registry = BaseRegistry[MockPlugin]()
    plugin = MockPlugin("Plugin1")
    registry.register("plugin1", plugin)

    assert registry.is_registered("plugin1")

    registry.unregister("plugin1")

    assert not registry.is_registered("plugin1")


def test_unregister_non_existing_item_raises_error():
    """
    Test that trying to unregister a non-existing item raises an ItemNotFoundError.
    """
    registry = BaseRegistry[MockPlugin]()

    with pytest.raises(ItemNotFoundError):
        registry.unregister("non_existing")


def test_get_non_existing_item_raises_error():
    """
    Test that trying to retrieve a non-existing item raises an ItemNotFoundError.
    """
    registry = BaseRegistry[MockPlugin]()

    with pytest.raises(ItemNotFoundError):
        registry.get("non_existing")


def test_count_and_clear():
    """
    Test counting registered items and clearing the registry.
    """
    registry = BaseRegistry[MockPlugin]()
    registry.register("plugin1", MockPlugin("Plugin1"))
    registry.register("plugin2", MockPlugin("Plugin2"))
    registry.register("plugin3", MockPlugin("Plugin3"))

    assert registry.count() == 3

    registry.clear()

    assert registry.count() == 0
