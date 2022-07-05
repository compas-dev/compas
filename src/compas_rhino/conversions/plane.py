from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Frame
from ._primitives import plane_to_rhino
from ._primitives import frame_to_rhino
from ._primitives import plane_to_compas
from ._primitives import plane_to_compas_frame

from ._geometry import RhinoGeometry


class RhinoPlane(RhinoGeometry):
    """Wrapper for Rhino planes."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Plane` | :class:`~compas.geometry.Plane` | :class:`~compas.geometry.Frame`
            The geometry object defining a plane.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a plane.

        """
        if not isinstance(geometry, Rhino.Geometry.Plane):
            if isinstance(geometry, Frame):
                geometry = frame_to_rhino(geometry)
            else:
                geometry = plane_to_rhino(geometry)
        self._geometry = geometry

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            A COMPAS plane.
        """
        return plane_to_compas(self.geometry)

    def to_compas_frame(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            A COMPAS frame.
        """
        return plane_to_compas_frame(self.geometry)
