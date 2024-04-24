from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import BrepVertex
from compas.geometry import Point
from compas_rhino.conversions import point_to_compas


class RhinoBrepVertex(BrepVertex):
    """A wrapper for a Rhino Brep vertex.

    Attributes
    ----------
    native_vertex : :class:`Rhino.Geometry.BrepVertex`
        The underlying Rhino BrepBertex object.
    point : :class:`compas.geometry.Point`, read-only
        The geometry of this vertex as a point in 3D space.

    """

    def __init__(self, rhino_vertex=None):
        super(RhinoBrepVertex, self).__init__()
        self._vertex = None
        self._point = None
        if rhino_vertex:
            self.native_vertex = rhino_vertex

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        return {
            "point": self._point.__data__,
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
        instance._point = Point.__from_data__(data["point"])
        instance.native_vertex = builder.add_vertex(instance.point)
        return instance

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def point(self):
        return self._point

    @property
    def native_vertex(self):
        return self._vertex

    @native_vertex.setter
    def native_vertex(self, vertex):
        self._vertex = vertex
        self._point = point_to_compas(self._vertex.Location)
