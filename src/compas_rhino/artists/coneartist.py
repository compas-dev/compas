from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import Cone as RhinoCone  # type: ignore
from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas.geometry import Frame
from compas_rhino.conversions import frame_to_rhino
from .artist import RhinoArtist


def cone_to_rhino_cone(cone):
    """Convert a COMPAS cone to a Rhino cone.

    Parameters
    ----------
    cone : :class:`~compas.geometry.Cone`
        A COMPAS cone.

    Returns
    -------
    Rhino.Geometry.Cone

    """
    frame = Frame(cone.frame.point + cone.frame.zaxis * cone.height, cone.frame.xaxis, cone.frame.yaxis)
    return RhinoCone(frame_to_rhino(frame), -cone.height, cone.radius)


def cone_to_rhino_brep(cone):
    """Convert a COMPAS cone to a Rhino Brep.

    Parameters
    ----------
    cone : :class:`~compas.geometry.Cone`
        A COMPAS cone.

    Returns
    -------
    Rhino.Geometry.Brep

    """
    return RhinoCone.ToBrep(cone_to_rhino_cone(cone), True)


class ConeArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`~compas.geometry.Cone`
        A COMPAS cone.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, cone, **kwargs):
        super(ConeArtist, self).__init__(geometry=cone, **kwargs)

    def draw(self, color=None):
        """Draw the cone associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cone.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        # color = Color.coerce(color) or self.color
        # u = u or self.u
        # vertices, faces = self.shape.to_vertices_and_faces(u=u)
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
        guid = sc.doc.Objects.AddBrep(cone_to_rhino_brep(self.geometry), attr)
        return [guid]
