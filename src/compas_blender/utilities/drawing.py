
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.utilities import set_deselect

from compas.geometry import distance_point_point
from compas.geometry import centroid_points

try:
    import bpy
    from mathutils import Vector
except ImportError:
    pass

from math import acos
from math import atan2


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'create_material',
    'xdraw_labels',
    'xdraw_points',
    'xdraw_pointcloud',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
]


def _link_objects(objects):

    for object in objects:
        bpy.context.collection.objects.link(object)

    return objects


def create_material(color, alpha=1):
    
    ckey  = '-'.join(['{0:.2f}'.format(i) for i in color + [alpha]])
    names = [i.name for i in bpy.data.materials]

    if ckey not in names:
        material = bpy.data.materials.new(name=ckey)
        material.diffuse_color = color
        return material
    else: 
        return bpy.data.materials[ckey]


def xdraw_labels(labels, **kwargs):

    raise NotImplementedError


def xdraw_points(points, **kwargs):

    objects = [0] * len(points)

    for c, data in enumerate(points):
        
        bpy.ops.object.empty_add(type='SPHERE', radius=data['radius'], location=data['pos'])
        object = bpy.context.object
        
        object.name = data.get('name', 'point')
        # layer
        objects[c] = object

    set_deselect(objects=objects)

    return objects


def xdraw_lines(lines, **kwargs):

    objects = []

    for data in lines:

        start = data.get('start')
        end   = data.get('end')
        name  = data.get('name', 'line')
        
        bpy.ops.curve.primitive_nurbs_curve_add(radius=1, location=(0, 0, 0))
        object = bpy.context.object

        spline = object.data.splines[0]
        spline.points[0].co = start + [1]
        spline.points[1].co = start + [1]
        spline.points[2].co = end + [1]
        spline.points[3].co = end + [1]
        spline.order_u = 1

        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = data.get('width', 0.05)
        object.data.bevel_resolution = 0
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        # layer
        
        objects.append(object)
        
    set_deselect(objects=objects)

    return objects


def xdraw_geodesics(geodesics, **kwargs):

    raise NotImplementedError


def xdraw_breps(faces, **kwargs):

    raise NotImplementedError


def xdraw_cylinders(cylinders, div=10, **kwargs):
    
    objects = []

    for data in cylinders:
        
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=div, location=[0, 0, 0])
        object = bpy.context.object
        
        radius = data.get('radius', 1)
        start  = data.get('start', [0, 0, 0])
        end    = data.get('end', [0, 0, 1])
        L      = distance_point_point(start, end)
        pos    = centroid_points([start, end])
        
        object.name = data.get('name', 'cylinder')
        object.rotation_euler[1] = acos((end[2] - start[2]) / L)
        object.rotation_euler[2] = atan2(end[1] - start[1], end[0] - start[0])
        object.location = pos
        object.scale = ((radius, radius, L))
        # layer
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects.append(object)

    set_deselect(objects=objects)

    return objects


def xdraw_pipes(pipes, cap=2, fit=1.0, **kwargs):

    raise NotImplementedError


def xdraw_forces(forces, color, **kwargs):

    raise NotImplementedError


def xdraw_spheres(spheres, div=10, **kwargs):
    
    objects = []

    for data in spheres:
        
        bpy.ops.mesh.primitive_uv_sphere_add(radius=data['radius'], location=data['pos'], ring_count=div, segments=div)
        object = bpy.context.object
        
        object.name = data.get('name', 'sphere')
        # layer
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects.append(object)

    set_deselect(objects=objects)

    return objects



def xdraw_cubes(cubes, **kwargs):
    
    objects = []

    for data in cubes:
        
        bpy.ops.mesh.primitive_cube_add(size=data['radius'], location=data['pos'])
        object = bpy.context.object
        
        object.name = data.get('name', 'cube')
        # layer
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects.append(object)

    set_deselect(objects=objects)

    return objects


def xdraw_mesh(vertices, edges=None, faces=None, name='mesh', color=[1, 1, 1], **kwargs):

    edges = [] if not edges else edges
    faces = [] if not faces else faces

    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)

    object = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(object)
    object.show_wire = True
    object.data.materials.append(create_material(color=color))
    # layer
    
    set_deselect(objects=[object])
    
    return object    


def xdraw_faces(faces, **kwargs):

    raise NotImplementedError
    
    
def xdraw_pointcloud(points):

    objects = []

    for data in points:

        object = xdraw_mesh(name=data.get('name', 'pt'), vertices=[[0, 0, 0]])

        object.location = data['pos']
        # layer
        objects.append(object)
        
    set_deselect(objects=objects)

    return objects


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    
    from compas_blender.utilities import set_objects_show_names

    points = [
        {'pos': [0, 0, 1], 'radius': 0.2, 'name': 'pt'},
        {'pos': [0, 0, 3], 'radius': 0.5},
    ]
    
    spheres = [
        {'pos': [1, 0, 1], 'radius': 0.2, 'name': 'sphere', 'color': [1, 0, 0]},
        {'pos': [1, 0, 3], 'radius': 0.5, 'color': [0, 1, 0]},
    ]
    
    cubes = [
        {'pos': [2, 0, 1], 'radius': 0.2, 'name': 'cube', 'color': [1, 1, 0]},
        {'pos': [2, 0, 3], 'radius': 0.5, 'color': [0, 1, 1]},
    ]
    
    cylinders = [
        {'start': [3, 1, 1], 'end': [3, 0, 2], 'radius': 0.2, 'name': 'cylinder', 'color': [1, 0, 1]},
        {'start': [3, 1, 3], 'end': [3, 0, 4], 'radius': 0.1, 'color': [0, 0, 1]},
    ]
    
    lines = [
        {'start': [4, 1, 1], 'end': [4, 0, 2], 'radius': 0.05, 'name': 'line', 'color': [1, 0, 0]},
        {'start': [4, 1, 3], 'end': [4, 0, 4], 'radius': 0.1, 'color': [1, 0, 1]},
    ]

    for i in range(1):
        #xdraw_points(points=points)
        #xdraw_spheres(spheres=spheres)
        #xdraw_cubes(cubes=cubes)
        #xdraw_cylinders(cylinders=cylinders)
        #xdraw_lines(lines=lines)
        objects = xdraw_pointcloud(points=points)
    
    #vertices = [[-1, 0, 1], [-2, 0, 2], [-2, 1, 1], [-1, 1, 0]]
    #faces    = [[0, 1, 2], [2, 3, 0]]
    #bmesh    = xdraw_mesh(name='bmesh', vertices=vertices, faces=faces, color=[1, 0, 1])
    
    set_objects_show_names(objects=objects, show=1)
    