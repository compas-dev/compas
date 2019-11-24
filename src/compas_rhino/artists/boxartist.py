from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.artists import _ShapeArtist


__all__ = ['BoxArtist']


class BoxArtist(_ShapeArtist):
    """Artist for drawing ``Box`` objects.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    layer : str (optional)
        The name of the layer that will contain the box.
        Default value is ``None``, in which case the current layer will be used.

    Examples
    --------
    >>>

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, box, layer=None):
        super(BoxArtist, self).__init__(box, layer=layer)
        self.settings.update({
            'color.box': (0, 0, 0)})

    def draw(self):
        """Draw the box.

        Returns
        -------
        guids: list of str
            The GUIDs of the created Rhino objects.

        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
