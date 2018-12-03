
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

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
    'get_objects_coordinates',
    'get_object_attributes',
    'get_objects_attributes',
    'get_points',
    'get_curves',
    'get_meshes',
    'get_points_coordinates',
    'get_curves_coordinates',
    'select_object',
    'select_objects',
    'select_point',
    'select_points',
    'select_curve',
    'select_curves',
    'select_surface',
    'select_surfaces',
    'select_mesh',
    'select_meshes',
    'set_select',
    'set_deselect',
    'set_objects_layer',
    'set_objects_coordinates',
    'set_objects_rotations',
    'set_objects_scales',
    'set_objects_show_names',
    'set_objects_visible',
]


# ==============================================================================
# Delete
# ==============================================================================

def delete_object(object):

    set_deselct(object=object)
    bpy.data.objects.remove(object)
    # crashes 2.80


def delete_objects(objects):

    for object in objects:
        delete_object(object=object)


def delete_objects_by_names(names):

    objects = [bpy.data.objects[name] for name in names]
    delete_objects(objects=objects)


def purge_objects(objects):
    
    raise NotImplementedError


# ==============================================================================
# Objects
# ==============================================================================

def get_objects(names=None, color=None, layer=None, type=None):

    if names:
        objects = [bpy.data.objects[name] for name in names]

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

    return [get_object_name(i) for i in objects]


def get_objects_layers(objects):

    return [i.users_collection for i in objects]


def get_objects_types(objects):

    return [i.type for i in objects]


def get_objects_coordinates(objects):

    return [list(i.location) for i in objects]


def get_object_attributes(object):

    name = object.name.replace("'", '"')
    
    if name[-5:-3] == '}.':
        name = name[:-4]

    try:
        return json.loads(name)
    except:
        return


def get_objects_attributes(objects):
    
    return [get_object_attributes(i) for i in objects]


def select_object(message="Select an object."):

    raise NotImplementedError


def select_objects(message='Select objects.'):

    raise NotImplementedError


# ==============================================================================
# Points
# ==============================================================================

def get_points(layer=None):

    return [i for i in get_objects(layer=layer) if i.type == 'EMPTY']


def select_point(message='Select a point.'):

    raise NotImplementedError


def select_points(message='Select points.'):

    raise NotImplementedError


def get_points_coordinates(objects):

    return [list(i.location) for i in objects if i.type == 'EMPTY']


# ==============================================================================
# Curves
# ==============================================================================

def get_curves(layer=None):

    return [i for i in get_objects(layer=layer) if i.type == 'CURVE']


def select_curve(message='Select curve.'):

    raise NotImplementedError


def select_curves(message='Select curves.'):

    raise NotImplementedError


def get_curves_coordinates(objects):

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


# ==============================================================================
# Set
# ==============================================================================

def set_select(objects=None):

    if objects:
        for i in objects:
            i.select_set(state=True)
    else:
        bpy.ops.object.select_all(action='SELECT')


def set_deselect(objects=None):

    if objects:
        for i in objects:
            i.select_set(state=False)
    else:
        bpy.ops.object.select_all(action='DESELECT')


def set_objects_layer(objects):

    raise NotImplementedError


def set_objects_coordinates(objects, coords):

    for i, j in zip(objects, coords):
        i.location = j


def set_objects_rotations(objects, rotations):

    for i, j in zip(objects, rotations):
        i.rotation_euler = j


def set_objects_scales(objects, scales):

    for i, j in zip(objects, scales):
        i.scale = j


def set_objects_show_names(objects, show=True):

    for i in objects:
        i.show_name = show


def set_objects_visible(objects, visible=True):

    for i in objects:
        i.hide_viewport = not visible


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    objects = get_objects(layer='Collection 1')

    #print(get_objects(names=['Plane', 'Sphere']))
    #print(get_objects(layer='Collection 2'))
    #print(get_objects(type='Mesh'))
    
    #print(get_object_name(object=objects[1]))
    #print(get_objects_names(objects=objects))
    #print(get_objects_types(objects=objects))
    #print(get_objects_coordinates(objects=objects))
    #print(get_objects_layers(objects=objects))
    
    #print(get_points())
    #print(get_curves())
    #print(get_meshes())

    #a = get_objects_attributes(objects=objects)
    
    #set_deselect()
    #set_deselect(objects=objects)

    #for i in dir(objects[0]):
    #    print(i)

    #set_objects_coordinates(objects=objects, coords=[[0, 0, 3], [0, 0, 4]])
    #set_objects_rotations(objects=objects, rotations=[[2, 0, 0], [0, 0, 2]])
    #set_objects_scales(objects=objects, scales=[[2, 2, 2], [3, 3, 3]])

    #set_objects_show_names(objects=objects, show=1)
    #set_objects_visible(objects=objects, visible=1)
    
    #delete_object(object=objects[0])
