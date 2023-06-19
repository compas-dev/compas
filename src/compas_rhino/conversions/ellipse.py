from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from ._primitives import ellipse_to_compas
from ._primitives import ellipse_to_rhino

from ._geometry import RhinoGeometry


class RhinoEllipse(RhinoGeometry):
    """Wrapper for Rhino ellipses."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Ellipse` | :class:`~compas.geometry.Ellipse`
            The geometry object defining an ellipse.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to an ellipse.
        """
        if not isinstance(geometry, Rhino.Geometry.Ellipse):
            geometry = ellipse_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Ellipse`
            A COMPAS ellipse.
        """
        return ellipse_to_compas(self.geometry)
