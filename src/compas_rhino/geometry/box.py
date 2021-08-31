from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
from ..conversions import box_to_compas
from ..conversions import box_to_rhino
from ._geometry import BaseRhinoGeometry


class RhinoBox(BaseRhinoGeometry):
    """Wrapper for a Rhino box objects.
    """

    def __init__(self):
        super(RhinoBox, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a box wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Box` or :class:`compas.geometry.Box`
            The geometry object defining a box.

        Returns
        -------
        :class:`RhinoBox`
            The Rhino box wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Box):
            geometry = box_to_rhino(geometry)
        box = cls()
        box.geometry = geometry
        return box

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`Box`
            A COMPAS box.
        """
        return box_to_compas(self.geometry)
