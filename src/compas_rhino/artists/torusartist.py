from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from .artist import RhinoArtist


class TorusArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        A COMPAS torus.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, torus, layer=None, **kwargs):
        super(TorusArtist, self).__init__(shape=torus, layer=layer, **kwargs)

    def draw(self, color=None, u=None, v=None):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the torus.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~TorusArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~TorusArtist.v``.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        color = color or self.color
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        guid = compas_rhino.draw_mesh(vertices,
                                      faces,
                                      layer=self.layer,
                                      name=self.shape.name,
                                      color=color,
                                      disjoint=True)
        return [guid]
