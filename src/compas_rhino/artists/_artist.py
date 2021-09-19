from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import Artist


class RhinoArtist(Artist):
    """Base class for all Rhino artists.

    Attributes
    ----------
    guids : list
        A list of the GUID of the Rhino objects created by the artist.

    """

    def __init__(self):
        self._guids = []

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear(self):
        if not self._guids:
            return
        compas_rhino.delete_objects(self._guids)
        self._guids = []
