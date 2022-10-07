from compas.geometry import BrepTrim, Point
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Line
from compas_rhino.conversions import circle_to_rhino_curve
from compas_rhino.conversions import curve_to_compas_circle
from compas_rhino.conversions import curve_to_compas_ellipse
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import ellipse_to_rhino_curve
from compas_rhino.conversions import line_to_rhino_curve
from compas_rhino.conversions import point_to_compas
from compas_rhino.geometry import RhinoNurbsCurve

from .vertex import RhinoBrepVertex
from .edge import RhinoBrepEdge


class RhinoBrepTrim(BrepTrim):

    def __init__(self, native_trim=None):
        super(RhinoBrepTrim, self).__init__()
        self._start_vertex = None
        self._end_vertex = None
        self._point_at_start = None
        self._point_at_end = None
        self._trim_curve = None
        self._edge = None

        if native_trim:
            self._set_trim(native_trim)

    def _set_trim(self, native_trim):
        self._start_vertex = RhinoBrepVertex(native_trim.StartVertex)
        self._end_vertex = RhinoBrepVertex(native_trim.EndVertex)
        self._point_at_start = point_to_compas(native_trim.PointAtStart)
        self._point_at_end = point_to_compas(native_trim.PointAtEnd)
        self._trim_curve = native_trim.TrimCurve
        self._edge = RhinoBrepEdge(native_trim.Edge)
        self._trim = native_trim

    @property
    def data(self):
        if self.is_line:
            type_ = "line"
            curve = curve_to_compas_line(self._trim_curve)
        elif self.is_circle:
            type_ = "circle"
            curve = curve_to_compas_circle(self._trim_curve)
        elif self.is_ellipse:
            type_ = "ellipse"
            curve = curve_to_compas_ellipse(self._trim_curve)
        else:
            type_ = "nurbs"
            curve = RhinoNurbsCurve.from_rhino(self._trim_curve)
        return {
            "type": type_,
            "value": curve.data,
            "vertices": [self.start_vertex.point.data, self.end_vertex.point.data],
            "points": [self.point_at_start.data, self.point_at_end.data],
            "edge": self._edge.data
        }

    @data.setter
    def data(self, value):
        curve_type = value["type"]
        if curve_type == "line":
            self._trim_curve = line_to_rhino_curve(Line.from_data(value["value"]))  # this returns a Nurbs Curve, why?
        elif curve_type == "circle":
            self._trim_curve = circle_to_rhino_curve(Circle.from_data(value["value"]))  # this returns a Nurbs Curve, why?
        elif curve_type == "ellipse":
            self._trim_curve = ellipse_to_rhino_curve(Ellipse.from_data(value["value"]))
        else:
            self._trim_curve = RhinoNurbsCurve.from_data(value["value"]).rhino_curve
        self._edge = RhinoBrepEdge.from_data(value["edge"])
        self._start_vertex = RhinoBrepVertex()
        self._end_vertex = RhinoBrepVertex()
        self._start_vertex._point = Point.from_data(value["vertices"][0])
        self._end_vertex._point = Point.from_data(value["vertices"][1])
        self._point_at_start = Point.from_data(value["points"][0])
        self._point_at_end = Point.from_data(value["points"][1])

    @property
    def edge(self):
        return self._edge

    @property
    def curve(self):
        return self._trim_curve

    @property
    def start_vertex(self):
        return self._start_vertex

    @property
    def end_vertex(self):
        return self._end_vertex

    @property
    def point_at_start(self):
        return self._point_at_start

    @property
    def point_at_end(self):
        return self._point_at_end

    @property
    def is_circle(self):
        return self._trim.IsCircle()

    @property
    def is_line(self):
        return self._trim.IsLinear()

    @property
    def is_ellipse(self):
        return self._trim.IsEllipse()


