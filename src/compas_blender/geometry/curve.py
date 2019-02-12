
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors

from compas_blender.geometry import BlenderGeometry

try:
    import bpy
    from mathutils.geometry import interpolate_bezier
except ImportError:
    pass


__all__ = [
    'BlenderCurve',
]


class BlenderCurve(BlenderGeometry):

    def __init__(self, object):
        super(BlenderCurve, self).__init__(object)


    @classmethod
    def from_points(cls, points, degree=None):

        raise NotImplementedError


    def control_points(self):

        return self.geometry.splines[0].bezier_points


    def control_point_coordinates(self):

        points = self.control_points()
        middle = [list(i.co) for i in points]
        left   = [list(i.handle_left) for i in points]
        right  = [list(i.handle_right) for i in points]

        return middle, left, right


    def control_points_on(self):

        raise NotImplementedError


    def control_points_off(self):

        raise NotImplementedError


    def select_control_point(self):

        raise NotImplementedError


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


    def divide(self, number_of_segments):

        m, l, r = self.control_point_coordinates()
        points  = [list(i) for i in interpolate_bezier(m[0], r[0], l[1], m[1], number_of_segments + 1)]

        return [add_vectors(self.location, point) for point in points]


    def divide_length(self, length_of_segments):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None, return_param=False):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas_blender.utilities import xdraw_points
    from compas_blender.utilities import get_object_by_name


    object = get_object_by_name(name='BezierCurve')

    curve = BlenderCurve(object=object)

    print(curve)
    print(curve.control_points())
    print(curve.control_point_coordinates())

    points = [{'pos': i, 'radius': 0.1} for i in curve.divide(number_of_segments=5)]

    xdraw_points(points=points)
