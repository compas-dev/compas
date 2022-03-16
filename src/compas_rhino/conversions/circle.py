from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from ._primitives import circle_to_compas
from ._primitives import circle_to_rhino

from ._geometry import RhinoGeometry


class RhinoCircle(RhinoGeometry):
    """Wrapper for Rhino circles."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Circle` | :class:`~compas.geometry.Circle`
            The geometry object defining a circle.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a box.
        """
        if not isinstance(geometry, Rhino.Geometry.Circle):
            geometry = circle_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Circle`
            A COMPAS circle.
        """
        return circle_to_compas(self.geometry)
