from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Plane

__all__ = ['Circle']


class Circle(Primitive):
    """A circle is defined by a plane and a radius.

    Attributes
    ----------
    data
    plane
    radius
    normal
    diameter
    center
    area
    circumference

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Circle
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    """

    __slots__ = ['_plane', '_radius']

    def __init__(self, plane, radius):
        self._plane = None
        self._radius = None
        self.plane = plane
        self.radius = radius

    @classmethod
    def from_data(cls, data):
        """Construct a circle from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Circle
            The constructed circle.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> data = {'plane': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 'radius': 5.}
        >>> circle = Circle.from_data(data)
        """
        return cls(data['plane'], data['radius'])

    def to_data(self):
        """Returns the data dictionary that represents the circle.

        Returns
        -------
        dict
            The circle data.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Point
        >>> from compas.geometry import Vector
        >>> circle = Circle(Plane(Point(0.0, 0.0, 0.0), Vector(0.0, 0.0, 1.0)), 1.0)
        >>> circle.to_data()
        {'plane': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 'radius': 1.0}
        """
        return self.data

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def data(self):
        """Returns the data dictionary that represents the circle.

        Returns
        -------
        dict
            The circle data.
        """
        return {'plane': [list(self.plane.point), list(self.plane.normal)], 'radius': self.radius}

    @data.setter
    def data(self, data):
        self.plane = data['plane']
        self.radius = data['radius']

    @property
    def plane(self):
        """Plane: The plane of the circle."""
        return self._plane

    @plane.setter
    def plane(self, plane):
        self._plane = Plane(plane[0], plane[1])

    @property
    def radius(self):
        """float: The radius of the circle."""
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def normal(self):
        """Vector: The normal of the circle."""
        return self.plane.normal

    @property
    def diameter(self):
        """float: The diameter of the circle."""
        return self.radius * 2

    @property
    def center(self):
        """Point: The center of the circle."""
        return self.plane.point

    @center.setter
    def center(self, point):
        self.plane.point = point

    @property
    def area(self):
        """Float: The area of the circle."""
        return pi * (self.radius**2)

    @property
    def circumference(self):
        """Float: The circumference of the circle."""
        return 2 * pi * self.radius

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Circle({0}, {1})'.format(self.plane, self.radius)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.plane
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.plane = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.plane, self.radius])

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Makes a copy of this ``Circle``.

        Returns
        -------
        Circle
            The copy.

        Examples
        --------
        >>> c1 = Circle([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], 1.0)
        >>> c2 = c1.copy()
        >>> c1 == c2
        False
        """
        cls = type(self)
        return cls(self.plane.copy(), self.radius)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the circle.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the circle.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> circle = Circle(Plane.worldXY(), 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> circle.transform(T)
        """
        self.plane.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current circle.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the circle.

        Returns
        -------
        :class:`circle`
            The transformed circle.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> circle = Circle(Plane.worldXY(), 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> circle_transformed = circle.transformed(T)
        """
        circle = self.copy()
        circle.transform(transformation)
        return circle


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
