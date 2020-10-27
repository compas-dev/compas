from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin
from math import sqrt

from compas.utilities import pairwise

from compas.geometry import matrix_from_frame
from compas.geometry import transform_points
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane

from ._shape import Shape


__all__ = ['Cone']


class Cone(Shape):
    """A cone is defined by a circle and a height.

    Parameters
    ----------
    circle : tuple or :class:`compas.geometry.Circle`
        The base circle of the cone.
    height : float
        The height of the cone.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane containing the circle.
    circle : :class:`compas.geometry.Circle`
        The base circle of the cone.
    radius : float
        The radius of the base circle.
    height : float
        The height of the cone.
    normal (read-only) : :class:`compas.geometry.Vector`
        The normal of the base plane.
    diameter : float
        The diameter of the cone.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cone
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cone = Cone(circle, 7)

    """

    __slots__ = ['_circle', '_height']

    def __init__(self, circle, height):
        super(Cone, self).__init__()
        self._circle = None
        self._height = None
        self.circle = circle
        self.height = height

    @property
    def data(self):
        """Returns the data dictionary that represents the cone.

        Returns
        -------
        dict
            The cone data.

        """
        return {'circle': self.circle.data, 'height': self.height}

    @data.setter
    def data(self, data):
        self.circle = Circle.from_data(data['circle'])
        self.height = data['height']

    @property
    def plane(self):
        """Plane: The plane of the cone."""
        return self.circle.plane

    @plane.setter
    def plane(self, plane):
        self.circle.plane = Plane(plane[0], plane[1])

    @property
    def circle(self):
        """float: The circle of the cone."""
        return self._circle

    @circle.setter
    def circle(self, circle):
        self._circle = Circle(circle[0], circle[1])

    @property
    def radius(self):
        """float: The radius of the cone."""
        return self.circle.radius

    @radius.setter
    def radius(self, radius):
        self.circle.radius = float(radius)

    @property
    def height(self):
        """float: The height of the cone."""
        return self._height

    @height.setter
    def height(self, height):
        self._height = float(height)

    @property
    def normal(self):
        """Vector: The normal of the cone."""
        return self.plane.normal

    @property
    def diameter(self):
        """float: The diameter of the cone."""
        return self.circle.diameter

    @property
    def center(self):
        """Point: The center of the cone."""
        return self.circle.center

    @center.setter
    def center(self, point):
        self.circle.center = point

    @property
    def area(self):
        """Float: The surface area of the cone."""
        r = self.circle.radius
        return pi * r * (r + sqrt(self.height**2 + r**2))

    @property
    def volume(self):
        """Float: The volume of the cone."""
        return pi * self.circle.radius**2 * (self.height / 3)

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Cone({0}, {1})'.format(self.circle, self.height)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.circle
        elif key == 1:
            return self.height
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.circle = value
        elif key == 1:
            self.height = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.circle, self.height])

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a cone from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Cone
            The constructed cone.

        Examples
        --------
        >>> from compas.geometry import Cone
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
        >>> cone = Cone.from_data(data)

        """
        cone = cls(Circle(Plane.worldXY(), 1), 1)
        cone.data = data
        return cone

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=10):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.

        Returns
        -------
        (vertices, faces)
            A list of vertex locations and a list of faces,
            with each face defined as a list of indices into the list of vertices.
        """
        if u < 3:
            raise ValueError('The value for u should be u > 3.')

        vertices = [[0, 0, 0]]
        a = 2 * pi / u
        for i in range(u):
            x = self.circle.radius * cos(i * a)
            y = self.circle.radius * sin(i * a)
            vertices.append([x, y, 0])
        vertices.append([0, 0, self.height])

        frame = Frame.from_plane(self.circle.plane)
        M = matrix_from_frame(frame)
        vertices = transform_points(vertices, M)

        faces = []
        first = 0
        last = len(vertices) - 1
        for i, j in pairwise(range(1, last)):
            faces.append([i, j, last])
            faces.append([j, i, first])
        faces.append([last - 1, 1, last])
        faces.append([1, last - 1, first])

        return vertices, faces

    def transform(self, transformation):
        """Transform the cone.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the cone.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Cone
        >>> from compas.geometry import Circle
        >>> circle = Circle(Plane.worldXY(), 5)
        >>> cone = Cone(circle, 7)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> cone.transform(T)

        """
        self.circle.transform(transformation)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    # from compas.geometry import Transformation

    # cone = Cone(Circle(Plane.worldXY(), 5), 7)
    # frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    # print(frame.normal)
    # T = Transformation.from_frame(frame)
    # cone.transform(T)
    # print(cone)

    # print(Plane.worldXY().data)
    # data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
    # cone = Cone.from_data(data)
    # print(cone)

    import doctest
    doctest.testmod()
