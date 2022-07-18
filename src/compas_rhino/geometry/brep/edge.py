from compas.data import Data
from compas.geometry import BrepEdge
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import line_to_rhino_curve


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
        # TODO: need to check what kind of Curve this is LineCurve/NURBSCurve etc.
        # TODO: maybe this check belongs in compas_rhino.conversions.RhinoCurve which does this check compas=>rhino
        self._curve = curve_to_compas_line(self._edge.EdgeCurve)
        self._start_vertex = RhinoBrepVertex(self._edge.StartVertex)
        self._end_vertex = RhinoBrepVertex(self._edge.EndVertex)

    @property
    def data(self):
        return {"type": "nurbs", "value": self._curve.data, "points": [self._start_vertex.point, self._end_vertex.point]}
