from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

__all__ = ["_Artist"]


class _Artist(object):
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

    def __init__(self, settings):
        self.settings = {'layer': None}
        self.settings.update(settings)

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError

    def draw_dynamic(self):
        # should become a wrapper for using conduits
        raise NotImplementedError

    def draw_animation(self):
        raise NotImplementedError

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
