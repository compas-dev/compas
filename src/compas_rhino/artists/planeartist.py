from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import GeometryArtist
from .artist import RhinoArtist


class PlaneArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing planes.

    Parameters
    ----------
    plane : :class:`~compas.geometry.Plane`
        A COMPAS plane.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, plane, **kwargs):
        super(PlaneArtist, self).__init__(geometry=plane, **kwargs)

    def draw(self):
        """Draw the plane.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        raise NotImplementedError
