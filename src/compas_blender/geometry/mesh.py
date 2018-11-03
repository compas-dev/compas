
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_blender.geometry import BlenderGeometry


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderMesh',
]


class BlenderMesh(BlenderGeometry):
    """"""

    def __init__(self, guid):
        super(BlenderMesh, self).__init__()


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    def get_vertex_coordinates(self):

        raise NotImplementedError


    def get_face_vertices(self):

        raise NotImplementedError


    def get_vertex_colors(self):

        raise NotImplementedError


    def set_vertex_colors(self, colors):

        raise NotImplementedError


    def unset_vertex_colors(self):

        raise NotImplementedError


    def get_vertices_and_faces(self):

        raise NotImplementedError


    def get_border(self):

        raise NotImplementedError


    def get_vertex_index(self):

        raise NotImplementedError


    def get_face_index(self):

        raise NotImplementedError


    def get_edge_index(guid):

        raise NotImplementedError


    def get_vertex_indices(guid):

        raise NotImplementedError


    def get_face_indices(guid):

        raise NotImplementedError


    def get_vertex_face_indices(guid):

        raise NotImplementedError


    def get_face_vertex_indices(guid):

        raise NotImplementedError


    def get_edge_vertex_indices(guid):

        raise NotImplementedError


    def normal(self, point):

        raise NotImplementedError


    def normals(self, points):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
