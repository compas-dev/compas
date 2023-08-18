from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import Box as RhinoBox  # type: ignore
from Rhino.Geometry import Interval  # type: ignore
from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import frame_to_rhino
from .artist import RhinoArtist


def box_to_rhino_box(box):
    """Convert a COMPAS box to a Rhino box.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.

    Returns
    -------
    Rhino.Geometry.Box

    """
    return RhinoBox(
        frame_to_rhino(box.frame),
        Interval(-0.5 * box.xsize, +0.5 * box.xsize),
        Interval(-0.5 * box.ysize, +0.5 * box.ysize),
        Interval(-0.5 * box.zsize, +0.5 * box.zsize),
    )


class BoxArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`GeometryArtist`.

    """

    def __init__(self, box, **kwargs):
        super(BoxArtist, self).__init__(geometry=box, **kwargs)

    def draw(self, color=None):
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            Default is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        # color = Color.coerce(color) or self.color
        # vertices = [list(vertex) for vertex in self.shape.vertices]  # type: ignore
        # faces = self.shape.faces  # type: ignore
        # guid = compas_rhino.draw_mesh(
        #     vertices,
        #     faces,
        #     layer=self.layer,
        #     name=self.shape.name,  # type: ignore
        #     color=color.rgb255,  # type: ignore
        #     disjoint=True,
        # )
        # return [guid]

        color = Color.coerce(color) or self.color
        attr = ObjectAttributes()
        attr.ObjectColor = FromArgb(*color.rgb255)  # type: ignore
        attr.ColorSource = ColorFromObject
        guid = sc.doc.Objects.AddBox(box_to_rhino_box(self.geometry), attr)
        return [guid]
