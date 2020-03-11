from compas_blender.utilities import delete_object
from compas_blender.utilities import set_objects_layer

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors

try:
    import bpy
except ImportError:
    pass

from math import acos
from math import atan2


__all__ = [
    'create_material',

    'draw_points',
    'draw_lines',
    'draw_geodesics',
    'draw_breps',
    'draw_cylinders',
    'draw_pipes',
    'draw_forces',
    'draw_spheres',
    'draw_cubes',
    'draw_faces',
    'draw_texts',

    'draw_pointcloud',
    'draw_mesh',
    'draw_plane',
]


# ==============================================================================
# Helpers
# ==============================================================================

def link_objects(objects, layer=None):
    for obj in objects:
        bpy.context.collection.objects.link(obj)
    if layer:
        set_objects_layer(objects, layer)


def create_material(rgb, alpha=1):
    rgba = rgb + [alpha]
    name = '-'.join(['{0:.2f}'.format(i) for i in rgba])
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.diffuse_color = rgba
    return material


def set_object_color(obj, rgb, alpha=1.0):
    rgba = rgb + [alpha]
    material = create_material(rgb, alpha)
    obj.color = rgba
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
    obj.active_material = material


# ==============================================================================
# Annotations
# ==============================================================================

def draw_texts(texts, layer=None):
    bpy.ops.obj.text_add()
    empty = bpy.context.active_object
    objects = [0] * len(texts)
    for index, data in enumerate(texts):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('radius', 1)
        obj.name = data.get('name', 'text')
        obj.data.body = data.get('text', 'text')
        rgb = data.get('color') or [1, 1, 1]
        obj.color = rgb + [1]
        objects[index] = obj
    delete_object(empty)
    link_objects(objects, layer=layer)
    return objects


# ==============================================================================
# Primitives
# ==============================================================================

def draw_points(points, layer=None):
    bpy.ops.object.empty_add(type='SPHERE')
    empty = bpy.context.active_object
    objects = [0] * len(points)
    for index, data in enumerate(points):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('radius', 1)
        obj.name = data.get('name', 'point')
        rgb = data.get('color') or [1.0, 1.0, 1.0]
        obj.color = rgb + [1.0]
        set_object_color(obj, rgb)
        objects[index] = obj
    link_objects(objects, layer=layer)
    delete_object(empty)
    return objects


def draw_lines(lines, layer=None, centroid=True):
    objects = [0] * len(lines)
    for index, data in enumerate(lines):
        sp = data['start']
        ep = data['end']
        mp = centroid_points([sp, ep]) if centroid else [0, 0, 0]
        name = data.get('name', 'line')
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('NURBS')
        spline.points.add(2)
        spline.points[0].co = list(subtract_vectors(sp, mp)) + [1]
        spline.points[1].co = list(subtract_vectors(ep, mp)) + [1]
        spline.order_u = 1
        obj = bpy.data.objects.new(name, curve)
        obj.location = mp
        obj.data.fill_mode = 'FULL'
        obj.data.bevel_depth = data.get('width', 0.05)
        obj.data.bevel_resolution = 0
        obj.data.resolution_u = 20
        rgb = data.get('color') or [1.0, 1.0, 1.0]
        set_object_color(obj, rgb)
        objects[index] = obj
    link_objects(objects, layer=layer)
    return objects


def draw_faces(faces, **kwargs):
    objects = []
    for face in faces:
        points = face['points']
        indices = [list(range(len(points)))]
        name = face.get('name', 'face')
        layer = face.get('layer', None)
        color = face.get('color') or [1, 1, 1]
        obj = draw_mesh(name=name, vertices=points, faces=indices, color=color, layer=layer)
        # a lot of basic stuff is done by draw_mesh
        objects.append(obj)
    return objects


# make collection
# name after pointcloud
# draw point objects
# add points to collection
# assign collection to layer
def draw_pointcloud(points, layer=None):
    objects = [0] * len(points)
    for index, data in enumerate(points):
        obj = draw_mesh(name=data.get('name', 'pt'), vertices=[[0, 0, 0]])
        obj.location = data['pos']
        objects[index] = obj
    link_objects(objects, layer=layer)
    return objects


def draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, name='plane', layer=None, color=[1, 1, 1]):
    nx = int(Lx / dx)
    ny = int(Ly / dy)
    x = [i * dx for i in range(nx + 1)]
    y = [i * dy for i in range(ny + 1)]
    vertices = [[xi, yi, 0] for yi in y for xi in x]
    faces = [[(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
              (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
             for i in range(nx) for j in range(ny)]
    return draw_mesh(name=name, vertices=vertices, faces=faces, layer=layer, color=color, centroid=False)


# ==============================================================================
# Shapes
# ==============================================================================

# replace div by uv
def draw_cylinders(cylinders, div=10, layer=None):
    # don't set the obvious defaults?
    bpy.ops.mesh.primitive_cylinder_add(location=[0, 0, 0], radius=1, depth=1, vertices=div)
    empty = bpy.context.active_object
    objects = [0] * len(cylinders)
    for index, data in enumerate(cylinders):
        sp = data['start']
        ep = data['end']
        mp = centroid_points([sp, ep])
        radius = data.get('radius', 1.0)
        length = distance_point_point(sp, ep)
        obj = empty.copy()
        obj.name = data.get('name', 'cylinder')
        # get this from geometry package
        obj.rotation_euler[1] = acos((ep[2] - sp[2]) / length)
        obj.rotation_euler[2] = atan2(ep[1] - sp[1], ep[0] - sp[0])
        obj.location = mp
        obj.scale = ((radius, radius, length))
        rgb = data.get('color') or [1.0, 1.0, 1.0]
        set_object_color(obj, rgb)
        objects[index] = obj
    delete_object(empty)
    link_objects(objects, layer=layer)
    return objects


# rename div to u, v
def draw_spheres(spheres, div=10, layer=None):
    bpy.ops.mesh.primitive_uv_sphere_add(location=[0, 0, 0], radius=1.0, segments=div, ring_count=div)
    empty = bpy.context.active_object
    objects = [0] * len(spheres)
    for index, data in enumerate(spheres):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('radius', 1.0)
        obj.name = data.get('name', 'sphere')
        values = [True] * len(obj.data.polygons)
        obj.data.polygons.foreach_set("use_smooth", values)
        rgb = data.get('color') or [1.0, 1.0, 1.0]
        set_object_color(obj, rgb)
        objects[index] = obj
    delete_object(empty)
    link_objects(objects, layer=layer)
    return objects


def draw_cubes(cubes, layer):
    bpy.ops.mesh.primitive_cube_add(size=1, location=[0, 0, 0])
    empty = bpy.context.active_object
    objects = [0] * len(cubes)
    for index, data in enumerate(cubes):
        obj = empty.copy()
        obj.location = data['pos']
        obj.scale *= data.get('size', 1)
        obj.name = data.get('name', 'cube')
        rgb = data.get('color') or [1.0, 1.0, 1.0]
        set_object_color(obj, rgb)
        objects[index] = obj
    delete_object(empty)
    link_objects(objects, layer=layer)
    return objects


def draw_pipes(pipes, **kwargs):
    raise NotImplementedError


# ==============================================================================
# NURBS
# ==============================================================================

def draw_breps(faces, **kwargs):
    raise NotImplementedError


# ==============================================================================
# Other
# ==============================================================================

def draw_geodesics(geodesics, **kwargs):
    raise NotImplementedError


# ==============================================================================
# Data Structures
# ==============================================================================

def draw_mesh(vertices, edges=None, faces=None, name='mesh', color=[1, 1, 1],
              centroid=True, layer=None, **kwargs):
    edges = [] if not edges else edges
    faces = [] if not faces else faces
    mp = centroid_points(vertices) if centroid else [0, 0, 0]
    vertices = [subtract_vectors(vertex, mp) for vertex in vertices]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    obj = bpy.data.objects.new(name, mesh)
    obj.show_wire = True
    obj.location = mp
    set_object_color(obj, color)
    link_objects([obj], layer=layer)
    return obj


# ==============================================================================
# Structures
# ==============================================================================

def draw_forces(forces, **kwargs):
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
