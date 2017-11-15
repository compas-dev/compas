from abc import ABCMeta
from abc import abstractmethod

from compas.utilities.decorators import abstractstatic


# rename to DatastructureArtistInterface?
class ArtistInterface(object):
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def redraw(self):
    #     pass

    @abstractmethod
    def clear_layer(self):
        """Clear the main drawing layer."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all items drawn by the artist, without clearing the main drawing layer."""
        pass


class ArtistMixinInterface(object):
    __metaclass__ = ABCMeta


class GeometryInterface(object):
    __metaclass__ = ABCMeta

    @abstractstatic
    def find(guid):
        """Find the object using its identifier."""
        pass


class PointGeometryInterface(GeometryInterface):
    pass


class CurveGeometryInterface(GeometryInterface):
    pass


class SurfaceGeometryInterface(GeometryInterface):
    pass


class MeshGeometryInterface(GeometryInterface):
    pass


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
