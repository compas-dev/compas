
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


def _link_objects(objects):

    for object in objects:
        pass
        #bpy.context.scene.objects.link(object)
#    deselect_all_objects()
    return objects


def xdraw_labels(labels, **kwargs):

    raise NotImplementedError


def xdraw_points(points, **kwargs):

    bpy.ops.object.empty_add(type='SPHERE', radius=1, location=[0, 0, 0])

    object  = bpy.context.object
    objects = []

    for point in points:

        copy = object.copy()
#        copy.scale *= point.get('radius', 1)
        copy.location = Vector(point.get('pos', [0, 0, 0]))
#        copy.name = point.get('name', 'point')

#        set_object_layer(object=copy, layer=point.get('layer', 0))
        objects.append(copy)

#    delete_object(object=object)
    return _link_objects(objects)


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


def xdraw_spheres(spheres, **kwargs):

    raise NotImplementedError


def xdraw_mesh(vertices, faces, name=None, color=None, **kwargs):

    raise NotImplementedError


def xdraw_faces(faces, **kwargs):

    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    points = [
        {'pos': [0, 0, 1]},
        {'pos': [0, 0, 3]},
    ]

    xdraw_points(points=points)
