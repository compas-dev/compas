from compas.geometry import Point
from compas.geometry import BrepVertex
from compas_rhino.conversions import point_to_compas


class RhinoBrepVertex(BrepVertex):
    """A wrapper for a Rhino Brep vertex.

    Attributes
    ----------
    point : :class:`~compas.geometry.Point`
        The geometry of this vertex as a point in 3D space.

    """

    def __init__(self, rhino_vertex=None):
        super(RhinoBrepVertex, self).__init__()
        self._vertex = None
        self._point = None
        if rhino_vertex:
            self._set_vertex(rhino_vertex)

    def _set_vertex(self, native_vertex):
        self._vertex = native_vertex
        self._point = point_to_compas(self._vertex.Location)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        return {
            "point": self._point.data,
        }

    @data.setter
    def data(self, data):
        # Rhino.BrepVertex has no public constructor
        # Vertex creation is via Brep.Vertices.Add(Rhino.Point3D)
        self._point = Point.from_data(data["point"])

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def point(self):
        return self._point
