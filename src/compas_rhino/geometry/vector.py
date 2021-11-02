from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from ..conversions import vector_to_rhino
from ..conversions import vector_to_compas
from ._geometry import RhinoGeometry


class RhinoVector(RhinoGeometry):
    """Wrapper for Rhino vectors.
    """

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a vector wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Vector3d` or :class:`compas.geometry.Vector` or list of float
            The input geometry.

        Returns
        -------
        :class:`RhinoVector`
            The Rhino vector wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Vector3d):
            geometry = vector_to_rhino(geometry)
        vector = cls()
        vector.geometry = geometry
        return vector

    def to_compas(self):
        """Convert the wrapper to a COMPAS object.

        Returns
        -------
        :class:`compas.geometry.Vector`
            A COMPAS vector.
        """
        return vector_to_compas(self.geometry)
