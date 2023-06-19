from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import Artist


class RhinoArtist(Artist):
    """Base class for all Rhino artists.

    Parameters
    ----------
    layer : str, optional
        A layer name.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`Artist` for more info.

    """

    def __init__(self, layer=None, **kwargs):
        super(RhinoArtist, self).__init__(**kwargs)
        self.layer = layer

    def clear_layer(self):
        """Clear the layer of the artist.

        Returns
        -------
        None

        """
        if self.layer:
            compas_rhino.clear_layer(self.layer)
