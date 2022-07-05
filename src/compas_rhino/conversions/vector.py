from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino

from ._primitives import vector_to_rhino
from ._primitives import vector_to_compas

from ._geometry import RhinoGeometry


class RhinoVector(RhinoGeometry):
    """Wrapper for Rhino vectors."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Vector3d` | :class:`~compas.geometry.Vector` or list of float
            The input geometry.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a vector.
        """
        if not isinstance(geometry, Rhino.Geometry.Vector3d):
            geometry = vector_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert the wrapper to a COMPAS object.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            A COMPAS vector.
        """
        return vector_to_compas(self.geometry)
