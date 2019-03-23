
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
    'xdraw_points',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_breps',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_forces',
    'xdraw_spheres',
    'xdraw_cubes',
    'xdraw_mesh',
    'xdraw_faces',
    'xdraw_pointcloud',
    'xdraw_texts',
    'draw_cylinder',
    'draw_plane',
    'draw_text',
    'draw_line',
]


def _link_objects(objects, copy=None, layer=None):
    for object in objects:
        bpy.context.collection.objects.link(object)
    if copy:
        delete_object(object=copy)
    if layer:
        set_objects_layer(objects=objects, layer=layer)
    return objects


def create_material(color, alpha=1):
    ckey  = '-'.join(['{0:.2f}'.format(i) for i in color + [alpha]])
    names = [i.name for i in bpy.data.materials]
    if ckey not in names:
        material = bpy.data.materials.new(name=ckey)
        material.diffuse_color = color + [alpha]
        return material
    else:
        return bpy.data.materials[ckey]


def xdraw_points(points, layer=None):
    bpy.ops.object.empty_add(type='SPHERE', radius=1, location=[0, 0, 0])
    copy = bpy.context.object
    objects = [0] * len(points)
    for c, data in enumerate(points):
        object          = copy.copy()
        object.scale   *= data.get('radius', 1)
        object.location = data.get('pos', [0, 0, 0])
        object.name     = data.get('name', 'point')
        objects[c]      = object
    return _link_objects(objects, copy, layer)


def xdraw_lines(lines, centroid=True, layer=None):
    objects = [0] * len(lines)
    for c, data in enumerate(lines):
        name = data.get('name', 'line')
        sp   = data.get('start', [0, 0, 0])
        ep   = data.get('end', [1, 1, 1])
        mp   = centroid_points([sp, ep]) if centroid else [0, 0, 0]
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        object = bpy.data.objects.new(name, curve)
        object.location = mp
        spline = curve.splines.new('NURBS')
        spline.points.add(2)
        spline.points[0].co = list(subtract_vectors(sp, mp)) + [1]
        spline.points[1].co = list(subtract_vectors(ep, mp)) + [1]
        spline.order_u = 1
        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = data.get('width', 0.05)
        object.data.bevel_resolution = 0
        object.data.resolution_u = 20
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object
    return _link_objects(objects=objects, layer=layer)


def xdraw_geodesics(geodesics, **kwargs):
    raise NotImplementedError


def xdraw_breps(faces, **kwargs):
    raise NotImplementedError


def xdraw_cylinders(cylinders, div=10, layer=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=div, location=[0, 0, 0])
    copy = bpy.context.object
    objects = [0] * len(cylinders)
    for c, data in enumerate(cylinders):
        radius = data.get('radius', 1)
        start  = data.get('start', [0, 0, 0])
        end    = data.get('end', [0, 0, 1])
        L      = distance_point_point(start, end)
        pos    = centroid_points([start, end])
        object = copy.copy()
        object.name = data.get('name', 'cylinder')
        object.rotation_euler[1] = acos((end[2] - start[2]) / L)
        object.rotation_euler[2] = atan2(end[1] - start[1], end[0] - start[0])
        object.location = pos
        object.scale = ((radius, radius, L))
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object
    return _link_objects(objects=objects, copy=copy, layer=layer)


def xdraw_pipes(pipes, **kwargs):
    raise NotImplementedError


def xdraw_forces(forces, **kwargs):
    raise NotImplementedError


def xdraw_spheres(spheres, div=10, layer=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=[0, 0, 0], ring_count=div, segments=div)
    copy = bpy.context.object
    objects = [0] * len(spheres)
    for c, data in enumerate(spheres):
        object          = copy.copy()
        object.name     = data.get('name', 'sphere')
        object.scale   *= data.get('radius', 1)
        object.location = data.get('pos', [0, 0, 0])
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object
    return _link_objects(objects=objects, layer=layer, copy=copy)


def xdraw_cubes(cubes, layer):
    bpy.ops.mesh.primitive_cube_add(size=1, location=[0, 0, 0])
    copy = bpy.context.object
    objects = [0] * len(cubes)
    for c, data in enumerate(cubes):
        object          = copy.copy()
        object.name     = data.get('name', 'cube')
        object.scale   *= data.get('radius', 1)
        object.location = data.get('pos', [0, 0, 0])
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object
    return _link_objects(objects=objects, layer=layer, copy=copy)


def xdraw_mesh(vertices, edges=None, faces=None, name='mesh', color=[1, 1, 1], centroid=True, layer=None, **kwargs):
    edges = [] if not edges else edges
    faces = [] if not faces else faces
    mp       = centroid_points(vertices) if centroid else [0, 0, 0]
    vertices = [subtract_vectors(vertex, mp) for vertex in vertices]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    object = bpy.data.objects.new(name, mesh)
    object.show_wire = True
    object.data.materials.append(create_material(color=color))
    object.location = mp
    bpy.context.collection.objects.link(object)
    if layer:
        set_objects_layer(objects=[object], layer=layer)
    return object


def xdraw_faces(faces, **kwargs):
    for face in faces:
        name    = face.get('name', 'face')
        points  = face.get('points')
        layer   = face.get('layer', None)
        color   = face.get('color', [1, 1, 1])
        indices = [list(range(len(points)))]
        xdraw_mesh(name=name, vertices=points, faces=indices, color=color, layer=layer)


def xdraw_pointcloud(points, layer=None):
    objects = [0] * len(points)
    for c, data in enumerate(points):
        object = xdraw_mesh(name=data.get('name', 'pt'), vertices=[[0, 0, 0]])
        object.location = data['pos']
        objects[c] = object
    if layer:
        set_objects_layer(objects=objects, layer=layer)
    return objects


def xdraw_texts(texts, layer=None):
    bpy.ops.object.text_add(view_align=True)
    copy = bpy.context.object
    objects = [0] * len(texts)
    for c, data in enumerate(texts):
        object           = copy.copy()
        object.scale    *= data.get('radius', 1)
        object.location  = data.get('pos', [0, 0, 0])
        object.name      = data.get('name', 'text')
        object.data.body = data.get('text', 'text')
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object
    return _link_objects(objects=objects, layer=layer, copy=copy)


def draw_cylinder(start, end, radius=1, color=[1, 1, 1], layer=None, div=10, name='cylinder'):
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=div, location=[0, 0, 0])
    L   = distance_point_point(start, end)
    pos = centroid_points([start, end])
    object = bpy.context.object
    object.name = name
    object.rotation_euler[1] = acos((end[2] - start[2]) / L)
    object.rotation_euler[2] = atan2(end[1] - start[1], end[0] - start[0])
    object.location = pos
    object.scale = ((radius, radius, L))
    object.data.materials.append(create_material(color=color))
    if layer:
        set_objects_layer(objects=[object], layer=layer)
    return object


def draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, name='plane', layer=None, color=[1, 1, 1]):
    nx = int(Lx / dx)
    ny = int(Ly / dy)
    x  = [i * dx for i in range(nx + 1)]
    y  = [i * dy for i in range(ny + 1)]
    vertices = [[xi, yi, 0] for yi in y for xi in x]
    faces    = [[(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
                 (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
                for i in range(nx) for j in range(ny)]
    return xdraw_mesh(name=name, vertices=vertices, faces=faces, layer=layer, color=color, centroid=False)


def draw_text(radius=1, pos=[0, 0, 0], text='text', layer=None, color=[1, 1, 1]):
    bpy.ops.object.text_add(view_align=False)
    object           = bpy.context.object
    object.scale    *= radius
    object.location  = pos
    object.data.body = text
    object.data.materials.append(create_material(color=color))
    if layer:
        set_objects_layer(objects=[object], layer=layer)
    return object


def draw_line(start=[0, 0, 0], end=[1, 1, 1], width=0.05, centroid=True, name='line', color=[1, 1, 1], layer=None):
    mp = centroid_points([start, end]) if centroid else [0, 0, 0]
    curve = bpy.data.curves.new(name, type='CURVE')
    curve.dimensions = '3D'
    object = bpy.data.objects.new(name, curve)
    object.location = mp
    spline = curve.splines.new('NURBS')
    spline.points.add(2)
    spline.points[0].co = list(subtract_vectors(start, mp)) + [1]
    spline.points[1].co = list(subtract_vectors(end, mp)) + [1]
    spline.order_u = 1
    object.data.fill_mode = 'FULL'
    object.data.bevel_depth = width
    object.data.bevel_resolution = 0
    object.data.resolution_u = 20
    object.data.materials.append(create_material(color=color))
    bpy.context.collection.objects.link(object)
    if layer:
        set_objects_layer(objects=[object], layer=layer)
    return object


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas_blender.utilities import clear_layers
    from compas_blender.utilities import set_objects_show_names

    clear_layers(layers=['Collection 1', 'Collection 2'])

    n = 10

    points  = [{'pos': [0, 0, i], 'radius': 0.2, 'name': 'pt{0}'.format(i)} for i in range(n)]
    lines   = [{'start': [1, 1, i], 'end': [1, 0, i], 'radius': 0.1, 'color': [1, 0, 1]} for i in range(n)]
    cyls    = [{'start': [2, 1, i], 'end': [2, 0, i], 'radius': 0.1, 'color': [0, 0, 1]} for i in range(n)]
    spheres = [{'pos': [3, 0, i], 'radius': 0.5, 'color': [0, 1, 0]} for i in range(n)]
    cubes   = [{'pos': [4, 0, i], 'radius': 0.5, 'color': [0, 1, 1]} for i in range(n)]
    texts   = [{'text': 'text2', 'radius': 0.5, 'color': [1, 0, 1], 'pos': [5, 0, i]} for i in range(n)]

    draw_cylinder(start=[0, 0, 0], end=[1, 1, 1], radius=0.1, color=[1, 0, 1], layer='Collection 2')
    draw_line(start=[2, 2, 2], end=[1, 1, 1], width=0.05, name='line', color=[1, 1, 0])
    draw_text(radius=1, pos=[0, 0, 0], text='text', layer='Collection 2', color=[1, 0, 0])

    xdraw_points(points=points)
    xdraw_lines(lines=lines, layer='Collection 2')
    xdraw_cylinders(cylinders=cyls, layer='Collection 2')
    xdraw_spheres(spheres=spheres)
    xdraw_cubes(cubes=cubes, layer='Collection 2')
    xdraw_texts(texts=texts, layer='Collection 2')

    draw_plane(Lx=2, Ly=1, dx=0.5, dy=0.5, name='plane', layer=None, color=[1, 0, 1])

    vertices = [[-1, 0, 1], [-2, 0, 2], [-2, 1, 1], [-1, 1, 0]]
    faces    = [[0, 1, 2], [2, 3, 0]]
    mesh     = xdraw_mesh(name='mesh', vertices=vertices, faces=faces, layer='Collection 2', color=[1, 0, 1])

    objects = xdraw_pointcloud(points=points)
    set_objects_show_names(objects=objects, show=True)
