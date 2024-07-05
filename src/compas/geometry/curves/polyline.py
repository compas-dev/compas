from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import is_point_on_line
from compas.geometry import is_point_on_polyline
from compas.geometry import transform_points
from compas.itertools import pairwise
from compas.tolerance import TOL

from .curve import Curve


class Polyline(Curve):
    """A polyline is a curve defined by a sequence of points connected by line segments.

    A Polyline can be open or closed.
    It can be self-intersecting.
    It does not have an interior.

    The parameter space is defined along the consecutive direction vectors of the line segments of the polyline.
    The coordinate system of the parametrisation is the world coordinate system.
    Transformations of polylines are defined as transformations of the points defining the polyline.

    Parameters
    ----------
    points : list[[float, float, float] | :class:`compas.geometry.Point`]
        An ordered list of points.
        Each consecutive pair of points forms a segment of the polyline.
    name : str, optional
        The name of the polyline.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`, read-only
        The frame of the spatial coordinates of the polyline.
        This is always the world XY frame.
    points : list[:class:`compas.geometry.Point`]
        The points of the polyline.
    lines : list[:class:`compas.geometry.Line`], read-only
        The lines of the polyline.
    length : float, read-only
        The length of the polyline.
    start : :class:`compas.geometry.Point`, read-only
        The start point of the polyline.
    end : :class:`compas.geometry.Point`, read-only
        The end point of the polyline.
    is_selfintersecting : bool, read-only
        True if the polyline is self-intersecting.
    is_closed : bool, read-only
        True if the polyline is closed.

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

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "points": {"type": "array", "minItems": 2, "items": Point.DATASCHEMA},
        },
        "required": ["points"],
    }

    @property
    def __data__(self):
        return {"points": [point.__data__ for point in self.points]}

    def __init__(self, points, name=None):
        super(Polyline, self).__init__(name=name)
        self._points = []
        self._lines = []
        self.points = points

    def __repr__(self):
        return "{0}({1!r})".format(
            type(self).__name__,
            self.points,
        )

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = Point(*value)
        self._lines = None

    def __iter__(self):
        return iter(self.points)

    def __len__(self):
        return len(self.points)

    def __eq__(self, other):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return TOL.is_allclose(self, other)

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def frame(self):
        return Frame.worldXY()

    @frame.setter
    def frame(self, frame):
        raise AttributeError("Setting the coordinate frame of a polyline is not supported.")

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*xyz) for xyz in points]
        self._lines = None

    @property
    def lines(self):
        if self._lines is None:
            self._lines = [Line(a, b) for a, b in pairwise(self.points)]
        return self._lines

    @property
    def length(self):
        return sum([line.length for line in self.lines])

    @property
    def start(self):
        return self.points[0]

    @property
    def end(self):
        return self.points[-1]

    @property
    def is_selfintersecting(self):
        raise NotImplementedError

    @property
    def is_closed(self):
        return self.points[0] == self.points[-1]

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Transform this polyline.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(90))
        >>> polyline.transform(R)

        """
        for index, point in enumerate(transform_points(self.points, T)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]

    # ==========================================================================
    # Methods
    # ==========================================================================

    def append(self, point):
        """Append a point to the end of the polyline.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point to append.

        """
        self.points.append(Point(*point))
        self._lines = None

    def insert(self, i, point):
        """Insert a point at the specified index.

        Parameters
        ----------
        i : int
            The index of the insertion point.
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point to insert.

        """
        self.points.insert(i, Point(*point))
        self._lines = None

    def point_at(self, t, snap=False):
        """Point on the polyline at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The parameter value.
        snap : bool, optional
            If True, return the closest polyline point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point on the polyline.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> polyline.point_at(0.75)
        Point(x=1.000, y=0.500, z=0.000)

        """
        if t < 0 or t > 1:
            return None

        points = self.points
        if t == 0:
            return points[0]
        if t == 1:
            return points[-1]

        polyline_length = self.length

        x = 0
        i = 0
        while x <= t:
            line = Line(points[i], points[i + 1])
            line_length = line.length
            dx = line_length / polyline_length
            if x + dx > t:
                if snap:
                    if t - x < x + dx - t:
                        return line.start
                    else:
                        return line.end
                return line.point_at((t - x) * polyline_length / line_length)
            x += dx
            i += 1

    def parameter_at(self, point, tol=None):
        """Parameter of the polyline at a specific point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point on the polyline.
        tol : float, optional
            A tolerance value for verifying that the point is on the polyline.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        float
            The parameter of the polyline.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> polyline.parameter_at(Point(0.1, 0.0, 0.0))
        0.05

        """
        if not is_point_on_polyline(point, self, tol):
            raise Exception("{} not found!".format(point))
        dx = 0
        for line in self.lines:
            if not is_point_on_line(point, line, tol):
                dx += line.length
                continue
            dx += line.start.distance_to_point(point)
            break
        return dx / self.length

    def tangent_at(self, t):
        """Tangent vector at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The parameter value.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The tangent vector at the specified parameter.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> print(polyline.tangent_at(0.75))
        Vector(x=0.000, y=1.000, z=0.000)

        """
        if t < 0 or t > 1:
            return None

        points = self.points
        if t == 0:
            return points[1] - points[0]
        if t == 1:
            return points[-1] - points[-2]

        polyline_length = self.length

        x = 0
        i = 0
        while x <= t:
            line = Line(points[i], points[i + 1])
            line_length = line.length
            dx = line_length / polyline_length
            if x + dx > t:
                return line.direction
            x += dx
            i += 1

    def tangent_at_point(self, point):
        """Calculates the tangent vector of a point on a polyline

        Parameters
        ----------
        point: [float, float, float] | :class:`compas.geometry.Point`

        Returns
        -------
        :class:`compas.geometry.Vector`

        """
        for line in self.lines:
            if is_point_on_line(point, line):
                return line.direction
        raise Exception("{} not found!".format(point))

    def split_at_corners(self, angle_threshold):
        """Splits a polyline at corners larger than the given angle_threshold

        Parameters
        ----------
        angle_threshold : float
            In radians.

        Returns
        -------
        list[:class:`compas.geometry.Polyline`]

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
                split_polylines.append(Polyline(points[id1 : id2 + 1]))
            else:
                looped_pts = [points[i] for i in range(id1, len(points))] + points[1 : id2 + 1]
                split_polylines.append(Polyline(looped_pts))

        if self.is_closed and not corner_ids:
            return [Polyline(self.points)]

        return split_polylines

    def divide_at_corners(self, angle_threshold):
        """Divides a polyline at corners larger than the given angle_threshold

        Parameters
        ----------
        angle_threshold : float
            In radians.

        Returns
        -------
        list[:class:`compas.geometry.Point`]

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

    def divide(self, num_segments):
        """Divide a polyline in equal segments.

        Parameters
        ----------
        num_segments : int

        Returns
        -------
        list
            list[:class:`compas.geometry.Point`]

        Examples
        --------
        >>> polyline = Polyline([(0, 0, 0), (1, 1, 0), (2, 3, 0), (4, 4, 0), (5, 2, 0)])
        >>> len(polyline.divide(3))
        4

        """
        segment_length = self.length / num_segments
        return self.divide_by_length(segment_length, False)

    def divide_by_length(self, length, strict=True, tol=None):
        """Divide a polyline in segments of a given length.

        Parameters
        ----------
        length : float
            Length of the segments.
        strict : bool, optional
            If False, the remainder segment will be added even if it is smaller than the desired length
        tol : float, optional
            Floating point error tolerance.
            Defaults to `TOL.absolute`.

        Returns
        -------
        list[:class:`compas.geometry.Point`]

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
        tol = tol or TOL.absolute

        num_pts = int(self.length / length)
        total_length = [0, 0]
        division_pts = [self.points[0]]
        new_polyline = self

        for i in range(num_pts):
            for i_ln, line in enumerate(new_polyline.lines):
                total_length.append(total_length[-1] + line.length)  # type: ignore
                if total_length[-1] > length:
                    amp = (length - total_length[-2]) / line.length
                    new_pt = line.start + line.vector.scaled(amp)
                    division_pts.append(new_pt)
                    total_length = [0, 0]
                    remaining_pts = new_polyline.points[i_ln + 2 :]
                    new_polyline = Polyline([new_pt, line.end] + remaining_pts)
                    break
                elif total_length[-1] == length:
                    total_length = [0, 0]
                    division_pts.append(line.end)

            if len(division_pts) == num_pts + 1:
                break

        if strict is False and not self.is_closed and len(division_pts) < num_pts + 1:
            division_pts.append(new_polyline.points[-1])
        elif strict is False and division_pts[-1].distance_to_point(self.points[-1]) > tol:
            division_pts.append(self.points[-1])

        return division_pts

    def split_by_length(self, length, strict=True):
        """Split a polyline in segments of a given length.

        Parameters
        ----------
        length : float
            Length of the segments.
        strict : bool, optional
            If False, the remainder segment will be added even if it is smaller than the desired length
        tol : float, optional
            Floating point error tolerance.

        Returns
        -------
        list[:class:`compas.geometry.Polyline`]

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
        segment = Polyline([self[0]])  # Start a new segment
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
                segment = Polyline([new_pt])  # Start a new segment
                current_length = 0
                i += 1
                polyline_points_num = len(polyline_copy)
        if not strict and len(divided_polylines):
            divided_polylines.append(segment)  # Add the last segment
        return divided_polylines

    def split(self, num_segments):
        """Split a polyline in equal segments.

        Parameters
        ----------
        num_segments : int

        Returns
        -------
        list
            list[:class:`compas.geometry.Polyline`]

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

    def extend(self, length):
        """Extends a polyline by a given length, by modifying the first and/or last point tangentially.

        Parameters
        ----------
        length: float or tuple[float, float]
            A single length value to extend the polyline only at the end,
            or two length values to extend at both ends.

        Returns
        -------
        None

        """
        try:
            start, end = length
            self.points[0] = self.points[0] + self.lines[0].vector.unitized().scaled(-start)
            self._lines = None
        except TypeError:
            start = end = length
        self.points[-1] = self.points[-1] + self.lines[-1].vector.unitized().scaled(end)
        self._lines = None

    def extended(self, length):
        """Returns a copy of this polyline extended by a given length.

        Parameters
        ----------
        length: float or tuple[float, float]
            A single length value to extend the polyline only at the end,
            or two length values to extend at both ends.

        Returns
        -------
        :class:`compas.geometry.Polyline`

        """
        crv = self.copy()
        crv.extend(length)
        return crv

    def shorten(self, length):
        """Shortens a polyline by a given length.

        Parameters
        ----------
        length: float or tuple[float, float]
            A single length value to shorten the polyline only at the end,
            or two length values to shorten at both ends.

        Returns
        -------
        None

        """
        try:
            start, end = length
            total_length = 0
            for line in self.lines:
                total_length += line.length
                if total_length < start:
                    del self.points[0]
                elif total_length == start:
                    del self.points[0]
                    break
                else:
                    self.points[0] = line.end + line.vector.unitized().scaled(-(total_length - start))
                    break
        except TypeError:
            start = end = length

        total_length = 0
        for i in range(len(self.lines)):
            line = self.lines[-(i + 1)]
            total_length += line.length
            if total_length < end:
                del self.points[-1]
            elif total_length == end:
                del self.points[-1]
                break
            else:
                self.points[-1] = line.start + line.vector.unitized().scaled(total_length - end)
                break
        self._lines = None

    def shortened(self, length):
        """Returns a copy of this polyline shortened by a given length.

        Parameters
        ----------
        length: float or tuple[float, float]
            A single length value to shorten the polyline only at the end,
            or two length values to shorten at both ends.

        Returns
        -------
        :class:`compas.geometry.Polyline`

        """
        crv = self.copy()
        crv.shorten(length)
        return crv
