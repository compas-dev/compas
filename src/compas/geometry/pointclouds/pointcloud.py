from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from random import uniform
from compas.base import Base


__all__ = ['Pointcloud']


class Pointcloud(Base):
    """Class for working with pointclouds."""

    def __init__(self, points):
        super(Pointcloud, self).__init__()
        self._points = None
        self.points = points

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @classmethod
    def from_ply(cls, filepath):
        """Construct a pointcloud from a PLY file."""
        pass

    @classmethod
    def from_pcd(cls, filepath):
        """Construct a pointcloud from a PCD file."""
        pass

    @classmethod
    def from_bbox(cls, box, n):
        """Construct a point cloud within a given box.

        Parameters
        ----------
        box: :class:`compas.geometry.Box`
            The axis aligned bounding box of the cloud.
        n: int
            The number of points in the cloud.

        Returns
        -------
        :class:`compas.geometry.Pointcloud`

        Examples
        --------
        >>> cloud = Pointcloud.from_box(Box.from_width_height_depth(10, 3, 5), 100)
        >>> all((-5 < x < +5) and (-2.5 < y < +2.5) and (-1.5 < z < +1.5) for x, y, z in cloud.points)
        True

        """
        points = box.points
        x, y, z = zip(*points)
        xmin, xmax = min(x), max(x)
        ymin, ymax = min(y), max(y)
        zmin, zmax = min(z), max(z)
        x = [uniform(xmin, xmax) for i in range(n)]
        y = [uniform(ymin, ymax) for i in range(n)]
        z = [uniform(zmin, zmax) for i in range(n)]
        return cls(list(map(list, zip(x, y, z))))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
