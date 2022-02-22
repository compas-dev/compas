from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from ._primitives import line_to_compas
from ._primitives import line_to_rhino

from ._curves import curve_to_compas_line

from ._geometry import RhinoGeometry


class RhinoLine(RhinoGeometry):
    """Wrapper for Rhino lines."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Line` | :class:`~compas.geometry.Line`
            The input geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a line.
        """
        if not isinstance(geometry, Rhino.Geometry.Line):
            if isinstance(geometry, Rhino.Geometry.Curve):
                geometry = curve_to_compas_line(geometry)
            geometry = line_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert the line to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Line`
            A COMPAS line.
        """
        return line_to_compas(self.geometry)
