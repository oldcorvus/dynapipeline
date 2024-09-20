"""
This module contains unit tests for the StateRegistry class.
"""
import pytest

from dynapipeline.exceptions.registry import (
    ItemAlreadyRegisteredError,
    ItemNotFoundError,
)
from dynapipeline.pipelines.state_registry import StateRegistry
from dynapipeline.utils.pipeline_state import PiplineState


def test_default_state_types_registered():
    """
    Check that all the default state types from PiplineState are automatically registered.
    """
    registry = StateRegistry()

    for state in PiplineState:
        assert registry.is_registered(state.name) is True
        assert registry.get(state.name) == state.value


def test_register_new_state_type():
    """
    Verify that a new custom state type can be added to the registry.
    """
    registry = StateRegistry()

    registry.register("CUSTOM_STATE", "custom_state_value")

    assert registry.is_registered("CUSTOM_STATE") is True
    assert registry.get("CUSTOM_STATE") == "custom_state_value"


def test_register_existing_state_type_raises_error():
    """
    Ensure that trying to register an existing state type triggers an ItemAlreadyRegisteredError.
    """
    registry = StateRegistry()

    with pytest.raises(ItemAlreadyRegisteredError):
        registry.register(PiplineState.INITIALIZED.name, PiplineState.INITIALIZED.value)


def test_get_non_existing_state_type_raises_error():
    """
    Ensure that fetching a non-existing state type throws an ItemNotFoundError.
    """
    registry = StateRegistry()

    with pytest.raises(ItemNotFoundError):
        registry.get("NON_EXISTING_STATE")


def test_unregister_state_type():
    """
    Check that a registered state type can be properly removed from the registry.
    """
    registry = StateRegistry()

    assert registry.is_registered(PiplineState.INITIALIZED.name) is True

    registry.unregister(PiplineState.INITIALIZED.name)

    assert registry.is_registered(PiplineState.INITIALIZED.name) is False


def test_unregister_non_existing_state_type_raises_error():
    """
    Ensure that trying to remove a non-existing state type raises an ItemNotFoundError.
    """
    registry = StateRegistry()

    with pytest.raises(ItemNotFoundError):
        registry.unregister("NON_EXISTING_STATE")


def test_list_all_state_types():
    """
    Verify that listing all state types returns the correct dictionary of registered types.
    """
    registry = StateRegistry()

    items = registry.list_items()

    assert len(items) == len(PiplineState)

    for state in PiplineState:
        assert state.name in items
        assert items[state.name] == state.value


def test_set_default_false():
    """
    Ensure that when set_default is False, no default state types are added to the registry.
    """
    registry = StateRegistry(set_default=False)

    assert registry.count() == 0
