"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas_rhino.utilities


This package contains many convenience functions for working and interacting
with Rhino.


document
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    get_document_basename
    get_document_filename
    get_document_filepath
    get_document_dirname


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

.. note::

    Note that the meaning of the naming conventions used here is somewhat different
    than those used in Rhino and rhinoscriptsyntax modules.

    Functions prefixed with ``get_`` imply that guids are obtained by applying some
    kind of filter. For example, get all lines with a specified naming pattern, on a
    specific layer, or with a specific color.

    Functions prefixed with ``select_`` imply that guids are obtained by manual
    selection.


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


misc
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    wait
    get_tolerance
    toggle_toolbargroup
    pick_point
    browse_for_folder
    browse_for_file
    print_display_on
    display_message
    display_text
    display_image
    display_html
    update_settings
    update_named_values
    screenshot_current_view


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


geometry
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    uv_points_from_surface


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
