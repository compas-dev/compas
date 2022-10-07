from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import allclose
from compas.geometry import transform_points

from compas.geometry.predicates import is_point_on_line
from compas.geometry.primitives import Line
from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Point

from compas.utilities import pairwise


class Polyline(Primitive):
    """A polyline is defined by a sequence of points connected by line segments.

    Parameters
    ----------
    points : list[[float, float, float] | :class:`~compas.geometry.Point`]
        An ordered list of points.
        Each consecutive pair of points forms a segment of the polyline.

    Attributes
    ----------
    points : list[:class:`~compas.geometry.Point`]
        The points of the polyline.
    lines : list[:class:`~compas.geometry.Line`], read-only
        The lines of the polyline.
    length : float, read-only
        The length of the polyline.

    Notes
    -----
    A polyline is a piecewise linear element.
    It does not have an interior.
    It can be open or closed.
    It can be self-intersecting.

    Examples
    --------
    >>> polyline = Polyline([[0,0,0], [1,0,0], [2,0,0], [3,0,0]])
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

    __slots__ = ["_points", "_lines"]

    def __init__(self, points, **kwargs):
        super(Polyline, self).__init__(**kwargs)
        self._points = []
        self._lines = []
        self.points = points

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        from schema import Schema
        from compas.data import is_float3

        return Schema({"points": lambda points: all(is_float3(point) for point in points)})

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "polyline"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the polyline."""
        return {"points": [point.data for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = [Point.from_data(point) for point in data["points"]]

    @classmethod
    def from_data(cls, data):
        """Construct a polyline from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Polyline`
            The constructed polyline.

        Examples
        --------
        >>> Polyline.from_data({'points': [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]})
        Polyline([Point(0.000, 0.000, 0.000), Point(1.000, 0.000, 0.000), Point(1.000, 1.000, 0.000)])

        """
        return cls([Point.from_data(point) for point in data["points"]])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*xyz) for xyz in points]
        self._lines = None

    # consider caching below based on point setter

    @property
    def lines(self):
        if not self._lines:
            self._lines = [Line(a, b) for a, b in pairwise(self.points)]
        return self._lines

    @property
    def length(self):
        return sum([line.length for line in self.lines])

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Polyline([{0}])".format(", ".join(["{0!r}".format(point) for point in self.points]))

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = Point(*value)
        self._lines = None

    def __iter__(self):
        return iter(self.points)

    def __eq__(self, other):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return allclose(self, other)

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def point(self, t, snap=False):
        """Point on the polyline at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The parameter value.
        snap : bool, optional
            If True, return the closest polyline point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The point on the polyline.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> polyline.point(0.75)
        Point(1.000, 0.500, 0.000)

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
                return line.point((t - x) * polyline_length / line_length)
            x += dx
            i += 1

    def is_selfintersecting(self):
        """Determine if the polyline is self-intersecting.

        Returns
        -------
        bool
            True if the polyline is self-intersecting.
            False otherwise.

        Examples
        --------
        >>>

        """
        raise NotImplementedError

    def is_closed(self):
        """Determine if the polyline is closed.

        Returns
        -------
        bool
            True if the polyline is closed, False otherwise.

        Examples
        --------
        >>> polyline = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]])
        >>> polyline.is_closed()
        False
        >>> polyline.points.append(polyline.points[0])
        >>> polyline.is_closed()
        True

        """
        return self.points[0] == self.points[-1]

    def transform(self, T):
        """Transform this polyline.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation` | list[list[float]]
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

    def split_at_corners(self, angle_threshold):
        """Splits a polyline at corners larger than the given angle_threshold

        Parameters
        ----------
        angle_threshold : float
            In radians.

        Returns
        -------
        list[:class:`~compas.geometry.Polyline`]

        """
        corner_ids = []
        split_polylines = []
        points = self.points
        seg_ids = list(range(len(self.lines)))

        if self.is_closed():
            seg_ids.append(0)

        for seg1, seg2 in pairwise(seg_ids):
            angle = self.lines[seg1].vector.angle(self.lines[seg2].vector)
            if angle >= angle_threshold:
                corner_ids.append(seg1 + 1)

        if self.is_closed() and len(corner_ids) > 0:
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

        if self.is_closed() and not corner_ids:
            return [Polyline(self.points)]

        return split_polylines

    def tangent_at_point_on_polyline(self, point):
        """Calculates the tangent vector of a point on a polyline

        Parameters
        ----------
        point: [float, float, float] | :class:`~compas.geometry.Point`

        Returns
        -------
        :class:`~compas.geometry.Vector`

        """
        for line in self.lines:
            if is_point_on_line(point, line):
                return line.direction
        raise Exception("{} not found!".format(point))

    tangent_at = tangent_at_point_on_polyline

    def divide_polyline(self, num_segments):
        """Divide a polyline in equal segments.

        Parameters
        ----------
        num_segments : int

        Returns
        -------
        list
            list[:class:`~compas.geometry.Point`]

        """
        segment_length = self.length / num_segments
        return self.divide_polyline_by_length(segment_length, False)

    divide = divide_polyline

    def divide_polyline_by_length(self, length, strict=True, tol=1e-06):
        """Splits a polyline in segments of a given length.

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
        list[:class:`~compas.geometry.Point`]

        Notes
        -----
        The points of the new polyline are constrained to the segments of the old polyline.
        However, since the old points are not part of the new set of points, the geometry of the polyline will change.

        """
        num_pts = int(self.length / length)
        total_length = [0, 0]
        division_pts = [self.points[0]]
        new_polyline = self

        for i in range(num_pts):
            for i_ln, line in enumerate(new_polyline.lines):
                total_length.append(total_length[-1] + line.length)
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

        if strict is False and not self.is_closed() and len(division_pts) < num_pts + 1:
            division_pts.append(new_polyline.points[-1])
        elif strict is False and division_pts[-1].distance_to_point(self.points[-1]) > tol:
            division_pts.append(self.points[-1])

        return division_pts

    divide_by_length = divide_polyline_by_length

    def extend(self, length):
        """Extends a polyline by a given length, by modifying the first and/or last point tangentially.

        Parameters:
        -----------
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
        except TypeError:
            start = end = length
        self.points[-1] = self.points[-1] + self.lines[-1].vector.unitized().scaled(end)

    def extended(self, length):
        """Returns a copy of this polyline extended by a given length.

        Parameters:
        -----------
        length: float or tuple[float, float]
            A single length value to extend the polyline only at the end,
            or two length values to extend at both ends.

        Returns
        -------
        :class:`~compas.geometry.Polyline`

        """
        crv = self.copy()
        crv.extend(length)
        return crv

    def shorten(self, length):
        """Shortens a polyline by a given length.

        Parameters:
        -----------
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

    def shortened(self, length):
        """Returns a copy of this polyline shortened by a given length.

        Parameters:
        -----------
        length: float or tuple[float, float]
            A single length value to shorten the polyline only at the end,
            or two length values to shorten at both ends.

        Returns
        -------
        :class:`~compas.geometry.Polyline`

        """
        crv = self.copy()
        crv.shorten(length)
        return crv
