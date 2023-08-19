from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import Torus as RhinoTorus  # type: ignore
from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import frame_to_rhino
from .artist import RhinoArtist


def torus_to_rhino(torus):
    """Convert a COMPAS torus to a Rhino torus.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.

    Returns
    -------
    tuple
        The Rhino torus representation.

    """
    return RhinoTorus(frame_to_rhino(torus.frame), torus.radius_axis, torus.radius_pipe)


def torus_to_rhino_brep(torus):
    """Convert a COMPAS torus to a Rhino Brep.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.

    Returns
    -------
    Rhino.Geometry.Brep
        The Rhino brep representation.

    """
    return torus_to_rhino(torus).ToNurbsSurface().ToBrep()


class TorusArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, torus, **kwargs):
        super(TorusArtist, self).__init__(geometry=torus, **kwargs)

    def draw(self, color=None):
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.
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

        brep = torus_to_rhino_brep(self.geometry)

        guid = sc.doc.Objects.AddBrep(brep, attr)
        return [guid]
