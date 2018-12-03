
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.utilities import set_deselect

try:
    import bpy
    from mathutils import Vector
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'create_material',
    'xdraw_labels',
    'xdraw_points',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_polylines',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
]


#def _link_objects(objects):
#
#    for object in objects:
#        bpy.context.scene.objects.link(object)
#    return objects


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

    objects = []

    for data in points:
        
        bpy.ops.object.empty_add(type='SPHERE', radius=data['radius'], location=data['pos'])
        object = bpy.context.object
        
        object.name = data.get('name', 'point')
        # layer
        objects.append(object)

    set_deselect(objects=objects)

    return objects


def xdraw_lines(lines, **kwargs):

    raise NotImplementedError


def xdraw_geodesics(geodesics, **kwargs):

    raise NotImplementedError


def xdraw_polylines(polylines, **kwargs):

    raise NotImplementedError


def xdraw_breps(faces, **kwargs):

    raise NotImplementedError


def xdraw_cylinders(cylinders, cap=False, **kwargs):

    raise NotImplementedError


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


def xdraw_mesh(vertices, faces, name=None, color=None, **kwargs):

    raise NotImplementedError


def xdraw_faces(faces, **kwargs):

    raise NotImplementedError


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

    objects = xdraw_points(points=points)
    objects = xdraw_spheres(spheres=spheres)
    objects = xdraw_cubes(cubes=cubes)
    
    set_objects_show_names(objects=objects, show=1)
