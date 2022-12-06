from compas.geometry import Point
from compas.geometry import BrepVertex
from compas_rhino.conversions import point_to_compas


class RhinoBrepVertex(BrepVertex):
    """A wrapper for a Rhino Brep vertex.

    Attributes
    ----------
    point : :class:`~compas.geometry.Point`, read-only
        The geometry of this vertex as a point in 3D space.

    """

    def __init__(self, rhino_vertex=None, builder=None):
        super(RhinoBrepVertex, self).__init__()
        self._builder = builder
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
        self._point = Point.from_data(data["point"])
        self._vertex = self._builder.add_vertex(self._point)

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
    def point(self):
        return self._point
