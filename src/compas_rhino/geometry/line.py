from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas_rhino.conversions import line_to_compas
from compas_rhino.conversions import line_to_rhino

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
        geometry : :rhino:`Rhino_Geometry_Line` or :class:`compas.geometry.Line`
            The input geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a line.
        """
        if not isinstance(geometry, Rhino.Geometry.Line):
            geometry = line_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert the line to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Line`
            A COMPAS line.
        """
        return line_to_compas(self.geometry)
