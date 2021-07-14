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

    def __init__(self, item, layer=None):
        super(Artist, self).__init__(item)
        self.layer = layer

    def redraw(self):
        """Trigger a redraw."""
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
