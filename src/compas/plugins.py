# The COMPAS plugin system owes a lot to pluggy, the pytest plugin framework
# There are portions of code loosely based on pluggy's
# and while it is not strictly derivative work, we include
# their license and copyright notice to give credit where credit is due.
#
# MIT license
# Copyright (c) 2015 holger krekel (rather uses bitbucket/hpk42)
#
# https://github.com/pytest-dev/pluggy
"""
********************************************************************************
plugins
********************************************************************************

.. currentmodule:: compas.plugins

COMPAS has an extensible architecture based on plugins that allows to
customize and extend the functionality of the core framework.

Check out the developer guide to :ref:`plugins` for additional details.

Decorators
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    pluggable
    plugin

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PluginManager

Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    PluginNotInstalledError
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import inspect
import pkgutil
import threading

__all__ = [
    'pluggable',
    'plugin',
    'plugin_manager',
    'PluginManager',
    'PluginNotInstalledError',
]


class PluginNotInstalledError(Exception):
    """Exception raised when an extension point is invoked but no plugin is available."""
    pass


def _get_extension_point_url_from_name(domain, category, pluggable_name):
    """Get the extension point URL based on a pluggable method name"""
    return '{}/{}/{}'.format(domain, category, pluggable_name).replace('//', '/')


def _get_extension_point_url_from_method(domain, category, plugin_method):
    """Get the extension point URL based on a method instance"""
    name = getattr(plugin_method, '__name__', None) or str(id(plugin_method))
    return '{}/{}/{}'.format(domain, category, name).replace('//', '/')


class PluginImpl(object):
    """Internal data class to keep track of a loaded plugin implementation.

    Parameters
    ----------
    plugin : module
        Instance of the module containing one or more plugin implementations.
    method : method
        Method implementing the a plugin's behavior.
    plugin_opts : dict
        Dictionary containing plugin options.
    """

    def __init__(self, plugin, method, plugin_opts):
        self.plugin = plugin
        self.method = method
        self.opts = plugin_opts

        if plugin_opts['tryfirst']:
            self.key = 1
        elif plugin_opts['trylast']:
            self.key = 3
        else:
            self.key = 2

    @property
    def id(self):
        """Identifier of the plugin implementation."""
        return '{}.{}'.format(self.plugin.__name__, self.method.__name__)

    def __repr__(self):
        return '<PluginImpl id={}, plugin_module={}>'.format(self.id, self.plugin)


class PluginManager(object):
    """Plugin Manager handles discovery and registry of plugins.

    Usually there is only one instance of a plugin manager per host.
    """
    DEBUG = False

    def __init__(self):
        self.importer = Importer()
        self._registry = {}
        self._discovery_done = False
        self._discovery_lock = threading.Lock()

    @property
    def registry(self):
        """Plugin registry.

        Lazy-loaded dictionary of all plugins available in the system.

        Returns
        -------
        dict
            Dictionary of available plugins. The keys are extension point URLs
            and the values are instances of :class:`PluginImpl`.
        """
        if not self._discovery_done:
            self.load_plugins()

        return self._registry

    def load_plugins(self):
        """Load available plugin modules.

        Returns
        -------
        int
            Number of loaded plugins.
        """
        # Since we modify global state,
        # let's lock around this.
        with self._discovery_lock:
            count = 0

            modules = [
                module_name
                for _importer, module_name, is_pkg in pkgutil.iter_modules()
                if is_pkg and module_name.startswith('compas')
            ]

            modules_to_inspect = dict()

            for module_name in modules:
                module = self.importer.try_import(module_name)
                if module:
                    modules_to_inspect[module_name] = module
                else:
                    if self.DEBUG:
                        print('Error importing module {}, skipping entire package.'.format(module_name))
                    continue

                if '__all_plugins__' in dir(module):
                    for plugin_module_name in module.__all_plugins__:
                        plugin_module = self.importer.try_import(plugin_module_name)
                        if plugin_module:
                            modules_to_inspect[plugin_module_name] = plugin_module
                        else:
                            if self.DEBUG:
                                print('Error importing plugin {}, skipping.'.format(plugin_module_name))

            if self.DEBUG:
                print('Will inspect modules: {}'.format(list(modules_to_inspect.keys())))

            for plugin_module in modules_to_inspect.values():
                count += self.register_module(plugin_module)

            self._discovery_done = True

        return count

    def register_module(self, plugin_module):
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

        # Iterate over the plugin to locate specific @plugin decorated methods
        for name in dir(plugin_module):
            plugin_method = getattr(plugin_module, name)
            plugin_opts = self._parse_plugin_opts(plugin_method)

            if plugin_opts is not None:
                plugin_impl = PluginImpl(plugin_module, plugin_method, plugin_opts)
                plugins_list = self._registry.setdefault(plugin_opts['extension_point_url'], [])
                plugins_list.append(plugin_impl)
                plugins_list.sort(key=lambda p: p.key)

                if self.DEBUG:
                    print('Registered plugin with ID "{}" for extension point: {}'.format(plugin_impl.id, plugin_opts['extension_point_url']))
                count += 1

        return count

    def _parse_plugin_opts(self, plugin_method):
        if not inspect.isroutine(plugin_method):
            return
        try:
            res = getattr(plugin_method, '__plugin_spec__', None)
        except Exception:
            res = {}
        if res is not None and not isinstance(res, dict):
            # false positive
            res = None
        return res


def pluggable(pluggable_method=None, category=None, selector='first_match', domain='https://plugins.compas.dev/'):
    """Decorator to mark a method as a pluggable extension point.

    A pluggable interface is uniquely identifiable/locatable via a URL
    derived from the parameters ``domain``, ``category`` and name ``pluggable_method``.
    In the example below, the URL of the pluggable definition is::

        https://plugins.compas.dev/triangulation/triangulate_mesh

    Parameters
    ----------
    pluggable_method : callable
        The method to decorate as ``pluggable``.
    category : :obj:`str`, optional
        An optional string to group or categorize extension points.
    selector : :obj:`str`, optional
        String that determines the selection mode of extension points.

        - ``"first_match"``: (:obj:`str`) Execute the first matching implementation.
        - ``"collect_all"``: (:obj:`str`) Executes all matching implementations and return list of its return values.

    domain : :obj:`str`, optional
        Domain name that "owns" the pluggable extension point.
        This is useful to avoid name collisions between extension points
        of different packages.

    Examples
    --------
    >>> @pluggable(category='triangulation')
    ... def triangulate_mesh(mesh):
    ...    pass
    """
    def pluggable_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            extension_point_url = _get_extension_point_url_from_method(domain, category, func)

            # Select first matching plugin
            if selector == 'first_match':
                plugin_impl = _select_plugin(extension_point_url)

                # Invoke plugin
                return plugin_impl.method(*args, **kwargs)

            # Collect all matching plugins
            elif selector == 'collect_all':
                results = []

                for plugin_impl in _collect_plugins(extension_point_url):
                    results.append(plugin_impl.method(*args, **kwargs))

                return results
            else:
                raise ValueError('Unexpected selector type. Must be either: first_match or collect_all')

        return wrapper

    if pluggable_method is None:
        return pluggable_decorator
    else:
        return pluggable_decorator(pluggable_method)


def plugin(method=None, category=None, requires=None, tryfirst=False, trylast=False, pluggable_name=None, domain='https://plugins.compas.dev/'):
    """Decorator to declare a plugin.

    A plugin decorator marks a method as a plugin for a specified
    :meth:`pluggable` extension point. Plugins are matched to their pluggable
    counterparts by a combination of the name of the plugin method, the category
    and the domain specified. These 3 parts form the **extension point URL** used
    for matching.

    Parameters
    ----------
    method : callable
        The method to decorate as ``plugin``.
    category : str, optional
        An optional string to group or categorize plugins.
    requires : list of str, optional
        Optionally defines a list of packages that should be importable
        for this plugin to be used.
    tryfirst : bool, optional
        Plugins can declare a preferred priority by setting this to ``True``.
        By default ``False``.
    trylast : bool, optional
        Alternatively, a plugin can demote itself to be least preferable
        setting ``trylast`` to ``True``. By default ``False``.
    pluggable_name : str, optional
        Usually, the name of the decorated plugin method matches that of the
        pluggable interface. When that is not the case, the pluggable name can be
        specified via this parameter.
    domain : str, optional
        Domain name that "owns" the pluggable extension point.
        This is useful to disambiguate name collisions between extension points
        of different packages.
    """
    def setattr_hookspec_opts(func):
        if tryfirst and trylast:
            raise ValueError('You cannot set a plugin to try first and last at the same time.')

        name = pluggable_name or getattr(func, '__name__', None)
        extension_point_url = _get_extension_point_url_from_name(domain, category, name)

        setattr(
            func,
            '__plugin_spec__',
            dict(
                extension_point_url=extension_point_url,
                pluggable_name=name,
                requires=requires,
                tryfirst=tryfirst,
                trylast=trylast,
            ),
        )
        return func

    if method is not None:
        return setattr_hookspec_opts(method)
    else:
        return setattr_hookspec_opts


class Importer(object):
    """Internal class to help importing modules."""

    def __init__(self):
        # dictionary of module_name => bool (importable yes/no)
        self._cache = {}

    def try_import(self, module_name):
        """Attempt to import a module, but do not raise in case of error.

        Parameters
        ----------
        module_name : str
            Module to try to import.

        Returns
        -------
        module
            If importable, it returns the imported module, otherwise ``None``.
        """
        module = None

        try:
            module = __import__(module_name, fromlist=['__name__'], level=0)
            self._cache[module_name] = True
        except ImportError:
            self._cache[module_name] = False

        return module

    def check_importable(self, module_name):
        """Check if a module is importable.

        Parameters
        ----------
        module_name : str
            Name of the module to check for importability.

        Returns
        -------
        bool
            ``True`` if the module can be imported correctly, otherwise ``False``.
        """
        if module_name not in self._cache:
            self.try_import(module_name)

        return self._cache[module_name]


def is_plugin_selectable(plugin, manager):
    if plugin.opts['requires']:
        importable_requirements = (manager.importer.check_importable(name) for name in plugin.opts['requires'])

        if not all(importable_requirements):
            if manager.DEBUG:
                print('Requirements not satisfied. Plugin will not be used: {}'.format(plugin.id))
            return False

    return True


def select_plugin(extension_point_url, manager):
    if manager.DEBUG:
        print('Extension Point URL {} invoked. Will select a matching plugin'.format(extension_point_url))

    plugins = manager.registry.get(extension_point_url) or []
    for plugin in plugins:
        if is_plugin_selectable(plugin, manager):
            return plugin

    # Nothing found, raise
    raise PluginNotInstalledError('Plugin not found for extension point URL: {}'.format(extension_point_url))


def collect_plugins(extension_point_url, manager):
    if manager.DEBUG:
        print('Extension Point URL {} invoked. Will select a matching plugin'.format(extension_point_url))

    plugins = manager.registry.get(extension_point_url) or []
    return [plugin for plugin in plugins if is_plugin_selectable(plugin, manager)]


plugin_manager = PluginManager()
_select_plugin = functools.partial(select_plugin, manager=plugin_manager)
_collect_plugins = functools.partial(collect_plugins, manager=plugin_manager)
