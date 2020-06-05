from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import transform_points

from compas.geometry._primitives import Primitive
from compas.geometry._primitives import Point
from compas.geometry._primitives import Line


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

    __module__ = "compas.geometry"

    __slots__ = ["_points", "_lines"]

    def __init__(self, points):
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
        self._lines = [Line(self._points[i], self._points[i + 1]) for i in range(0, len(self._points) - 1)]

    @property
    def lines(self):
        """list of Line: The lines of the polyline."""
        return self._lines

    @property
    def length(self):
        """float : The length of the polyline."""
        return sum([line.length for line in self.lines])

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Polyline({})".format(", ".join(["{}".format(point) for point in self.points]))

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __iter__(self):
        return iter(self.points)

    def __eq__(self, other):
        return all(a == b for a, b in zip(self, other))

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
    # queries
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
        """Make a copy of this polyline.

        Returns
        -------
        :class:`compas.geometry.Polyline`
            The copy.

        Examples
        --------
        >>> p1 = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
        >>> p2 = p1.copy()
        >>> p1 == p2
        True
        >>> p1 is p2
        False
        """
        cls = type(self)
        return cls([point.copy() for point in self.points])

    # ==========================================================================
    # methods
    # ==========================================================================

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

    # ==========================================================================
    # transformations
    # ==========================================================================

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

    def transformed(self, T):
        """Return a transformed copy of this polyline.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation.

        Returns
        -------
        :class:`compas.geometry.Polyline`
            The transformed copy.

        Examples
        --------
        >>> from compas.geometry import Scale
        >>> p1 = Polyline([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
        >>> S = Scale([1.0, 1.0, 1.0])
        >>> p2 = p1.transformed(S)
        >>> p1 == p2
        True
        >>> p1 is p2
        False
        """
        polyline = self.copy()
        polyline.transform(T)
        return polyline
    
    def shorten(self, start_distance=0, end_distance=0):
        """Returns a new polyline which is shorter than the original in one end side, other or both by a given distance
        
        Parameters
        ----------
        start_distance : float.
            distance to shorten from the starting point of the polyline
        end_distance : float.
            distance to shorten from the ending point of the polyline

        Returns
        -------
        :class:`compas.geometry.Polyline`
            The transformed copy.
        """
        if start_distance !=0 or end_distance!=0:
            points=[]
            acum_length=0
            switch=True
            for i, line in enumerate(self.lines):
                acum_length += line.length
                if acum_length < start_distance:
                    continue
                elif acum_length > start_distance and switch:
                    if start_distance == 0:
                        points.append(line.start)
                    else:
                        points.append(self.point(start_distance/self.length))
                    switch=False
                else:
                    if end_distance==0:
                        if i!= len(self.lines)-1:
                            points.append(line.start)
                        else:
                            points.append(line.start)
                            points.append(line.end)
                    else:
                        if acum_length < (self.length - end_distance):
                            points.append(line.start)
                        else:
                            points.append(line.start)
                            points.append(self.point(1-(end_distance/self.length)))
                            break
            return points
        return self

    def rebuild(self, number=20, decimals=100000):
        """Reconstructs a polyline with evenly spaced points based on a number of interpolations
        Returns new rebuilt polyline

        Parameters
        ----------
        number : integer.
            number of points for the amount of definition of the polyline

        Returns
        -------
        list of equally spaced points on the polyline
        """
        points = [self.point(i * float(1/ number)) for i in range(number)]
        points.append(self.point(1))
        point_list = [Point(x,y,z) for x,y,z in points]
        polyline = self.copy
        polyline.points(point_list)
        return polyline
    
    def divide_by_count(self, number =10, includeEnds= False):
        """Divides a polyline by count. Returns list of Points from the division

        Parameters
        ----------
        number : integer.
            number of divisions
        includeEnds : boolean
            True if including start and ending points.
            False if not including start and ending points.

        Returns
        -------
        points : list of points resulting from dividing the polyline
        """
        points = [self.point(i * float(1/ number)) for i in range(number)]
        if includeEnds:
            points.append(self.point(1))
        else:
            points.pop(0)
        return points
    
    def tween(self, polyline_two, number=50):
        """Creates an average polyline between two polylines interpolating their points

        Parameters
        ----------
        polyline_two : compas.geometry.Polyline
            polyline to create the tween polyline
        number : number of points of the tween polyline

        Returns
        -------
        list of compas.geometry.Point
        """
        rebuilt_polyline_one = self.rebuild(number)
        rebuilt_polyline_two = polyline_two.rebuild(number)
        lines = [Line(point_one, point_two) for point_one, point_two in zip(rebuilt_polyline_one, rebuilt_polyline_two)]
        return [line.midpoint for line in lines]

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest

    doctest.testmod(globs=globals())
