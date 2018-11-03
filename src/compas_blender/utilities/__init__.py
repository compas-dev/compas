
"""
********************************************************************************
compas_blender.utilities
********************************************************************************

.. currentmodule:: compas_blender.utilities

This package contains many convenience functions for working and interacting
with Blender.


document
========

.. autosummary::
    :toctree: generated/

    get_document_name
    get_document_filename
    get_document_path
    get_document_dirname


layers
======

.. autosummary::
    :toctree: generated/

    create_layers_from_path
    create_layers_from_paths
    create_layers_from_dict
    create_layer
    create_layers
    clear_layer
    clear_layers
    clear_current_layer
    delete_layers


objects
=======

.. autosummary::
    :toctree: generated/

    get_objects
    get_object_names
    get_object_attributes
    get_object_attributes_from_name
    delete_object
    delete_objects
    purge_objects
    get_points
    get_curves
    get_lines
    get_polylines
    get_polygons
    get_point_coordinates
    get_line_coordinates
    get_polyline_coordinates
    get_polygon_coordinates
    get_meshes
    get_mesh_face_vertices
    get_mesh_vertex_coordinates
    get_mesh_vertex_colors
    set_mesh_vertex_colors
    get_mesh_vertices_and_faces
    get_mesh_vertex_index
    get_mesh_face_index
    get_mesh_edge_index
    select_point
    select_points
    select_curve
    select_curves
    select_line
    select_lines
    select_polyline
    select_polylines
    select_polygon
    select_polygons
    select_surface
    select_surfaces
    select_mesh
    select_meshes
    is_curve_line
    is_curve_polyline
    is_curve_polygon


drawing
=======

.. autosummary::
    :toctree: generated/

    xdraw_labels
    xdraw_points
    xdraw_lines
    xdraw_polylines
    xdraw_faces
    xdraw_cylinders
    xdraw_pipes
    xdraw_spheres
    xdraw_mesh


geometry
========

.. autosummary::
    :toctree: generated/

    uv_points_from_surface

"""

from .document import *
from .layers import *
from .objects import *
from .drawing import *
from .geometry import *

from .document import __all__ as a
from .layers import __all__ as b
from .objects import __all__ as c
from .drawing import __all__ as d
from .geometry import __all__ as e

__all__ = a + b + c + d + e
