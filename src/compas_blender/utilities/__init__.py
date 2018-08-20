"""
********************************************************************************
compas_blender.utilities
********************************************************************************

.. currentmodule:: compas_blender.utilities


This package contains many convenience functions for working and interacting
with Blender.


document
--------

.. autosummary::
    :toctree: generated/


layers
------

.. autosummary::
    :toctree: generated/

    clear_layer
    clear_layers
    layer_mask


objects
-------

.. autosummary::
    :toctree: generated/

    delete_object
    delete_objects
    delete_all_objects
    get_objects
    get_object_name
    get_objects_name
    get_object_attributes
    get_objects_attributes
    get_object_location
    get_objects_location
    get_points
    get_curves
    get_meshes
    set_object_layer
    set_objects_layer
    set_object_show_name
    set_objects_show_name
    set_object_location
    set_objects_location
    set_object_rotation
    set_objects_rotation
    set_object_scale
    set_objects_scale
    join_objects
    select_point
    select_points
    select_curve
    select_curves
    select_mesh
    select_meshes
    select_object
    select_objects
    select_all_objects
    deselect_object
    deselect_objects
    deselect_all_objects
    hide_object
    hide_objects
    show_object
    show_objects


misc
----

.. autosummary::
    :toctree: generated/


drawing
-------

.. autosummary::
    :toctree: generated/

    delete_all_materials
    create_material
    draw_cuboid
    draw_cubes
    draw_pipes
    draw_plane
    draw_spheres
    draw_lines
    draw_points
    xdraw_cubes
    xdraw_faces
    xdraw_labels
    xdraw_lines
    xdraw_mesh
    xdraw_pipes
    xdraw_pointcloud
    xdraw_points
    xdraw_spheres
    xdraw_texts


modifiers
---------

.. autosummary::
    :toctree: generated/

    bevel
    linear_array
    subdivide
    triangulate


"""
from __future__ import absolute_import

from .document import *
from .objects import *
from .misc import *
from .drawing import *
from .modifiers import *
from .layers import *

from . import document
from . import layers
from . import objects
from . import misc
from . import drawing
from . import modifiers

__all__ = []

__all__ += document.__all__
__all__ += layers.__all__
__all__ += objects.__all__
__all__ += misc.__all__
__all__ += drawing.__all__
__all__ += modifiers.__all__

