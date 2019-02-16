
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.geometry import BlenderGeometry


__all__ = [
    'BlenderSurface',
]


class BlenderSurface(BlenderGeometry):

    def __init__(self, guid):
        super(BlenderSurface, self).__init__()


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    def space(self, density=10):

        raise NotImplementedError


    def heightfield(self, density=10, over_space=True):

        raise NotImplementedError


    def descent(self, points=None):

        raise NotImplementedError


    def curvature(self, points=None):

        raise NotImplementedError


    def borders(self, type=1):

        raise NotImplementedError


    def project_point(self, point, direction=(0, 0, 1)):

        raise NotImplementedError


    def project_points(self, points, direction=(0, 0, 1), include_none=True):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError


    def pull_point(self, point):

        raise NotImplementedError


    def pull_points(self, points):

        raise NotImplementedError


    def pull_curve(self, curve):

        raise NotImplementedError


    def pull_curves(self, curves):

        raise NotImplementedError


    def pull_mesh(self, mesh, fixed=None, d=1.0):

        raise NotImplementedError


    def pull_meshes(self, meshes):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
