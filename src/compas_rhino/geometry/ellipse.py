from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
from ..conversions import ellipse_to_compas
from ..conversions import ellipse_to_rhino
from ._geometry import BaseRhinoGeometry


class RhinoEllipse(BaseRhinoGeometry):
    """Wrapper for Rhino ellipse objects.
    """

    def __init__(self):
        super(RhinoEllipse, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct an ellipse wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Ellipse` or :class:`compas.geometry.Ellipse`
            The geometry object defining an ellipse.

        Returns
        -------
        :class:`RhinoEllipse`
            The Rhino ellipse wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Ellipse):
            geometry = ellipse_to_rhino(geometry)
        plane = cls()
        plane.geometry = geometry
        return plane

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Ellipse`
            A COMPAS ellipse.
        """
        return ellipse_to_compas(self.geometry)
