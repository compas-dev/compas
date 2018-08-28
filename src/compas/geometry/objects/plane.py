from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import orthonormalize_vectors

from compas.geometry.transformations import transform_points
from compas.geometry.transformations import transform_vectors

from compas.geometry.objects import Vector
from compas.geometry.objects import Point


__all__ = ['Plane']


class Plane(object):
    """A plane is defined by a base point and a normal vector.

    Parameters
    ----------
    point : point
        The base point of the plane.
    normal : vector
        The normal vector of the plane.

    Examples
    --------
    >>>

    Notes
    -----
    For more info on lines and linear equations, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Plane (geometry)*.
           Available at: https://en.wikipedia.org/wiki/Plane_(geometry).

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

        """
        normal = Vector.cross(u, v)
        return cls(point, normal)

    @classmethod
    def from_points(cls, points):
        """Construct the *best-fit* plane through more than three (non-coplanar) points.

        Parameters
        ----------
        points : list of point
            List of points.

        Returns
        -------
        Plane
            A plane that minimizes the distance to each point in the list.

        """
        raise NotImplementedError

    # ==========================================================================
    # descriptors
    # ==========================================================================

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

    # @property
    # def frame(self):
    #     """Frame: The frame that forms a basis for the local coordinates of all
    #     points in the half-spaces defined by the plane.
    #     """
    #     a, b, c = self.normal
    #     u = 1.0, 0.0, - a / c
    #     v = 0.0, 1.0, - b / c
    #     u, v = orthonormalize_vectors([u, v])
    #     u = Vector(*u)
    #     v = Vector(*v)
    #     u.unitize()
    #     v.unitize()
    #     return self.point, u, v

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
        raise NotImplementedError

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

        """
        cls = type(self)
        return cls(self.point.copy(), self.normal.copy())

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Plane`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        point = transform_points([self.point], matrix)
        normal = transform_vectors([self.normal], matrix)
        self.point.x = point[0]
        self.point.y = point[1]
        self.point.z = point[2]
        self.normal.x = normal[0]
        self.normal.y = normal[1]
        self.normal.z = normal[2]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    base = Point(1.0, 0.0, 0.0)
    normal = Vector(1.0, 1.0, 1.0)

    plane = Plane(base, normal)

    print(plane)
