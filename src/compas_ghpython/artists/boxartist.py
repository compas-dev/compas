from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import GHArtist


class BoxArtist(GHArtist, ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.ShapeArtist` for more info.

    """

    def __init__(self, box, **kwargs):
        super(BoxArtist, self).__init__(shape=box, **kwargs)

    def draw(self, color=None):
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        color = Color.coerce(color) or self.color
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        mesh = compas_ghpython.draw_mesh(vertices, faces, color=color.rgb255)
        return mesh
