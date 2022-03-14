from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.artists import Artist
import scriptcontext as sc
import Rhino.Display


class GHArtist(Artist):
    """Base class for all GH artists.
    """

    def __init__(self, **kwargs):
        super(GHArtist, self).__init__(**kwargs)

    def __del__(self):
        if 'displays' not in sc.sticky:
            return
        for name in list(sc.sticky['displays'].keys()):
            display = sc.sticky['displays'][name]
            display.Dispose()
            del sc.sticky['displays'][name]

    @staticmethod
    def clear():
        """Clear all the registered custom displays.

        Returns
        -------
        None

        """
        if 'displays' not in sc.sticky:
            return
        for name in list(sc.sticky['displays'].keys()):
            display = sc.sticky['displays'][name]
            display.Dispose()
            del sc.sticky['displays'][name]

    def display(self, name):
        """Get a display for the artist.

        Parameters
        ----------
        name : str
            The display name.

        Returns
        -------
        :rhino:`Rhino.Display.CustomDisplay`

        """
        if 'displays' not in sc.sticky:
            sc.sticky['displays'] = {}
        if name in sc.sticky['displays']:
            display = sc.sticky['displays'][name]
            display.Dispose()
            del sc.sticky['displays'][name]
        display = Rhino.Display.CustomDisplay(True)
        sc.sticky['displays'][name] = display
        return display
