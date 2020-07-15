"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas_rhino.utilities


layers
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    create_layers
    clear_layers
    delete_layers


objects
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delete_object
    delete_objects
    get_line_coordinates
    get_objects
    get_object_attributes
    get_object_attributes_from_name
    get_object_layers
    get_object_types
    get_object_names
    get_object_name
    get_point_coordinates
    get_polyline_coordinates
    get_polygon_coordinates
    purge_objects
    select_curve
    select_curves
    select_line
    select_lines
    select_mesh
    select_meshes
    select_point
    select_points
    select_polygon
    select_polygons
    select_polyline
    select_polylines
    select_surface
    select_surfaces


drawing
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    draw_labels
    draw_points
    draw_lines
    draw_polylines
    draw_faces
    draw_cylinders
    draw_pipes
    draw_spheres
    draw_mesh


constructors
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    volmesh_from_polysurfaces

"""
from __future__ import absolute_import

from .document import *  # noqa: F401 F403
from .layers import *  # noqa: F401 F403
from .objects import *  # noqa: F401 F403
from .misc import *  # noqa: F401 F403
from .drawing import *  # noqa: F401 F403
from .geometry import *  # noqa: F401 F403
from .constructors import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
