from compas.geometry import BrepEdge
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Circle
from compas_rhino.geometry import RhinoNurbsCurve
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import curve_to_compas_circle
from compas_rhino.conversions import line_to_rhino_curve
from compas_rhino.conversions import circle_to_rhino_curve

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
        self._edge = native_edge
        self._curve = self._edge.EdgeCurve
        self._start_vertex = RhinoBrepVertex(self._edge.StartVertex)
        self._end_vertex = RhinoBrepVertex(self._edge.EndVertex)

    @property
    def data(self):
        if self.is_line:
            type_ = "line"
            curve = curve_to_compas_line(self._curve)
        elif self.is_circle:
            type_ = "circle"
            curve = curve_to_compas_circle(self._curve)
        else:
            type_ = "nurbs"
            curve = RhinoNurbsCurve.from_rhino(self._curve)
        return {"type": type_, "value": curve.data, "points": [self._start_vertex.point.data, self._end_vertex.point.data]}

    @data.setter
    def data(self, value):
        curve_type = value["type"]
        if curve_type == "line":
            self._curve = line_to_rhino_curve(Line.from_data(value["value"]))  # this returns a Nurbs Curve, why?
        elif curve_type == "circle":
            self._curve = circle_to_rhino_curve(Circle.from_data(value["value"]))  # this returns a Nurbs Curve, why?
        else:
            self._curve = RhinoNurbsCurve.from_data(value["value"]).rhino_curve
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

    @property
    def vertices(self):
        return [self._start_vertex, self._end_vertex]

    @property
    def is_circle(self):
        return self._curve.IsCircle()

    @property
    def is_line(self):
        return self._curve.IsLinear()
