from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import compas_rhino

__all__ = ["Artist"]


_ITEM_ARTIST = {}


class Artist(object):
    """Base class for all ``Artist`` objects.

    Parameters
    ----------
    primitive : :class:`compas.geometry.Primitive`
        The instance of the primitive.
    settings : dict (optional)
        A dictionary with visualisation settings.

    Attributes
    ----------
    settings : dict
        Visualisation settings.

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, **settings):
        self.guids = []
        self.settings = {'layer': None}
        self.settings.update(settings)

    @property
    def layer(self):
        """str: The layer that contains the mesh."""
        return self.settings['layer']

    @layer.setter
    def layer(self, value):
        self.settings['layer'] = value

    @staticmethod
    def register(item_type, artist_type):
        _ITEM_ARTIST[item_type] = artist_type

    @staticmethod
    def build(item, **kwargs):
        artist_type = _ITEM_ARTIST[type(item)]
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        artist = artist_type(item, **kwargs)
        return artist

    # this method should be part of the scene
    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    update_scene = redraw

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def draw_dynamic(self):
        # should become a wrapper for using conduits
        raise NotImplementedError

    def draw_animation(self):
        raise NotImplementedError

    def clear(self):
        if not self.guids:
            return
        compas_rhino.delete_objects(self.guids)

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.settings['layer']:
            compas_rhino.clear_layer(self.settings['layer'])
        else:
            compas_rhino.clear_current_layer()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
