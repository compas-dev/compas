from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from ..conversions import polyline_to_compas
from ..conversions import polyline_to_rhino
from ._geometry import BaseRhinoGeometry


class RhinoPolyline(BaseRhinoGeometry):
    """Wrapper for Rhino polyline objects.
    """

    def __init__(self):
        super(RhinoPolyline, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a line from an existing Rhino polyline geometry object.
s
        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Polyline` or :class:`compas.geometry.Polyline` or list of points
            The input geometry.

        Returns
        -------
        :class:`RhinoPolyline`
        """
        if not isinstance(geometry, Rhino.Geometry.Polyline):
            geometry = polyline_to_rhino(geometry)
        polyline = cls()
        polyline.geometry = geometry
        return polyline

    @classmethod
    def from_selection(cls):
        """Construct a polyline wrapper by selecting an existing Rhino polyline object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`RhinoPolyline`
            The Rhino polyline wrapper.
        """
        guid = compas_rhino.select_polyline()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the polyline to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Polyline`
            A COMPAS polyline.
        """
        return polyline_to_compas(self.geometry)
