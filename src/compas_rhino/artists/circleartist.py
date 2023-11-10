from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import circle_to_rhino

# from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class CircleArtist(RhinoArtist, GeometryObject):
    """Artist for drawing circles.

    Parameters
    ----------
    circle : :class:`~compas.geometry.Circle`
        A COMPAS circle.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, circle, **kwargs):
        super(CircleArtist, self).__init__(geometry=circle, **kwargs)

    def draw(self, color=None):
        """Draw the circle.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the circle.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = circle_to_rhino(self.geometry)

        if self.transformation:
            geometry.Transform(transformation_to_rhino(self.transformation))

        return sc.doc.Objects.AddCircle(geometry, attr)
