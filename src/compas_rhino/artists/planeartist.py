from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import PrimitiveArtist
from .artist import RhinoArtist


class PlaneArtist(RhinoArtist, PrimitiveArtist):
    """Artist for drawing planes.

    Parameters
    ----------
    plane : :class:`~compas.geometry.Plane`
        A COMPAS plane.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`PrimitiveArtist`.

    """

    def __init__(self, plane, layer=None, **kwargs):
        super(PlaneArtist, self).__init__(primitive=plane, layer=layer, **kwargs)

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        raise NotImplementedError
