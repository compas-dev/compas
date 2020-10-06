"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas_blender.utilities

This package contains low-level functions for working and interacting with Blender.


collections
===========

.. autosummary::
    :toctree: generated/

    create_collection
    create_collections
    create_collections_from_path
    clear_collection
    clear_collections


data
====

.. autosummary::
    :toctree: generated/

    delete_unused_data


drawing
=======

.. autosummary::
    :toctree: generated/

    draw_points
    draw_pointcloud
    draw_lines
    draw_cylinders
    draw_spheres
    draw_cubes
    draw_mesh
    draw_faces
    draw_texts


objects
=======

.. autosummary::
    :toctree: generated/

    delete_object
    delete_objects
    delete_object_by_name
    delete_objects_by_names
    get_object_by_name
    get_objects_by_names

"""
from .data import *  # noqa: F401 F403
from .objects import *  # noqa: F401 F403
from .collections import *  # noqa: F401 F403
from .drawing import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
