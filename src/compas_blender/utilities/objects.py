
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'delete_object',
    'delete_objects',
    'delete_objects_by_names',
    'purge_objects',
    'get_objects',
    'get_object_name',
    'get_objects_names',
    'get_objects_layers',
    'get_objects_types',
    # 'get_object_attributes',
    # 'get_object_attributes_from_name',
    'get_points',
    'get_curves',
    # 'get_point_coordinates',
    # 'get_line_coordinates',
    # 'get_polyline_coordinates',
    # 'get_polygon_coordinates',
    'get_meshes',
    # 'get_mesh_face_vertices',
    # 'get_mesh_vertex_coordinates',
    # 'get_mesh_vertex_colors',
    # 'set_mesh_vertex_colors',
    # 'get_mesh_vertices_and_faces',
    # 'get_mesh_vertex_index',
    # 'get_mesh_face_index',
    # 'get_mesh_edge_index',
    # 'select_object',
    # 'select_objects',
    'select_point',
    'select_points',
    'select_curve',
    'select_curves',
    'select_surface',
    'select_surfaces',
    'select_mesh',
    'select_meshes',
]


# ==============================================================================
# Delete
# ==============================================================================

def delete_object(object):

    bpy.data.objects.remove(object)


def delete_objects(objects):

    for object in objects:
        delete_object(object)


def delete_objects_by_names(names):

    objects = [bpy.data.objects[name] for name in names]
    delete_objects(objects)


def purge_objects(objects):
    raise NotImplementedError


# ==============================================================================
# Get
# ==============================================================================

def get_objects(name=None, color=None, layer=None, type=None):

    if name:
        objects = [bpy.data.objects[name]]

    elif color:
        raise NotImplementedError

    elif layer:
        objects = list(bpy.data.collections[layer].objects)

    elif type:
        objects = [i for i in bpy.data.objects if i.type == type.upper()]

    else:
        objects = list(bpy.data.objects)

    return objects


def get_object_name(object):

    return object.name.split('.')[0]


def get_objects_names(objects):

    return [get_object_name(object) for object in objects]


def get_objects_layers(objects):

    raise NotImplementedError


def get_objects_types(objects):

    return [object.type for object in objects]


# ==============================================================================
# Points
# ==============================================================================

def get_points(layer=None):

    return [i for i in get_objects(layer=layer) if i.type == 'EMPTY']


def select_point(message='Select a point.'):

    raise NotImplementedError


def select_points(message='Select points.'):

    raise NotImplementedError


# ==============================================================================
# Curves
# ==============================================================================

def get_curves(layer=None):

    return [i for i in get_objects(layer=layer) if i.type == 'CURVE']


def select_curve(message='Select curve.'):

    raise NotImplementedError


def select_curves(message='Select curves.'):

    raise NotImplementedError


# ==============================================================================
# Meshes
# ==============================================================================

def get_meshes(layer=None):

    return [i for i in get_objects(layer=layer) if i.type == 'MESH']


def select_mesh(message='Select a mesh.'):

    raise NotImplementedError


def select_meshes(message='Select meshes.'):

    raise NotImplementedError


# ==============================================================================
# Surfaces
# ==============================================================================

def select_surface(message='Select a surface.'):

    raise NotImplementedError


def select_surfaces(message='Select surfaces.'):

    raise NotImplementedError

























def get_object_attributes(guids):

    raise NotImplementedError


def get_object_attributes_from_name(guids):

    raise NotImplementedError


def select_object(message="Select an object."):

    raise NotImplementedError


def select_objects(message='Select objects.'):

    raise NotImplementedError


def get_point_coordinates(guids):

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

    objects = get_objects()

    print(objects)
    print(get_object_types(objects=objects))
    print(get_object_names(objects=objects))

    #bpy.ops.object.move_to_collection(collection_index=2)
#    delete_objects(get_objects(layer=layer))
#    elif isinstance(layers, list):
#        for layer in layers:
#            delete_objects(get_objects(layer=layer))
