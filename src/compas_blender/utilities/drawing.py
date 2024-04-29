from typing import Dict
from typing import List
from typing import Text
from typing import Tuple
from typing import Union

import bpy  # type: ignore

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors
from compas_blender.collections import create_collection

RGBColor = Union[Tuple[int, int, int], Tuple[float, float, float]]


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
    name = "-".join(["{0:.2f}".format(i) for i in rgba])
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


def draw_texts(
    texts: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> List[bpy.types.Object]:
    """Draw text objects.

    Parameters
    ----------
    texts : list[dict]
        A list of dicts describing the text objects.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.
    color : tuple[int, int, int] or tuple[float, float, float], optional
        The text color.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    bpy.ops.object.text_add()
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(texts)
    for index, data in enumerate(texts):
        obj = empty.copy()
        obj.data = empty.data.copy()
        _set_object_color(obj, data.get("color", color))
        obj.location = data["pos"]
        obj.data.body = data["text"]
        obj.scale *= data.get("size", 1)
        obj.name = data.get("name", "text")
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
def draw_points(points: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw point objects.

    Parameters
    ----------
    points : list[dict]
        A list of dicts describing the points.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(points)
    N = len(str(P))
    add_point = bpy.ops.mesh.primitive_uv_sphere_add
    objects = [0] * P
    for index, point in enumerate(points):
        xyz = point["pos"]
        radius = point.get("radius", 1.0)
        name = point.get("name", f"P.{index:0{N}d}")
        color = list(point.get("color", [1.0, 1.0, 1.0]))
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
def draw_pointcloud(points: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> bpy.types.Object:
    """Draw point objects as a single cloud.

    Parameters
    ----------
    points : list[dict]
        A list of dicts describing the points of the pointcloud.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(points)
    N = len(str(P))
    bpy.ops.mesh.primitive_uv_sphere_add(location=[0, 0, 0], radius=1.0, segments=10, ring_count=10)
    empty = bpy.context.object
    _link_object(empty, collection)
    _set_object_color(empty, [1.0, 1.0, 1.0])
    objects = [0] * P
    for index, data in enumerate(points):
        obj = empty.copy()
        obj.location = data["pos"]
        obj.scale *= data.get("radius", 1.0)
        obj.name = data.get("name", f"P.{index:0{N}d}")
        # obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# replace this by a custom line shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_lines(
    lines: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    centroid: bool = True,
) -> List[bpy.types.Object]:
    """Draw line objects.

    Parameters
    ----------
    lines : list[dict]
        A list of dicts describing the lines.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.
    centroid : bool, optional
        If True, use the centroids of the lines as the relative base for their coordinates,
        instead of the origin of the world coordinates system.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    L = len(lines)
    N = len(str(L))
    objects = [0] * L
    for index, data in enumerate(lines):
        sp = data["start"]
        ep = data["end"]
        origin = centroid_points([sp, ep]) if centroid else [0, 0, 0]
        name = data.get("name", f"L.{index:0{N}d}")
        curve = bpy.data.curves.new(name, type="CURVE")
        curve.dimensions = "3D"
        spline = curve.splines.new("POLY")
        spline.points.add(1)
        spline.points[0].co = subtract_vectors(sp, origin) + [1.0]
        spline.points[1].co = subtract_vectors(ep, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        # obj.data.fill_mode = 'FULL'
        # obj.data.bevel_depth = data.get('width', 0.05)
        # obj.data.bevel_resolution = 0
        # obj.data.resolution_u = 20
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


# replace this by a custom polyline shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_polylines(
    polylines: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    centroid: bool = True,
) -> List[bpy.types.Object]:
    """Draw polyline objects.

    Parameters
    ----------
    polylines : list[dict]
        A list of dicts describing the polylines.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.
    centroid : bool, optional
        If True, use the centroids of the polylines as the relative base for their coordinates,
        instead of the origin of the world coordinates system.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(polylines)
    N = len(str(P))
    objects = [0] * P
    for index, data in enumerate(polylines):
        points = data["points"]
        origin = centroid_points(points) if centroid else [0, 0, 0]
        name = data.get("name", f"POLY.{index:0{N}d}")
        curve = bpy.data.curves.new(name, type="CURVE")
        curve.dimensions = "3D"
        spline = curve.splines.new("POLY")
        spline.points.add(len(points) - 1)
        for i, point in enumerate(points):
            spline.points[i].co = subtract_vectors(point, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        # obj.data.fill_mode = 'FULL'
        # obj.data.bevel_depth = data.get('width', 0.05)
        # obj.data.bevel_resolution = 0
        # obj.data.resolution_u = 20
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


def draw_polygons(
    polygons: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    centroid: bool = True,
) -> List[bpy.types.Object]:
    """Draw polyline objects.

    Parameters
    ----------
    polygons : list[dict]
        A list of dicts describing the polygons.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.
    centroid : bool, optional
        If True, use the centroids of the polygons as the relative base for their coordinates,
        instead of the origin of the world coordinates system.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    raise NotImplementedError


def draw_faces(faces: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw polygonal faces.

    Parameters
    ----------
    faces : list[dict]
        A list of dicts describing the faces.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    F = len(faces)
    N = len(str(F))
    objects = [0] * F
    for index, face in enumerate(faces):
        points = face["points"]
        indices = [list(range(len(points)))]
        name = face.get("name", f"FACE.{index:0{N}d}")
        color = face.get("color", [1.0, 1.0, 1.0])
        obj = draw_mesh(
            name=name,
            vertices=points,
            faces=indices,
            color=color,
            collection=collection,
        )
        objects[index] = obj
    return objects


def draw_circles(circles: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw circle objects as mesh primitives.

    Parameters
    ----------
    circles : list[dict]
        A list of dicts describing the circles.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    from math import acos
    from math import atan2

    bpy.ops.mesh.primitive_circle_add()
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(circles)
    for index, data in enumerate(circles):
        obj = empty.copy()
        obj.name = data.get("name", "circle")
        radius = data.get("radius", 1.0)
        point, normal = data.get("plane", ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)))
        obj.rotation_euler[1] = acos(normal[2])
        obj.rotation_euler[2] = atan2(normal[1], normal[0])
        obj.location = point
        obj.scale = (radius, radius, 1.0)
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


def draw_planes(planes: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw plane objects as mesh primitives.

    Parameters
    ----------
    planes : list[dict]
        A list of dicts describing the planes.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    from math import acos
    from math import atan2

    bpy.ops.mesh.primitive_plane_add()
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(planes)
    for index, data in enumerate(planes):
        obj = empty.copy()
        obj.name = data.get("name", "plane")
        point, normal = data.get("plane", ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)))
        obj.rotation_euler[1] = acos(normal[2])
        obj.rotation_euler[2] = atan2(normal[1], normal[0])
        obj.location = point
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# ==============================================================================
# Shapes
# ==============================================================================


def draw_cylinders(
    cylinders: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    uv: int = 10,
) -> List[bpy.types.Object]:
    """Draw cylinder objects as mesh primitives.

    Parameters
    ----------
    cylinders : list[dict]
        A list of dicts describing the cylinders.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    from math import acos
    from math import atan2

    bpy.ops.mesh.primitive_cylinder_add(location=[0, 0, 0], radius=1, depth=1, vertices=uv)
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(cylinders)
    for index, data in enumerate(cylinders):
        sp = data["start"]
        ep = data["end"]
        mp = centroid_points([sp, ep])
        radius = data.get("radius", 1.0)
        length = distance_point_point(sp, ep)
        obj = empty.copy()
        obj.name = data.get("name", "cylinder")
        obj.rotation_euler[1] = acos((ep[2] - sp[2]) / length)
        obj.rotation_euler[2] = atan2(ep[1] - sp[1], ep[0] - sp[0])
        obj.location = mp
        obj.scale = (radius, radius, length)
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# these objects are all linked.
# therefore they cannot have different colors
# also, if the linked mesh data block is changed, it will affect all objects
def draw_spheres(
    spheres: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    uv: int = 10,
) -> List[bpy.types.Object]:
    """Draw sphere objects as mesh primitives.

    Parameters
    ----------
    spheres : list[dict]
        A list of dicts describing the spheres.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    bpy.ops.mesh.primitive_uv_sphere_add(location=[0, 0, 0], radius=1.0, segments=uv, ring_count=uv)
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(spheres)
    for index, data in enumerate(spheres):
        obj = empty.copy()
        obj.location = data["pos"]
        obj.scale *= data.get("radius", 1.0)
        obj.name = data.get("name", "sphere")
        # values = [True] * len(obj.data.polygons)
        # obj.data.polygons.foreach_set("use_smooth", values)
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


def draw_cubes(cubes: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw cube objects as mesh primitives.

    Parameters
    ----------
    cubes : list[dict]
        A list of dicts describing the cubes.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    bpy.ops.mesh.primitive_cube_add(size=1, location=[0, 0, 0])
    empty = bpy.context.object
    _link_object(empty, collection)
    objects = [0] * len(cubes)
    for index, data in enumerate(cubes):
        obj = empty.copy()
        obj.location = data["pos"]
        obj.scale *= data.get("size", 1)
        obj.name = data.get("name", "cube")
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    empty.hide_set(True)
    return objects


# replace this by a custom polyline shader
# https://docs.blender.org/api/current/gpu.html#custom-shader-for-dotted-3d-line
# https://docs.blender.org/api/current/gpu.html#triangle-with-custom-shader
def draw_pipes(
    pipes: List[Dict],
    collection: Union[Text, bpy.types.Collection] = None,
    centroid: bool = True,
    smooth: bool = True,
) -> List[bpy.types.Object]:
    """Draw polyline objects.

    Parameters
    ----------
    pipes : list[dict]
        A list of dicts describing the pipes.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.
    centroid : bool, optional
        If True, use the centroids of the pipes as the relative base for their coordinates,
        instead of the origin of the world coordinates system.
    smooth : bool, optional
        If True, use a NURBS curve instead of a polyline.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(pipes)
    N = len(str(P))
    objects = [0] * P
    for index, data in enumerate(pipes):
        points = data["points"]
        origin = centroid_points(points) if centroid else [0, 0, 0]
        name = data.get("name", f"POLY.{index:0{N}d}")
        curve = bpy.data.curves.new(name, type="CURVE")
        curve.dimensions = "3D"
        curve.fill_mode = "FULL"
        curve.bevel_depth = data.get("width", 0.05)
        curve.bevel_resolution = 0
        curve.resolution_u = 20
        curve.use_fill_caps = True
        if smooth:
            spline = curve.splines.new("NURBS")
        else:
            spline = curve.splines.new("POLY")
        spline.points.add(len(points) - 1)
        for i, point in enumerate(points):
            spline.points[i].co = subtract_vectors(point, origin) + [1.0]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = origin
        rgb = data.get("color", [1.0, 1.0, 1.0])
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


# ==============================================================================
# Data Structures
# ==============================================================================


def draw_mesh(
    vertices: List[List[float]],
    faces: List[List[int]],
    name: str = "mesh",
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    centroid: bool = True,
    collection: Union[Text, bpy.types.Collection] = None,
    **kwargs,
) -> bpy.types.Object:
    """Draw a mesh object.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`compas.geometry.Point`]
        The vertices of the mesh.
    faces : list[list[int]]
        The faces of the mesh.
    color : tuple[float, float, float], optional
        The color of the mesh.
    centroid : bool, optional
        If True, use the centroid of the mesh as the relative base for the vertex coordinates,
        instead of the origin of the world coordinates system.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
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
# Curves and Surfaces
# ==============================================================================


def draw_curves(curves: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw curve objects.

    Parameters
    ----------
    curves : list[dict]
        A list of dicts describing the curves.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(curves)
    N = len(str(P))
    objects = [None] * P
    for index, props in enumerate(curves):
        origin = [0, 0, 0]
        curve = props["curve"]
        name = props.get("name", f"CURVE.{index:0{N}d}")
        rgb = props.get("color", [1.0, 1.0, 1.0])
        # create a curve data block
        bcurve = bpy.data.curves.new(name, type="CURVE")
        bcurve.dimensions = "3D"
        # add a spline segment to the data block
        spline = bcurve.splines.new("NURBS")
        spline.points.add(len(curve.points) - 1)
        for i, (point, weight) in enumerate(zip(curve.points, curve.weights)):
            spline.points[i].co = [point[0], point[1], point[2], weight]
            spline.points[i].weight = weight
        spline.order_u = curve.order
        spline.use_cyclic_u = curve.is_periodic
        spline.use_endpoint_u = True
        # create a scene object from the data block
        obj = bpy.data.objects.new(name, bcurve)
        obj.location = origin
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    return objects


def draw_surfaces(surfaces: List[Dict], collection: Union[Text, bpy.types.Collection] = None) -> List[bpy.types.Object]:
    """Draw surface objects.

    Parameters
    ----------
    surfaces : list[dict]
        A list of dicts describing the surfaces.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection that should contain the objects created by this function.

    Returns
    -------
    list[:blender:`bpy.types.Object`]

    """
    P = len(surfaces)
    N = len(str(P))
    objects = [None] * P
    for index, props in enumerate(surfaces):
        origin = [0, 0, 0]
        surface = props["surface"]
        name = props.get("name", f"SURFACE.{index:0{N}d}")
        rgb = props.get("color", [1.0, 1.0, 1.0])
        # create a surface data block
        surfdata = bpy.data.curves.new(name, type="SURFACE")
        surfdata.dimensions = "3D"
        surfdata.resolution_u = 32
        surfdata.resolution_v = 32
        # add the U(V) splines
        for points, weights in zip(surface.points, surface.weights):
            spline = surfdata.splines.new("NURBS")
            spline.points.add(len(points) - 1)
            for i, (point, weight) in enumerate(zip(points, weights)):
                spline.points[i].co = [point[0], point[1], point[2], 1.0]
                spline.points[i].weight = weight
            spline.use_endpoint_u = True
            spline.use_endpoint_v = True
            spline.order_u = surface.u_degree + 1
            spline.order_v = surface.v_degree + 1
        # create a scene object from the data block
        obj = bpy.data.objects.new(name, surfdata)
        obj.location = origin
        # colors and stuff
        _set_object_color(obj, rgb)
        objects[index] = obj
    _link_objects(objects, collection)
    for obj in objects:
        # select the control points
        for s in obj.data.splines:  # type: ignore
            for p in s.points:
                p.select = True
        # switch to edit mode
        # connect the spline points with segments
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.curve.make_segment()
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    return objects
