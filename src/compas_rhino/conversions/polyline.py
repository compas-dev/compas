from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from ._primitives import polyline_to_compas
from ._primitives import polyline_to_rhino

from ._geometry import RhinoGeometry


class RhinoPolyline(RhinoGeometry):
    """Wrapper for Rhino polylines."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Polyline` | :class:`~compas.geometry.Polyline` or list of points
            The input geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a polyline.
        """
        if not isinstance(geometry, Rhino.Geometry.Polyline):
            geometry = polyline_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert the polyline to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Polyline`
            A COMPAS polyline.
        """
        return polyline_to_compas(self.geometry)
