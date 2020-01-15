from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Vector
from compas.geometry.primitives import Point


__all__ = ['Plane']


class Plane(Primitive):
    """A plane is defined by a base point and a normal vector.

    Parameters
    ----------
    point : point
        The base point of the plane.
    normal : vector
        The normal vector of the plane.

    Notes
    -----
    For more info on lines and linear equations, see [1]_.

    References
    ----------
    .. [1] `Wikipedia: Plane (geometry) <https://en.wikipedia.org/wiki/Plane_%28geometry%29>`_

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> plane.point
    Point(0.000, 0.000, 0.000)
    >>> plane.normal
    Vector(0.000, 0.000, 1.000)
    """

    __slots__ = ['_point', '_normal']

    def __init__(self, point, normal):
        self._point = None
        self._normal = None
        self.point = point
        self.normal = normal

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def from_three_points(cls, a, b, c):
        """Construct a plane from three points in three-dimensional space.

        Parameters
        ----------
        a : point
            The first point.
        b : point
            The second point.
        c : point
            The second point.

        Returns
        -------
        Plane
            A plane with base point ``a`` and normal vector defined as the unitized
            cross product of the vectors ``ab`` and ``ac``.

        Examples
        --------
        >>> plane = Plane.from_three_points([0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0])
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)
        """
        a = Point(*a)
        b = Point(*b)
        c = Point(*c)
        normal = Vector.cross(b - a, c - a)
        return cls(a, normal)

    @classmethod
    def from_point_and_two_vectors(cls, point, u, v):
        """Construct a plane from a base point and two vectors.

        Parameters
        ----------
        point : point
            The base point.
        u : vector
            The first vector.
        v : vector
            The second vector.

        Returns
        -------
        Plane
            A plane with base point ``point`` and normal vector defined as the unitized
            cross product of vectors ``u`` and ``v``.

        Examples
        --------
        >>> plane = Plane.from_three_points([0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0])
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)
        """
        normal = Vector.cross(u, v)
        return cls(point, normal)

    @classmethod
    def worldXY(cls):
        """Construct the world XY plane.

        Returns
        -------
        Plane
            The world XY plane.

        """
        return cls([0, 0, 0], [0, 0, 1])

    @classmethod
    def from_data(cls, data):
        """Construct a plane from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Plane
            The constructed plane.

        Examples
        --------
        >>> plane = Plane.from_data({'point': [0.0, 0.0, 0.0], 'normal': [0.0, 0.0, 1.0]})
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)
        """
        return cls(data['point'], data['normal'])

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def data(self):
        """Returns the data dictionary that represents the plane.

        Returns
        -------
        dict
            The plane data.

        """
        return {'point': list(self.point),
                'normal': list(self.normal)}

    @data.setter
    def data(self, data):
        self.point = data['point']
        self.normal = data['normal']

    @property
    def point(self):
        """Point: The base point of the plane."""
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def normal(self):
        """Vector: The normal vector of the plane."""
        return self._normal

    @normal.setter
    def normal(self, vector):
        self._normal = Vector(*vector)
        self._normal.unitize()

    @property
    def d(self):
        """:obj:`float`: The *d* parameter of the linear equation describing the plane."""
        a, b, c = self.normal
        x, y, z = self.point
        return - a * x - b * y - c * z

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Plane({0}, {1})'.format(self.point, self.normal)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.point
        if key == 1:
            return self.normal
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.normal = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.point, self.normal])

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        return self.point == other[0] and self.normal == other[1]

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
        """Make a copy of this ``Plane``.

        Returns
        -------
        Plane
            The copy.

        Examples
        --------
        >>> p1 = Plane.worldXY()
        >>> p2 = p1.copy()
        >>> p2.point.x += 1.0
        >>> p2 == p1
        False
        """
        cls = type(self)
        return cls(self.point.copy(), self.normal.copy())

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform this ``Plane`` using a given ``Transformation``.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the plane.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f)
        >>> plane = Plane.worldXY()
        >>> plane.transform(T)
        """
        self.point.transform(transformation)
        self.normal.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current plane.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the plane.

        Returns
        -------
        :class:`Plane`
            The transformed plane.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f)
        >>> p1 = Plane.worldXY()
        >>> p2 = p1.transformed(T)
        """
        plane = self.copy()
        plane.transform(transformation)
        return plane


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
