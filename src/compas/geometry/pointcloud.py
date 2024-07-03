from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import uniform

from compas.geometry import Geometry
from compas.geometry import KDTree
from compas.geometry import Point
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import closest_point_in_cloud
from compas.geometry import transform_points
from compas.tolerance import TOL


class Pointcloud(Geometry):
    """Class for working with pointclouds.

    Parameters
    ----------
    points : sequence[point]
        A sequence of points to add to the cloud.
    name : str, optional
        The name of the pointcloud.

    Attributes
    ----------
    points : list[:class:`compas.geometry.Point`]
        The points of the cloud.

    Examples
    --------
    >>>

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "items": Point.DATASCHEMA, "minItems": 1},
        },
        "required": ["points"],
    }

    @property
    def __data__(self):
        return {"points": [point.__data__ for point in self.points]}

    def __init__(self, points, name=None):
        super(Pointcloud, self).__init__(name=name)
        self._points = None
        self._tree = None
        self.points = points

    def __repr__(self):
        return "{0}(points={1!r})".format(type(self).__name__, self.points)

    def __str__(self):
        return "{0}(len(points)={1})".format(type(self).__name__, len(self.points))

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
        if len(self) != len(other):
            return False
        A = sorted(self, key=lambda point: (point[0], point[1], point[2]))
        B = sorted(other, key=lambda point: (point[0], point[1], point[2]))
        return all(a == b for a, b in zip(A, B))

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def points(self):
        if self._points is None:
            self._points = []
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*point) for point in points]
        self._tree = None

    @property
    def tree(self):
        if not self._tree:
            self._tree = KDTree(self.points)
        return self._tree

    @property
    def centroid(self):
        return centroid_points(self.points)

    @property
    def aabb(self):
        from compas.geometry import Box

        return Box.from_bounding_box(bounding_box(self.points))

    @property
    def obb(self):
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box_numpy

        return Box.from_bounding_box(oriented_bounding_box_numpy(self.points))

    # ==========================================================================
    # Constructors
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
        :class:`compas.geometry.Pointcloud`

        """
        from compas.files import PLY

        points = []
        ply = PLY(filepath)
        for vertex in ply.reader.vertices:  # type: ignore
            points.append([vertex["x"], vertex["y"], vertex["z"]])
        cloud = cls(points)
        return cloud

    @classmethod
    def from_pcd(cls, filepath):
        """Construct a pointcloud from a PCD file.

        Parameters
        ----------
        filepath : str | bytes | os.PathLike
            Path of the PCD file.

        Returns
        -------
        :class:`compas.geometry.Pointcloud`

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
        :class:`compas.geometry.Pointcloud`

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
        box: :class:`compas.geometry.Box`
            The axis aligned bounding box of the cloud.
        n: int
            The number of points in the cloud.

        Returns
        -------
        :class:`compas.geometry.Pointcloud`

        Examples
        --------
        >>> from compas.geometry import Box
        >>> cloud = Pointcloud.from_box(Box.from_width_height_depth(10, 3, 5), 100)
        >>> all((-5 < x < +5) and (-2.5 < y < +2.5) and (-1.5 < z < +1.5) for x, y, z in cloud.points)
        True

        """
        xmin, xmax = box.xmin, box.xmax
        ymin, ymax = box.ymin, box.ymax
        zmin, zmax = box.zmin, box.zmax
        x = [uniform(xmin, xmax) for i in range(n)]
        y = [uniform(ymin, ymax) for i in range(n)]
        z = [uniform(zmin, zmax) for i in range(n)]
        return cls(list(map(list, zip(x, y, z))))

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Apply a transformation to the pointcloud.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
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

    # ==========================================================================
    # Methods
    # ==========================================================================

    def closest_point(self, point):
        """Compute the closest point on the pointcloud to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The closest point on the pointcloud.

        """
        distance, point, index = closest_point_in_cloud(point, self.points)
        return point

    def closest_points(self, point, k=1):
        """Compute the closest point on the pointcloud to a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The point.
        k : int, optional
            The number of closest points to find.

        Returns
        -------
        list of :class:`~compas.geometry.Point`
            The closest points on the pointcloud.

        """
        tree = self.tree
        return [self.points[nbr[1]] for nbr in tree.nearest_neighbors(point, k, True)]

    def add(self, other, tol=None):
        """Add another pointcloud to this pointcloud.

        Parameters
        ----------
        other : :class:`~compas.geometry.Pointcloud`
            The other pointcloud.
        tol : float, optional
            The absolute tolerance for comparing the distance between points to zero.
            Default is ``None``, in which case ``compas.tolerance.TOL.absolute`` is used.

        Returns
        -------
        None
            The pointcloud is modified in place.

        Notes
        -----
        Duplicate points are not added.

        """
        tol = tol or TOL.absolute

        tree = self.tree
        self.points += [point for point in other if tree.nearest_neighbor(point)[2] > tol]

    def union(self, other, tol=None):
        """Compute the union with another pointcloud.

        Parameters
        ----------
        other : :class:`~compas.geometry.Pointcloud`
            The other pointcloud.
        tol : float, optional
            The absolute tolerance for comparing the distance between points to zero.
            Default is ``None``, in which case ``compas.tolerance.TOL.absolute`` is used.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`
            The union pointcloud.

        """
        tol = tol or TOL.absolute

        tree = self.tree
        return Pointcloud(self.points + [point for point in other if tree.nearest_neighbor(point)[2] > tol])

    def subtract(self, other, tol=None):  # type: (Pointcloud, ...) -> None
        """Subtract another pointcloud from this pointcloud.

        Parameters
        ----------
        other : :class:`~compas.geometry.Pointcloud`
            The other pointcloud.
        tol : float, optional
            The absolute tolerance for comparing the distance between points to zero.
            Default is ``None``, in which case ``compas.tolerance.TOL.absolute`` is used.

        Returns
        -------
        None
            The pointcloud is modified in place.

        """
        tol = tol or TOL.absolute

        tree = KDTree(other)
        self.points = [point for point in self.points if tree.nearest_neighbor(point)[2] > tol]

    def difference(self, other, tol=None):  # type: (Pointcloud, ...) -> Pointcloud
        """Compute the difference with another pointcloud.

        Parameters
        ----------
        other : :class:`~compas.geometry.Pointcloud`
            The other pointcloud.
        tol : float, optional
            The absolute tolerance for comparing the distance between points to zero.
            Default is ``None``, in which case ``compas.tolerance.TOL.absolute`` is used.

        Returns
        -------
        :class:`~compas.geometry.Pointcloud`
            The difference pointcloud.

        """
        tol = tol or TOL.absolute

        tree = KDTree(other)
        return Pointcloud([point for point in self.points if tree.nearest_neighbor(point)[2] > tol])
