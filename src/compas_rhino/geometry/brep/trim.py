from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import BrepTrim
from compas_rhino.geometry import RhinoNurbsCurve

from .vertex import RhinoBrepVertex


class RhinoBrepTrim(BrepTrim):
    """Trims hold topological information about how the edges of a Brep face are are organized.

    Attributes
    ----------
    curve : :class:`compas.geometry.NurbsCurve`, read_only
        Returns the geometry for this trim as a 2d curve.
    iso_status : literal(NONE|X|Y|West|South|East|North)
        The isoparametric curve direction on the surface.
    is_reversed : bool
        True if this trim is reversed from its associated edge curve and False otherwise.
    native_trim : :class:`Rhino.Geometry.BrepTrim`
        The underlying Rhino BrepTrim object.
    start_vertex : :class:`compas_rhino.geometry.RhinoBrepVertex`, read-only
        The start vertex of this trim.
    end_vertex : :class:`compas_rhino.geometry.RhinoBrepVertex`, read-only
        The end vertex of this trim.
    vertices : list[:class:`compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this trim (start and end).

    """

    def __init__(self, rhino_trim=None):
        super(RhinoBrepTrim, self).__init__()
        self._trim = None
        self._curve = None
        self._is_reversed = None
        self._iso_type = None
        self._start_vertex = None
        self._end_vertex = None
        if rhino_trim:
            self.native_trim = rhino_trim

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        return {
            "start_vertex": self._trim.StartVertex.VertexIndex,
            "end_vertex": self._trim.EndVertex.VertexIndex,
            "edge": self._trim.Edge.EdgeIndex if self._trim.Edge else -1,  # singular trims have no associated edge
            "curve": RhinoNurbsCurve.from_rhino(self._trim.TrimCurve.ToNurbsCurve()).__data__,
            "iso": str(self._trim.IsoStatus),
            "is_reversed": "true" if self._trim.IsReversed() else "false",
        }

    @classmethod
    def __from_data__(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`compas_rhino.geometry.BrepLoopBuilder`
            The object reconstructing the current BrepLoop.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        instance = cls()
        curve = RhinoNurbsCurve.__from_data__(data["curve"]).rhino_curve
        iso_status = getattr(Rhino.Geometry.IsoStatus, data["iso"])
        is_reversed = True if data["is_reversed"] == "true" else False
        instance.native_trim = builder.add_trim(curve, data["edge"], is_reversed, iso_status, data["start_vertex"])
        return instance

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def curve(self):
        return self._curve

    @property
    def start_vertex(self):
        return self._start_vertex

    @property
    def end_vertex(self):
        return self._end_vertex

    @property
    def vertices(self):
        return [self.start_vertex, self.end_vertex]

    @property
    def is_reverse(self):
        return self._curve

    @property
    def iso_status(self):
        return self._iso_type

    @property
    def native_trim(self):
        return self._trim

    @native_trim.setter
    def native_trim(self, rhino_trim):
        self._trim = rhino_trim
        self._curve = RhinoNurbsCurve.from_rhino(rhino_trim.TrimCurve.ToNurbsCurve())
        self._is_reversed = rhino_trim.IsReversed()
        self._iso_type = int(rhino_trim.IsoStatus)
        self._start_vertex = RhinoBrepVertex(rhino_trim.StartVertex)
        self._end_vertex = RhinoBrepVertex(rhino_trim.EndVertex)
