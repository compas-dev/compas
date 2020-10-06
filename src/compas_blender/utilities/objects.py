import bpy
from typing import List, Iterable, Text

from .data import delete_unused_data


__all__ = [
    "delete_object",
    "delete_objects",
    "delete_all_objects",
    "delete_object_by_name",
    "delete_objects_by_names",
    "get_object_by_name",
    "get_objects_by_names",
]


# ==============================================================================
# Delete
# ==============================================================================


def delete_all_objects(purge_data: bool = True):
    """Delete all mesh and curve scene objects, and the attached mesh and curve data blocks."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True, confirm=False)
    if purge_data:
        delete_unused_data()


def delete_object(obj: bpy.types.Object, purge_data: bool = True):
    """Delete a scene object.
    """
    bpy.data.objects.remove(obj)
    if purge_data:
        delete_unused_data()


def delete_objects(objects: Iterable[bpy.types.Object], purge_data: bool = True):
    """Delete multiple scene objects."""
    for obj in objects:
        delete_object(obj, purge_data=False)
    if purge_data:
        delete_unused_data()


def delete_object_by_name(name: str):
    """Delete the scene object corresponding to the given name."""
    obj = get_object_by_name(name)
    delete_object(obj)


def delete_objects_by_names(names: Iterable[Text]):
    """Delete the scene objects corresponding to the list of names."""
    objects = get_objects_by_names(names)
    delete_objects(objects)


# ==============================================================================
# Get
# ==============================================================================


def get_object_by_name(name: str) -> bpy.types.Object:
    """Get the object with the given name."""
    return bpy.data.objects[name]


def get_objects_by_names(names: Iterable[str]) -> List[bpy.types.Object]:
    """Get the objects corresponding to the given names."""
    return [bpy.data.objects[name] for name in names]


# def get_objects(names=None, color=None, layer=None, type=None):
#     if names:
#         objects = get_objects_by_names(names)
#     elif color:
#         raise NotImplementedError
#     elif layer:
#         objects = list(bpy.data.collections[layer].objects)
#     elif type:
#         objects = [obj for obj in bpy.data.objects if obj.type == type.upper()]
#     else:
#         objects = list(bpy.data.objects)
#     return objects


# def get_object_name(obj):
#     return obj.name


# def get_objects_names(objects):
#     return [get_object_name(obj) for obj in objects]


# def get_objects_layers(objects):
#     return [obj.users_collection for obj in objects]


# def get_objects_types(objects):
#     return [obj.type for obj in objects]


# def get_objects_coordinates(objects):
#     return [list(obj.location) for obj in objects]


# def get_object_property(obj, property_name):
#     return obj.get(property_name)


# def get_objects_property(objects, property_name):
#     return [get_object_property(obj, property_name) for obj in objects]


# def select_object(message="Select an object."):
#     raise NotImplementedError


# def select_objects(message="Select objects."):
#     raise NotImplementedError


# ==============================================================================
# Points
# ==============================================================================


# def get_points(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "EMPTY"]


# def get_points_coordinates(objects=None):
#     if objects is None:
#         objects = get_points()
#     return [list(obj.location) for obj in objects if obj.type == "EMPTY"]


# def select_point(message="Select a point."):
#     raise NotImplementedError


# def select_points(message="Select points."):
#     raise NotImplementedError


# ==============================================================================
# Curves
# ==============================================================================


# def select_curve(message="Select curve."):
#     raise NotImplementedError


# def select_curves(message="Select curves."):
#     raise NotImplementedError


# def get_curves(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "CURVE"]


# def get_curves_coordinates(objects):
#     raise NotImplementedError


# ==============================================================================
# Meshes
# ==============================================================================


# def select_mesh(message="Select a mesh."):
#     raise NotImplementedError


# def select_meshes(message="Select meshes."):
#     raise NotImplementedError


# def get_meshes(layer=None):
#     return [obj for obj in get_objects(layer=layer) if obj.type == "MESH"]


# def mesh_from_bmesh(bmesh):
#     vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
#     faces = [list(face.vertices) for face in bmesh.data.polygons]
#     return Mesh.from_vertices_and_faces(vertices=vertices, faces=faces)


# ==============================================================================
# Surfaces
# ==============================================================================


# ==============================================================================
# Set
# ==============================================================================

# def set_select(objects=None):
#     if objects:
#         for obj in objects:
#             obj.select_set(state=True)
#     else:
#         bpy.ops.object.select_all(action="SELECT")


# def set_deselect(objects=None):
#     if objects:
#         for obj in objects:
#             obj.select_set(state=False)
#     else:
#         bpy.ops.object.select_all(action="DESELECT")


# def set_objects_layer(objects, layer):
#     collection_new = bpy.data.collections.get(layer) or bpy.data.collections.new(layer)
#     for obj in objects:
#         for collection_old in obj.users_collection:
#             collection_old.objects.unlink(obj)
#         collection_new.objects.link(obj)


# def set_objects_coordinates(objects, coords):
#     for obj, xyz in zip(objects, coords):
#         obj.location = xyz


# def set_objects_rotations(objects, rotations):
#     for obj, r in zip(objects, rotations):
#         obj.rotation_euler = r


# def set_objects_scales(objects, scales):
#     for obj, s in zip(objects, scales):
#         obj.scale = s


# def set_objects_show_names(objects, show=True):
#     for obj in objects:
#         obj.show_name = show


# def set_objects_visible(objects, visible=True):
#     for obj in objects:
#         obj.hide_viewport = not visible


# def set_object_property(obj, property_name, property_value):
#     obj[property_name] = property_value


# def set_objects_property(objects, property_name, property_value):
#     for obj in objects:
#         obj[property_name] = property_value


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
