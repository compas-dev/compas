try:
    import bpy
except ImportError:
    pass

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'delete_object',
    'delete_objects',
    'delete_all_objects',
    'get_objects',
    'get_object_name',
    'get_objects_name',
    'get_object_attributes',
    'get_objects_attributes',
    'get_object_location',
    'get_objects_location',
    'get_points',
    'get_curves',
    'get_meshes',
    'set_object_layer',
    'set_objects_layer',
    'set_object_show_name',
    'set_objects_show_name',
    'set_object_location',
    'set_objects_location',
    'set_object_rotation',
    'set_objects_rotation',
    'set_object_scale',
    'set_objects_scale',
    'join_objects',
    'select_point',
    'select_points',
    'select_curve',
    'select_curves',
    'select_mesh',
    'select_meshes',
    'select_object',
    'select_objects',
    'select_all_objects',
    'deselect_object',
    'deselect_objects',
    'deselect_all_objects',
    'hide_object',
    'hide_objects',
    'show_object',
    'show_objects'
]


# ==============================================================================
# Deleting
# ==============================================================================

def delete_object(object):
    """ Delete an object.

    Parameters:
        object (object): Object to delete.

    Returns:
        None
    """
    objs = bpy.data.objects
    objs.remove(object, True)


def delete_objects(objects):
    """ Delete a list of objects.

    Parameters:
        objects (list): Objects to delete.

    Returns:
        None
    """
    objs = bpy.data.objects
    for object in objects:
        objs.remove(object, True)


def delete_all_objects():
    """ Delete all scene objects.

     Parameters:
        None

    Returns:
        None
    """
    for layer in range(20):
        delete_objects(get_objects(layer=layer))


# ==============================================================================
# Get
# ==============================================================================

def get_objects(layer=None, name=None):
    """ Retrieves the objects on a given layer or by its name.

    Parameters:
        layer (int): Layer number.
        name (str): Object name.

    Returns:
        list: Objects in the layer or of given name.
    """
    if layer is not None:
        objects = [object for object in bpy.data.objects if object.layers[layer]]
    elif name:
        try:
            objects = bpy.data.objects[name]
        except Exception:
            objects = []
    return objects


def get_object_location(object):
    """ Retrieves the location of an object.

    Parameters:
        object (obj): Object to get location.

    Returns:
        list: Object location.
    """
    return list(object.location)


def get_objects_location(objects):
    """ Retrieves the location of objects.

    Parameters:
        objects (list): Objects to get locations.

    Returns:
        list: Object locations.
    """
    return [list(object.location) for object in objects]


def get_object_name(object):
    """ Retrieves the name of object.

    Parameters:
        object (obj): Object to get name.

    Returns:
        str: Object name.
    """
    if object.name[-5:-3] == '}.':
        return object.name[:-4]
    return object.name


def get_objects_name(objects):
    """ Retrieves the names of objects.

    Parameters:
        objects (list): Objects to get names.

    Returns:
        list: Object names.
    """
    names = []
    for object in objects:
        if object.name[-5:-3] == '}.':
            names.append(object.name[:-4])
        else:
            names.append(object.name)
    return names


def get_object_attributes(object):
    """ Retrieves the attributes from the names of object.

    Parameters:
        object (obj): Object to get attributes.

    Returns:
        dic: Object attributes.
    """
    name_ = get_object_name(object)
    name = name_.replace("'", '"')
    try:
        return json.loads(name)
    except Exception:
        print('Error reading object names with JSON')


def get_objects_attributes(objects):
    """ Retrieves the attributes from the names of objects.

    Parameters:
        objects (list): Objects to get attributes.

    Returns:
        list: Object attributes.
    """
    names = []
    for name in get_objects_name(objects):
        names.append(name.replace("'", '"'))
    try:
        return [json.loads(name) for name in names]
    except Exception:
        print('Error reading object names with JSON')


def get_points():
    """ Retrieves all Empty objects in scene.

    Parameters:
        None

    Returns:
        list: Empty objects.
    """
    objects = bpy.context.scene.objects
    return [object for object in objects if object.type == 'EMPTY']


def get_curves():
    """ Retrieves all Curve objects in scene.

    Parameters:
        None

    Returns:
        list: Curve objects.
    """
    objects = bpy.context.scene.objects
    return [object for object in objects if object.type == 'CURVE']


def get_meshes():
    """ Retrieves all Mesh objects in scene.

    Parameters:
        None

    Returns:
        list: Mesh objects.
    """
    objects = bpy.context.scene.objects
    return [object for object in objects if object.type == 'MESH']


# ==============================================================================
# Select
# ==============================================================================

def select_point():
    """ Select point (empty) object.

    Parameters:
        None

    Returns:
        obj: Empty object or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        for object in selected:
            if object.type == 'EMPTY':
                return object
    print('***** Point (empty) object was not selected *****')
    return None


def select_points():
    """ Select points (empty) objects.

    Parameters:
        None

    Returns:
        list: Empty objects or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        return [object for object in selected if object.type == 'EMPTY']
    print('***** Point (empty) objects were not selected *****')
    return None


def select_curve():
    """ Select curve object.

    Parameters:
        None

    Returns:
        obj: Curve object or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        for object in selected:
            if object.type == 'CURVE':
                return object
    print('***** Curve object was not selected *****')
    return None


def select_curves():
    """ Select curve objects.

    Parameters:
        None

    Returns:
        list: Curve objects or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        return [object for object in selected if object.type == 'CURVE']
    print('***** Curve objects were not selected *****')
    return None


def select_mesh():
    """ Select Blender mesh object.

    Parameters:
        None

    Returns:
        obj: Blender mesh object or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        for object in selected:
            if object.type == 'MESH':
                return object
    print('***** Mesh object was not selected *****')
    return None


def select_meshes():
    """ Select Blender mesh objects.

    Parameters:
        None

    Returns:
        list: Blender mesh objects or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        return [object for object in selected if object.type == 'MESH']
    print('***** Mesh objects were not selected *****')
    return None


def select_object(object):
    """ Select specific object.

    Parameters:
        object (obj): Object to select.

    Returns:
        None
    """
    object.select = True


def select_objects(objects):
    """ Select specific objects.

    Parameters:
        objects (list): Objects to select.

    Returns:
        None
    """
    for object in objects:
        object.select = True


def select_all_objects():
    """ Select all objects.

    Parameters:
        None

    Returns:
        None
    """
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = True


def deselect_object(object):
    """ De-select a specific object.

    Parameters:
        object (obj): Object to de-select.

    Returns:
        None
    """
    object.select = False


def deselect_objects(objects):
    """ De-select specific objects.

    Parameters:
        objects (list): Objects to de-select.

    Returns:
        None
    """
    if not isinstance(objects, list):
        objects = [objects]
    for object in objects:
        object.select = False


def deselect_all_objects():
    """ De-select all objects.

    Parameters:
        None

    Returns:
        None
    """
    deselect_objects(list(bpy.data.objects))


# ==============================================================================
# Visibility
# ==============================================================================

def hide_object(object):
    """ Hide specific object.

    Parameters:
        object (obj): Object to hide.

    Returns:
        None
    """
    object.hide = True


def hide_objects(objects):
    """ Hide specific objects.

    Parameters:
        objects (list): Objects to hide.

    Returns:
        None
    """
    for object in objects:
        object.hide = True


def show_object(object):
    """ Show specific object.

    Parameters:
        object (obj): Object to show.

    Returns:
        None
    """
    object.hide = False


def show_objects(objects):
    """ Show specific objects.

    Parameters:
        objects (list): Objects to show.

    Returns:
        None
    """
    for object in objects:
        object.hide = False


# ==============================================================================
# Set attributes
# ==============================================================================

def set_object_layer(object, layer):
    """ Changes the layer of the object.

    Parameters:
        object (obj): Object for layer change.
        layer (int): Layer number.

    Returns:
        None
    """
    mask = tuple(i == layer for i in range(20))
    object.layers = mask


def set_objects_layer(objects, layer):
    """ Changes the layer of the objects.

    Parameters:
        objects (list): Objects for layer change.
        layer (int): Layer number.

    Returns:
        None
    """
    mask = tuple(i == layer for i in range(20))
    for object in objects:
        object.layers = mask


def set_object_show_name(object, show=True):
    """ Display the name of an object.

    Parameters:
        object (obj): Object to display name.
        show (bool): True or False.

    Returns:
        None
    """
    object.show_name = show


def set_objects_show_name(objects, show=True):
    """ Display the name of objects.

    Parameters:
        objects (list): Objects to display name.
        show (bool): True or False.

    Returns:
        None
    """
    for object in objects:
        object.show_name = show


def set_object_location(object, location):
    """ Set the location of an object.

    Parameters:
        object (obj): Object to set location.
        location (list): Location.

    Returns:
        None
    """
    object.location = location


def set_objects_location(objects, locations):
    """ Set the location of objects.

    Parameters:
        objects (list): Objects to set location.
        locations (list): List of locations.

    Returns:
        None
    """
    for i, location in enumerate(locations):
        objects[i].location = location


def set_object_rotation(object, rotation):
    """ Set the rotation of an object.

    Parameters:
        object (obj): Object to set rotation.
        rotation (list): Rotation.

    Returns:
        None
    """
    object.rotation_euler = rotation


def set_objects_rotation(objects, rotations):
    """ Set the rotation of objects.

    Parameters:
        objects (list): Objects to set rotation.
        rotations (list): List of rotations.

    Returns:
        None
    """
    for i, rotation in enumerate(rotations):
        objects[i].rotation_euler = rotation


def set_object_scale(object, scale):
    """ Set the scale of an object.

    Parameters:
        object (obj): Object to set scale.
        scale (list): Scale.

    Returns:
        None
    """
    object.scale = scale


def set_objects_scale(objects, scales):
    """ Set the scale of objects.

    Parameters:
        objects (list): Objects to set scale.
        scales (list): List of scales.

    Returns:
        None
    """
    for i, scale in enumerate(scales):
        objects[i].scale = scale


# ==============================================================================
# Misc
# ==============================================================================

def join_objects(objects):
    """ Join a list of objects.

    Notes:
        - The first object in the list becomes the master object.

    Parameters:
        objects (list): Objects to join.

    Returns:
        obj: Joined object.
    """
    select_objects(objects=objects)
    bpy.context.scene.objects.active = objects[0]
    bpy.ops.object.join()
    return objects[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    objects = get_objects(layer=0)
    object = objects[0]
