from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.geometry import Point
from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class VectorArtist(RhinoArtist, GeometryObject):
    """Artist for drawing vectors.

    Parameters
    ----------
    vector : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, vector, **kwargs):
        super(VectorArtist, self).__init__(geometry=vector, **kwargs)

    def draw(self, color=None, point=None):
        """Draw the vector.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the vector.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer, arrow="end")

        point = point or [0, 0, 0]
        start = Point(*point)
        end = start + self.geometry

        return sc.doc.Objects.AddLine(point_to_rhino(start), point_to_rhino(end), attr)
