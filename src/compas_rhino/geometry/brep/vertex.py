from compas.data import Data
from compas.geometry import Point
from compas_rhino.conversions import point_to_compas


class RhinoBrepVertex(Data):
    def __init__(self, rhino_vertex=None):
        super(RhinoBrepVertex, self).__init__()
        self._vertex = None
        self._point = None
        if rhino_vertex:
            self._set_vertex(rhino_vertex)

    def _set_vertex(self, native_vertex):
        self._vertex = native_vertex
        self._point = point_to_compas(self._vertex.Location)

    @property
    def data(self):
        return {
            "point": self._point.data,
        }

    @data.setter
    def data(self, data):
        """

        Parameters
        ----------
        data

        Returns
        -------

        """
        # Rhino.BrepVertex has no public constructor
        # Vertex creation is via Brep.Vertices.Add(Rhino.Point3D)
        self._point = Point.from_data(data["point"])

    @property
    def point(self):
        return self._point
