# Developing an Extension

COMPAS extensions are separate Python distributions that depend on the core
framework and provide domain-specific algorithms, integrations, or workflows.
Keeping extensions separate allows the core package to remain
host-independent and keeps optional dependencies out of ordinary COMPAS
installations.

An extension should declare COMPAS as a dependency, expose a focused public
API, and use the plugin system when it supplies implementations for core
pluggables.
