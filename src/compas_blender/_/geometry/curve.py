from compas.geometry import add_vectors

from compas_blender.geometry import BlenderGeometry
from compas_blender.utilities import select_curve

try:
    import bpy
    from mathutils.geometry import interpolate_bezier
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['BlenderCurve']


class BlenderCurve(BlenderGeometry):
    """"""

    def __init__(self, object):
        self.guid = object.name
        self.curve = object
        self.geometry = self.curve.data
        self.attributes = {}
        self.type = self.curve.type

    @classmethod
    def from_selection(cls):
        object = select_curve()
        return cls(object)

    @property
    def xyz(self):
        return list(self.curve.location)

    def hide(self):
        self.curve.hide = True

    def show(self):
        self.curve.hide = False

    def select(self):
        self.curve.select = True

    def unselect(self):
        self.curve.select = False

    def space(self, density):
        raise NotImplementedError

    def heightfield(self, density):
        raise NotImplementedError

    def curvature(self):
        raise NotImplementedError

    def tangents(self, points):
        raise NotImplementedError

    def descent(self, points):
        raise NotImplementedError
        
    def handles(self):
        points = self.curve.data.splines[0].bezier_points
        middle = [list(i.co) for i in points]
        left = [list(i.handle_left) for i in points]
        right = [list(i.handle_right) for i in points]
        return middle, left, right

    def divide(self, number_of_segments):
        middle, left, right = self.handles()
        n = number_of_segments + 1
        points = [list(i) for i in interpolate_bezier(middle[0], right[0], left[1], middle[1], n)]
        return [add_vectors(self.xyz, point) for point in points]
        
    def divide_length(self, length_of_segments):
        raise NotImplementedError

    def closest_point(self, point, maxdist=None):
        raise NotImplementedError

    def closest_points(self, points, maxdist=None):
        raise NotImplementedError
        
    def to_bmesh(self, divisions=10):
        self.curve.data.resolution_u = divisions
        mesh = self.curve.to_mesh(bpy.context.scene, True, 'PREVIEW')
        bmesh = bpy.data.objects.new(self.guid + '-bmesh', mesh)
        bmesh.location = self.xyz
        bpy.context.scene.objects.link(bmesh)
        return bmesh


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas_blender.utilities import draw_cuboid

    curve = BlenderCurve.from_selection()

    print(curve.guid)
    print(curve.curve)
    print(curve.geometry)
    print(curve.attributes)
    print(curve.type)
    print(curve.xyz)
    
    curve.hide()
    curve.show()
    curve.unselect()
    curve.select()
    curve.to_bmesh()
    
    points = curve.divide(number_of_segments=10)
    for point in points:
        draw_cuboid(Lx=0.1, Ly=0.1, Lz=0.1, pos=point)
