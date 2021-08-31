from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
from ..conversions import circle_to_compas
from ..conversions import circle_to_rhino
from ._geometry import BaseRhinoGeometry


class RhinoCircle(BaseRhinoGeometry):
    """Wrapper for a Rhino circle objects.
    """

    def __init__(self):
        super(RhinoCircle, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a circle wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Circle` or :class:`compas.geometry.Circle` or tuple of plane and radius
            The geometry object defining a circle.

        Returns
        -------
        :class:`RhinoCircle`
            The Rhino circle wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Circle):
            geometry = circle_to_rhino(geometry)
        circle = cls()
        circle.geometry = geometry
        return circle

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`Circle`
            A COMPAS circle.
        """
        return circle_to_compas(self.geometry)
