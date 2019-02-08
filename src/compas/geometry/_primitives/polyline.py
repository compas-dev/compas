from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from compas.geometry.transformations import transform_points

from compas.geometry.distance import distance_point_point

from compas.geometry._primitives import Point
from compas.geometry._primitives import Line


__all__ = ['Polyline']


class Polyline(object):
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

    Examples
    --------
    >>> polyline = Polyline([[0,0,0], [1,0,0], [2,0,0], [3,0,0]])
    >>> polyline.length
    3.0

    >>> type(polyline.points[0])
    <class 'point.Point'>
    >>> polyline.points[0].x
    0.0

    >>> type(polyline.lines[0])
    <class 'line.Line'>
    >>> polyline.lines[0].length
    1.0

    """
    __slots__ = ['_points', '_lines', '_p', '_l']

    def __init__(self, points):
        self._points = []
        self._lines = []
        self._p = 0
        self._l = 0
        self.points = points

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def points(self):
        """list of Point: The points of the polyline."""
        return self._points

    @points.setter
    def points(self, points):
        self._points = [Point(*xyz) for xyz in points]
        self._p = len(points)
        self._lines = [Line(self._points[i], self._points[i + 1]) for i in range(0, self._p - 1)]
        self._l = len(self._lines)

    @property
    def lines(self):
        """list of Line: The lines of the polyline."""
        return self._lines

    @property
    def p(self):
        """int: The number of points."""
        return self._p

    @property
    def l(self):
        """int: The number of lines."""
        return self._l

    @property
    def length(self):
        """float: The length of the polyline."""
        return sum([line.length for line in self.lines])

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Polyline({0})'.format(", ".join(map(lambda point: format(point, ""), self.points)))

    def __len__(self):
        return self.p

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key < self.p:
            return self.points[key]
        raise KeyError

    def __setitem__(self, key, value):
        if key < self.p:
            self.points[key] = value
            return
        raise KeyError

    def __iter__(self):
        return iter(self.points)

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        raise NotImplementedError

    # ==========================================================================
    # queries
    # ==========================================================================

    def point(self, t, snap = False):
        """Point: The point from the start to the end at a specific normalized parameter.
        If snap is True, return the closest polyline point."""

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

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Polyline``.

        Returns
        -------
        Polyline
            The copy.

        """
        cls = type(self)
        return cls([point.copy() for point in self.points])

    # ==========================================================================
    # methods
    # ==========================================================================

    def is_selfintersecting(self):
        """Determine if the polyline is self-intersecting.
        """
        raise NotImplementedError

    def is_closed(self):
        """Determine if the polyline is closed.

        Returns
        -------
        bool
            True if the polyline is closed, False otherwise.

        """
        return self.points[0] == self.points[-1]

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Polyline`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        for index, point in enumerate(transform_points(self.points, matrix)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]

    def transformed(self, matrix):
        """Return a transformed copy of this ``Polyline`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Polyline
            The transformed copy.

        """
        polyline = self.copy()
        polyline.transform(matrix)
        return polyline


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from math import pi

    from compas.geometry import matrix_from_axis_and_angle
    from compas.plotters import Plotter


    M = matrix_from_axis_and_angle([0, 0, 1.0], pi / 2)
    p = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]])
    q = p.transformed(M)

    #plotter = Plotter(figsize=(10, 7))

    #plotter.draw_polygons([{'points': p.points}, {'points': q.points}])
    #plotter.show()

    print(p.point(.7, snap = True))
