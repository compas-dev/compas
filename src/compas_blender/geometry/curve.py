
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.geometry import BlenderGeometry


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderCurve',
]


class BlenderCurve(BlenderGeometry):

    def __init__(self, guid):
        super(BlenderCurve, self).__init__()


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    @classmethod
    def from_points(cls, points, degree=None):

        raise NotImplementedError


    def is_line(self):

        raise NotImplementedError


    def is_polyline(self):

        raise NotImplementedError


    def control_points(self):

        raise NotImplementedError


    def control_point_coordinates(self):

        raise NotImplementedError


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


    def divide(self, number_of_segments, over_space=False):

        raise NotImplementedError


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

    pass
