
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh

try:
    import bpy
except ImportError:
    pass


__all__ = [
    'delete_object',
    'delete_objects',
    'delete_object_by_name',
    'delete_objects_by_names',
    'get_object_by_name',
    'get_objects_by_names',
    'get_objects',
    'get_object_name',
    'get_objects_names',
    'get_objects_layers',
    'get_objects_types',
    'get_objects_coordinates',
    'get_object_property',
    'get_objects_property',
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
    'set_object_property',
    'set_objects_property',
    'mesh_from_bmesh',
]


# ==============================================================================
# Delete
# ==============================================================================

def delete_object(object):
    bpy.data.objects.remove(object)
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def delete_objects(objects):
    for object in objects:
        bpy.data.objects.remove(object)
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


def delete_object_by_name(name):
    delete_object(object=get_object_by_name(name))


def delete_objects_by_names(names):
    delete_objects(objects=get_objects_by_names(names))


# ==============================================================================
# Get
# ==============================================================================

def get_object_by_name(name):
    return bpy.data.objects[name]


def get_objects_by_names(names):
    return [bpy.data.objects[name] for name in names]


def get_objects(names=None, color=None, layer=None, type=None):
    if names:
        objects = get_objects_by_names(names)
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
    return object.name


def get_objects_names(objects):
    return [get_object_name(object) for object in objects]


def get_objects_layers(objects):
    return [object.users_collection for object in objects]


def get_objects_types(objects):
    return [object.type for object in objects]


def get_objects_coordinates(objects):
    return [list(object.location) for object in objects]


def get_object_property(object, property):
    try:
        return object[property]
    except:
        return None


def get_objects_property(objects, property):
    return [get_object_property(object, property) for object in objects]


def select_object(message="Select an object."):
    raise NotImplementedError


def select_objects(message='Select objects.'):
    raise NotImplementedError


# ==============================================================================
# Points
# ==============================================================================

def get_points(layer=None):
    return [object for object in get_objects(layer=layer) if object.type == 'EMPTY']


def get_points_coordinates(objects=None):
    if objects is None:
        objects = get_points()
    return [list(object.location) for object in objects if object.type == 'EMPTY']


def select_point(message='Select a point.'):
    raise NotImplementedError


def select_points(message='Select points.'):
    raise NotImplementedError


# ==============================================================================
# Curves
# ==============================================================================


def select_curve(message='Select curve.'):
    raise NotImplementedError


def select_curves(message='Select curves.'):
    raise NotImplementedError


def get_curves(layer=None):
    return [object for object in get_objects(layer=layer) if object.type == 'CURVE']


def get_curves_coordinates(objects):
    raise NotImplementedError


# ==============================================================================
# Meshes
# ==============================================================================

def select_mesh(message='Select a mesh.'):
    raise NotImplementedError


def select_meshes(message='Select meshes.'):
    raise NotImplementedError


def get_meshes(layer=None):
    return [object for object in get_objects(layer=layer) if object.type == 'MESH']


def mesh_from_bmesh(bmesh):
    vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
    faces    = [list(face.vertices) for face in bmesh.data.polygons]
    return Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)


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


def set_objects_layer(objects, layer):
    for object in objects:
        for collection in object.users_collection:
            collection.objects.unlink(object)
        bpy.data.collections[layer].objects.link(object)


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


def set_object_property(object, property, value):
        object[property] = value


def set_objects_property(objects, property, value):
    for object in objects:
        object[property] = value


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    objects = get_objects(layer='Collection 1')
    delete_objects(objects=objects)
    # delete_objects(['Cube', 'Cylinder'])
    # points  = get_points()

    # print(get_objects(names=['Plane', 'Sphere']))
    # print(get_object_by_name(name='Plane'))
    # print(get_objects_by_names(names=['Plane', 'Sphere']))
    # print(get_objects(layer='Collection 1'))
    # print(get_objects(type='Mesh'))

    # print(get_object_name(object=objects[0]))
    # print(get_objects_names(objects=objects))
    # print(get_objects_layers(objects=objects))
    # print(get_objects_types(objects=objects))
    # print(get_objects_coordinates(objects=objects))
    # print(get_object_property(object=objects[0], property='ex'))
    # print(get_objects_property(objects=objects, property='ex'))

    # print(get_points_coordinates())
    # print(get_curves())
    # print(get_meshes())

    # set_select(points)
    # set_deselect(points)

    # set_objects_coordinates(objects=objects[:2], coords=[[0, 0, 3], [0, 0, 4]])
    # set_objects_rotations(objects=objects[:2], rotations=[[2, 0, 0], [0, 2, 2]])
    # set_objects_scales(objects=objects[:2], scales=[[2, 2, 2], [3, 3, 3]])

    # set_objects_show_names(objects=objects, show=0)
    # set_objects_visible(objects=objects, visible=1)

    # set_object_property(object=objects[1], property='ex', value=[1, 2, 3])
    # set_objects_property(objects=objects, property='ex', value=[1, 2, 3])
