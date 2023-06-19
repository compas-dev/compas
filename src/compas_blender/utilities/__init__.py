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
    :nosignatures:

    create_collection
    create_collections
    create_collections_from_path
    clear_collection
    clear_collections


data
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delete_unused_data


drawing
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    draw_points
    draw_pointcloud
    draw_lines
    draw_cylinders
    draw_spheres
    draw_cubes
    draw_mesh
    draw_faces
    draw_texts
    draw_curves
    draw_surfaces


objects
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delete_object
    delete_objects
    delete_object_by_name
    delete_objects_by_names
    get_object_by_name
    get_objects_by_names

misc
====

.. autosummary::
    :toctree: generated/

    unload_modules

"""
from .data import delete_unused_data
from .objects import (
    delete_object,
    delete_objects,
    delete_all_objects,
    delete_object_by_name,
    delete_objects_by_names,
    get_object_by_name,
    get_objects_by_names,
)
from .collections import (
    create_collection,
    create_collections,
    create_collections_from_path,
    clear_collection,
    clear_collections,
)
from .drawing import (
    draw_circles,
    draw_cylinders,
    draw_cubes,
    draw_faces,
    draw_lines,
    draw_mesh,
    draw_pipes,
    draw_planes,
    draw_pointcloud,
    draw_points,
    draw_polylines,
    draw_spheres,
    draw_texts,
    draw_curves,
    draw_surfaces,
    RGBColor,
)
from .misc import unload_modules


__all__ = [
    "delete_unused_data",
    "delete_object",
    "delete_objects",
    "delete_all_objects",
    "delete_object_by_name",
    "delete_objects_by_names",
    "get_object_by_name",
    "get_objects_by_names",
    "create_collection",
    "create_collections",
    "create_collections_from_path",
    "clear_collection",
    "clear_collections",
    "draw_circles",
    "draw_cylinders",
    "draw_cubes",
    "draw_faces",
    "draw_lines",
    "draw_mesh",
    "draw_pipes",
    "draw_planes",
    "draw_pointcloud",
    "draw_points",
    "draw_polylines",
    "draw_spheres",
    "draw_texts",
    "draw_curves",
    "draw_surfaces",
    "RGBColor",
    "unload_modules",
]
