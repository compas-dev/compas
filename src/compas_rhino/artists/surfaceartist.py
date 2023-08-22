from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import surface_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class SurfaceArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing surfaces.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Geometry`
        A COMPAS surface.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, surface, **kwargs):
        super(SurfaceArtist, self).__init__(geometry=surface, **kwargs)

    def draw(self, color=None):
        """Draw the surface.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the surface.
            The default color is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color) or self.color
        surface = surface_to_rhino(self.geometry)
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)
        guid = sc.doc.Objects.AddSurface(surface, attr)
        return [guid]
