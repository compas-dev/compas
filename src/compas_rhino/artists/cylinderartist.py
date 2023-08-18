from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import Cylinder as RhinoCylinder  # type: ignore
from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import circle_to_rhino
from .artist import RhinoArtist


def cylinder_to_rhino_cylinder(cylinder):
    """Convert a COMPAS cylinder to a Rhino cylinder.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.

    Returns
    -------
    Rhino.Geometry.Cylinder

    """
    circle = cylinder.circle
    circle.frame.point = circle.frame.point - circle.frame.zaxis * cylinder.height * 0.5
    return RhinoCylinder(circle_to_rhino(circle), cylinder.height)


def cylinder_to_rhino_brep(cylinder):
    """Convert a COMPAS cylinder to a Rhino Brep.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.

    Returns
    -------
    Rhino.Geometry.Brep

    """
    return RhinoCylinder.ToBrep(cylinder_to_rhino_cylinder(cylinder), True, True)


class CylinderArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`ShapeArtist`.

    """

    def __init__(self, cylinder, **kwargs):
        super(CylinderArtist, self).__init__(geometry=cylinder, **kwargs)

    def draw(self, color=None):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cylinder.
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
        guid = sc.doc.Objects.AddBrep(cylinder_to_rhino_brep(self.geometry), attr)
        return [guid]
