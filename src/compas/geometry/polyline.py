from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Union
from typing import overload

from typing_extensions import Self

from compas._typing import Coordinates
from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.itertools import pairwise
from compas.tolerance import TOL

from ._core.predicates_3 import is_point_on_line
from ._core.predicates_3 import is_point_on_polyline
from ._core.transformations import transform_points
from ._typing import TransformationType
from .geometry import Geometry
from .line import Line
from .point import Point
from .vector import Vector


class Polyline(Geometry):
    """A polyline is a geometric primitive defined by connected line segments.

    A Polyline can be open or closed.
    It can be self-intersecting.
    It does not have an interior.

    The parameter space is defined along the consecutive direction vectors of the line segments of the polyline.
    The coordinate system of the parametrisation is the world coordinate system.
    Transformations of polylines are defined as transformations of the points defining the polyline.

    Parameters
    ----------
    points
        An ordered list of points.
        Each consecutive pair of points forms a segment of the polyline.
    name
        The name of the polyline.

    Examples
    --------
    >>> polyline = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]])
    >>> polyline.length
    3.0

    >>> type(polyline.points[0]) == Point
    True
    >>> polyline.points[0].x
    0.0

    >>> type(polyline.lines[0]) == Line
    True
    >>> polyline.lines[0].length
    1.0

    """

    @property
    def __data__(self) -> dict[str, list[list[float]]]:
        """The data representation of the polyline."""
        return {"points": [point.__data__ for point in self.points]}

    def __init__(self, points: CoordinatesType, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._points: list[Point] = []
        self.points = points

    def __repr__(self) -> str:
        return "{0}({1!r})".format(
            type(self).__name__,
            self.points,
        )

    @overload
    def __getitem__(self, key: int) -> Point: ...

    @overload
    def __getitem__(self, key: slice) -> list[Point]: ...

    def __getitem__(self, key: Union[int, slice]) -> Union[Point, list[Point]]:
        return self.points[key]

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        self.points[key] = Point(value[0], value[1], value[2])

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)

    def __len__(self) -> int:
        return len(self.points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinates) or len(self) != len(other):
            return False
        return TOL.is_allclose(self, other)

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def points(self) -> list[Point]:
        """The defining points of the polyline.

        Notes
        -----
        Assigning a collection of three-component coordinates creates an
        independent `Point` for every item. The returned list itself is mutable;
        the derived line segments always reflect its current contents.

        Examples
        --------
        >>> source = Point(1, 2, 3)
        >>> polyline = Polyline([[0, 0, 0], source])
        >>> polyline.points[1] == source and polyline.points[1] is not source
        True

        """
        return self._points

    @points.setter
    def points(self, points: CoordinatesType) -> None:
        self._points = [Point(xyz[0], xyz[1], xyz[2]) for xyz in points]

    @property
    def lines(self) -> list[Line]:
        """The line segments connecting consecutive points.

        The lines are derived from the current points on every access.

        Examples
        --------
        >>> polyline = Polyline([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
        >>> len(polyline.lines)
        2
        >>> polyline.lines is polyline.lines
        False

        """
        return [Line(a, b) for a, b in pairwise(self.points)]

    @property
    def length(self) -> float:
        """The sum of the segment lengths.

        Examples
        --------
        >>> Polyline([[0, 0, 0], [3, 4, 0]]).length
        5.0

        """
        return sum(line.length for line in self.lines)

    @property
    def start(self) -> Point:
        """The first point of the polyline.

        Raises
        ------
        IndexError
            If the polyline has no points.

        """
        return self.points[0]

    @property
    def end(self) -> Point:
        """The last point of the polyline.

        Raises
        ------
        IndexError
            If the polyline has no points.

        """
        return self.points[-1]

    @property
    def is_closed(self) -> bool:
        """Whether the first and last points coincide.

        Raises
        ------
        IndexError
            If the polyline has no points.

        """
        return self.points[0] == self.points[-1]

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform this polyline.

        Parameters
        ----------
        transformation
            The transformation.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(90))
        >>> polyline.transform(R)

        """
        for index, point in enumerate(transform_points(self.points, transformation)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]

    # ==========================================================================
    # Methods
    # ==========================================================================

    def append(self, point: CoordinateType) -> None:
        """Append a point to the end of the polyline.

        Parameters
        ----------
        point
            The point to append.

        """
        self.points.append(Point(point[0], point[1], point[2]))

    def insert(self, i: int, point: CoordinateType) -> None:
        """Insert a point at the specified index.

        Parameters
        ----------
        i
            The index of the insertion point.
        point
            The point to insert.

        """
        self.points.insert(i, Point(point[0], point[1], point[2]))

    def _parameterization_data(self) -> tuple[list[Line], float]:
        lines = self.lines
        length = sum(line.length for line in lines)
        if length == 0.0:
            raise ValueError("A zero-length polyline has no parameterization.")
        return lines, length

    def point_at(self, t: float, snap: bool = False) -> Optional[Point]:
        """Point on the polyline at a specific normalized parameter.

        Parameters
        ----------
        t
            The parameter value.
        snap
            If `True`, return the closest defining point.

        Returns
        -------
        Optional[Point]
            The point on the polyline, or `None` if `t` is outside `[0, 1]`.

        Raises
        ------
        ValueError
            If the polyline has zero length.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> polyline.point_at(0.75)
        Point(x=1.000, y=0.500, z=0.000)

        """
        if t < 0 or t > 1:
            return None

        lines, polyline_length = self._parameterization_data()
        points = self.points
        if t == 0:
            return points[0]
        if t == 1:
            return points[-1]

        x = 0
        for line in lines:
            line_length = line.length
            if line_length == 0.0:
                continue
            dx = line_length / polyline_length
            if x + dx > t:
                if snap:
                    if t - x < x + dx - t:
                        return line.start
                    else:
                        return line.end
                return line.point_at((t - x) * polyline_length / line_length)
            x += dx
        return points[-1]

    def parameter_at(self, point: CoordinateType, tol: Optional[float] = None) -> float:
        """Parameter of the polyline at a specific point.

        Parameters
        ----------
        point
            The point on the polyline.
        tol
            A tolerance value for verifying that the point is on the polyline.
            Default is `TOL.absolute`.

        Returns
        -------
        float
            The parameter of the polyline.

        Raises
        ------
        ValueError
            If the polyline has zero length or the point is not on the polyline.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> polyline.parameter_at(Point(0.1, 0.0, 0.0))
        0.05

        """
        point = Point(point[0], point[1], point[2])
        lines, polyline_length = self._parameterization_data()
        if not is_point_on_polyline(point, self, tol):
            raise ValueError("{} not found!".format(point))
        dx = 0
        for line in lines:
            if not is_point_on_line(point, line, tol):
                dx += line.length
                continue
            dx += line.start.distance_to_point(point)
            break
        return dx / polyline_length

    def tangent_at(self, t: float) -> Optional[Vector]:
        """Tangent vector at a specific normalized parameter.

        Parameters
        ----------
        t
            The parameter value.

        Returns
        -------
        Optional[Vector]
            The tangent vector, or `None` if `t` is outside `[0, 1]`.

        Raises
        ------
        ValueError
            If the polyline has zero length.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> print(polyline.tangent_at(0.75))
        Vector(x=0.000, y=1.000, z=0.000)

        """
        if t < 0 or t > 1:
            return None

        lines, polyline_length = self._parameterization_data()
        if t == 0:
            return next(line.direction for line in lines if line.length > 0.0)
        if t == 1:
            return next(line.direction for line in reversed(lines) if line.length > 0.0)

        x = 0
        tangent = None
        for line in lines:
            line_length = line.length
            if line_length == 0.0:
                continue
            tangent = line.direction
            dx = line_length / polyline_length
            if x + dx > t:
                return tangent
            x += dx
        return tangent

    def tangent_at_point(self, point: CoordinateType) -> Vector:
        """Calculate the tangent vector at a point on the polyline.

        Parameters
        ----------
        point
            The point on the polyline.

        Returns
        -------
        Vector
            The tangent vector.

        Raises
        ------
        ValueError
            If the polyline has zero length or the point is not on the polyline.

        """
        point = Point(point[0], point[1], point[2])
        lines, _ = self._parameterization_data()
        for line in lines:
            if line.length == 0.0:
                continue
            if is_point_on_line(point, line):
                return line.direction
        raise ValueError("{} not found!".format(point))

    def split_at_corners(self, angle_threshold: float) -> list[Self]:
        """Split the polyline at corners larger than a threshold.

        Parameters
        ----------
        angle_threshold
            In radians.

        Returns
        -------
        list[Self]
            The split polylines.

        """
        corner_ids = []
        split_polylines = []
        points = self.points
        seg_ids = list(range(len(self.lines)))

        if self.is_closed:
            seg_ids.append(0)

        for seg1, seg2 in pairwise(seg_ids):
            angle = self.lines[seg2].vector.angle(-self.lines[seg1].vector)
            if angle >= angle_threshold:
                corner_ids.append(seg1 + 1)

        if self.is_closed and len(corner_ids) > 0:
            if corner_ids[-1] != len(points):
                corner_ids = [corner_ids[-1]] + corner_ids
        else:
            corner_ids = [0] + corner_ids + [len(points)]

        for id1, id2 in pairwise(corner_ids):
            if id1 < id2:
                split_polylines.append(type(self)(points[id1 : id2 + 1]))
            else:
                looped_pts = [points[i] for i in range(id1, len(points))] + points[1 : id2 + 1]
                split_polylines.append(type(self)(looped_pts))

        if self.is_closed and not corner_ids:
            return [type(self)(self.points)]

        return split_polylines

    def divide_at_corners(self, angle_threshold: float) -> list[Point]:
        """Return the points at corners larger than a threshold.

        Parameters
        ----------
        angle_threshold
            In radians.

        Returns
        -------
        list[Point]
            The corner points.

        """
        corner_ids = []
        seg_ids = list(range(len(self.lines)))
        if self.is_closed:
            seg_ids.insert(0, seg_ids[-1])

        for seg1, seg2 in pairwise(seg_ids):
            angle = self.lines[seg2].vector.angle(-self.lines[seg1].vector)
            if angle >= angle_threshold:
                corner_ids.append(seg1 + 1)
        return [self.points[i] for i in corner_ids]

    def divide(self, num_segments: int) -> list[Point]:
        """Divide a polyline in equal segments.

        Parameters
        ----------
        num_segments
            The number of equal-length segments.

        Returns
        -------
        list[Point]
            The division points.

        Raises
        ------
        ValueError
            If `num_segments` is less than one.

        Examples
        --------
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.divide(3))
        4

        """
        if num_segments < 1:
            raise ValueError("Number of segments must be greater than or equal to 1.")
        segment_length = self.length / num_segments
        return self.divide_by_length(segment_length, False)

    def divide_by_length(self, length: float, strict: bool = True, tol: Optional[float] = None) -> list[Point]:
        """Divide a polyline in segments of a given length.

        Parameters
        ----------
        length
            Length of the segments.
        strict
            If `False`, include a remainder segment shorter than `length`.
        tol
            Floating point error tolerance.
            Defaults to `TOL.absolute`.

        Returns
        -------
        list[Point]
            The division points.

        Raises
        ------
        ValueError
            If `length` is not positive or is greater than the polyline length.

        Notes
        -----
        The points of the new polyline are constrained to the segments of the old polyline.
        However, since the old points are not part of the new set of points, the geometry of the polyline will change.

        Examples
        --------
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.divide_by_length(3))
        3

        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.divide_by_length(3, strict=False))
        4

        """
        if length <= 0.0:
            raise ValueError("Length must be greater than zero.")
        if length > self.length:
            raise ValueError("Polyline length {0} is smaller than input length {1}.".format(self.length, length))

        tol = TOL.absolute if tol is None else tol

        num_pts = int(self.length / length)
        total_length: list[float] = [0.0, 0.0]
        division_pts = [self.points[0]]
        new_polyline = self

        for i in range(num_pts):
            for i_ln, line in enumerate(new_polyline.lines):
                total_length.append(total_length[-1] + line.length)
                if total_length[-1] > length:
                    amp = (length - total_length[-2]) / line.length
                    new_pt = line.start + line.vector.scaled(amp)
                    division_pts.append(new_pt)
                    total_length = [0.0, 0.0]
                    remaining_pts = new_polyline.points[i_ln + 2 :]
                    new_polyline = type(self)([new_pt, line.end] + remaining_pts)
                    break
                elif total_length[-1] == length:
                    total_length = [0.0, 0.0]
                    division_pts.append(line.end)

            if len(division_pts) == num_pts + 1:
                break

        if strict is False and not self.is_closed and len(division_pts) < num_pts + 1:
            division_pts.append(new_polyline.points[-1])
        elif strict is False and division_pts[-1].distance_to_point(self.points[-1]) > tol:
            division_pts.append(self.points[-1])

        return division_pts

    def split_by_length(self, length: float, strict: bool = True) -> list[Self]:
        """Split a polyline in segments of a given length.

        Parameters
        ----------
        length
            Length of the segments.
        strict
            If `False`, include a remainder segment shorter than `length`.

        Returns
        -------
        list[Self]
            The split polylines.

        Examples
        --------
        >>> from compas.geometry import Polyline
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.split_by_length(3))
        2

        >>> from compas.geometry import Polyline
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.split_by_length(3, strict=False))
        3

        """
        if length <= 0:
            raise ValueError("Length should be bigger than 0.")
        elif length > self.length:
            raise ValueError("Polyline length {0} is smaller than input length {1}.".format(self.length, length))
        divided_polylines = []
        polyline_copy = self.copy()
        segment = type(self)([self[0]])  # Start a new segment
        i, current_length = 0, 0
        polyline_points_num = len(polyline_copy)
        while i < polyline_points_num - 1:
            pt1, pt2 = polyline_copy.points[i : i + 2]
            line_length = pt1.distance_to_point(pt2)
            current_length += line_length
            if current_length <= length:
                segment.points.append(pt2)
                i += 1
            else:
                amp = 1 - ((current_length - length) / line_length)
                new_pt = pt1 + (pt2 - pt1).scaled(amp)
                polyline_copy.points.insert(i + 1, new_pt)
                segment.points.append(new_pt)
                divided_polylines.append(segment)
                segment = type(self)([new_pt])  # Start a new segment
                current_length = 0
                i += 1
                polyline_points_num = len(polyline_copy)
        if not strict and len(divided_polylines):
            divided_polylines.append(segment)  # Add the last segment
        return divided_polylines

    def split(self, num_segments: int) -> list[Self]:
        """Split a polyline in equal segments.

        Parameters
        ----------
        num_segments
            The number of equal-length segments.

        Returns
        -------
        list[Self]
            The split polylines.

        Examples
        --------
        >>> from compas.geometry import Polyline
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> polylines = polyline.split(3)
        >>> len(polylines)
        3

        """
        if num_segments < 1:
            raise ValueError("Number of segments must be greater than or equal to 1.")
        elif num_segments == 1:
            return [self]
        total_length = self.length
        segment_length = total_length / num_segments
        return self.split_by_length(segment_length, False)

    def extend(self, length: Union[float, Sequence[float]]) -> None:
        """Extend the polyline tangentially at one or both ends.

        Parameters
        ----------
        length
            A single length value to extend the polyline only at the end,
            or two length values to extend at both ends.

        """
        if isinstance(length, Sequence):
            start, end = length
            self.points[0] = self.points[0] + self.lines[0].vector.unitized().scaled(-start)
        else:
            end = length
        self.points[-1] = self.points[-1] + self.lines[-1].vector.unitized().scaled(end)

    def extended(self, length: Union[float, Sequence[float]]) -> Self:
        """Return an extended copy of the polyline.

        Parameters
        ----------
        length
            A single length value to extend the polyline only at the end,
            or two length values to extend at both ends.

        Returns
        -------
        Self
            The extended copy.

        """
        polyline = self.copy()
        polyline.extend(length)
        return polyline

    def shorten(self, length: Union[float, Sequence[float]]) -> None:
        """Shorten the polyline at one or both ends.

        Parameters
        ----------
        length
            A single length value to shorten the polyline only at the end,
            or two length values to shorten at both ends.

        """
        # Both ends are shortened against the original segmentation even though
        # the point list is mutated during the operation.
        lines = self.lines

        if isinstance(length, Sequence):
            start, end = length
            total_length = 0
            for line in lines:
                total_length += line.length
                if total_length < start:
                    del self.points[0]
                elif total_length == start:
                    del self.points[0]
                    break
                else:
                    self.points[0] = line.end + line.vector.unitized().scaled(-(total_length - start))
                    break
        else:
            end = length

        total_length = 0
        for i in range(len(lines)):
            line = lines[-(i + 1)]
            total_length += line.length
            if total_length < end:
                del self.points[-1]
            elif total_length == end:
                del self.points[-1]
                break
            else:
                self.points[-1] = line.start + line.vector.unitized().scaled(total_length - end)
                break

    def shortened(self, length: Union[float, Sequence[float]]) -> Self:
        """Return a shortened copy of the polyline.

        Parameters
        ----------
        length
            A single length value to shorten the polyline only at the end,
            or two length values to shorten at both ends.

        Returns
        -------
        Self
            The shortened copy.

        """
        polyline = self.copy()
        polyline.shorten(length)
        return polyline
