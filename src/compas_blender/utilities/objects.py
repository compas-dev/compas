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
    'delete_objects',
    'delete_all_objects',
    'get_objects',
    'get_objects_names',
    'get_objects_attributes_from_name',
    'get_object_location',
    'get_objects_locations',
    'get_points',
    'get_curves',
    'get_meshes',
    'get_mesh_vertex_coordinates',
    'get_mesh_face_vertices',
    'get_mesh_edge_vertices',
    'get_mesh_vertices_and_faces',
    'set_object_layer',
    'set_objects_layer',
    'set_objects_show_name',
    'set_object_location',
    'set_objects_locations',
    'set_objects_rotations',
    'set_objects_scales',
    'join_objects',
    'select_point',
    'select_curve',
    'select_mesh',
    'select_objects',
    'select_all_objects',
    'deselect_objects',
    'deselect_all_objects',
    'hide_objects',
    'show_objects'
]


# ==============================================================================
# Deleting
# ==============================================================================

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
    for layer in list(range(20)):
        delete_objects(get_objects(layer=layer))


# ==============================================================================
# Get
# ==============================================================================

def get_objects(layer=None, name=None):
    """ Retrieves the objects on a given layer.

    Parameters:
        layer (int): Layer number.
        name (str): Object name.

    Returns:
        list: Objects in the layer or of given nme.
    """
    if layer is not None:
        objects = [object for object in bpy.context.scene.objects if object.layers[layer]]
    elif name:
        try:
            objects = [bpy.context.scene.objects[name]]
        except:
            objects = [None]
    return objects


def get_object_location(object):
    """ Retrieves the location of an object.

    Parameters:
        object (obj): Object to get locations of.

    Returns:
        list: Object location.
    """
    return list(object.location)


def get_objects_locations(objects):
    """ Retrieves the locations of objects.

    Parameters:
        objects (list): Objects to get locations of.

    Returns:
        list: Object locations.
    """
    return [list(object.location) for object in objects]


def get_objects_names(objects):
    """ Retrieves the names of objects.

    Parameters:
        objects (list): Objects to get names of.

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


def get_objects_attributes(objects):
    raise NotImplementedError


def get_objects_attributes_from_name(objects):
    """ Retrieves the attributes from the names of objects.

    Parameters:
        objects (list): Objects to get attributes of.

    Returns:
        list: Object attributes.
    """
    names = []
    for name in get_objects_names(objects):
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


def get_mesh_vertex_coordinates(bmesh):
    """ Return the Blender mesh's vertex co-ordinates.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertices xyz co-ordinates.
    """
    return [list(vertex.co) for vertex in bmesh.data.vertices]


def get_mesh_face_vertices(bmesh):
    """ Return the Blender mesh's face vertices.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertex indices for each face.
    """
    return [list(face.vertices) for face in bmesh.data.polygons]


def get_mesh_edge_vertices(bmesh):
    """ Return the Blender mesh's edge vertices.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertex indices for each edge.
    """
    return [list(edge.vertices) for edge in bmesh.data.edges]


def get_mesh_vertices_and_faces(bmesh):
    """ Return the Blender mesh's vertices and faces data.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertices xyz co-ordinates.
        list: Vertex indices for each face.
    """
    vertices = get_mesh_vertex_coordinates(bmesh)
    faces = get_mesh_face_vertices(bmesh)
    return vertices, faces


def get_mesh_vertex_colors(bmesh):
    raise NotImplementedError


def get_mesh_vertex_index(bmesh):
    raise NotImplementedError


def get_mesh_face_index(bmesh):
    raise NotImplementedError


def get_mesh_edge_index(bmesh):
    raise NotImplementedError


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
        if selected[0].type == 'EMPTY':
            return selected[0]
    print('***** Point (empty) object was not selected *****')
    return None


def select_points():
    raise NotImplementedError


def select_curve():
    """ Select curve object.

    Parameters:
        None

    Returns:
        obj: Curve object or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        if selected[0].type == 'CURVE':
            return selected[0]
    print('***** Curve object was not selected *****')
    return None


def select_curves():
    raise NotImplementedError


def select_mesh():
    """ Select mesh object.

    Parameters:
        None

    Returns:
        obj: Mesh object or None.
    """
    selected = bpy.context.selected_objects
    if selected:
        if selected[0].type == 'MESH':
            return selected[0]
    print('***** Mesh object was not selected *****')
    return None


def select_meshes():
    raise NotImplementedError


def select_objects(objects):
    """ Select specific objects.

    Parameters:
        objects (obj): Objects to select.

    Returns:
        None
    """
    deselect_all_objects()
    if not isinstance(objects, list):
        objects = [objects]
    for object in objects:
        object.select = True


def select_all_objects():
    """ Select all objects.

    Parameters:
        None

    Returns:
        list: All objects.
    """
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = True


def deselect_objects(objects):
    """ De-select specific objects.

    Parameters:
        objects (obj): Objects to de-select.

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
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = False


# ==============================================================================
# Visibility
# ==============================================================================

def hide_objects(objects):
    """ Hide specific objects.

    Parameters:
        objects (obj): Objects to hide.

    Returns:
        None
    """
    if not isinstance(objects, list):
        objects = [objects]
    for object in objects:
        object.hide = True


def show_objects(objects):
    """ Show specific objects.

    Parameters:
        objects (obj): Objects to show.

    Returns:
        None
    """
    if not isinstance(objects, list):
        objects = [objects]
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
        object (obj): Object to set location of.
        location (list): Location.

    Returns:
        None
    """
    object.location = location


def set_objects_locations(objects, locations):
    """ Set the locations of objects.

    Parameters:
        objects (list): Objects to set locations.
        locations (list): List of locations.

    Returns:
        None
    """
    for i, location in enumerate(locations):
        objects[i].location = location


def set_objects_rotations(objects, rotations):
    """ Set the rotations of objects.

    Parameters:
        objects (list): Objects to set rotations.
        rotations (list): List of rotations.

    Returns:
        None
    """
    for i, rotation in enumerate(rotations):
        objects[i].rotation_euler = rotation


def set_objects_scales(objects, scales):
    """ Set the scales of objects.

    Parameters:
        objects (list): Objects to set scales.
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

    Note:
        - The first object in the list becomes the master object.

    Parameters:
        objects (list): Objects to join.

    Returns:
        obj: Joined object.
    """
    select_objects(objects)
    bpy.context.scene.objects.active = objects[0]
    bpy.ops.object.join()
    return objects[0]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    objects = get_objects(layer=0)

    print(get_objects_names(objects=objects))
    print(get_objects_attributes_from_name(objects=objects))
    print(get_objects_locations(objects=objects))
    set_objects_locations(objects=objects, locations=[[0, 0, 0], [4, 4, 4]])
