from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Point

from compas.geometry._shapes import Shape

__all__ = ['Sphere']


class Sphere(Shape):
    """A sphere is defined by a point and a radius.

    Parameters
    ----------
    point: :class:`compas.geometry.Point` list of float
        The center of the sphere.
    radius: float
        The radius of the sphere.

    Attributes
    ----------
    point: :class:`compas.geometry.Point`
        The center of the sphere.
    radius: float
        The radius of the sphere.
    center (read-only): :class:`compas.geometry.Point`
        The center of the sphere.
    area (read-only): float
        The surface area of the sphere.
    volume (read-only): float
        The volume of the sphere.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Sphere
    >>> sphere1 = Sphere(Point(1, 1, 1), 5)
    >>> sphere2 = Sphere((2, 4, 1), 2)
    >>> sphere3 = Sphere([2, 4, 1], 2)
    """

    __module__ = "compas.geometry"

    __slots__ = ['_point', '_radius']

    def __init__(self, point, radius):
        self._point = None
        self._radius = None
        self.point = point
        self.radius = radius

    @classmethod
    def from_data(cls, data):
        """Construct a sphere from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Sphere
            The constructed sphere.

        Examples
        --------
        >>> from compas.geometry import Sphere
        >>> data = {'point': [1., 2., 3.], 'radius': 4.}
        >>> sphere = Sphere.from_data(data)

        """
        sphere = cls([0, 0, 0], 1)
        sphere.data = data
        return sphere

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def point(self):
        """Point: The center of the sphere."""
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def radius(self):
        """float: The radius of the sphere."""
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def center(self):
        return self.point

    @property
    def area(self):
        """float: The surface area of the sphere."""
        return 4 * pi * self.radius**2

    @property
    def volume(self):
        """float: The volume of the sphere."""
        return 4./3. * pi * self.radius**3

    @property
    def data(self):
        """Returns the data dictionary that represents the sphere.

        Returns
        -------
        dict
            The sphere data.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere(Point(1, 1, 1), 5)
        >>> sdict = {'point': [1., 1., 1.], 'radius': 5.}
        >>> sdict == sphere.data
        True

        """
        return {'point': list(self.point),
                'radius': self.radius}

    @data.setter
    def data(self, data):
        self.point = data['point']
        self.radius = data['radius']

    def to_data(self):
        """Returns the data dictionary that represents the sphere.

        Returns
        -------
        dict
            The sphere data.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere(Point(1, 1, 1), 5)
        >>> sdict = {'point': [1., 1., 1.], 'radius': 5.}
        >>> sdict == sphere.to_data()
        True

        """
        return self.data

    def to_vertices_and_faces(self, **kwargs):
        """Returns a list of vertices and faces"""

        u = kwargs.get('u') or 10
        v = kwargs.get('v') or 10
        if u < 3:
            raise ValueError('The value for u should be u > 3.')
        if v < 3:
            raise ValueError('The value for v should be v > 3.')

        theta = pi / v
        phi = pi*2 / u
        hpi = pi * 0.5

        vertices = []
        for i in range(1, v):
            for j in range(u):
                tx = self.radius * cos(i * theta - hpi) * cos(j * phi) + self.point.x
                ty = self.radius * cos(i * theta - hpi) * sin(j * phi) + self.point.y
                tz = self.radius * sin(i * theta - hpi) + self.point.z
                vertices.append([tx, ty, tz])

        vertices.append([self.point.x, self.point.y, self.point.z + self.radius])
        vertices.append([self.point.x, self.point.y, self.point.z - self.radius])

        faces = []

        # south pole triangle fan
        sp = len(vertices) - 1
        for j in range(u):
            faces.append([sp, (j+1) % u, j])

        for i in range(v-2):
            for j in range(u):
                jj = (j + 1) % u
                a = i * u + j
                b = i * u + jj
                c = (i + 1) * u + jj
                d = (i + 1) * u + j
                faces.append([a, b, c, d])

        # north pole triangle fan
        np = len(vertices) - 2
        for j in range(u):
            nc = len(vertices) - 3 - j
            nn = len(vertices) - 3 - (j + 1) % u
            faces.append([np, nn, nc])

        return vertices, faces

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Sphere({0}, {1})'.format(self.point, self.radius)

    def __len__(self):
        return 2

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.point
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.point, self.radius])

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Makes a copy of this ``Sphere``.

        Returns
        -------
        Sphere
            The copy.

        Examples
        --------
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere(Point(1, 1, 1), 5)
        >>> sphere_copy = sphere.copy()

        """
        cls = type(self)
        return cls(self.point.copy(), self.radius)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the sphere.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Sphere.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere(Point(1, 1, 1), 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> sphere.transform(T)

        """
        self.point.transform(transformation)

    def transformed(self, transformation):
        """Returns a transformed copy of the current sphere.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Sphere.

        Returns
        -------
        :class:`Sphere`
            The transformed sphere.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere(Point(1, 1, 1), 5)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> sphere_transformed = sphere.transformed(T)

        """
        sphere = self.copy()
        sphere.transform(transformation)
        return sphere


if __name__ == '__main__':
    from compas.geometry import Frame
    from compas.geometry import Transformation
    sphere = Sphere(Point(1, 1, 1), 5)
    frame = Frame([5, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(frame)
    sphere.transform(T)
    print(sphere)

    sphere = Sphere(Point(1, 1, 1), 5)
    print(sphere.data)
    print(sphere)
    sphere = Sphere.from_data(sphere.data)
    print(sphere)

    import doctest
    doctest.testmod()
