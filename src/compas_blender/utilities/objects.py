
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'get_objects',
    'get_object_layers',
    'get_object_types',
    'get_object_names',
    'get_object_name',
    'get_object_attributes',
    'get_object_attributes_from_name',
    'delete_object',
    'delete_objects',
    'delete_objects_by_name',
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
]


# ==============================================================================
# Objects
# ==============================================================================

def get_objects(name=None, color=None, layer=None, type=None):

    raise NotImplementedError


def delete_object(guid, purge=None):

    raise NotImplementedError


def delete_objects(guids, purge=None):

    raise NotImplementedError


def delete_objects_by_name(name, purge=None):

    raise NotImplementedError


def purge_objects(guids):

    raise NotImplementedError


def get_object_layers(guids):

    raise NotImplementedError


def get_object_types(guids):

    raise NotImplementedError


def get_object_names(guids):

    raise NotImplementedError


def get_object_name(guid):

    raise NotImplementedError


def get_object_attributes(guids):

    raise NotImplementedError


def get_object_attributes_from_name(guids):

    raise NotImplementedError


def select_object(message="Select an object."):

    raise NotImplementedError


def select_objects(message='Select objects.'):

    raise NotImplementedError


# ==============================================================================
# Points
# ==============================================================================

def select_point(message='Select a point.'):

    raise NotImplementedError


def select_points(message='Select points.'):

    raise NotImplementedError


def get_points(layer=None):

    raise NotImplementedError


def get_point_coordinates(guids):

    raise NotImplementedError


# ==============================================================================
# Curves
# ==============================================================================

def is_curve_line(guid):

    raise NotImplementedError


def is_curve_polyline(guid):

    raise NotImplementedError


def is_curve_polygon(guid):

    raise NotImplementedError


def select_curve(message='Select curve.'):

    raise NotImplementedError


def select_curves(message='Select curves.'):

    raise NotImplementedError


def select_line(message='Select line.'):

    raise NotImplementedError


def select_lines(message='Select lines.'):

    raise NotImplementedError


def select_polyline(message='Select a polyline (curve with degree = 1, and multiple segments).'):

    raise NotImplementedError


def select_polylines(message='Select polylines (curves with degree = 1, and multiple segments).'):

    raise NotImplementedError


def select_polygon(message='Select a polygon (closed curve with degree = 1)'):

    raise NotImplementedError


def select_polygons(message='Select polygons (closed curves with degree = 1)'):

    raise NotImplementedError


def get_curves(layer=None):

    raise NotImplementedError


def get_lines(layer=None):

    raise NotImplementedError


def get_polylines(layer=None):

    raise NotImplementedError


def get_polygons(layer=None):

    raise NotImplementedError


def get_curve_coordinates():

    raise NotImplementedError


def get_line_coordinates(guids):

    raise NotImplementedError


def get_polycurve_coordinates():

    raise NotImplementedError


def get_polyline_coordinates(guids):

    raise NotImplementedError


def get_polygon_coordinates(guids):

    raise NotImplementedError


# ==============================================================================
# Surfaces
# ==============================================================================

def select_surface(message='Select a surface.'):

    raise NotImplementedError


def select_surfaces(message='Select surfaces.'):

    raise NotImplementedError


# ==============================================================================
# Meshes
# ==============================================================================

def select_mesh(message='Select a mesh.'):

    raise NotImplementedError


def select_meshes(message='Select meshes.'):

    raise NotImplementedError


def get_meshes(layer=None):

    raise NotImplementedError


def get_mesh_border(guid):

    raise NotImplementedError


def get_mesh_face_vertices(guid):

    raise NotImplementedError


def get_mesh_vertex_coordinates(guid):

    raise NotImplementedError


def get_mesh_vertex_colors(guid):

    raise NotImplementedError


def set_mesh_vertex_colors(guid, colors):

    raise NotImplementedError


def get_mesh_vertices_and_faces(guid):

    raise NotImplementedError


def get_mesh_vertex_index(guid):

    raise NotImplementedError


def get_mesh_face_index(guid):

    raise NotImplementedError


def get_mesh_edge_index(guid):

    raise NotImplementedError


def get_mesh_vertex_indices(guid):

    raise NotImplementedError


def get_mesh_face_indices(guid):

    raise NotImplementedError


def get_mesh_vertex_face_indices(guid):

    raise NotImplementedError


def get_mesh_face_vertex_indices(guid):

    raise NotImplementedError


def get_mesh_edge_vertex_indices(guid):

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
