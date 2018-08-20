from math import acos
from math import atan2

from compas_blender.utilities import delete_object
from compas_blender.utilities import deselect_all_objects
from compas_blender.utilities import set_object_layer
from compas_blender.utilities import set_objects_show_name

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.utilities import random_name

try:
    import bpy
    from mathutils import Vector
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'delete_all_materials',
    'create_material',
    'draw_cuboid',
    'draw_cubes',
    'draw_pipes',
    'draw_plane',
    'draw_spheres',
    'draw_lines',
    'draw_points',
    'xdraw_cubes',
    'xdraw_faces',
    'xdraw_labels',
    'xdraw_lines',
    'xdraw_mesh',
    'xdraw_pipes',
    'xdraw_pointcloud',
    'xdraw_points',
    'xdraw_spheres',
    'xdraw_texts',
]


# ==============================================================================
# materials
# ==============================================================================

def delete_all_materials():
    """ Delete all scene materials.

    Parameters:
        None

    Returns:
        None
    """
    materials = bpy.data.materials
    for material in materials:
        material.user_clear()
        materials.remove(material)


def create_material(color, alpha=1):
    """ Create a material of given RGB color and alpha.

    Notes:
        - If the material already exists, the existing object is returned.

    Parameters:
        color (list): [R, G, B] with values in range [0, 1].
        alpha (float): Alpha value in range [0, 1].

    Returns:
        obj: Created/existing material object.
    """
    ckey = '-'.join(['{0:.2f}'.format(i) for i in color + [alpha]])
    names = [i.name for i in list(bpy.data.materials)]
    if ckey not in names:
        material = bpy.data.materials.new(name=ckey)
        material.diffuse_color = color
        material.use_transparency = True
        material.alpha = alpha
        material.emit = 2
        return material
    else:
        return bpy.data.materials[ckey]


# ==============================================================================
# draw functions
# ==============================================================================

def draw_cubes(pos=[[0, 0, 0]], radius=1, layer=0, color=[1, 1, 1]):
    """ Draw multiple cubes.

    Parameters:
        pos (list): Centroid locations [[x, y, z], ..].
        radius (float): Radius of cubes.
        layer (int): Layer number.
        color (list): Material color.

    Returns:
        list: Created cube objects.
    """
    return xdraw_cubes([{'pos': i, 'radius': radius, 'layer': layer, 'color': color} for i in pos])


def draw_cuboid(Lx=1, Ly=1, Lz=1, pos=[0, 0, 0], layer=0, color=[1, 1, 1], wire=True):
    """ Draw a cuboid.

    Parameters:
        Lx (float): Length in x.
        Ly (float): Length in y.
        Lz (float): Length in z.
        pos (list): Centroid position [x, y, z].
        layer (int): Layer number.
        color (list): Material color.
        wire (bool): Show wires for faces.

    Returns:
        obj: Created cube object.
    """
    bpy.ops.mesh.primitive_cube_add(radius=1, location=pos)
    cube = bpy.context.object
    cube.dimensions = [Lx, Ly, Lz]
    cube.show_wire = wire
    material = create_material(color=color)
    cube.data.materials.append(material)
    set_object_layer(object=cube, layer=layer)
    cube.select = False
    return cube


def draw_lines(start=[[0, 0, 0]], end=[[1, 1, 1]], width=1, layer=0, color=[1, 1, 1]):
    """ Draw multiple lines.

    Parameters:
        start (list): Line start points.
        end (list): Line end points.
        width (float): Width of lines.
        layer (int): Layer number.
        color (list): Material color.

    Returns:
        list: Created line objects.
    """
    return xdraw_lines([{'start': u, 'end': v, 'width': width, 'layer': layer, 'color': color}
                        for u, v in zip(start, end)])


def draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, name='plane', layer=0, color=[1, 1, 1], wire=True, bracing=None):
    """ Create a plane mesh in x-y.

    Parameters:
        Lx (float): Length of the plane in x.
        Ly (float): Length of the plane in y.
        dx (float): Spacing in x direction.
        dy (float): Spacing in y direction.
        name (str): Name for Blender mesh.
        layer (int): Layer to draw the plane on.
        color (list): Material color.
        wire (bool): Show wires for faces.
        bracing (str): None, 'cross', 'diagonals-right' or 'diagonals-left'.

    Returns:
        obj: Created plane Blender mesh object.
    """
    nx = int(Lx / dx)
    ny = int(Ly / dy)
    x = [i * dx for i in range(nx + 1)]
    y = [i * dy for i in range(ny + 1)]
    vertices = [[xi, yi, 0] for yi in y for xi in x]
    if not bracing:
        faces = [[(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
                  (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
                 for i in range(nx) for j in range(ny)]
    else:
        faces = []
        for i in range(nx):
            for j in range(ny):
                face = [(j + 0) * (nx + 1) + i + 0, (j + 0) * (nx + 1) + i + 1,
                        (j + 1) * (nx + 1) + i + 1, (j + 1) * (nx + 1) + i + 0]
                if bracing == 'cross':
                    n = len(vertices)
                    vertices.append(centroid_points([vertices[k] for k in face]))
                    faces.extend([[face[0], face[1], n], [face[1], face[2], n],
                                  [face[2], face[3], n], [face[3], face[0], n]])
                elif bracing == 'diagonals-right':
                    faces.extend([[face[0], face[1], face[2]], [face[2], face[3], face[0]]])
                elif bracing == 'diagonals-left':
                    faces.extend([[face[1], face[2], face[3]], [face[3], face[0], face[1]]])
    bmesh = xdraw_mesh(name=name, vertices=vertices, faces=faces, layer=layer, color=color, wire=wire)
    material = create_material(color=color)
    bmesh.data.materials.append(material)
    bmesh.select = False
    return bmesh


def draw_pipes(start=[[0, 0, 0]], end=[[1, 1, 1]], radius=1, layer=0, color=[1, 1, 1]):
    """ Draw multiple pipes.

    Parameters:
        start (list): Pipe start points.
        end (list): Pipe end points.
        radius (float): Radius of pipes.
        layer (int): Layer number.
        color (list): Material color.

    Returns:
        list: Created pipe objects.
    """
    return xdraw_pipes([{'start': u, 'end': v, 'radius': radius, 'layer': layer, 'color': color}
                        for u, v in zip(start, end)])


def draw_points(pos=[[0, 0, 0]], radius=1, layer=0):
    """ Draw multiple points (empties).

    Parameters:
        pos (list): Centroid locations [[x, y, z], ...].
        radius (float): Radius of points.
        layer (int): Layer number.

    Returns:
        list: Created point objects.
    """
    return xdraw_points([{'pos': i, 'radius': radius, 'layer': layer} for i in pos])


def draw_spheres(pos=[[0, 0, 0]], radius=1, layer=0, color=[1, 1, 1]):
    """ Draw multiple spheres.

    Parameters:
        pos (list): Centroid locations [[x, y, z], ...].
        radius (float): Radius of spheres.
        layer (int): Layer number.
        color (list): Material color.

    Returns:
        list: Created sphere objects.
    """
    return xdraw_spheres([{'pos': i, 'radius': radius, 'layer': layer, 'color': color} for i in pos])


def _link_objects(objects):
    for object in objects:
        mask = [i for i in object.layers]
        bpy.context.scene.objects.link(object)
        object.layers[:] = mask
    deselect_all_objects()
    return objects


# ==============================================================================
# xdraw functions
# ==============================================================================

def xdraw_cubes(cubes):
    """ Draw a set of cubes.

    Parameters:
        cubes (list): {'radius':, 'pos':, 'color':, 'name':, 'layer':}.

    Returns:
        list: Created cube objects.
    """
    bpy.ops.mesh.primitive_cube_add()
    object = bpy.context.object
    objects = []
    for cube in cubes:
        copy = object.copy()
        copy.scale *= cube.get('radius', 1)
        copy.location = Vector(cube.get('pos', [0, 0, 0]))
        material = create_material(color=cube.get('color', [1, 1, 1]))
        copy.data.materials.append(material)
        copy.name = cube.get('name', 'cube')
        copy.data = copy.data.copy()
        set_object_layer(object=copy, layer=cube.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_faces(faces, alpha=1):
    """ Draw a set of faces.

    Parameters:
        faces (list): {'color':, 'points':, 'name':, 'layer': }.
        alpha (float): Alpha [0, 1].

    Returns:
        None
    """
    for face in faces:
        color = face.get('color', [1, 1, 1])
        points = face['points']
        name = face.get('name', 'face')
        indices = [list(range(len(points)))]
        layer = face.get('layer')
        xdraw_mesh(name=name, vertices=points, faces=indices, color=color, layer=layer, alpha=alpha)


def xdraw_labels(labels):
    """ Draw pointcloud text labels.

    Parameters:
        labels (dic): {'pos':, 'name':, 'layer':}.

    Returns:
        list: Created label objects (bmeshes).
    """
    objects = xdraw_pointcloud(points=labels)
    set_objects_show_name(objects=objects, show=True)
    return objects


def xdraw_lines(lines):
    """ Draw a set of lines.

    Parameters:
        lines (list): {'color':, 'start':, 'end':, 'name':, 'width':, 'layer': }.

    Returns:
        list: Created line objects.
    """
    objects = []
    for line in lines:
        curve = bpy.data.curves.new(line.get('name', 'line'), type='CURVE')
        curve.dimensions = '3D'
        object = bpy.data.objects.new(line.get('name', 'line'), curve)
        object.location = [0, 0, 0]
        line_ = curve.splines.new('NURBS')
        line_.points.add(2)
        line_.points[0].co = list(line.get('start')) + [1]
        line_.points[1].co = list(line.get('end')) + [1]
        line_.order_u = 1
        material = create_material(color=line.get('color', [1, 1, 1]))
        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = line.get('width', 0.05)
        object.data.bevel_resolution = 0
        object.data.materials.append(material)
        set_object_layer(object=object, layer=line.get('layer', 0))
        objects.append(object)
    deselect_all_objects()
    return _link_objects(objects)


def xdraw_mesh(vertices=[], faces=[], edges=[], name=None, color=[1, 1, 1], layer=0, alpha=1, wire=True):
    """ Draws a Blender mesh.

    Parameters:
        vertices (list): Vertices co-ordinates.
        faces (list): Face vertex indices.
        edges (list): Edge vertex indices.
        name (str): Blender mesh name. If ``None``, it defaults to a randomly generated name.
        color (list): Material color.
        layer (int): Layer number.
        alpha (float): Alpha [0, 1].
        wire (bool): Show wires for faces.

    Returns:
        obj: Created Blender mesh object.
    """
    name = name or random_name()
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    bmesh = bpy.data.objects.new(name, mesh)
    bpy.context.scene.objects.link(bmesh)
    bmesh.show_wire = wire
    material = create_material(color=color, alpha=alpha)
    bmesh.data.materials.append(material)
    set_object_layer(object=bmesh, layer=layer)
    bmesh.select = False
    return bmesh


def xdraw_pipes(pipes, div=8):
    """ Draw a set of pipes.

    Parameters:
        pipes (list): {'radius':, 'start':, 'end':, 'color':, 'name':, 'layer':}.
        div (int): Divisions around cross-section.

    Returns:
        list: Created pipe objects.
    """
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=div, location=[0, 0, 0])
    object = bpy.context.object
    objects = []
    for pipe in pipes:
        radius = pipe.get('radius', 1)
        start = pipe.get('start', [0, 0, 0])
        end = pipe.get('end', [0, 0, 1])
        L = distance_point_point(start, end)
        pos = centroid_points([start, end])
        copy = object.copy()
        copy.name = pipe.get('name', 'pipe')
        copy.rotation_euler[1] = acos((end[2] - start[2]) / L)
        copy.rotation_euler[2] = atan2(end[1] - start[1], end[0] - start[0])
        copy.location = Vector(pos)
        copy.data = copy.data.copy()
        copy.scale = ((radius, radius, L))
        copy.show_wire = True
        material = create_material(color=pipe.get('color', [1, 1, 1]))
        copy.data.materials.append(material)
        set_object_layer(object=copy, layer=pipe.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_pointcloud(points):
    """ Draw a set of points using Blender mesh vertices.

    Parameters:
        points (dic): {'pos':, 'name':, 'layer':}.

    Returns:
        list: Created point objects (bmeshes).
    """
    object = xdraw_mesh(name='pt', vertices=[[0, 0, 0]])
    objects = []
    for point in points:
        copy = object.copy()
        copy.location = Vector(point.get('pos', [0, 0, 0]))
        copy.name = point.get('name', 'point')
        copy.data = copy.data.copy()
        set_object_layer(object=copy, layer=point.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_points(points):
    """ Draw a set of points (empties).

    Parameters:
        points (list): {'radius':, 'pos':, 'name':, 'layer':}.

    Returns:
        list: Created empty objects.
    """
    bpy.ops.object.empty_add(type='SPHERE', radius=1, location=[0, 0, 0])
    object = bpy.context.object
    objects = []
    for point in points:
        copy = object.copy()
        copy.scale *= point.get('radius', 1)
        copy.location = Vector(point.get('pos', [0, 0, 0]))
        copy.name = point.get('name', 'point')
        set_object_layer(object=copy, layer=point.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_spheres(spheres, div=20):
    """ Draw a set of spheres.

    Parameters:
        spheres (dic): {'radius':, 'pos':, 'color':, 'name':, 'layer':}.
        div (int): Divisions for spheres.

    Returns:
        list: Created sphere objects.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(ring_count=div, segments=div)
    object = bpy.context.object
    objects = []
    for sphere in spheres:
        copy = object.copy()
        copy.scale *= sphere.get('radius', 1)
        copy.location = Vector(sphere.get('pos', [0, 0, 0]))
        copy.name = sphere.get('name', 'sphere')
        copy.data = copy.data.copy()
        material = create_material(color=sphere.get('color', [1, 1, 1]))
        copy.data.materials.append(material)
        set_object_layer(object=copy, layer=sphere.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_texts(texts):
    """ Draw a set of text objects.

    Parameters:
        texts (list): {'radius':, 'pos':, 'color':, 'name':, 'text':, 'layer':}.

    Returns:
        list: Created text objects.
    """
    bpy.ops.object.text_add(view_align=True)
    object = bpy.context.object
    objects = []
    for text in texts:
        copy = object.copy()
        copy.scale *= text.get('radius', 1)
        copy.location = Vector(text.get('pos', [0, 0, 0]))
        copy.name = text.get('name', 'text')
        copy.data.body = text.get('text', 'text')
        copy.data = copy.data.copy()
        material = create_material(color=text.get('color', [1, 1, 1]))
        copy.data.materials.append(material)
        set_object_layer(object=copy, layer=text.get('layer', 0))
        objects.append(copy)
    delete_object(object=object)
    return _link_objects(objects)


def xdraw_polylines():
    NotImplementedError


def xdraw_geodesics():
    NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas_blender.utilities import clear_layer
    from numpy.random import rand

    clear_layer(layer=1)

    vertices = [[-1, 0, 0], [-2, 0, 0], [-2, 1, 0], [-1, 1, 0]]
    faces = [[0, 1, 2], [2, 3, 0]]
    bmesh = xdraw_mesh(name='bmesh', vertices=vertices, faces=faces, color=[1, 1, 1], alpha=0.5, layer=1)

    draw_cubes(pos=[[0, 3, 0]], radius=0.5, color=[1, 1, 0], layer=1)
    xdraw_cubes([{'radius': 0.5, 'pos': [0, 2, 0], 'color': [1, 0, 0], 'layer': 1}])

    draw_spheres(pos=[[-2, 2, 0]], radius=0.5, color=[0, 1, 0], layer=1)
    xdraw_spheres([{'radius': 0.5, 'pos': [-2, -1, 0], 'layer': 1}])

    xdraw_texts([{'radius': 0.5, 'pos': [5, 0, 0], 'color': [0, 0, 1], 'text': 'TEXT', 'layer': 1}])

    points = [{'pos': [i[0], i[1], i[2] + 2], 'radius': 0.01, 'layer': 1} for i in list(rand(10, 3))]
    xdraw_points(points)

    draw_lines(start=[[3, 0, 0]], end=[[5, 2, 0]], width=0.1, color=[0, 0, 0], layer=1)
    xdraw_lines([{'color': [0, 0.5, 1], 'start': [3, 1, 0], 'end': [5, -1, 0], 'width': 0.1, 'layer': 1}])

    draw_pipes(start=[[0, -2, 0]], end=[[0, -2, 1]], radius=0.1, color=[0, 0, 1], layer=1)
    xdraw_pipes([{'radius': 0.1, 'start': [0, -1, 0], 'end': [0, -1, 1], 'color': [0, 1, 0], 'layer': 1}])

    draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, bracing='cross', color=[1, 0, 1], layer=1)

    draw_cuboid(Lx=1, Ly=3, Lz=2, pos=[2, 0, 0], color=[1, 1, 0], layer=1)
