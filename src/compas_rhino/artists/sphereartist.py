from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.Geometry import Sphere as RhinoSphere  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import frame_to_rhino
from .artist import RhinoArtist


def sphere_to_rhino(sphere):
    """Convert a COMPAS sphere to a Rhino sphere.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.

    Returns
    -------
    Rhino.Geometry.Sphere

    """
    return RhinoSphere(frame_to_rhino(sphere.frame), sphere.radius)


class SphereArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, sphere, **kwargs):
        super(SphereArtist, self).__init__(geometry=sphere, **kwargs)

    def draw(self, color=None):
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the sphere.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        # color = Color.coerce(color) or self.color
        # u = u or self.u
        # v = v or self.v
        # vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        # vertices = [list(vertex) for vertex in vertices]
        # guid = compas_rhino.draw_mesh(
        #     vertices,
        #     faces,
        #     layer=self.layer,
        #     name=self.shape.name,
        #     color=color.rgb255,
        #     disjoint=True,
        # )
        # return [guid]

        color = Color.coerce(color) or self.color
        color = FromArgb(*color.rgb255)  # type: ignore

        attr = ObjectAttributes()
        attr.ObjectColor = color
        attr.ColorSource = ColorFromObject

        guid = sc.doc.Objects.AddSphere(sphere_to_rhino(self.geometry), attr)
        return [guid]
