
********************************************************************************
API Reference
********************************************************************************

compas
------

This package is the core package of the COMPAS framework.
It defines all functionality for geometry processing,
data structures, topology, numerical methods, robotics, the plugin mechanism, remote procedure calls ...
and can be used independently of CAD systems in any environment that supports Python programming.

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: compas

    compas.colors
    compas.data
    compas.datastructures
    compas.files
    compas.geometry
    compas.plugins
    compas.rpc
    compas.scene


compas_blender
--------------

This package provides functionality for reading and writing Blender geometry, for visualising
COMPAS geometry and data structures in Blender, and for basic user inter interaction.

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: compas_blender

    compas_blender.conversions
    compas_blender.geometry
    compas_blender.scene


compas_ghpython
---------------

This package provides functionality for reading and writing Rhino geometry, and for visualising
COMPAS geometry and data structures in Rhino, through GHPython.

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: compas_ghpython

    compas_ghpython.components
    compas_ghpython.scene


compas_rhino
------------

This package provides functionality for reading and writing Rhino geometry, for visualising
COMPAS geometry and data structures in Rhino, and for basic user inter interaction.

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: compas_rhino

    compas_rhino.conversions
    compas_rhino.geometry
    compas_rhino.scene


compas_rhino8
-------------

.. warning::
    
    This package is still in development and should not be used in production.

This package provides functionality for reading and writing geometry, for visualising
COMPAS geometry and data structures, and for basic user inter interaction in Rhino 8, using CPython specifically.

.. toctree::
    :maxdepth: 1
    :titlesonly:
    :caption: compas_rhino

    compas_rhino8.conversions
    compas_rhino8.install
    compas_rhino8.layers
    compas_rhino8.objects
    compas_rhino8.scene
