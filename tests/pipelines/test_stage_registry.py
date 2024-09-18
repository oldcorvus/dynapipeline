"""
This module contains unit tests for the StageTypeRegistry class"""
import pytest

from dynapipeline.exceptions.registry_exceptions import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)
from dynapipeline.pipelines.stage_type_registry import StageTypeRegistry
from dynapipeline.utils.stage_types import StageType


def test_default_stage_types_registered():
    """
    Check that all the default stage types are automatically registered
    when the StageTypeRegistry is initialized.
    """
    registry = StageTypeRegistry()

    for st_type in StageType:
        assert registry.is_registered(st_type.name) is True
        assert registry.get(st_type.name) == st_type.value


def test_register_new_stage_type():
    """
    Verify that a new custom stage type can be added to the registry.
    """
    registry = StageTypeRegistry()

    registry.register("CUSTOM_STAGE", "custom_stage_value")

    assert registry.is_registered("CUSTOM_STAGE") is True
    assert registry.get("CUSTOM_STAGE") == "custom_stage_value"


def test_register_existing_stage_type_raises_error():
    """
    Ensure that trying to register an existing stage type triggers an ItemAlreadyRegisteredError.
    """
    registry = StageTypeRegistry()

    with pytest.raises(ItemAlreadyRegisteredError):
        registry.register(StageType.INIT.name, StageType.INIT.value)


def test_get_non_existing_stage_type_raises_error():
    """
    Ensure that fetching a non-existing stage type throws an ItemNotFoundError.
    """
    registry = StageTypeRegistry()

    with pytest.raises(ItemNotFoundError):
        registry.get("NON_EXISTING_STAGE")


def test_unregister_stage_type():
    """
    Check that a registered stage type can be properly removed from the registry.
    """
    registry = StageTypeRegistry()

    assert registry.is_registered(StageType.INIT.name) is True

    registry.unregister(StageType.INIT.name)

    assert registry.is_registered(StageType.INIT.name) is False


def test_unregister_non_existing_stage_type_raises_error():
    """
    Ensure that trying to remove a non-existing stage type raises an ItemNotFoundError.
    """
    registry = StageTypeRegistry()

    with pytest.raises(ItemNotFoundError):
        registry.unregister("NON_EXISTING_STAGE")


def test_list_all_stage_types():
    """
    Verify that listing all stage types returns the correct dictionary of registered types.
    """
    registry = StageTypeRegistry()

    items = registry.list_items()

    assert len(items) == len(StageType)

    for st_type in StageType:
        assert st_type.name in items
        assert items[st_type.name] == st_type.value


def test_set_default_false():
    """
    Ensure that when set_default is False, no default stage types are added to the registry.
    """
    registry = StageTypeRegistry(set_default=False)

    assert registry.count() == 0
