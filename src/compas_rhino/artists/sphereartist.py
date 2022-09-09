from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import RhinoArtist


class SphereArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.
    layer : str, optional
        The layer that should contain the drawing.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, sphere, layer=None, **kwargs):
        super(SphereArtist, self).__init__(shape=sphere, layer=layer, **kwargs)

    def draw(self, color=None, u=None, v=None):
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the sphere.
            Default is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`SphereArtist.u`.
        v : int, optional
            Number of faces in the "v" direction.
            Default is :attr:`SphereArtist.v`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        vertices = [list(vertex) for vertex in vertices]
        guid = compas_rhino.draw_mesh(
            vertices,
            faces,
            layer=self.layer,
            name=self.shape.name,
            color=color.rgb255,
            disjoint=True,
        )
        return [guid]
