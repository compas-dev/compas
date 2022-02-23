from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from .artist import RhinoArtist


class CylinderArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, cylinder, layer=None, **kwargs):
        super(CylinderArtist, self).__init__(shape=cylinder, layer=layer, **kwargs)

    def draw(self, color=None, u=None):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int], optional
            The RGB color of the cylinder.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`CylinderArtist.u`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = color or self.color
        u = u or self.u
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        vertices = [list(vertex) for vertex in vertices]
        guid = compas_rhino.draw_mesh(vertices,
                                      faces,
                                      layer=self.layer,
                                      name=self.shape.name,
                                      color=color,
                                      disjoint=True)
        return [guid]
