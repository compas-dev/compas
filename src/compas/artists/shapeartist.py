from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .geometryartist import GeometryArtist


class ShapeArtist(GeometryArtist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape : :class:`~compas.geometry.Shape`
        The geometry of the shape.

    Attributes
    ----------
    u : int
        The resolution in the U direction of the discrete shape representation.
    v : int
        The resolution in the V direction of the discrete shape representation.

    See Also
    --------
    :class:`compas.artists.MeshArtist`
    :class:`compas.artists.NetworkArtist`
    :class:`compas.artists.VolMeshArtist`

    """

    def __init__(self, shape, **kwargs):
        super(ShapeArtist, self).__init__(geometry=shape, **kwargs)
        self._u = None
        self._v = None
        self.u = kwargs.get("u")
        self.v = kwargs.get("v")

    @property
    def u(self):
        if not self._u:
            self._u = 16
        return self._u

    @u.setter
    def u(self, u):
        if u and u > 3:
            self._u = u

    @property
    def v(self):
        if not self._v:
            self._v = 16
        return self._v

    @v.setter
    def v(self, v):
        if v and v > 3:
            self._v = v
