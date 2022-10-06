from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import RhinoArtist


class BoxArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, box, layer=None, **kwargs):
        super(BoxArtist, self).__init__(shape=box, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        guid = compas_rhino.draw_mesh(
            vertices,
            faces,
            layer=self.layer,
            name=self.shape.name,
            color=color.rgb255,
            disjoint=True,
        )
        return [guid]
