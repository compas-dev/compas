from compas.data import Data
from compas_rhino.conversions import curve_to_compas_line
from compas_rhino.conversions import line_to_rhino_curve


from .vertex import RhinoBRepVertex

class RhinoBRepEdge(Data):
    def __init__(self, rhino_edge=None):
        super(RhinoBRepEdge, self).__init__()
        self._rhino_edge = None
        self._curve = None
        self._start_vertex = None
        self._end_vertex = None

        if rhino_edge:
            self.rhino_edge = rhino_edge

    @property
    def rhino_edge(self):
        return self._rhino_edge

    @rhino_edge.setter
    def rhino_edge(self, value):
        self._rhino_edge = value
        # TODO: need to check what kind of Curve this is LineCurve/NURBSCurve etc.
        # TODO: maybe this check belongs in compas_rhino.conversions.RhinoCurve which does this check compas=>rhino
        self._curve = curve_to_compas_line(self._rhino_edge.EdgeCurve)
        self._start_vertex = RhinoBRepVertex(self._rhino_edge.StartVertex)
        self._end_vertex = RhinoBRepVertex(self._rhino_edge.EndVertex)

    @property
    def data(self):
        return {
            "type": "nurbs",
            "value": self._curve.data,
            "points": [self._start_vertex.point, self._end_vertex.point]
        }






