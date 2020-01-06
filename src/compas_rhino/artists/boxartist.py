from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist


__all__ = ['BoxArtist']


class BoxArtist(MeshArtist):
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

    def __init__(self, box, **kwargs):
        super(BoxArtist, self).__init__(None, **kwargs)
        self._box = None
        self.box = box
        self.settings.update({
            'color.vertices': (0, 0, 0),
            'color.edges': (255, 0, 0),
            'color.faces': (255, 200, 200)})

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, box):
        self._box = box
        self.datastructure = Mesh.from_shape(box)

    def draw(self):
        self.draw_vertices()
        self.draw_faces()
        self.draw_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # import time
    from compas.geometry import Box

    box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 1.0)

    artist = BoxArtist(box)

    artist.draw()
