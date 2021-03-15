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
from .data import delete_unused_data
from .objects import (
    delete_object,
    delete_objects,
    delete_all_objects,
    delete_object_by_name,
    delete_objects_by_names,
    get_object_by_name,
    get_objects_by_names
)
from .collections import (
    create_collection,
    create_collections,
    create_collections_from_path,
    clear_collection,
    clear_collections
)
from .drawing import (
    draw_points,
    draw_pointcloud,
    draw_lines,
    draw_polylines,
    draw_cylinders,
    draw_spheres,
    draw_cubes,
    draw_pipes,
    draw_faces,
    draw_texts,
    draw_mesh
)
from .misc import unload_modules


__all__ = [
    'delete_unused_data',
    'delete_object',
    'delete_objects',
    'delete_all_objects',
    'delete_object_by_name',
    'delete_objects_by_names',
    'get_object_by_name',
    'get_objects_by_names',
    'create_collection',
    'create_collections',
    'create_collections_from_path',
    'clear_collection',
    'clear_collections',
    'draw_points',
    'draw_pointcloud',
    'draw_lines',
    'draw_polylines',
    'draw_cylinders',
    'draw_spheres',
    'draw_cubes',
    'draw_pipes',
    'draw_faces',
    'draw_texts',
    'draw_mesh',
    'unload_modules'
]
