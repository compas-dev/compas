from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

import compas_rhino
from compas.geometry import Line

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoLine']


class RhinoLine(BaseRhinoGeometry):
    """Wrapper for a Rhino line objects.

    Attributes
    ----------
    start (read-only) : Rhino.Geometry.Point3d
        The starting point of the line.
    end (read-only) : Rhino.Geometry.Point3d
        The end point of the line.
    """

    def __init__(self):
        super(RhinoLine, self).__init__()

    @property
    def start(self):
        return self.geometry.From

    @property
    def end(self):
        return self.geometry.To

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a line from an existing Rhino line geometry object.

        Parameters
        ----------
        geometry : two points or :class:`Rhino.Geometry.Line`
            The input geometry.

        Returns
        -------

        """
        if not isinstance(geometry, Rhino.Geometry.Line):
            start = Rhino.Geometry.Point3d(* geometry[0])
            end = Rhino.Geometry.Point3d(* geometry[1])
            geometry = Rhino.Geometry.Line(start, end)
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
            The wrapped line.
        """
        guid = compas_rhino.select_line()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the line to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Line`
            The equivalent COMPAS geometry line.
        """
        return Line(self.start, self.end)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
