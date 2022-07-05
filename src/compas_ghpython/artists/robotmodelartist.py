from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_ghpython
from compas.utilities import rgb_to_rgb

from compas_rhino.geometry.transformations import xtransform

from compas.artists import RobotModelArtist
from .artist import GHArtist


class RobotModelArtist(GHArtist, RobotModelArtist):
    """Artist for drawing robot models.

    Parameters
    ----------
    model : :class:`~compas.robots.RobotModel`
        Robot model.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.RobotModelArtist` for more info.

    """

    def __init__(self, model, **kwargs):
        super(RobotModelArtist, self).__init__(model=model, **kwargs)

    # again not really sure why this is here
    def transform(self, native_mesh, transformation):
        xtransform(native_mesh, transformation)

    # same here
    # there is no reference to self...
    def create_geometry(self, geometry, name=None, color=None):
        if color:
            color = rgb_to_rgb(color[0], color[1], color[2])

        vertices, faces = geometry.to_vertices_and_faces(triangulated=False)

        mesh = compas_ghpython.draw_mesh(vertices, faces, color=color)
        # Try to fix invalid meshes
        if not mesh.IsValid:
            mesh.FillHoles()
        return mesh

    def draw(self):
        """Draw the visual meshes of the robot model.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        return self.draw_visual()
