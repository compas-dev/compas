from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from itertools import zip_longest

import compas_rhino
# from compas.utilities import like_list
from compas_rhino.artists import _ShapeArtist


__all__ = ['BoxArtist']


def list_like(target, value, fillvalue=None):
    p = len(target)

    if isinstance(value, list):
        matched_list = value
    else:
        matched_list = [value] * p

    d = len(matched_list)
    if d < p:
        matched_list.extend([fillvalue] * (p - d))

    return matched_list


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
