


import json

__all__ = [
    'delete_object',
    'delete_objects',
    'delete_objects_by_name',
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
    'set_select',
    'set_deselect',

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
#    'select_mesh',
#    'select_meshes',
#    'select_all_objects',
#    'deselect_object',
#    'deselect_all_objects',
#    'hide_object',
#    'hide_objects',
#    'show_object',
#    'show_objects'
]










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





def set_select(objects=[]):

    if objects:
        if not isinstance(objects, list):
            objects = [objects]
        for object in objects:
            object.select_set(action='SELECT')

    else:
        bpy.ops.object.select_all(action='SELECT')


def set_deselect(objects=[]):

    if objects:
        if not isinstance(objects, list):
            objects = [objects]
        for object in objects:
            object.select_set(action='DESELECT')

    else:
        bpy.ops.object.select_all(action='DESELECT')


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


    set_deselect()

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
    #print(bpy.data.objects['SurfSphere'].type)

