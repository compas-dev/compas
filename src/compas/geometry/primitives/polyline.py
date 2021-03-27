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


__all__ = ['Polyline']


class Polyline(Primitive):
    """A polyline is a sequence of points connected by line segments.

    A polyline is a piecewise linear element.
    It does not have an interior.
    It can be open or closed.
    It can be self-intersecting.

    Parameters
    ----------
    points : list of point
        An ordered list of points.
        Each consecutive pair of points forms a segment of the polyline.

    Attributes
    ----------
    data : dict
        The data representation of the polyline.
    points : list of :class:`compas.geometry.Point`
        The polyline points.
    lines : list of :class:`compas.geometry.Line`, read-only
        The polyline segments.
    length : float, read-only
        The length of the polyline.

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

    def __init__(self, points):
        super(Polyline, self).__init__()
        self._points = []
        self._lines = []
        self.points = points

    @property
    def data(self):
        """Returns the data dictionary that represents the polyline.

        Returns
        -------
        dict
            The polyline's data.
        """
        return {'points': [list(point) for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = data['points']

    @property
    def points(self):
        """list of Point: The points of the polyline."""
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*xyz) for xyz in points]
        self._lines = None

    # consider caching below based on point setter

    @property
    def lines(self):
        """list of :class:`compas.geometry.Line` : The lines of the polyline."""
        if not self._lines:
            self._lines = [Line(a, b) for a, b in pairwise(self.points)]
        return self._lines

    @property
    def length(self):
        """float : The length of the polyline."""
        return sum([line.length for line in self.lines])

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Polyline([{}])".format(", ".join(["{}".format(point) for point in self.points]))

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
        if not hasattr(other, '__iter__') or not hasattr(other, '__len__') or len(self) != len(other):
            return False
        return allclose(self, other)

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a polyline from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Polyline`
            The constructed polyline.

        Examples
        --------
        >>> polyline = Polyline.from_data({'points': [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]})
        >>> polyline
        Polyline(Point(0.000, 0.000, 0.000), Point(1.000, 0.000, 0.000), Point(1.000, 1.000, 0.000))
        """
        return cls(data['points'])

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
        Point
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
        T : :class:`compas.geometry.Transformation` or list of list
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

        Parameters:
        -----------
        angle_threshold : float
            In radians.

        Returns
        -------
        list of :class:`compas.geometry.Polyline`

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
                corner_ids.append(seg1+1)

        if self.is_closed() and len(corner_ids) > 0:
            if corner_ids[-1] != len(points):
                corner_ids = [corner_ids[-1]] + corner_ids
        else:
            corner_ids = [0] + corner_ids + [len(points)]

        for id1, id2 in pairwise(corner_ids):
            if id1 < id2:
                split_polylines.append(Polyline(points[id1:id2+1]))
            else:
                looped_pts = [points[i] for i in range(id1, len(points))] + points[1:id2+1]
                split_polylines.append(Polyline(looped_pts))

        if self.is_closed() and not corner_ids:
            return [Polyline(self.points)]

        return split_polylines

    def tangent_at_point_on_polyline(self, point):
        """Calculates the tangent vector of a point on a polyline

        Parameters:
        -----------
        point: :class:`compas.geometry.Point`

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        for line in self.lines:
            if is_point_on_line(point, line):
                return line.direction
        raise Exception('{} not found!'.format(point))

    def divide_polyline(self, num_segments):
        """Divide a polyline in equal segments.

        Parameters:
        -----------
        num_segments : int

        Returns
        -------
        list
            list of :class:`compas.geometry.Point`
        """
        segment_length = self.length/num_segments

        return self.divide_polyline_by_length(segment_length, False)

    def divide_polyline_by_length(self, length, strict=True):
        """Splits a polyline in segments of a given length

        Parameters:
        -----------
        length : float

        strict : bool
            If set to ``False``, the remainder segment will be added even if it is smaller than the desired length

        Returns
        -------
        list
            list of :class:`compas.geometry.Point`
        """
        num_pts = int(self.length/length)
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
                    remaining_pts = new_polyline.points[i_ln+2:]
                    new_polyline = Polyline([new_pt, line.end] + remaining_pts)
                    break
                elif total_length[-1] == length:
                    total_length = [0, 0]
                    division_pts.append(line.end)

            if len(division_pts) == num_pts+1:
                break

        if strict is False and not self.is_closed() and len(division_pts) < num_pts+1:
            division_pts.append(new_polyline.points[-1])
        elif strict is False and division_pts[-1] != self.points[-1]:
            division_pts.append(self.points[-1])

        return division_pts
# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
