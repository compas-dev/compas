from compas.geometry import BrepEdge
from compas.geometry import Line
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas_rhino.geometry import RhinoNurbsCurve
from compas_rhino.conversions import curve_to_compas_line
# from compas_rhino.conversions import curve_to_compas_circle
# from compas_rhino.conversions import curve_to_compas_ellipse
from compas_rhino.conversions import line_to_rhino_curve
from compas_rhino.conversions import circle_to_rhino_curve
from compas_rhino.conversions import ellipse_to_rhino_curve


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
    start_vertex : :class:`~compas_rhino.geometry.RhinoBrepVertex`, read-only
        The start vertex of this edge (taken from BrepTrim).
    end_vertex : :class:`~compas_rhino.geometry.RhinoBrepVertex`, read-only
        The end vertex of this edge (taken from BrepTrim).
    vertices : list[:class:`~compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this edge (start and end)
    is_circle : bool, read-only
        True if the geometry of this edge is a circle, False otherwise.
    is_line : bool, read-only
        True if the geometry of this edge is a line, False otherwise.

    """

    def __init__(self, rhino_edge=None, builder=None):
        super(RhinoBrepEdge, self).__init__()
        self._builder = builder
        self._edge = None
        self._curve = None
        self._curve_type = None
        self._start_vertex = None
        self._end_vertex = None
        if rhino_edge:
            self._set_edge(rhino_edge)

    def _set_edge(self, rhino_edge):
        self._edge = rhino_edge
        self._curve = RhinoNurbsCurve.from_rhino(rhino_edge.EdgeCurve.ToNurbsCurve())
        self._start_vertex = RhinoBrepVertex(rhino_edge.StartVertex)
        self._end_vertex = RhinoBrepVertex(rhino_edge.EndVertex)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        curve_type, curve = self._get_curve_geometry()
        return {
            "curve_type": curve_type,
            "curve": curve.data,
            "start_vertex": self._edge.StartVertex.VertexIndex,
            "end_vertex": self._edge.EndVertex.VertexIndex
        }

    @data.setter
    def data(self, value):
        edge_curve = self._create_curve_from_data(value["curve_type"], value["curve"])
        edge = self._builder.add_edge(edge_curve, value["start_vertex"], value["end_vertex"])
        self._set_edge(edge)

    @classmethod
    def from_data(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`~compas_rhino.geometry.BrepBuilder`
            The object reconstructing the current Brep.

        Returns
        -------
        :class:`~compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        obj = cls(builder=builder)
        obj.data = data
        return obj

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
    def is_circle(self):
        return self._edge.EdgeCurve.IsCircle()

    @property
    def is_line(self):
        return self._edge.EdgeCurve.IsLinear()

    @property
    def is_ellipse(self):
        return self._edge.EdgeCurve.IsEllipse()

    def _get_curve_geometry(self):
        curve = self._edge.EdgeCurve
        if self.is_line:
            type_ = "line"
            curve = curve_to_compas_line(curve)
        # TODO: there is an edge/trim direction issue when creating and edge from circle
        # elif self.is_circle:
        #     type_ = "circle"
        #     curve = curve_to_compas_circle(curve)
        # elif self.is_ellipse:
        #     type_ = "ellipse"
        #     curve = curve_to_compas_ellipse(curve)
        else:
            type_ = "nurbs"
            curve = self._curve   
        return  type_, curve

    @staticmethod
    def _create_curve_from_data(curve_type, curve_data):       
        if curve_type == "line":
            return line_to_rhino_curve(Line.from_data(curve_data))
        elif curve_type == "circle":
            return circle_to_rhino_curve(Circle.from_data(curve_data))
        elif curve_type == "ellipse":
            return ellipse_to_rhino_curve(Ellipse.from_data(curve_data))
        else:
            return RhinoNurbsCurve.from_data(curve_data).rhino_curve
