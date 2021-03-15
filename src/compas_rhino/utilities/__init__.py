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

from .document import (
    get_document_basename,
    get_document_filename,
    get_document_extension,
    get_document_filepath,
    get_document_dirname
)
from .layers import (
    create_layers_from_path,
    create_layers_from_paths,
    create_layers_from_dict,
    create_layers,
    clear_layer,
    clear_current_layer,
    clear_layers,
    delete_layers
)
from .objects import (
    find_object,
    get_objects,
    get_object_layers,
    get_object_types,
    get_object_names,
    get_object_name,
    get_object_attributes,
    get_object_attributes_from_name,
    delete_object,
    delete_objects,
    purge_objects,
    is_curve_line,
    is_curve_polyline,
    is_curve_polygon,
    get_points,
    get_curves,
    get_lines,
    get_polylines,
    get_polygons,
    get_point_coordinates,
    get_line_coordinates,
    get_polyline_coordinates,
    get_polygon_coordinates,
    get_meshes,
    get_mesh_face_vertices,
    get_mesh_vertex_coordinates,
    get_mesh_vertex_colors,
    set_mesh_vertex_colors,
    get_mesh_vertices_and_faces,
    get_mesh_vertex_index,
    get_mesh_face_index,
    get_mesh_edge_index,
    select_object,
    select_objects,
    select_point,
    select_points,
    select_curve,
    select_curves,
    select_line,
    select_lines,
    select_polyline,
    select_polylines,
    select_polygon,
    select_polygons,
    select_surface,
    select_surfaces,
    select_mesh,
    select_meshes
)
from .misc import (
    wait,
    get_tolerance,
    toggle_toolbargroup,
    pick_point,
    browse_for_folder,
    browse_for_file,
    print_display_on,
    display_message,
    display_text,
    display_image,
    display_html,
    update_settings,
    update_named_values,
    screenshot_current_view,
    select_folder,
    select_file,
    unload_modules
)
from .drawing import (
    draw_labels,
    draw_points,
    draw_lines,
    draw_geodesics,
    draw_polylines,
    draw_faces,
    draw_cylinders,
    draw_pipes,
    draw_spheres,
    draw_mesh,
    draw_circles
)
from .geometry import uv_points_from_surface
from .constructors import volmesh_from_polysurfaces


__all__ = [
    'get_document_basename',
    'get_document_filename',
    'get_document_extension',
    'get_document_filepath',
    'get_document_dirname',
    'create_layers_from_path',
    'create_layers_from_paths',
    'create_layers_from_dict',
    'create_layers',
    'clear_layer',
    'clear_current_layer',
    'clear_layers',
    'delete_layers',
    'find_object',
    'get_objects',
    'get_object_layers',
    'get_object_types',
    'get_object_names',
    'get_object_name',
    'get_object_attributes',
    'get_object_attributes_from_name',
    'delete_object',
    'delete_objects',
    'purge_objects',
    'is_curve_line',
    'is_curve_polyline',
    'is_curve_polygon',
    'get_points',
    'get_curves',
    'get_lines',
    'get_polylines',
    'get_polygons',
    'get_point_coordinates',
    'get_line_coordinates',
    'get_polyline_coordinates',
    'get_polygon_coordinates',
    'get_meshes',
    'get_mesh_face_vertices',
    'get_mesh_vertex_coordinates',
    'get_mesh_vertex_colors',
    'set_mesh_vertex_colors',
    'get_mesh_vertices_and_faces',
    'get_mesh_vertex_index',
    'get_mesh_face_index',
    'get_mesh_edge_index',
    'select_object',
    'select_objects',
    'select_point',
    'select_points',
    'select_curve',
    'select_curves',
    'select_line',
    'select_lines',
    'select_polyline',
    'select_polylines',
    'select_polygon',
    'select_polygons',
    'select_surface',
    'select_surfaces',
    'select_mesh',
    'select_meshes',
    'wait',
    'get_tolerance',
    'toggle_toolbargroup',
    'pick_point',
    'browse_for_folder',
    'browse_for_file',
    'print_display_on',
    'display_message',
    'display_text',
    'display_image',
    'display_html',
    'update_settings',
    'update_named_values',
    'screenshot_current_view',
    'select_folder',
    'select_file',
    'unload_modules',
    'draw_labels',
    'draw_points',
    'draw_lines',
    'draw_geodesics',
    'draw_polylines',
    'draw_faces',
    'draw_cylinders',
    'draw_pipes',
    'draw_spheres',
    'draw_mesh',
    'draw_circles',
    'uv_points_from_surface',
    'volmesh_from_polysurfaces'
]
