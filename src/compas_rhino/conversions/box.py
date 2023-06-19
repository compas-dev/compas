from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino

from compas.geometry import Box

from ._exceptions import ConversionError
from ._geometry import RhinoGeometry
from ._shapes import box_to_compas
from ._shapes import box_to_rhino


class RhinoBox(RhinoGeometry):
    """Wrapper for Rhino boxes."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Box` | :class:`~compas.geometry.Box`
            The geometry object defining a box.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a box.
        """
        if not isinstance(geometry, Rhino.Geometry.Box):
            if isinstance(geometry, Rhino.Geometry.Extrusion):
                plane = geometry.GetPathPlane(0)
                box = geometry.GetBoundingBox(plane)
                geometry = Rhino.Geometry.Box(plane, box)
            elif isinstance(geometry, Box):
                geometry = box_to_rhino(geometry)
            else:
                raise ConversionError("Geometry object cannot be converted to a box: {}".format(geometry))

        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Box`
            A COMPAS box.
        """
        return box_to_compas(self.geometry)
