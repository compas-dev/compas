try:
    import bpy
except ImportError:
    pass

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'delete_objects',
    'delete_all_objects',
    'get_objects',
    'get_objects_names',
    'get_objects_attributes_from_name',
    'get_objects_locations',
    'get_points',
    'get_curves',
    'get_meshes',
    'get_mesh_vertex_coordinates',
    'get_mesh_face_vertices',
    'get_mesh_edge_vertices',
    'get_mesh_vertices_and_faces',
    'set_objects_layer',
    'set_objects_show_name',
    'set_objects_locations',
    'set_objects_rotations',
    'set_objects_scales',
    'join_objects',
    'select_objects',
    'select_objects_by_layer',
    'select_all_objects',
    'deselect_all_objects',
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
        delete_objects(get_objects(layer))


# ==============================================================================
# Get
# ==============================================================================

def get_objects(layer=0):
    """ Retrieves the objects on a given layer.

    Parameters:
        layer (int): Layer number.

    Returns:
        list: Objects in the layer.
    """
    return [object for object in bpy.context.scene.objects if object.layers[layer]]


def get_objects_names(objects):
    """ Retrieves the names of objects.

    Parameters:
        objects (list): Objects to get names of.

    Returns:
        list: Object names.
    """
    return [object.name for object in objects]


def get_objects_locations(objects):
    """ Retrieves the locations of objects.

    Parameters:
        objects (list): Objects to get locations of.

    Returns:
        list: Object locations.
    """
    return [list(object.location) for object in objects]


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
    """ Return the Blender mesh's vertices data.

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
        list: Vertex indices for faces.
    """
    return [list(face.vertices) for face in bmesh.data.polygons]


def get_mesh_edge_vertices(bmesh):
    """ Return the Blender mesh's edge vertices.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertex indices for edges.
    """
    return [list(edge.vertices) for edge in bmesh.data.edges]


def get_mesh_vertices_and_faces(bmesh):
    """ Return the Blender mesh's vertices and faces data.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertices xyz co-ordinates.
        list: Vertex indices for faces.
    """
    vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
    faces = [list(face.vertices) for face in bmesh.data.polygons]
    return vertices, faces


def get_mesh_vertex_colors(bmesh):
    raise NotImplementedError


# ==============================================================================
# Select
# ==============================================================================

def select_objects(objects):
    """ Select specific objects.

    Parameters:
        objects (obj): Objects to select.

    Returns:
        None
    """
    deselect_all_objects()
    for object in objects:
        object.select = True


def select_objects_by_layer(layer):
    """ Select all objects in a given layer.

    Parameters:
        layer (int): Layer number.

    Returns:
        None
    """
    deselect_all_objects()
    objects = get_objects(layer)
    select_objects(objects)


def select_all_objects():
    """ Select all scene objects.

    Parameters:
        None

    Returns:
        list: All scene objects.
    """
    objects = bpy.context.scene.objects
    select_objects(objects)
    return objects


def deselect_all_objects():
    """ Deselect all scene objects.

    Parameters:
        None

    Returns:
        None
    """
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = False


def select_points():
    raise NotImplementedError


def select_curves():
    raise NotImplementedError


def select_meshes():
    raise NotImplementedError


# ==============================================================================
# Set attributes
# ==============================================================================

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


def set_objects_locations(objects, locations):
    """ Set the locations of objects.

    Parameters:
        objects (list): Objects to set location.
        locations (list): List of locations.

    Returns:
        None
    """
    for i in range(len(objects)):
        objects[i].location = locations[i]


def set_objects_rotations(objects, rotations):
    """ Set the rotations of objects.

    Parameters:
        objects (list): Objects to set rotation.
        rotations (list): List of rotations.

    Returns:
        None
    """
    for i in range(len(objects)):
        objects[i].rotation_euler = rotations[i]


def set_objects_scales(objects, scales):
    """ Set the scales of objects.

    Parameters:
        objects (list): Objects to set scale.
        scales (list): List of scales.

    Returns:
        None
    """
    for i in range(len(objects)):
        objects[i].scale = scales[i]


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
    print(get_objects_names(objects))
    print(get_objects_attributes_from_name(objects))
    print(get_objects_locations(objects))
    print(get_mesh_vertices_and_faces(objects[0]))
