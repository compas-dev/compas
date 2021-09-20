from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import Artist


class RhinoArtist(Artist):
    """Base class for all Rhino artists.
    """

    def clear_layer(self):
        if self.layer:
            compas_rhino.clear_layer(self.layer)
