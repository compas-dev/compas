from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.scene import BaseArtist


__all__ = ["Artist"]


class Artist(BaseArtist):
    """Base class for all Rhino artists.

    Attributes
    ----------
    guids : list
        A list of the GUID of the Rhino objects created by the artist.

    """

    def __init__(self):
        super(Artist, self).__init__()
        self._guids = []

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        """Trigger a redraw."""
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear(self):
        """Delete all objects created by the artist."""
        if not self._guids:
            return
        compas_rhino.delete_objects(self._guids)
        self._guids = []
