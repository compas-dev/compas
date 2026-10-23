from abc import abstractmethod
from types import ModuleType

import pytest
import compas.plugins
from compas.plugins import IncompletePluginImplError
from compas.plugins import PluginConflictError
from compas.plugins import PluginManager
from compas.plugins import PluginValidationError
from compas.plugins import pluggable
from compas.plugins import plugin
from compas.plugins import validate_plugin_implementation


class TestBaseClass(object):
    @abstractmethod
    def foo(self):
        pass

    @abstractmethod
    def bar(self):
        pass

    def baz(self):
        pass


class IncompleteImpl(TestBaseClass):
    def bar(self):
        pass


class CompleteImpl(IncompleteImpl):
    def foo(self):
        pass


def test_ensure_implementations_fails_with_incomplete_impl():
    with pytest.raises(IncompletePluginImplError):
        validate_plugin_implementation(IncompleteImpl)


def test_ensure_implementations_with_valid_impl():
    validate_plugin_implementation(CompleteImpl)


class EntryPoint:
    def __init__(self, name, module):
        self.name = name
        self.value = module.__name__
        self.module = module

    def load(self):
        return self.module


def plugin_module(name, priority=0):
    module = ModuleType(name)

    @plugin(category="tests", pluggable_name="operation", priority=priority)
    def implementation():
        return name

    module.implementation = implementation
    return module


def test_plugin_manager_discovers_declared_entry_points_only():
    modules = [plugin_module("plugins.second"), plugin_module("plugins.first")]
    requested_groups = []

    def discover(*, group):
        requested_groups.append(group)
        return [EntryPoint("second", modules[0]), EntryPoint("first", modules[1])]

    manager = PluginManager(entry_points_provider=discover)

    assert manager.load_plugins() == 2
    assert manager.load_plugins() == 0
    assert requested_groups == ["compas.plugins"]

    implementations = next(iter(manager.registry.values()))
    assert [implementation.plugin.__name__ for implementation in implementations] == [
        "plugins.first",
        "plugins.second",
    ]


def test_plugin_manager_reset_allows_clean_rediscovery():
    module = plugin_module("plugins.resettable")
    manager = PluginManager(entry_points_provider=lambda *, group: [EntryPoint("resettable", module)])

    assert manager.load_plugins() == 1
    manager.reset()
    assert manager.registry
    assert len(next(iter(manager.registry.values()))) == 1


def test_plugin_entry_point_must_load_a_module():
    entry_point = EntryPoint("invalid", plugin_module("plugins.invalid"))
    entry_point.module = object()
    manager = PluginManager(entry_points_provider=lambda *, group: [entry_point])

    with pytest.raises(TypeError, match="must resolve to a module"):
        manager.load_plugins()


def test_plugin_selection_uses_explicit_priority():
    manager = PluginManager(entry_points_provider=lambda *, group: [])
    manager.register_module(plugin_module("plugins.low", priority=1))
    manager.register_module(plugin_module("plugins.high", priority=2))

    implementation = manager.select(next(iter(manager.registry)))

    assert implementation.plugin.__name__ == "plugins.high"


def test_plugin_selection_rejects_ambiguous_priority():
    manager = PluginManager(entry_points_provider=lambda *, group: [])
    manager.register_module(plugin_module("plugins.first_conflict"))
    manager.register_module(plugin_module("plugins.second_conflict"))

    with pytest.raises(PluginConflictError, match="Multiple plugins"):
        manager.select(next(iter(manager.registry)))


def test_pluggable_validates_selected_plugin_call(monkeypatch):
    module = ModuleType("plugins.invalid_signature")

    @plugin(category="tests", pluggable_name="validated")
    def implementation(value, required):
        return value, required

    module.implementation = implementation
    manager = PluginManager(entry_points_provider=lambda *, group: [])
    manager.register_module(module)
    selected = next(iter(manager.registry.values()))[0]
    monkeypatch.setattr(compas.plugins.plugin_manager, "select", lambda extension_point: selected)

    @pluggable(category="tests")
    def validated(value):
        raise NotImplementedError

    with pytest.raises(PluginValidationError, match="cannot accept the call"):
        validated(1)


def test_collect_all_propagates_plugin_errors(monkeypatch):
    module = ModuleType("plugins.failing")

    @plugin(category="tests", pluggable_name="collect")
    def implementation():
        raise ValueError("failed")

    module.implementation = implementation
    manager = PluginManager(entry_points_provider=lambda *, group: [])
    manager.register_module(module)
    implementations = next(iter(manager.registry.values()))
    monkeypatch.setattr(compas.plugins.plugin_manager, "collect", lambda extension_point: implementations)

    @pluggable(category="tests", selector="collect_all")
    def collect():
        raise NotImplementedError

    with pytest.raises(ValueError, match="failed"):
        collect()


def test_collect_all_validates_every_plugin_call(monkeypatch):
    module = ModuleType("plugins.invalid_collect_signature")

    @plugin(category="tests", pluggable_name="collect")
    def implementation(value, required):
        return value, required

    module.implementation = implementation
    manager = PluginManager(entry_points_provider=lambda *, group: [])
    manager.register_module(module)
    implementations = next(iter(manager.registry.values()))
    monkeypatch.setattr(compas.plugins.plugin_manager, "collect", lambda extension_point: implementations)

    @pluggable(category="tests", selector="collect_all")
    def collect(value):
        raise NotImplementedError

    with pytest.raises(PluginValidationError, match="cannot accept the call"):
        collect(1)


def test_core_plugin_registration_is_explicit_and_signature_compatible():
    manager = PluginManager(builtin_modules=("compas.scene",), entry_points_provider=lambda *, group: [])

    assert manager.load_plugins() == 1

    extension_point, implementations = next(iter(manager.registry.items()))
    implementation = implementations[0]

    assert extension_point.category == "factories"
    assert extension_point.name == "register_scene_objects"
    assert implementation.id == "compas.scene.register_scene_objects_base"
    manager.validate_call(implementation, extension_point)
