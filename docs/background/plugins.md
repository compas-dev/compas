# Developing a Plugin For a Pluggable

The COMPAS plugin system allows separate packages to provide implementations
for extension points declared by the core framework. A pluggable defines the
public contract; one or more plugins provide concrete behavior.

Use [`compas.plugins`][compas.plugins] to define and register plugins. Keep
optional backend imports inside plugin implementations so importing the core
package does not require backend-specific dependencies.

## Declaring a plugin package

Plugin discovery is explicit. An extension package must expose each lightweight
registration module through the `compas.plugins` entry-point group in its
`pyproject.toml`:

```toml
[project.entry-points."compas.plugins"]
compas_occ = "compas_occ.plugins"
```

The entry point must load a Python module. Importing that module should only
register decorated functions; expensive or optional backend imports belong
inside those functions.

## Defining an extension point

```python
from compas.plugins import pluggable


@pluggable(category="brep-queries")
def brep_area(brep: "Brep") -> float:
    raise NotImplementedError
```

The decorated function defines the public signature and may provide a default
implementation. If it raises `NotImplementedError` and no plugin is available,
COMPAS raises `PluginNotInstalledError`.

## Implementing an extension point

```python
from compas.plugins import plugin


@plugin(category="brep-queries", requires=["OCP"], priority=100)
def brep_area(brep: "Brep") -> float:
    from compas_occ.brep import compute_area

    return compute_area(brep.native_brep)
```

The function name, category, and domain identify the extension point. Use
`pluggable_name` only when the implementation function needs a different name.
Higher numeric priorities are preferred. If multiple available implementations
share the highest priority, selection raises `PluginConflictError` instead of
depending on discovery order.

Requirements may be importable module names or zero-argument predicates. Module
requirements are checked with `importlib.util.find_spec` and are not imported
during selection.
