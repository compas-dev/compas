from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import rgb_to_rgb

from compas_rhino.geometry.transformations import xtransform

from compas.artists import RobotModelArtist
from compas_ghpython.utilities import draw_mesh
from .artist import GHArtist


class RobotModelArtist(GHArtist, RobotModelArtist):
    """Artist for drawing robot models.

    Parameters
    ----------
    model : :class:`compas.robots.RobotModel`
        Robot model.
    """

    def __init__(self, model, **kwargs):
        super(RobotModelArtist, self).__init__(model=model, **kwargs)

    def transform(self, native_mesh, transformation):
        xtransform(native_mesh, transformation)

    def create_geometry(self, geometry, name=None, color=None):
        if color:
            color = rgb_to_rgb(color[0], color[1], color[2])
        vertices, faces = geometry.to_vertices_and_faces()
        mesh = draw_mesh(vertices, faces, color=color)
        # Try to fix invalid meshes
        if not mesh.IsValid:
            mesh.FillHoles()
        return mesh

    def draw(self):
        self.draw_visual()
