from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import Arc
from compas.geometry import BrepEdge
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Frame
from compas.geometry import Line
from compas_rhino.conversions import arc_to_compas
from compas_rhino.conversions import arc_to_rhino
from compas_rhino.conversions import circle_to_compas
from compas_rhino.conversions import circle_to_rhino
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import ellipse_to_compas
from compas_rhino.conversions import ellipse_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import point_to_compas
from compas_rhino.geometry import RhinoNurbsCurve

from .vertex import RhinoBrepVertex


class RhinoBrepEdge(BrepEdge):
    """A wrapper for Rhino.Geometry.BrepEdge.

    The expected native type here is a Rhino.Geometry.BrepTrim.
    a BrepTrim holds a reference to its associated BrepEdge as well as its start a end vertices
    in a correct topological order (!).

    Attributes
    ----------
    curve : :class:`Rhino.Geometry.Curve3D`
        The underlying geometry of this edge.
    start_vertex : :class:`compas_rhino.geometry.RhinoBrepVertex`, read-only
        The start vertex of this edge (taken from BrepTrim).
    end_vertex : :class:`compas_rhino.geometry.RhinoBrepVertex`, read-only
        The end vertex of this edge (taken from BrepTrim).
    vertices : list[:class:`compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this edge (start and end)
    is_circle : bool, read-only
        True if the geometry of this edge is a circle, False otherwise.
    is_line : bool, read-only
        True if the geometry of this edge is a line, False otherwise.
    native_edge : :class:`Rhino.Geometry.BrepEdge`
        The underlying BrepEdge object.

    """

    def __init__(self, rhino_edge=None):
        super(RhinoBrepEdge, self).__init__()
        self._edge = None
        self._curve = None
        self._curve_type = None
        self._start_vertex = None
        self._end_vertex = None
        self._mass_props = None
        if rhino_edge:
            self.native_edge = rhino_edge

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        curve_type, curve, plane, domain = self._get_curve_geometry()
        return {
            "curve_type": curve_type,
            "curve": curve.__data__,
            "frame": plane_to_compas_frame(plane).__data__,
            "start_vertex": self._edge.StartVertex.VertexIndex,
            "end_vertex": self._edge.EndVertex.VertexIndex,
            "domain": domain,
        }

    @classmethod
    def __from_data__(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`compas_rhino.geometry.BrepBuilder`
            The object reconstructing the current Brep.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        instance = cls()
        edge_curve = cls._create_curve__from_data__(data["curve_type"], data["curve"], data["frame"], data["domain"])
        instance.native_edge = builder.add_edge(edge_curve, data["start_vertex"], data["end_vertex"])
        return instance

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def centroid(self):
        return point_to_compas(self._mass_props.Centroid)

    @property
    def curve(self):
        return self._curve

    @property
    def native_edge(self):
        return self._edge

    @native_edge.setter
    def native_edge(self, value):
        self._edge = value
        self._mass_props = Rhino.Geometry.LengthMassProperties.Compute(value.EdgeCurve)
        self._curve = RhinoNurbsCurve.from_rhino(value.EdgeCurve.ToNurbsCurve())
        self._start_vertex = RhinoBrepVertex(value.StartVertex)
        self._end_vertex = RhinoBrepVertex(value.EndVertex)

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
    def is_circle(self):
        return self._edge.EdgeCurve.IsCircle()

    @property
    def is_line(self):
        return self._edge.EdgeCurve.IsLinear()

    @property
    def is_ellipse(self):
        return self._edge.EdgeCurve.IsEllipse()

    @property
    def length(self):
        return self._mass_props.Length

    # ==============================================================================
    # Methods
    # ==============================================================================

    def _get_curve_geometry(self):
        curve = self._edge.EdgeCurve
        domain = [self._edge.Domain[0], self._edge.Domain[1]]
        _, frame = curve.FrameAt(0)
        if isinstance(curve, Rhino.Geometry.LineCurve):
            return "line", curve_to_compas_line(curve), frame, domain
        if isinstance(curve, Rhino.Geometry.NurbsCurve):
            return "nurbs", RhinoNurbsCurve.from_rhino(curve), frame, domain
        if isinstance(curve, Rhino.Geometry.ArcCurve):
            if not curve.IsClosed:
                return "arc", arc_to_compas(curve.Arc), curve.Arc.Plane, domain
            is_circle, circle = curve.TryGetCircle()
            if is_circle:
                return "circle", circle_to_compas(circle), circle.Plane, domain
            is_ellipse, ellipse = curve.TryGetEllipse()
            if is_ellipse:
                return "ellipse", ellipse_to_compas(ellipse), ellipse.Plane, domain
            return "nurbs", curve.ToNurbsCurve(), frame, domain
        raise ValueError("Unknown curve type: {}".format(curve.__class__.__name__))

    @staticmethod
    def _create_curve__from_data__(curve_type, curve_data, frame_data, domain):
        frame = Frame.__from_data__(frame_data)
        if curve_type == "line":
            line = Line.__from_data__(curve_data)
            curve = Rhino.Geometry.LineCurve(line_to_rhino(line))
        elif curve_type == "circle":
            circle = circle_to_rhino(Circle.__from_data__(curve_data))
            circle.Plane = frame_to_rhino_plane(frame)
            curve = Rhino.Geometry.ArcCurve(circle)
        elif curve_type == "ellipse":
            ellipse = ellipse_to_rhino(Ellipse.__from_data__(curve_data))
            ellipse.Plane = frame_to_rhino_plane(frame)
            curve = Rhino.Geometry.NurbsCurve.CreateFromEllipse(ellipse)
        elif curve_type == "arc":
            arc = arc_to_rhino(Arc.__from_data__(curve_data))
            curve = Rhino.Geometry.ArcCurve(arc)
        elif curve_type == "nurbs":
            curve = RhinoNurbsCurve.__from_data__(curve_data).rhino_curve
        else:
            raise ValueError("Unknown curve type: {}".format(curve_type))
        curve.Domain = Rhino.Geometry.Interval(*domain)
        return curve
