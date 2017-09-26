"""compas.cad.blender.utilities.drawing : Functions for drawing in Blender."""

from math import atan2
from math import acos

from compas_blender.utilities import delete_objects
from compas_blender.utilities import set_objects_layer
from compas_blender.utilities import set_objects_show_name
from compas_blender.utilities import deselect_all_objects

from compas.geometry import centroid_points
from compas.geometry import distance_point_point

try:
    import bpy
    from mathutils import Vector
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'delete_all_materials',
    'create_material',
    'draw_cuboid',
    'draw_cubes',
    'draw_spheres',
    'draw_bmesh',
    'draw_lines',
    'draw_pipes',
    'draw_plane',
    'draw_points',
    'xdraw_cubes',
    'xdraw_spheres',
    'xdraw_texts',
    'xdraw_pointcloud',
    'xdraw_lines',
    'xdraw_pipes',
    'xdraw_labels',
    'xdraw_points'
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


def create_material(name, color, alpha=1):
    """ Create a material of given RGB color and alpha.

    Parameters:
        name (str): Name of the material.
        color (tuple): (R, G, B) with values [0, 1].
        alpha (float): Alpha value from [0, 1].

    Returns:
        obj: Created material object.
    """
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.diffuse_shader = 'LAMBERT'
    material.diffuse_intensity = 1
    material.alpha = alpha
    material.ambient = 1
    material.emit = 2
    return material


try:
    delete_all_materials()
    create_material('red',    (1.0, 0.0, 0.0))
    create_material('orange', (1.0, 0.2, 0.0))
    create_material('yellow', (1.0, 1.0, 0.0))
    create_material('green',  (0.0, 1.0, 0.0))
    create_material('blue',   (0.0, 0.0, 1.0))
    create_material('indigo', (0.3, 0.0, 0.5))
    create_material('violet', (0.8, 0.3, 0.8))
    create_material('white',  (1.0, 1.0, 1.0))
    create_material('grey',   (0.5, 0.5, 0.5))
    create_material('black',  (0.0, 0.0, 0.0))
except NameError:
    pass

# ==============================================================================
# draw functions
# ==============================================================================

def draw_cuboid(Lx=1, Ly=1, Lz=1, location=[0, 0, 0], layer=0, wire=True):
    """ Draw a cuboid.

    Parameters:
        Lx (float): Length in x.
        Ly (float): Length in y.
        Lz (float): Length in z.
        location (list): Centroid location [x, y, z].
        layer (int): Layer number.
        colour (str): Material colour.
        wire (bool): Show wires for faces.

    Returns:
        obj: Created cube object.
    """
    bpy.ops.mesh.primitive_cube_add(radius=1, location=location)
    cube = bpy.context.object
    cube.dimensions = [Lx, Ly, Lz]
    cube.show_wire = wire
    set_objects_layer([cube], layer)
    cube.select = False
    return cube


def draw_cubes(pos=[[0, 0, 0]], radius=1, layer=0, color='grey'):
    """ Draw multiple cubes.

    Parameters:
        pos (list): Centroid locations [x, y, z].
        radius (float): Radius of cubes.
        layer (int): Layer number.
        color (str): Material color.

    Returns:
        obj: Created cube objects.
    """
    return xdraw_cubes([{'radius': radius, 'pos': i, 'color': color, 'layer': layer} for i in pos])


def draw_points(pos=[[0, 0, 0]], radius=1, layer=0):
    """ Draw multiple points (empties).

    Parameters:
        pos (list): Centroid locations [x, y, z].
        radius (float): Radius of points.
        layer (int): Layer number.

    Returns:
        obj: Created point objects.
    """
    return xdraw_points([{'radius': radius, 'pos': i, 'layer': layer} for i in pos])


def draw_spheres(pos=[[0, 0, 0]], radius=1, layer=0, color='grey'):
    """ Draw multiple spheres.

    Parameters:
        pos (list): Centroid locations [x, y, z].
        radius (float): Radius of spheres.
        layer (int): Layer number.
        color (str): Material color.

    Returns:
        obj: Created sphere objects.
    """
    return xdraw_spheres([{'radius': radius, 'pos': i, 'color': color, 'layer': layer} for i in pos])


def draw_lines(start=[[0, 0, 0]], end=[[1, 1, 1]], width=1, layer=0, color='grey'):
    """ Draw multiple lines.

    Parameters:
        start (list): Line start points.
        end (list): Line end points.
        width (float): Width of lines.
        layer (int): Layer number.
        color (str): Material color.

    Returns:
        obj: Created line objects.
    """
    return xdraw_lines([{'width': width, 'start': start[i], 'end': end[i], 'color': color, 'layer': layer}
                       for i in range(len(start))])


def draw_pipes(start=[[0, 0, 0]], end=[[1, 1, 1]], radius=1, layer=0, color='grey'):
    """ Draw multiple pipes.

    Parameters:
        start (list): Pipe start points.
        end (list): Pipe end points.
        radius (float): Radius of pipes.
        layer (int): Layer number.
        color (str): Material color.

    Returns:
        obj: Created pipe objects.
    """
    return xdraw_pipes([{'radius': radius, 'start': start[i], 'end': end[i], 'color': color, 'layer': layer}
                       for i in range(len(start))])


def draw_bmesh(name, vertices=[], edges=[], faces=[], layer=0, color='grey', wire=True):
    """ Draws a Blender mesh in the given layer.

    Parameters:
        name (str): Blender mesh name.
        vertices (list): Vertices [x, y, z].
        edges (list): Edges [vert1, vert2].
        faces (list): Faces [vert1, vert2, ...].
        layer (int): Layer number.
        color (str): Material color.
        wire (bool): Show wires for faces.

    Returns:
        obj: Created Blender mesh object.
    """
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    bmesh = bpy.data.objects.new(name, mesh)
    bpy.context.scene.objects.link(bmesh)
    bmesh.show_wire = wire
    bmesh.data.materials.append(bpy.data.materials[color])
    set_objects_layer([bmesh], layer)
    bmesh.select = False
    return bmesh


def draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, name='plane', layer=0, color='grey', wire=True, bracing=None):
    """ Create a plane mesh in x-y.

    Parameters:
        Lx (float): Length of the plane in x.
        Ly (float): Length of the plane in y.
        dx (float): Spacing in x direction.
        dy (float): Spacing in y direction.
        name (str): Name for Blender mesh plane.
        layer (int): Layer to draw the Blender mesh on.
        color (str): Material color.
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
    bmesh = draw_bmesh(name, vertices=vertices, faces=faces, layer=layer, color=color, wire=wire)
    bmesh.data.materials.append(bpy.data.materials[color])
    bmesh.select = False
    return bmesh


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
    objects = []
    bpy.ops.mesh.primitive_cube_add(radius=1, location=[0, 0, 0])
    object = bpy.context.object
    for cube in cubes:
        copy = object.copy()
        copy.name = cube.get('name', 'cube')
        copy.location = Vector(cube.get('pos', [0, 0, 0]))
        copy.scale *= cube.get('radius', 1)
        copy.data = copy.data.copy()
        copy.data.materials.append(bpy.data.materials[cube.get('color', 'white')])
        set_objects_layer([copy], cube.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_points(points):
    """ Draw a set of points (empties).

    Parameters:
        points (list): {'radius':, 'pos':, 'name':, 'layer':}.

    Returns:
        list: Created empty objects.
    """
    objects = []
    bpy.ops.object.empty_add(type='SPHERE', radius=1, location=[0, 0, 0])
    object = bpy.context.object
    for point in points:
        copy = object.copy()
        copy.name = point.get('name', 'point')
        copy.location = Vector(point.get('pos', [0, 0, 0]))
        copy.scale *= point.get('radius', 1)
        set_objects_layer([copy], point.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_labels(labels):
    """ Draw a set of text labels.

    Parameters:
        labels (dic): {'pos':, 'name':, 'layer':}.

    Returns:
        list: Created labels objects (bmeshes).
    """
    objects = xdraw_pointcloud(labels)
    set_objects_show_name(objects, show=True)
    deselect_all_objects()
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
        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = line.get('width', 0.05)
        object.data.bevel_resolution = 0
        object.data.materials.append(bpy.data.materials[line.get('color', 'white')])
        set_objects_layer([object], line.get('layer', 0))
        objects.append(object)
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_pipes(pipes, div=8):
    """ Draw a set of pipes.

    Parameters:
        pipes (list): {'radius':, 'start':, 'end':, 'color':, 'name':, 'layer':}.
        div (int): Divisions around cross-section.

    Returns:
        list: Created pipe objects.
    """
    objects = []
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=div, location=[0, 0, 0])
    object = bpy.context.object
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
        copy.data.materials.append(bpy.data.materials[pipe.get('color', 'white')])
        set_objects_layer([copy], pipe.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_pointcloud(points):
    """ Draw a set of points using Blender mesh vertices.

    Parameters:
        points (dic): {'pos':, 'name':, 'layer':}.

    Returns:
        list: Created point objects (bmeshes).
    """
    objects = []
    object = draw_bmesh('pt', vertices=[[0, 0, 0]])
    for point in points:
        copy = object.copy()
        copy.name = point.get('name', 'point')
        copy.location = Vector(point.get('pos', [0, 0, 0]))
        copy.data = copy.data.copy()
        set_objects_layer([copy], point.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_spheres(spheres, div=20):
    """ Draw a set of spheres.

    Parameters:
        spheres (dic): {'radius':, 'pos':, 'color':, 'name':, 'layer':}.
        div (int): Divisions for spheres.

    Returns:
        list: Created sphere objects.
    """
    objects = []
    bpy.ops.mesh.primitive_uv_sphere_add(size=1, location=[0, 0, 0], ring_count=div, segments=div)
    object = bpy.context.object
    for sphere in spheres:
        copy = object.copy()
        copy.name = sphere.get('name', 'sphere')
        copy.location = Vector(sphere.get('pos', [0, 0, 0]))
        copy.scale *= sphere.get('radius', 1)
        copy.data = copy.data.copy()
        copy.data.materials.append(bpy.data.materials[sphere.get('color', 'white')])
        set_objects_layer([copy], sphere.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_texts(texts):
    """ Draw a set of text objects.

    Parameters:
        texts (list): {'radius':, 'pos':, 'color':, 'name':, 'text':, 'layer':}.

    Returns:
        list: Created text objects.
    """
    objects = []
    bpy.ops.object.text_add(radius=1, view_align=True, location=[0, 0, 0])
    object = bpy.context.object
    for text in texts:
        copy = object.copy()
        copy.name = text.get('name', 'text')
        copy.data.body = text.get('text', 'text')
        copy.location = Vector(text.get('pos', [0, 0, 0]))
        copy.scale *= text.get('radius', 1)
        copy.data = copy.data.copy()
        copy.data.materials.append(bpy.data.materials[text.get('color', 'white')])
        set_objects_layer([copy], text.get('layer', 0))
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    deselect_all_objects()
    return objects


def xdraw_polylines():
    NotImplementedError


def xdraw_faces():
    NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from compas_blender.utilities import clear_layers
    from numpy.random import rand

    clear_layers([0])

    vertices = [[5, 0, 0], [6, 0, 0], [6, 1, 0], [5, 1, 0]]
    faces = [[0, 1, 2], [2, 3, 0]]
    bmesh = draw_bmesh('bmesh', vertices=vertices, faces=faces, color='red')

    draw_cubes(pos=[[0, 2, 0]], radius=0.5, color='red')
    xdraw_cubes([{'radius': 0.5, 'pos': [0, 0, 0], 'color': 'black'}])

    draw_spheres(pos=[[2, 2, 0]], radius=0.5, color='grey')
    xdraw_spheres([{'radius': 0.5, 'pos': [2, 0, 0], 'color': 'green'}])

    xdraw_texts([{'radius': 0.5, 'pos': [4, 0, 0], 'color': 'red', 'text': '1'}])

    points = [[i[0] - 2, i[1], i[2]] for i in list(rand(100, 3))]
    draw_points(pos=points, radius=0.01)

    draw_lines(start=[[3, 0, 0]], end=[[5, 2, 0]], width=0.1, color='blue')
    xdraw_lines([{'color': 'violet', 'start': [3, 1, 0], 'end': [5, 3, 0], 'width': 0.1}])

    draw_pipes(start=[[0, -3, 0]], end=[[0, -3, 1]], radius=0.1, color='blue')
    xdraw_pipes([{'radius': 0.1, 'start': [0, -2, 0], 'end': [0, -2, 1], 'color': 'green'}])

    draw_plane(Lx=1, Ly=1, dx=0.5, dy=0.5, bracing='diagonals-right', color='yellow')
