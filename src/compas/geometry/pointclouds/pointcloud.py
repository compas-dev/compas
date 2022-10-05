from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from random import uniform
from compas.geometry import transform_points
from compas.geometry import centroid_points
from compas.geometry import bounding_box
from compas.geometry import Primitive
from compas.geometry import Point


__all__ = ["Pointcloud"]


class Pointcloud(Primitive):
    """Class for working with pointclouds.

    Parameters
    ----------
    points : sequence[point]
        A sequence of points to add to the cloud.
    **kwargs : dict[str, Any], optional
        Additional keyword arguments collected in a dict.

    Attributes
    ----------
    points : list[:class:`~compas.geometry.Point`]
        The points of the cloud.

    Examples
    --------
    >>>

    """

    def __init__(self, points, **kwargs):
        super(Pointcloud, self).__init__(**kwargs)
        self._points = None
        self.points = points

    @property
    def DATASCHEMA(self):
        from schema import Schema
        from compas.data import is_float3

        return Schema({"points": lambda points: all(is_float3(point) for point in points)})

    @property
    def JSONSCHEMANAME(self):
        return "pointcloud"

    @property
    def data(self):
        return {"points": [point.data for point in self.points]}

    @data.setter
    def data(self, data):
        self._points = [Point.from_data(point) for point in data["points"]]

    @classmethod
    def from_data(cls, data):
        return cls(data["points"])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*point) for point in points]

    @property
    def centroid(self):
        return centroid_points(self.points)

    @property
    def bounding_box(self):
        return bounding_box(self.points)

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Pointcloud({0!r})".format(self.points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        if key > len(self) - 1:
            raise KeyError
        return self.points[key]

    def __setitem__(self, key, value):
        if key > len(self) - 1:
            raise KeyError
        self.points[key] = value

    def __iter__(self):
        return iter(self.points)

    def __eq__(self, other):
        """Is this pointcloud equal to the other pointcloud?

        Two pointclouds are considered equal if they have the same number of points
        and if the XYZ coordinates of the corresponding points are identical.

        Parameters
        ----------
        other : :class:`~compas.geometry.Pointcloud` | list[[float, float, float] | :class:`~compas.geometry.Point`]
            The pointcloud to compare.

        Returns
        -------
        bool
            True if the pointclouds are equal.
            False otherwise.

        """
        if len(self) != len(other):
            return False
        A = sorted(self, key=lambda point: (point[0], point[1], point[2]))
        B = sorted(other, key=lambda point: (point[0], point[1], point[2]))
        return all(a == b for a, b in zip(A, B))

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_ply(cls, filepath):
        """Construct a pointcloud from a PLY file.

        Parameters
        ----------
        filepath : str | bytes | os.PathLike
            Path of the PLY file.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`

        """
        pass

    @classmethod
    def from_pcd(cls, filepath):
        """Construct a pointcloud from a PCD file.

        Parameters
        ----------
        filepath : str | bytes | os.PathLike
            Path of the PCD file.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`

        """
        pass

    @classmethod
    def from_bounds(cls, x, y, z, n):
        """Construct a point cloud within a given box.

        Parameters
        ----------
        x : float | tuple[float, float]
            Size of the cloud in the X direction.
            If a single value, the size is (0, x).
            If a pair of values, the size is (x[0], x[1]).
        y : float | tuple[float, float]
            Size of the cloud in the Y direction.
            If a single value, the size is (0, y).
            If a pair of values, the size is (y[0], y[1]).
        z : float | tuple[float, float]
            Size of the cloud in the Z direction.
            If a single value, the size is (0, z).
            If a pair of values, the size is (z[0], z[1]).
        n : int
            The number of points in the cloud.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`

        Notes
        -----
        The XYZ coordinates of the `n` points are radnomly chosen within the provided `x`, `y`, and `z` bounds.
        Thererefor, there is no guarantee that the bounds are part of the resulting coordinates.

        Examples
        --------
        >>>

        """
        try:
            len(x)
        except TypeError:
            xmin = 0
            xmax = x
        else:
            xmin, xmax = x
        try:
            len(y)
        except TypeError:
            ymin = 0
            ymax = y
        else:
            ymin, ymax = y
        try:
            len(z)
        except TypeError:
            zmin = 0
            zmax = z
        else:
            zmin, zmax = z
        x = [uniform(xmin, xmax) for i in range(n)]
        y = [uniform(ymin, ymax) for i in range(n)]
        z = [uniform(zmin, zmax) for i in range(n)]
        return cls(list(map(list, zip(x, y, z))))

    @classmethod
    def from_box(cls, box, n):
        """Construct a point cloud within a given box.

        Parameters
        ----------
        box: :class:`~compas.geometry.Box`
            The axis aligned bounding box of the cloud.
        n: int
            The number of points in the cloud.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`

        Examples
        --------
        >>> from compas.geometry import Box
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

    # ==========================================================================
    # methods
    # ==========================================================================

    def transform(self, T):
        """Apply a transformation to the pointcloud.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
            The transformation.

        Returns
        -------
        None
            The cloud is modified in place.
        """
        for index, point in enumerate(transform_points(self.points, T)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]
