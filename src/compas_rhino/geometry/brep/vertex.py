from compas.data import Data
from compas.geometry import Point
from compas_rhino.conversions import point_to_compas


class RhinoBRepVertex(Data):
    def __init__(self, rhino_vertex=None):
        super(RhinoBRepVertex, self).__init__()
        self._rhino_vertex = None
        self._point = None
        if rhino_vertex:
            self.rhino_vertex = rhino_vertex

    @property
    def rhino_vertex(self):
        return self._rhino_vertex

    @rhino_vertex.setter
    def rhino_vertex(self, value):
        self._rhino_vertex = value
        self._point = point_to_compas(self._rhino_vertex.Location)

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
