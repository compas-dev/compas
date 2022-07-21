from compas.data import Data
from compas.geometry import BrepEdge
from compas.geometry import Line
from compas.geometry import Point
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import line_to_rhino_curve
from compas_rhino.conversions import point_to_rhino

import Rhino

from .vertex import RhinoBrepVertex


class RhinoBrepEdge(BrepEdge):

    def __init__(self, rhino_edge=None):
        super(RhinoBrepEdge, self).__init__()
        self._edge = None
        self._curve = None
        self._start_vertex = None
        self._end_vertex = None
        if rhino_edge:
            self._set_edge(rhino_edge)

    def _set_edge(self, native_edge):
        # TODO: need to check what kind of Curve this is LineCurve/NURBSCurve etc.
        # TODO: maybe this check belongs in compas_rhino.conversions.RhinoCurve which does this check compas=>rhino
        self._edge = native_edge
        self._curve = curve_to_compas_line(self._edge.EdgeCurve)
        self._start_vertex = RhinoBrepVertex(self._edge.StartVertex)
        self._end_vertex = RhinoBrepVertex(self._edge.EndVertex)

    @property
    def data(self):
        # TODO: determine the actual type of the underlying geometry
        type_ = "line"
        return {"type": type_, "value": self._curve.data, "points": [self._start_vertex.point.data, self._end_vertex.point.data]}

    @data.setter
    def data(self, value):
        self._curve = Line.from_data(value["value"])

        # TODO: can a single edge be defined with more than start and end vertices?
        self._start_vertex, self._end_vertex = RhinoBrepVertex(), RhinoBrepVertex()
        self._start_vertex._point = Point.from_data(value["points"][0])
        self._end_vertex._point = Point.from_data(value["points"][1])

    @property
    def curve(self):
        return self._curve

    @property
    def start_vertex(self):
        return self._start_vertex

    @property
    def end_vertex(self):
        return self._end_vertex

    def to_curve(self):
        """
        Returns a Rhino.Geometry.LineCurve for this edge
        Returns
        -------

        """
        start = point_to_rhino(self._start_vertex.point)
        end = point_to_rhino(self._end_vertex.point)
        line_curve = Rhino.Geometry.LineCurve(start, end)  # TODO: doesn't have to be a Line, determine actual geometry
        line_curve.Domain = Rhino.Geometry.Interval(0.0, 1.0)  # not sure what this is about, copied from example code
        return line_curve

    @property
    def vertices(self):
        return [self._start_vertex, self._end_vertex]
