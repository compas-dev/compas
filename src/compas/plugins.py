"""COMPAS plugin infrastructure.

Notes
-----
External plugin packages register lightweight plugin modules through the
`compas.plugins` package entry-point group. Core plugin modules are registered
explicitly. Discovery therefore imports only declared plugin modules rather
than scanning unrelated installed packages.

"""

# The COMPAS plugin system owes a lot to pluggy, the pytest plugin framework
# There are portions of code loosely based on pluggy's
# and while it is not strictly derivative work, we include
# their license and copyright notice to give credit where credit is due.
#
# MIT license
# Copyright (c) 2015 holger krekel (rather uses bitbucket/hpk42)
#
# https://github.com/pytest-dev/pluggy

import functools
import inspect
import threading
from collections.abc import Callable
from collections.abc import Sequence
from dataclasses import dataclass
from importlib import import_module
from importlib.metadata import entry_points
from importlib.util import find_spec
from types import ModuleType
from typing import Any
from typing import Literal
from typing import ParamSpec
from typing import TypeVar
from typing import overload

__all__ = [
    "pluggable",
    "plugin",
    "plugin_manager",
    "IncompletePluginImplError",
    "PluginManager",
    "PluginNotInstalledError",
    "validate_plugin_implementation",
    "PluginDefaultNotAvailableError",
    "PluginConflictError",
    "PluginValidationError",
    "ExtensionPoint",
    "PluginSpec",
]


class PluginNotInstalledError(Exception):
    """Exception raised when an extension point is invoked but no plugin is available."""

    pass


class PluginDefaultNotAvailableError(Exception):
    """Exception raised when an extension point is invoked but no plugin is available, and the default implementation is also not available.

    The most likely circumstance for this error is when the default implementation is based on Numpy, Scipy, or similar,
    and the pluggable is invoked in a context where these packages are not available.

    """

    pass


class PluginConflictError(Exception):
    """Raised when multiple selectable plugins have the same highest priority."""


class PluginValidationError(Exception):
    """Raised when a plugin cannot accept an extension-point invocation."""


type Requirement = str | Callable[[], bool]
type Selector = Literal["first_match", "collect_all"]

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class ExtensionPoint:
    """Unique identifier of a pluggable operation."""

    domain: str
    category: str | None
    name: str

    def __str__(self) -> str:
        return "{}/{}/{}".format(self.domain, self.category or "", self.name).replace("//", "/")


@dataclass(frozen=True, slots=True)
class PluginSpec:
    """Registration metadata attached to a plugin implementation."""

    extension_point: ExtensionPoint
    requires: tuple[Requirement, ...] = ()
    priority: int = 0


class IncompletePluginImplError(Exception):
    """Exception raised when a plugin does not have implementations for all abstract methods of its base class."""

    pass


@dataclass(frozen=True, slots=True)
class PluginImpl:
    """Registered implementation of an extension point."""

    plugin: ModuleType
    method: Callable[..., Any]
    spec: PluginSpec

    @property
    def id(self) -> str:
        """Identifier of the plugin implementation."""
        return "{}.{}".format(self.plugin.__name__, self.method.__name__)

    @property
    def priority(self) -> int:
        """Selection priority of the implementation."""
        return self.spec.priority


class PluginManager:
    """Plugin Manager handles discovery and registry of plugins.

    Usually there is only one instance of a plugin manager per host.

    """

    DEBUG = False

    # =============================================================================
    # Dunder methods
    # =============================================================================

    def __init__(self, builtin_modules: tuple[str, ...] = (), entry_points_provider: Callable[..., Any] = entry_points) -> None:
        self._registry: dict[ExtensionPoint, list[PluginImpl]] = {}
        self._builtin_modules = tuple(builtin_modules)
        self._entry_points_provider = entry_points_provider
        self._registered_modules = set()
        self._discovery_done = False
        self._discovery_lock = threading.Lock()

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def registry(self) -> dict[ExtensionPoint, list[PluginImpl]]:
        """Plugin registry.

        Lazy-loaded dictionary of all plugins available in the system.

        Returns
        -------
        dict[ExtensionPoint, list[PluginImpl]]
            Available implementations grouped by extension point.

        """
        if not self._discovery_done:
            self.load_plugins()

        return self._registry

    # =============================================================================
    # Methods
    # =============================================================================

    def load_plugins(self) -> int:
        """Load available plugin modules.

        Returns
        -------
        int
            Number of loaded plugins.

        """
        with self._discovery_lock:
            if self._discovery_done:
                return 0

            count = 0

            for module_name in self._builtin_modules:
                plugin_module = import_module(module_name)
                count += self.register_module(plugin_module)

            discovered = self._entry_points_provider(group="compas.plugins")
            for entry_point in sorted(discovered, key=lambda item: (item.name, item.value)):
                plugin_module = entry_point.load()
                if not isinstance(plugin_module, ModuleType):
                    raise TypeError("Plugin entry point {!r} must resolve to a module.".format(entry_point.name))
                count += self.register_module(plugin_module)

            self._discovery_done = True

        return count

    def register_module(self, plugin_module: ModuleType) -> int:
        """Register a module that potentially contains plugin implementations.

        Parameters
        ----------
        plugin_module : module
            Module instance to inspect for plugins.

        Returns
        -------
        int
            Count of successfully registered plugins in the module.

        """
        count = 0

        if plugin_module.__name__ in self._registered_modules:
            return count

        self._registered_modules.add(plugin_module.__name__)

        # Iterate over the plugin to locate specific @plugin decorated methods
        for name in dir(plugin_module):
            plugin_method = getattr(plugin_module, name)
            plugin_opts = self._parse_plugin_opts(plugin_method)

            if plugin_opts is not None:
                plugin_impl = PluginImpl(plugin_module, plugin_method, plugin_opts)
                plugins_list = self._registry.setdefault(plugin_opts.extension_point, [])
                plugins_list.append(plugin_impl)
                plugins_list.sort(key=lambda plugin: (-plugin.priority, plugin.id))

                if self.DEBUG:
                    print('Registered plugin with ID "{}" for extension point: {}'.format(plugin_impl.id, plugin_opts.extension_point))
                count += 1

        return count

    def reset(self) -> None:
        """Clear registered plugins and allow discovery to run again."""
        with self._discovery_lock:
            self._registry.clear()
            self._registered_modules.clear()
            self._discovery_done = False

    def verify_requirement(self, requirement: Requirement) -> bool:
        """Verify that one plugin requirement is available."""
        if callable(requirement):
            return requirement()
        return find_spec(requirement) is not None

    def is_selectable(self, plugin: PluginImpl) -> bool:
        """Determine whether all requirements of a plugin are available."""
        selectable = all(self.verify_requirement(requirement) for requirement in plugin.spec.requires)
        if not selectable and self.DEBUG:
            print("Requirements not satisfied. Plugin will not be used: {}".format(plugin.id))
        return selectable

    def select(self, extension_point: ExtensionPoint) -> PluginImpl | None:
        """Select the unique highest-priority implementation of an extension point."""
        plugins = [plugin for plugin in self.registry.get(extension_point, []) if self.is_selectable(plugin)]
        if not plugins:
            return None
        highest_priority = plugins[0].priority
        matches = [plugin for plugin in plugins if plugin.priority == highest_priority]
        if len(matches) > 1:
            raise PluginConflictError(
                'Multiple plugins have priority {} for extension point "{}": {}'.format(
                    highest_priority,
                    extension_point,
                    ", ".join(plugin.id for plugin in matches),
                )
            )
        return matches[0]

    def collect(self, extension_point: ExtensionPoint) -> list[PluginImpl]:
        """Collect all selectable implementations of an extension point."""
        return [plugin for plugin in self.registry.get(extension_point, []) if self.is_selectable(plugin)]

    def validate_call(self, plugin: PluginImpl, extension_point: ExtensionPoint, *args: object, **kwargs: object) -> None:
        """Verify that a plugin implementation can accept an extension-point call.

        Parameters
        ----------
        plugin
            The implementation to validate.
        extension_point
            The extension point being called.
        *args
            Positional arguments passed to the extension point.
        **kwargs
            Keyword arguments passed to the extension point.

        Raises
        ------
        PluginValidationError
            If the implementation cannot accept the call.

        """
        try:
            inspect.signature(plugin.method).bind(*args, **kwargs)
        except TypeError as error:
            raise PluginValidationError('Plugin "{}" cannot accept the call defined by extension point "{}".'.format(plugin.id, extension_point)) from error

    # =============================================================================
    # Private helpers
    # =============================================================================

    def _parse_plugin_opts(self, plugin_method: object) -> PluginSpec | None:
        if not inspect.isroutine(plugin_method):
            return
        try:
            res = getattr(plugin_method, "__plugin_spec__", None)
        except Exception:
            res = {}
        if res is not None and not isinstance(res, PluginSpec):
            return None
        return res


@overload
def pluggable(
    pluggable_method: Callable[P, R],
    category: str | None = None,
    selector: Literal["first_match"] = "first_match",
    domain: str = "https://plugins.compas.dev/",
) -> Callable[P, R]: ...


@overload
def pluggable(
    pluggable_method: Callable[P, R],
    category: str | None = None,
    *,
    selector: Literal["collect_all"],
    domain: str = "https://plugins.compas.dev/",
) -> Callable[P, list[R]]: ...


@overload
def pluggable(
    pluggable_method: None = None,
    category: str | None = None,
    selector: Literal["first_match"] = "first_match",
    domain: str = "https://plugins.compas.dev/",
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


@overload
def pluggable(
    pluggable_method: None = None,
    category: str | None = None,
    *,
    selector: Literal["collect_all"],
    domain: str = "https://plugins.compas.dev/",
) -> Callable[[Callable[P, R]], Callable[P, list[R]]]: ...


def pluggable(
    pluggable_method: Callable[P, R] | None = None,
    category: str | None = None,
    selector: Selector = "first_match",
    domain: str = "https://plugins.compas.dev/",
) -> Callable[..., Any]:
    """Decorator to mark a method as a pluggable extension point.

    A pluggable interface is uniquely identifiable/locatable via a URL
    derived from the `domain`, `category`, and `pluggable_method` name.
    For example:

    ```text
    https://plugins.compas.dev/triangulation/triangulate_mesh
    ```

    Parameters
    ----------
    pluggable_method : callable
        The method to decorate as `pluggable`.
    category : str, optional
        An optional string to group or categorize extension points.
    selector : str, optional
        String that determines the selection mode of extension points.

        - `"first_match"`: execute the uniquely highest-priority implementation.
        - `"collect_all"`: execute all matching implementations and return their results.

    domain : str, optional
        Domain name that "owns" the pluggable extension point.
        This is useful to avoid name collisions between extension points
        of different packages.

    Examples
    --------
    >>> @pluggable(category="triangulation")
    ... def triangulate_mesh(mesh):
    ...     pass

    """

    def pluggable_decorator(func: Callable[P, R]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | list[R]:
            extension_point = ExtensionPoint(domain, category, func.__name__)

            # Select first matching plugin
            if selector == "first_match":
                plugin_impl = plugin_manager.select(extension_point)
                if plugin_impl is None:
                    try:
                        return func(*args, **kwargs)
                    except NotImplementedError:
                        raise PluginNotInstalledError("Plugin not found and no default implementation for extension point: {}".format(extension_point))
                    except ImportError:
                        raise PluginDefaultNotAvailableError(
                            "Plugin not found and the default implementation is not available in your environment for extension point: {}".format(extension_point)
                        )

                # Invoke plugin
                plugin_manager.validate_call(plugin_impl, extension_point, *args, **kwargs)
                return plugin_impl.method(*args, **kwargs)

            # Collect all matching plugins
            elif selector == "collect_all":
                results = []
                for plugin_impl in plugin_manager.collect(extension_point):
                    plugin_manager.validate_call(plugin_impl, extension_point, *args, **kwargs)
                    results.append(plugin_impl.method(*args, **kwargs))
                return results
            else:
                raise ValueError("Unexpected selector type. Must be either: first_match or collect_all")

        return wrapper

    if pluggable_method is None:
        return pluggable_decorator
    else:
        return pluggable_decorator(pluggable_method)


@overload
def plugin(
    method: Callable[P, R],
    category: str | None = None,
    requires: Sequence[Requirement] | None = None,
    priority: int = 0,
    pluggable_name: str | None = None,
    domain: str = "https://plugins.compas.dev/",
) -> Callable[P, R]: ...


@overload
def plugin(
    method: None = None,
    category: str | None = None,
    requires: Sequence[Requirement] | None = None,
    priority: int = 0,
    pluggable_name: str | None = None,
    domain: str = "https://plugins.compas.dev/",
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def plugin(
    method: Callable[P, R] | None = None,
    category: str | None = None,
    requires: Sequence[Requirement] | None = None,
    priority: int = 0,
    pluggable_name: str | None = None,
    domain: str = "https://plugins.compas.dev/",
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to declare a plugin.

    A plugin decorator marks a method as a plugin for a specified `pluggable`
    extension point. Plugins are matched to their pluggable
    counterparts by a combination of the name of the plugin method, the category
    and the domain specified. These 3 parts form the **extension point URL** used
    for matching.

    Parameters
    ----------
    method : callable
        The method to decorate as `plugin`.
    category : str, optional
        An optional string to group or categorize plugins.
    requires : list, optional
        Optionally defines a list of requirements that should be fulfilled
        for this plugin to be used. The requirement can either be a package
        name (`str`) or a callable with a boolean return value,
        in which any arbitrary check can be implemented.
    priority : int, optional
        Selection priority. Higher values are selected first.
    pluggable_name : str, optional
        Usually, the name of the decorated plugin method matches that of the
        pluggable interface. When that is not the case, the pluggable name can be
        specified via this parameter.
    domain : str, optional
        Domain name that "owns" the pluggable extension point.
        This is useful to disambiguate name collisions between extension points
        of different packages.

    """

    def setattr_hookspec_opts(func: Callable[P, R]) -> Callable[P, R]:
        name = pluggable_name or func.__name__
        extension_point = ExtensionPoint(domain, category, name)

        setattr(
            func,
            "__plugin_spec__",
            PluginSpec(extension_point=extension_point, requires=tuple(requires or ()), priority=priority),
        )
        return func

    if method is not None:
        return setattr_hookspec_opts(method)
    else:
        return setattr_hookspec_opts


def validate_plugin_implementation(implementation_type: type[object]) -> None:
    """Verify that a class implements all inherited abstract methods.

    Parameters
    ----------
    implementation_type
        The implementation class to verify.

    Raises
    ------
    IncompletePluginImplError
        If an abstract method remains unimplemented.

    """
    for _, value in inspect.getmembers(implementation_type):
        if (inspect.isfunction(value) or inspect.ismethod(value)) and hasattr(value, "__isabstractmethod__"):
            raise IncompletePluginImplError("Abstract method not implemented: {}".format(value))


plugin_manager = PluginManager(builtin_modules=("compas.scene",))
