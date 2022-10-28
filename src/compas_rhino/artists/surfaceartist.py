from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import SurfaceArtist
from compas.colors import Color
from .artist import RhinoArtist


class SurfaceArtist(RhinoArtist, SurfaceArtist):
    """Artist for drawing surfaces.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Surface`
        A COMPAS surface.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.SurfaceArtist`.

    """

    def __init__(self, surface, layer=None, **kwargs):
        super(SurfaceArtist, self).__init__(surface=surface, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the surface.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the surface.
            The default color is :attr:`compas.artists.SurfaceArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        surfaces = [{"surface": self.surface, "color": color.rgb255, "name": self.surface.name}]
        return compas_rhino.draw_surfaces(surfaces, layer=self.layer, clear=False, redraw=False)
