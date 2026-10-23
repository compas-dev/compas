from collections.abc import Iterator
from random import uniform
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry import Geometry
from compas.geometry import KDTree
from compas.geometry import Point
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import closest_point_in_cloud
from compas.geometry import transform_points
from compas.tolerance import TOL

if TYPE_CHECKING:
    from compas.geometry import Box
    from compas.geometry import Transformation


class Pointcloud(Geometry):
    """A collection of points.

    Parameters
    ----------
    points
        A sequence of points to add to the cloud.
    name
        The name of the pointcloud.

    Examples
    --------
    >>> cloud = Pointcloud([[0, 0, 0], [1, 0, 0]])
    >>> len(cloud)
    2

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, list[list[float]]]:
        return {"points": [point.__data__ for point in self.points]}

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, points: CoordinatesType, name: str | None = None) -> None:
        super().__init__(name=name)
        self._points = None
        self._tree = None
        self.points = points

    def __repr__(self) -> str:
        return "{0}(points={1!r})".format(type(self).__name__, self.points)

    def __str__(self) -> str:
        return "{0}(len(points)={1})".format(type(self).__name__, len(self.points))

    def __len__(self) -> int:
        return len(self.points)

    def __getitem__(self, key: int) -> Point:
        if key > len(self) - 1:
            raise KeyError
        return self.points[key]

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        if key > len(self) - 1:
            raise KeyError
        self.points[key] = Point(value[0], value[1], value[2])
        self._tree = None

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pointcloud):
            return False
        if len(self) != len(other):
            return False
        A = sorted(self, key=lambda point: (point[0], point[1], point[2]))
        B = sorted(other, key=lambda point: (point[0], point[1], point[2]))
        return all(a == b for a, b in zip(A, B))

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def points(self) -> list[Point]:
        """The points of the cloud."""
        if self._points is None:
            self._points = []
        return self._points

    @points.setter
    def points(self, points: CoordinatesType) -> None:
        self._points = [Point(point[0], point[1], point[2]) for point in points]
        self._tree = None

    @property
    def tree(self) -> KDTree:
        """The cached nearest-neighbor tree.

        Notes
        -----
        Assigning points, replacing an indexed point, or transforming the cloud
        invalidates the cache.

        """
        if self._tree is None:
            self._tree = KDTree(self.points)
        return self._tree

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_ply(cls, filepath: FilePath) -> Self:
        """Construct a pointcloud from a PLY file.

        Parameters
        ----------
        filepath
            Path of the PLY file.

        Returns
        -------
        Self
            The constructed point cloud.

        """
        from compas.files import ply_data
        from compas.files import read_ply

        return cls(ply_data(read_ply(filepath)).vertices)

    @classmethod
    def from_bounds(
        cls,
        x: float | tuple[float, float],
        y: float | tuple[float, float],
        z: float | tuple[float, float],
        n: int,
    ) -> Self:
        """Construct a point cloud within a given box.

        Parameters
        ----------
        x
            Size of the cloud in the X direction.
            If a single value, the size is (0, x).
            If a pair of values, the size is (x[0], x[1]).
        y
            Size of the cloud in the Y direction.
            If a single value, the size is (0, y).
            If a pair of values, the size is (y[0], y[1]).
        z
            Size of the cloud in the Z direction.
            If a single value, the size is (0, z).
            If a pair of values, the size is (z[0], z[1]).
        n
            The number of points in the cloud.

        Returns
        -------
        Self
            The constructed point cloud.

        Notes
        -----
        The coordinates are chosen randomly within the provided bounds. The
        requested bounds are therefore not necessarily represented by points
        in the result.

        """
        xmin, xmax = x if isinstance(x, tuple) else (0.0, x)
        ymin, ymax = y if isinstance(y, tuple) else (0.0, y)
        zmin, zmax = z if isinstance(z, tuple) else (0.0, z)
        xvalues = [uniform(xmin, xmax) for _ in range(n)]
        yvalues = [uniform(ymin, ymax) for _ in range(n)]
        zvalues = [uniform(zmin, zmax) for _ in range(n)]
        return cls(list(map(list, zip(xvalues, yvalues, zvalues))))

    @classmethod
    def from_box(cls, box: "Box", n: int) -> Self:
        """Construct a point cloud within a given box.

        Parameters
        ----------
        box
            The box containing the cloud.
        n
            The number of points in the cloud.

        Returns
        -------
        Self
            The constructed point cloud.

        Examples
        --------
        >>> from compas.geometry import Box
        >>> cloud = Pointcloud.from_box(Box.from_width_height_depth(10, 3, 5), 100)
        >>> all((-5 < x < +5) and (-2.5 < y < +2.5) and (-1.5 < z < +1.5) for x, y, z in cloud.points)
        True

        """
        dx = 0.5 * box.xsize
        dy = 0.5 * box.ysize
        dz = 0.5 * box.zsize
        points = [[uniform(-dx, dx), uniform(-dy, dy), uniform(-dz, dz)] for _ in range(n)]
        return cls([box.frame.to_world_coordinates(point) for point in points])

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, transformation: "Transformation") -> None:
        """Apply a transformation to the pointcloud.

        Parameters
        ----------
        transformation
            The transformation.

        """
        for index, point in enumerate(transform_points(self.points, transformation)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]
        self._tree = None

    # ==========================================================================
    # Methods
    # ==========================================================================

    def centroid(self) -> list[float]:
        """Compute the centroid of the point cloud.

        Returns
        -------
        list[float]
            The centroid coordinates.

        """
        return centroid_points(self.points)

    def aabb(self) -> "Box":
        """Compute the axis-aligned bounding box of the point cloud.

        Returns
        -------
        Box

        """
        from compas.geometry import Box

        return Box.from_bounding_box(bounding_box(self.points))

    def obb(self) -> "Box":
        """Compute the oriented bounding box of the point cloud.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box

        return Box.from_bounding_box(oriented_bounding_box(self.points))

    def closest_point(self, point: CoordinateType) -> Point:
        """Compute the closest point on the pointcloud to a given point.

        Parameters
        ----------
        point
            The point.

        Returns
        -------
        Point
            The closest point on the pointcloud.

        """
        _, closest, _ = closest_point_in_cloud(point, self.points)
        return Point(closest[0], closest[1], closest[2])

    def closest_points(self, point: CoordinateType, k: int = 1) -> list[Point]:
        """Compute the closest point on the pointcloud to a given point.

        Parameters
        ----------
        point
            The point.
        k
            The number of closest points to find.

        Returns
        -------
        list[Point]
            The closest points on the pointcloud.

        """
        tree = self.tree
        return [self.points[neighbor.label] for neighbor in tree.nearest_neighbors(point, k, True)]

    def add(self, other: "Pointcloud", tol: float | None = None) -> None:
        """Add another pointcloud to this pointcloud.

        Parameters
        ----------
        other
            The other pointcloud.
        tol
            The absolute tolerance for comparing the distance between points to zero.
            Defaults to `TOL.absolute`.

        Notes
        -----
        Duplicate points are not added.

        """
        tol = TOL.absolute if tol is None else tol

        tree = self.tree
        points = []
        for point in other:
            neighbor = tree.nearest_neighbor(point)
            if neighbor is None or neighbor.distance > tol:
                points.append(point)
        self.points += points

    def union(self, other: "Pointcloud", tol: float | None = None) -> Self:
        """Compute the union with another pointcloud.

        Parameters
        ----------
        other
            The other pointcloud.
        tol
            The absolute tolerance for comparing the distance between points to zero.
            Defaults to `TOL.absolute`.

        Returns
        -------
        Self
            The union pointcloud.

        """
        tol = TOL.absolute if tol is None else tol

        tree = self.tree
        points = []
        for point in other:
            neighbor = tree.nearest_neighbor(point)
            if neighbor is None or neighbor.distance > tol:
                points.append(point)
        return type(self)(self.points + points)

    def subtract(self, other: "Pointcloud", tol: float | None = None) -> None:
        """Subtract another pointcloud from this pointcloud.

        Parameters
        ----------
        other
            The other pointcloud.
        tol
            The absolute tolerance for comparing the distance between points to zero.
            Defaults to `TOL.absolute`.

        """
        tol = TOL.absolute if tol is None else tol

        tree = KDTree(other.points)
        points = []
        for point in self.points:
            neighbor = tree.nearest_neighbor(point)
            if neighbor is None or neighbor.distance > tol:
                points.append(point)
        self.points = points

    def difference(self, other: "Pointcloud", tol: float | None = None) -> Self:
        """Compute the difference with another pointcloud.

        Parameters
        ----------
        other
            The other pointcloud.
        tol
            The absolute tolerance for comparing the distance between points to zero.
            Defaults to `TOL.absolute`.

        Returns
        -------
        Self
            The difference pointcloud.

        """
        tol = TOL.absolute if tol is None else tol

        tree = KDTree(other.points)
        points = []
        for point in self.points:
            neighbor = tree.nearest_neighbor(point)
            if neighbor is None or neighbor.distance > tol:
                points.append(point)
        return type(self)(points)
