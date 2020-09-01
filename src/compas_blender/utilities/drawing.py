import bpy

from typing import Dict, List, Union, Tuple, Text

from compas_blender.utilities import create_collection

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors


__all__ = [
    'draw_points',
    'draw_pointcloud',
    'draw_lines',
    'draw_polylines',
    'draw_cylinders',
    'draw_spheres',
    'draw_cubes',
    'draw_pipes',
    'draw_faces',
    'draw_texts',
    'draw_mesh',
]


def _link_object(obj, collection=None, layer=None):
    if not collection:
        collection = bpy.context.collection
    if not isinstance(collection, bpy.types.Collection):
        collection = create_collection(collection)
    # if not layer:
    #     layer = bpy.context.view_layer
    # layer_collection = layer.active_layer_collection.collection
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    # layer_collection.objects.link(obj)


def _link_objects(objects, collection=None, layer=None):
    if not collection:
        collection = bpy.context.collection
    if not isinstance(collection, bpy.types.Collection):
        collection = create_collection(collection)
    # if not layer:
    #     layer = bpy.context.view_layer
    # layer_collection = layer.active_layer_collection.collection
    for o in objects:
        for c in o.users_collection:
            c.objects.unlink(o)
        collection.objects.link(o)
        # layer_collection.objects.link(o)


def _create_material(rgb, alpha=1.0):
    rgba = list(rgb) + [alpha]
    name = '-'.join(['{0:.2f}'.format(i) for i in rgba])
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.diffuse_color = rgba
    return material


def _set_object_color(obj, rgb, alpha=1.0):
    rgba = list(rgb) + [alpha]
    material = _create_material(rgb, alpha)
    obj.color = rgba
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    obj.active_material = material


# ==============================================================================
# Annotations
# ==============================================================================


def draw_texts(texts: List[Dict],
               collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw text objects."""
    bpy.ops.object.text_add()
    empty = bpy.context.object
    _link_object(empty, collection)
    _set_object_color(empty, [1.0, 1.0, 1.0])
    objects = [0] * len(texts)
    for index, data in enumerate(texts):
        obj = empty.copy()
        obj.location = data['pos']
        obj.data.body = data['text']
        obj.scale *= data.get('size', 1)
        obj.name = data.get('name', 'text')
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# ==============================================================================
# Primitives
# ==============================================================================


# replace this by a custom point shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_points(points: List[Dict],
                collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw point objects."""
    P = len(points)
    N = len(str(P))
    add_point = bpy.ops.mesh.primitive_uv_sphere_add
    objects = [0] * P
    for index, point in enumerate(points):
        xyz = point['pos']
        radius = point.get('radius', 1.0)
        name = point.get('name', f'P.{index:0{N}d}')
        color = list(point.get('color', [1.0, 1.0, 1.0]))
        add_point(location=xyz, radius=radius, segments=10, ring_count=10)
        obj = bpy.context.object
        obj.name = name
        # values = [True] * len(obj.data.polygons)
        # obj.data.polygons.foreach_set("use_smooth", values)
        _set_object_color(obj, color)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


# replace this by a custom pointcloud shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_pointcloud(points: List[Dict],
                    collection: Union[Text, bpy.types.Collection] = None) -> bpy.types.Object:
    """Draw point objects as a single cloud."""
    P = len(points)
    N = len(str(P))
    bpy.ops.mesh.primitive_uv_sphere_add(location=[0, 0, 0], radius=1.0, segments=10, ring_count=10)
    empty = bpy.context.object
    _link_object(empty, collection)
    _set_object_color(empty, [1.0, 1.0, 1.0])
    objects = [0] * P
    for index, data in enumerate(points):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('radius', 1.0)
        obj.name = data.get('name', f'P.{index:0{N}d}')
        # obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# replace this by a custom line shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_lines(lines: List[Dict],
               collection: Union[Text, bpy.types.Collection] = None,
               centroid: bool = True) -> List[bpy.types.Object]:
    """Draw line objects."""
    L = len(lines)
    N = len(str(L))
    objects = [0] * L
    for index, data in enumerate(lines):
        sp = data['start']
        ep = data['end']
        origin = centroid_points([sp, ep]) if centroid else [0, 0, 0]
        name = data.get('name', f'L.{index:0{N}d}')
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = subtract_vectors(sp, origin) + [1.0]
        spline.points[1].co = subtract_vectors(ep, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        obj.data.fill_mode = 'FULL'
        obj.data.bevel_depth = data.get('width', 0.05)
        obj.data.bevel_resolution = 0
        obj.data.resolution_u = 20
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


# replace this by a custom polyline shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_polylines(polylines: List[Dict],
                   collection: Union[Text, bpy.types.Collection] = None,
                   centroid: bool = True) -> List[bpy.types.Object]:
    """Draw polyline objects."""
    P = len(polylines)
    N = len(str(P))
    objects = [0] * P
    for index, data in enumerate(polylines):
        points = data['points']
        origin = centroid_points(points) if centroid else [0, 0, 0]
        name = data.get('name', f'POLY.{index:0{N}d}')
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('POLY')
        spline.points.add(len(points) - 1)
        for i, point in enumerate(points):
            spline.points[i].co = subtract_vectors(point, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        obj.data.fill_mode = 'FULL'
        obj.data.bevel_depth = data.get('width', 0.05)
        obj.data.bevel_resolution = 0
        obj.data.resolution_u = 20
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


def draw_polygons(polygons: List[Dict],
                  collection: Union[Text, bpy.types.Collection] = None,
                  centroid: bool = True) -> List[bpy.types.Object]:
    """Draw polyline objects."""
    raise NotImplementedError


def draw_curves(curves: List[Dict],
                collection: Union[Text, bpy.types.Collection] = None,
                centroid: bool = True) -> List[bpy.types.Object]:
    """Draw curve objects."""
    raise NotImplementedError


def draw_faces(faces: List[Dict],
               collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw polygonal faces."""
    F = len(faces)
    N = len(str(F))
    objects = [0] * F
    for index, face in enumerate(faces):
        points = face['points']
        indices = [list(range(len(points)))]
        name = face.get('name', f'FACE.{index:0{N}d}')
        color = face.get('color', [1.0, 1.0, 1.0])
        obj = draw_mesh(name=name, vertices=points, faces=indices, color=color, collection=collection)
        objects[index] = obj
    return objects


# ==============================================================================
# Shapes
# ==============================================================================


def draw_cylinders(cylinders: List[Dict],
                   collection: Union[Text, bpy.types.Collection] = None,
                   uv: int = 10) -> List[bpy.types.Object]:
    """Draw cylinder objects as mesh primitives."""
    from math import acos
    from math import atan2
    bpy.ops.mesh.primitive_cylinder_add(location=[0, 0, 0], radius=1, depth=1, vertices=uv)
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(cylinders)
    for index, data in enumerate(cylinders):
        sp = data['start']
        ep = data['end']
        mp = centroid_points([sp, ep])
        radius = data.get('radius', 1.0)
        length = distance_point_point(sp, ep)
        obj = empty.copy()
        obj.name = data.get('name', 'cylinder')
        obj.rotation_euler[1] = acos((ep[2] - sp[2]) / length)
        obj.rotation_euler[2] = atan2(ep[1] - sp[1], ep[0] - sp[0])
        obj.location = mp
        obj.scale = ((radius, radius, length))
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# these objects are all linked.
# therefore they cannot have different colors
# also, if the linked mesh data block is chaged, it will affect all objects
def draw_spheres(spheres: List[Dict],
                 collection: Union[Text, bpy.types.Collection] = None,
                 uv: int = 10) -> List[bpy.types.Object]:
    """Draw sphere objects as mesh primitives."""
    bpy.ops.mesh.primitive_uv_sphere_add(location=[0, 0, 0], radius=1.0, segments=uv, ring_count=uv)
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(spheres)
    for index, data in enumerate(spheres):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('radius', 1.0)
        obj.name = data.get('name', 'sphere')
        # values = [True] * len(obj.data.polygons)
        # obj.data.polygons.foreach_set("use_smooth", values)
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# def draw_spheres(spheres, collection):
#     add_sphere = compas_blender.bpy.ops.mesh.primitive_uv_sphere_add
#     objects = []
#     for sphere in spheres:
#         add_sphere(location=[0, 0, 0], radius=1.0, segments=10, ring_count=10)
#         pos = sphere['pos']
#         radius = sphere['radius']
#         name = sphere['name']
#         color = sphere['color']
#         obj = compas_blender.bpy.context.active_object
#         obj.location = pos
#         obj.scale = radius
#         obj.name = name
#         compas_blender.drawing.set_object_color(obj, color)
#         objects.apend(obj)
#     for o in objects_vertices:
#         for c in o.user_collection:
#             c.objects.unlink(o)
#         collection.objects.link(o)


def draw_cubes(cubes: List[Dict],
               collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw cube objects as mesh primitives."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=[0, 0, 0])
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(cubes)
    for index, data in enumerate(cubes):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('size', 1)
        obj.name = data.get('name', 'cube')
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# replace this by a custom polyline shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_pipes(pipes: List[Dict],
               collection: Union[Text, bpy.types.Collection] = None,
               centroid: bool = True,
               smooth: bool = True) -> List[bpy.types.Object]:
    """Draw polyline objects."""
    P = len(pipes)
    N = len(str(P))
    objects = [0] * P
    for index, data in enumerate(pipes):
        points = data['points']
        origin = centroid_points(points) if centroid else [0, 0, 0]
        name = data.get('name', f'POLY.{index:0{N}d}')
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        curve.fill_mode = 'FULL'
        curve.bevel_depth = data.get('width', 0.05)
        curve.bevel_resolution = 0
        curve.resolution_u = 20
        curve.use_fill_caps = True
        if smooth:
            spline = curve.splines.new('NURBS')
        else:
            spline = curve.splines.new('POLY')
        spline.points.add(len(points) - 1)
        for i, point in enumerate(points):
            spline.points[i].co = subtract_vectors(point, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        rgb = data.get('color', [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


# ==============================================================================
# Data Structures
# ==============================================================================


def draw_mesh(vertices: List[List[float]],
              faces: List[List[int]],
              name: str = 'mesh',
              color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
              centroid: bool = True,
              collection: Union[Text, bpy.types.Collection] = None, **kwargs) -> bpy.types.Object:
    """Draw a mesh object."""
    mp = centroid_points(vertices) if centroid else [0, 0, 0]
    vertices = [subtract_vectors(vertex, mp) for vertex in vertices]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name, mesh)
    obj.show_wire = True
    obj.location = mp
    _set_object_color(obj, color)
    _link_objects([obj], collection=collection)
    return obj


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
