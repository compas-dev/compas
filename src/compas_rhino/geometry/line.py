from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from ..conversions import line_to_compas
from ..conversions import line_to_rhino
from ._geometry import BaseRhinoGeometry


class RhinoLine(BaseRhinoGeometry):
    """Wrapper for a Rhino line objects.
    """

    def __init__(self):
        super(RhinoLine, self).__init__()

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a line from an existing Rhino line geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Line` or :class:`Line` or tuple of two points
            The input geometry.

        Returns
        -------

        """
        if not isinstance(geometry, Rhino.Geometry.Line):
            geometry = line_to_rhino(geometry)
        line = cls()
        line.geometry = geometry
        return line

    @classmethod
    def from_selection(cls):
        """Construct a line wrapper by selecting an existing Rhino line object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoLine`
            The Rhino line wrapper.
        """
        guid = compas_rhino.select_line()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the line to a COMPAS geometry object.

        Returns
        -------
        :class:`Line`
            A COMPAS line.
        """
        return line_to_compas(self.geometry)
