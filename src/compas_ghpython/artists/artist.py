from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import Artist


class GHArtist(Artist):
    """Base class for all GH artists."""

    def __init__(self, **kwargs):
        super(GHArtist, self).__init__(**kwargs)

    def clear(self):
        pass
