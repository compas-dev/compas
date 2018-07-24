
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass

import json


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'delete_object',
    'delete_objects',
    'delete_objects_by_name',
    'get_objects',
#    'get_object_layers',
    'get_object_types',
    'get_object_name',
    'get_object_names',
    'get_object_attributes',
    'purge_objects',
    'get_points',
    'get_curves',
    'get_object_coordinates',
    'get_meshes',
#    'get_mesh_face_vertices',
#    'get_mesh_vertex_coordinates',
#    'get_mesh_vertex_colors',
#    'set_mesh_vertex_colors',
#    'get_mesh_vertices_and_faces',
#    'get_mesh_vertex_index',
#    'get_mesh_face_index',
#    'get_mesh_edge_index',
    'select_point',
    'select_points',
#    'select_curve',
#    'select_curves',
#    'select_surface',
#    'select_surfaces',
#    'select_mesh',
#    'select_meshes',
    
#    'set_object_layer',
#    'set_objects_layer',
#    'set_object_show_name',
#    'set_objects_show_name',
#    'set_object_location',
#    'set_objects_location',
#    'set_object_rotation',
#    'set_objects_rotation',
#    'set_object_scale',
#    'set_objects_scale',
#    'join_objects',
#    'select_point',
#    'select_points',
#    'select_curve',
#    'select_curves',
#    'select_mesh',
#    'select_meshes',
#    'select_object',
#    'select_objects',
#    'select_all_objects',
#    'deselect_object',
#    'deselect_objects',
#    'deselect_all_objects',
#    'hide_object',
#    'hide_objects',
#    'show_object',
#    'show_objects'
]


# ==============================================================================
# Deleting
# ==============================================================================

def delete_object(object):

   bpy.data.objects.remove(object)
   #bpy.data.objects.remove(object, True)  # unlinking argument crashes
    

def delete_objects(objects):

    for object in objects:
        delete_object(object)
        
def delete_objects_by_name(names):
    
    objects = [bpy.data.objects[name] for name in names]
    delete_objects(objects)


#def delete_all_objects():
#    """ Delete all scene objects.

#     Parameters:
#        None

#    Returns:
#        None
#    """
#    for layer in range(20):
#        delete_objects(get_objects(layer=layer))

def purge_objects():
    raise NotImplementedError


# ==============================================================================
# Get
# ==============================================================================

def get_objects(name=None, color=None, collection=None, type=None):
    
    objects = list(bpy.data.objects)
    
    if name:
        objects = [bpy.data.objects[name]]
        
    elif color:
        raise NotImplementedError
        
    elif collection:
        objects = list(bpy.data.collections[collection].objects)
        
    elif type:
        objects = [i for i in objects if i.type == type]

    return objects


def get_object_types(objects):
    
    return [object.type for object in objects]


def get_object_name(object):

    return object.name.split('.')[0]


def get_object_names(objects):
    
    return [get_object_name(object) for object in objects]


def get_object_attributes(objects):

    attrs = []
    for i in get_object_names(objects):
        name = i.replace("'", '"')
        try:
            attrs.append(json.loads(name))
        except Exception:
            attrs.append(None)
    return attrs
            

def get_object_coordinates(objects):

    return [list(object.location) for object in objects]


def get_points(collection=None):

    return [i for i in get_objects(collection=collection) if i.type == 'EMPTY']


def get_curves(collection=None):

    return [i for i in get_objects(collection=collection) if i.type == 'CURVE']


def get_meshes(collection=None):

    return [i for i in get_objects(collection=collection) if i.type == 'MESH']


# ==============================================================================
# Select
# ==============================================================================

def select_point():

    selected = bpy.context.selected_objects
    if selected:
        for object in selected:
            if object.type == 'EMPTY':
                return object
    print('***** A point (empty) object was not in the selection *****')
    return


def select_points():

    selected = bpy.context.selected_objects
    if selected:
        return [i for i in selected if i.type == 'EMPTY']
    print('***** Point (empty) objects were not in the selection *****')
    return


#def select_curve():
#    """ Select curve object.

#    Parameters:
#        None

#    Returns:
#        obj: Curve object or None.
#    """
#    selected = bpy.context.selected_objects
#    if selected:
#        for object in selected:
#            if object.type == 'CURVE':
#                return object
#    print('***** Curve object was not selected *****')
#    return None


#def select_curves():
#    """ Select curve objects.

#    Parameters:
#        None

#    Returns:
#        list: Curve objects or None.
#    """
#    selected = bpy.context.selected_objects
#    if selected:
#        return [object for object in selected if object.type == 'CURVE']
#    print('***** Curve objects were not selected *****')
#    return None


#def select_mesh():
#    """ Select Blender mesh object.

#    Parameters:
#        None

#    Returns:
#        obj: Blender mesh object or None.
#    """
#    selected = bpy.context.selected_objects
#    if selected:
#        for object in selected:
#            if object.type == 'MESH':
#                return object
#    print('***** Mesh object was not selected *****')
#    return None


#def select_meshes():
#    """ Select Blender mesh objects.

#    Parameters:
#        None

#    Returns:
#        list: Blender mesh objects or None.
#    """
#    selected = bpy.context.selected_objects
#    if selected:
#        return [object for object in selected if object.type == 'MESH']
#    print('***** Mesh objects were not selected *****')
#    return None


#def select_object(object):
#    """ Select specific object.

#    Parameters:
#        object (obj): Object to select.

#    Returns:
#        None
#    """
#    object.select = True


#def select_objects(objects):
#    """ Select specific objects.

#    Parameters:
#        objects (list): Objects to select.

#    Returns:
#        None
#    """
#    for object in objects:
#        object.select = True


#def select_all_objects():
#    """ Select all objects.

#    Parameters:
#        None

#    Returns:
#        None
#    """
#    objects = bpy.context.scene.objects
#    for object in objects:
#        object.select = True


#def deselect_object(object):
#    """ De-select a specific object.

#    Parameters:
#        object (obj): Object to de-select.

#    Returns:
#        None
#    """
#    object.select = False


#def deselect_objects(objects):
#    """ De-select specific objects.

#    Parameters:
#        objects (list): Objects to de-select.

#    Returns:
#        None
#    """
#    if not isinstance(objects, list):
#        objects = [objects]
#    for object in objects:
#        object.select = False


#def deselect_all_objects():
#    """ De-select all objects.

#    Parameters:
#        None

#    Returns:
#        None
#    """
#    deselect_objects(list(bpy.data.objects))


## ==============================================================================
## Visibility
## ==============================================================================

#def hide_object(object):
#    """ Hide specific object.

#    Parameters:
#        object (obj): Object to hide.

#    Returns:
#        None
#    """
#    object.hide = True


#def hide_objects(objects):
#    """ Hide specific objects.

#    Parameters:
#        objects (list): Objects to hide.

#    Returns:
#        None
#    """
#    for object in objects:
#        object.hide = True


#def show_object(object):
#    """ Show specific object.

#    Parameters:
#        object (obj): Object to show.

#    Returns:
#        None
#    """
#    object.hide = False


#def show_objects(objects):
#    """ Show specific objects.

#    Parameters:
#        objects (list): Objects to show.

#    Returns:
#        None
#    """
#    for object in objects:
#        object.hide = False


## ==============================================================================
## Set attributes
## ==============================================================================

#def set_object_layer(object, layer):
#    """ Changes the layer of the object.

#    Parameters:
#        object (obj): Object for layer change.
#        layer (int): Layer number.

#    Returns:
#        None
#    """
#    mask = tuple(i == layer for i in range(20))
#    object.layers = mask


#def set_objects_layer(objects, layer):
#    """ Changes the layer of the objects.

#    Parameters:
#        objects (list): Objects for layer change.
#        layer (int): Layer number.

#    Returns:
#        None
#    """
#    mask = tuple(i == layer for i in range(20))
#    for object in objects:
#        object.layers = mask


#def set_object_show_name(object, show=True):
#    """ Display the name of an object.

#    Parameters:
#        object (obj): Object to display name.
#        show (bool): True or False.

#    Returns:
#        None
#    """
#    object.show_name = show


#def set_objects_show_name(objects, show=True):
#    """ Display the name of objects.

#    Parameters:
#        objects (list): Objects to display name.
#        show (bool): True or False.

#    Returns:
#        None
#    """
#    for object in objects:
#        object.show_name = show


#def set_object_location(object, location):
#    """ Set the location of an object.

#    Parameters:
#        object (obj): Object to set location.
#        location (list): Location.

#    Returns:
#        None
#    """
#    object.location = location


#def set_objects_location(objects, locations):
#    """ Set the location of objects.

#    Parameters:
#        objects (list): Objects to set location.
#        locations (list): List of locations.

#    Returns:
#        None
#    """
#    for i, location in enumerate(locations):
#        objects[i].location = location


#def set_object_rotation(object, rotation):
#    """ Set the rotation of an object.

#    Parameters:
#        object (obj): Object to set rotation.
#        rotation (list): Rotation.

#    Returns:
#        None
#    """
#    object.rotation_euler = rotation


#def set_objects_rotation(objects, rotations):
#    """ Set the rotation of objects.

#    Parameters:
#        objects (list): Objects to set rotation.
#        rotations (list): List of rotations.

#    Returns:
#        None
#    """
#    for i, rotation in enumerate(rotations):
#        objects[i].rotation_euler = rotation


#def set_object_scale(object, scale):
#    """ Set the scale of an object.

#    Parameters:
#        object (obj): Object to set scale.
#        scale (list): Scale.

#    Returns:
#        None
#    """
#    object.scale = scale


#def set_objects_scale(objects, scales):
#    """ Set the scale of objects.

#    Parameters:
#        objects (list): Objects to set scale.
#        scales (list): List of scales.

#    Returns:
#        None
#    """
#    for i, scale in enumerate(scales):
#        objects[i].scale = scale


## ==============================================================================
## Misc
## ==============================================================================

#def join_objects(objects):
#    """ Join a list of objects.

#    Notes:
#        - The first object in the list becomes the master object.

#    Parameters:
#        objects (list): Objects to join.

#    Returns:
#        obj: Joined object.
#    """
#    select_objects(objects=objects)
#    bpy.context.scene.objects.active = objects[0]
#    bpy.ops.object.join()
#    return objects[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    #print(get_objects(name='Cube'))
    #print(get_objects(type='MESH'))
    #print(get_objects(collection='Collection 1'))
    
    #print(get_object_types(objects=get_objects(collection='Collection 1')))
    #print(get_object_name(object=get_objects(collection='Collection 1')[0]))
    #print(get_object_names(objects=get_objects(collection='Collection 1')))
    #print(get_object_attributes(objects=get_objects(collection='Collection 1')))
    
    #print(get_object_coordinates(objects=get_objects(collection='Collection 1')))
    
    #print(get_meshes())
    #print(get_points())
    #print(get_curves())
    #print(get_meshes(collection='Collection 1'))
    #print(get_points(collection='Collection 1'))
    
    #delete_object(get_objects(name='Cube')[0])
    #delete_objects_by_name(names=['Cube'])
    #delete_object(get_objects(collection='Collection 1'))
 
    #bpy.ops.object.select_by_type(type='MESH') 
    