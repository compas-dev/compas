from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import matrix_from_frame
from compas.geometry import transform_points
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Plane

from compas.geometry.shapes import Shape

__all__ = ['Cylinder']


class Cylinder(Shape):
    """A cylinder is defined by a circle and a height.

    Parameters
    ----------
    circle: :class:`compas.geometry.Circle`
        The circle of the cylinder.
    height: float
        The height of the cylinder.

    Attributes
    ----------
    plane : :class:`compas.geometry.Plane`
        The plane containing the circle.
    circle : :class:`compas.geometry.Circle`
        The base circle of the cylinder.
    radius : float
        The radius of the base circle.
    height : float
        The height of the cylinder.
    normal (read-only) : :class:`compas.geometry.Vector`
        The normal of the base plane.
    diameter : float
        The diameter of the cylinder.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cylinder = Cylinder(circle, 7)

    """

    __slots__ = ['_circle', '_height']

    def __init__(self, circle, height):
        super(Cylinder, self).__init__()
        self._circle = None
        self._height = None
        self.circle = circle
        self.height = height

    @property
    def data(self):
        """Returns the data dictionary that represents the cylinder.

        Returns
        -------
        dict
            The cylinder data.

        """
        return {'circle': self.circle.data,
                'height': self.height}

    @data.setter
    def data(self, data):
        self.circle = Circle.from_data(data['circle'])
        self.height = data['height']

    @property
    def plane(self):
        """Plane: The plane of the cylinder."""
        return self.circle.plane

    @plane.setter
    def plane(self, plane):
        self.circle.plane = Plane(plane[0], plane[1])

    @property
    def circle(self):
        """float: The circle of the cylinder."""
        return self._circle

    @circle.setter
    def circle(self, circle):
        self._circle = Circle(circle[0], circle[1])

    @property
    def radius(self):
        """float: The radius of the cylinder."""
        return self.circle.radius

    @radius.setter
    def radius(self, radius):
        self.circle.radius = float(radius)

    @property
    def height(self):
        """float: The height of the cylinder."""
        return self._height

    @height.setter
    def height(self, height):
        self._height = float(height)

    @property
    def normal(self):
        """Vector: The normal of the cylinder."""
        return self.plane.normal

    @property
    def diameter(self):
        """float: The diameter of the cylinder."""
        return self.circle.diameter

    @property
    def center(self):
        """Point: The center of the cylinder."""
        return self.circle.center

    @center.setter
    def center(self, point):
        self.circle.center = point

    @property
    def area(self):
        """Float: The surface area of the cylinder."""
        return (self.circle.area * 2) + (self.circle.circumference * self.height)

    @property
    def volume(self):
        """Float: The volume of the cylinder."""
        return self.circle.area * self.height

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Cylinder({0}, {1})'.format(self.circle, self.height)

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
        """Construct a cylinder from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Cylinder
            The constructed cylinder.

        Examples
        --------
        >>> from compas.geometry import Cylinder
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
        >>> cylinder = Cylinder.from_data(data)

        """
        cylinder = cls(Circle(Plane.worldXY(), 1), 1)
        cylinder.data = data
        return cylinder

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

        vertices = []
        a = 2 * pi / u
        z = self.height / 2
        for i in range(u):
            x = self.circle.radius * cos(i * a)
            y = self.circle.radius * sin(i * a)
            vertices.append([x, y, z])
            vertices.append([x, y, -z])
        # add v in bottom and top's circle center
        vertices.append([0, 0, z])
        vertices.append([0, 0, -z])

        # transform vertices to cylinder's plane
        frame = Frame.from_plane(self.circle.plane)
        M = matrix_from_frame(frame)
        vertices = transform_points(vertices, M)

        faces = []
        # side faces
        for i in range(0, u * 2, 2):
            faces.append([i, i + 1, (i + 3) % (u * 2), (i + 2) % (u * 2)])
        # top and bottom circle faces
        for i in range(0, u * 2, 2):
            top = [i, (i + 2) % (u * 2), len(vertices) - 2]
            bottom = [i + 1, (i + 3) % (u * 2), len(vertices) - 1]
            faces.append(top)
            faces.append(bottom[::-1])

        return vertices, faces

    def transform(self, transformation):
        """Transform the cylinder.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the cylinder.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Cylinder
        >>> circle = Circle(Plane.worldXY(), 5)
        >>> cylinder = Cylinder(circle, 7)
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(frame)
        >>> cylinder.transform(T)

        """
        self.circle.transform(transformation)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod()
