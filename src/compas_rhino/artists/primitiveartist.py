from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

__all__ = ['PrimitiveArtist']


class PrimitiveArtist(object):
    """Base class for all `Primitive` artists.

    Parameters
    ----------
    primitive : compas.geometry.primitives.Primitive
        The instnce of the primitive.
    settings : dict (optional)
        A dictionary with visualisation settings.
        Note that visualisation settings may also be provided
        one-by-one as keyword arguments.

    Attributes
    ----------
    settings : dict
        Visualisation settings.

    """

    def __init__(self, primitive, settings=None, **kwargs):
        self.primitive = primitive
        self.settings = settings or {}
        self.settings.update(kwargs)

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError

    def draw_dynamic(self):
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
