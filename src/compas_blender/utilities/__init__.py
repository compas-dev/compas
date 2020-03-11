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

    create_layer
    create_layers
    create_layers_from_path
    create_layers_from_paths
    create_layers_from_dict
    clear_layer
    clear_layers
    clear_current_layer
    delete_layer
    delete_layers


misc
====

.. autosummary::
    :toctree: generated/

    get_tolerance
    screenshot_current_view
    wait
    browse_for_folder
    browse_for_file
    display_message
    display_text
    display_image
    display_html
    update_settings
    update_attributes
    update_named_values


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
    get_objects
    get_object_name
    get_objects_names
    get_objects_layers
    get_objects_types
    get_objects_coordinates
    get_object_property
    get_objects_property
    get_points
    get_curves
    get_meshes
    get_points_coordinates
    get_curves_coordinates
    select_object
    select_objects
    select_point
    select_points
    select_curve
    select_curves
    select_surface
    select_surfaces
    select_mesh
    select_meshes
    set_select
    set_deselect
    set_objects_layer
    set_objects_coordinates
    set_objects_rotations
    set_objects_scales
    set_objects_show_names
    set_objects_visible
    set_object_property
    set_objects_property


drawing
=======

.. autosummary::
    :toctree: generated/

    create_material
    draw_points
    draw_lines
    draw_geodesics
    draw_breps
    draw_cylinders
    draw_pipes
    draw_forces
    draw_spheres
    draw_cubes
    draw_mesh
    draw_faces
    draw_pointcloud
    draw_texts

"""
from .misc import *  # noqa: F401 F403
from .document import *  # noqa: F401 F403
from .data import *  # noqa: F401 F403
from .objects import *  # noqa: F401 F403
from .layers import *  # noqa: F401 F403
from .collections import *  # noqa: F401 F403
from .drawing import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
