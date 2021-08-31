from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
from compas.geometry import Frame
from ..conversions import plane_to_rhino
from ..conversions import frame_to_rhino
from ..conversions import plane_to_compas
from ..conversions import plane_to_compas_frame
from ._geometry import BaseRhinoGeometry


class RhinoPlane(BaseRhinoGeometry):
    """Wrapper for a Rhino plane objects.

    Notes
    -----
    In Rhino, a plane and a frame are equivalent.
    Therefore, the COMPAS conversion function of this class returns a frame object instead of a plane.
    """

    def __init__(self):
        super(RhinoPlane, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a plane wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Plane` or :class:`compas.geometry.Frame` or tuple of point and normal
            The geometry object defining a plane.

        Returns
        -------
        :class:`RhinoPlane`
            The Rhino plane wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Plane):
            if isinstance(geometry, Frame):
                geometry = frame_to_rhino(geometry)
            else:
                geometry = plane_to_rhino(geometry)
        plane = cls()
        plane.geometry = geometry
        return plane

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`Frame`
            A COMPAS frame.
        """
        return plane_to_compas(self.geometry)

    def to_compas_frame(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`Frame`
            A COMPAS frame.
        """
        return plane_to_compas_frame(self.geometry)
