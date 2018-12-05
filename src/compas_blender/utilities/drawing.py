
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
    'xdraw_points',
    'xdraw_pointcloud',
    'xdraw_lines',
    'xdraw_geodesics',
    'xdraw_faces',
    'xdraw_cylinders',
    'xdraw_pipes',
    'xdraw_spheres',
    'xdraw_mesh',
    'xdraw_texts',
]


def _link_objects(objects):

    for object in objects:
        bpy.context.collection.objects.link(object)

    set_deselect(objects=objects)
    
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


def xdraw_points(points, **kwargs):

    bpy.ops.object.empty_add(type='SPHERE', radius=1, location=[0, 0, 0])
    copy = bpy.context.object
    
    objects = [0] * len(points)

    for c, data in enumerate(points):
        
        object          = copy.copy()
        object.scale   *= data['radius']
        object.location = data['pos']
        object.name     = data.get('name', 'point')
        # layer and delete copy
        objects[c]      = object

    return _link_objects(objects)


def xdraw_lines(lines, **kwargs):

    objects = [0] * len(lines)

    for c, data in enumerate(lines):
        
        name  = data.get('name', 'line')
        
        curve = bpy.data.curves.new(name, type='CURVE')
        curve.dimensions = '3D'
        object = bpy.data.objects.new(name, curve)
        object.location = [0, 0, 0]

        spline = curve.splines.new('NURBS')
        spline.points.add(2)
        spline.points[0].co = list(data.get('start')) + [1]
        spline.points[1].co = list(data.get('end')) + [1]
        spline.order_u = 1

        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = data.get('width', 0.05)
        object.data.bevel_resolution = 0
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        # layer
        objects[c] = object
         
    return _link_objects(objects)


def xdraw_geodesics(geodesics, **kwargs):

    raise NotImplementedError


def xdraw_breps(faces, **kwargs):

    raise NotImplementedError


def xdraw_cylinders(cylinders, div=10, **kwargs):
    
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
        # layer and delete copy
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        objects[c] = object

    return _link_objects(objects)


def xdraw_pipes(pipes, cap=2, fit=1.0, **kwargs):

    raise NotImplementedError


def xdraw_forces(forces, color, **kwargs):

    raise NotImplementedError


def xdraw_spheres(spheres, div=10, **kwargs):
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=[0, 0, 0], ring_count=div, segments=div)
    copy = bpy.context.object
    
    objects = [0] * len(spheres)

    for c, data in enumerate(spheres):
        
        object          = copy.copy()
        object.name     = data.get('name', 'sphere')
        object.scale   *= data['radius']    
        object.location = data['pos']  
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        # layer and delete copy
        objects[c] = object

    return _link_objects(objects)


def xdraw_cubes(cubes, **kwargs):
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=[0, 0, 0])
    copy = bpy.context.object
    
    objects = [0] * len(cubes)

    for c, data in enumerate(cubes):
        
            
        object          = copy.copy()
        object.name     = data.get('name', 'cube')
        object.scale   *= data['radius']
        object.location = data['pos']
        object.data.materials.append(create_material(color=data.get('color', [1, 1, 1])))
        # layer and delete copy
        objects[c] = object

    return _link_objects(objects)


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

    for face in faces:
        
        name    = face.get('name', 'face')
        points  = face['points']
        indices = [list(range(len(points)))]
        color   = face.get('color', [1, 1, 1])
        # layer
        xdraw_mesh(name=name, vertices=points, faces=indices, color=color)
    
    
def xdraw_pointcloud(points):

    for data in points:

        object = xdraw_mesh(name=data.get('name', 'pt'), vertices=[[0, 0, 0]])
        object.location = data['pos']
        objects.append(object)
        # layer
        
    set_deselect(objects=objects)

    return objects


def xdraw_texts(texts):
    
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
        # layer and delete copy
        objects[c] = object

    return _link_objects(objects)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    
    from compas_blender.utilities import set_objects_show_names
    
    from time import time
    
    
    n = 500

    points  = [{'pos': [0, 0, i], 'radius': 0.2, 'name': 'pt'} for i in range(n)]
    lines   = [{'start': [4, 1, i], 'end': [4, 0, i], 'radius': 0.1, 'color': [1, 0, 1]} for i in range(n)]
    cyls    = [{'start': [3, 1, i], 'end': [3, 0, i], 'radius': 0.1, 'color': [0, 0, 1]} for i in range(n)]
    spheres = [{'pos': [1, 0, i], 'radius': 0.5, 'color': [0, 1, 0]} for i in range(n)]
    cubes   = [{'pos': [2, 0, i], 'radius': 0.5, 'color': [0, 1, 1]} for i in range(n)]
    texts   = [{'text': 'text2', 'radius': 0.1, 'color': [1, 0, 1], 'pos': [5, 1, i]} for i in range(n)]
    
    tic = time()

    #xdraw_points(points=points)
    #xdraw_lines(lines=lines)
    #xdraw_cylinders(cylinders=cyls)
    #xdraw_spheres(spheres=spheres)
    #xdraw_cubes(cubes=cubes)
    xdraw_texts(texts=texts)
        
    print('Time: ', time() - tic)
    
    #vertices = [[-1, 0, 1], [-2, 0, 2], [-2, 1, 1], [-1, 1, 0]]
    #faces    = [[0, 1, 2], [2, 3, 0]]
    #bmesh    = xdraw_mesh(name='bmesh', vertices=vertices, faces=faces, color=[1, 0, 1])
    
    #objects = xdraw_pointcloud(points=points)
    #set_objects_show_names(objects=objects, show=1)
    