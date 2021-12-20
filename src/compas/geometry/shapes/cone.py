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


class Cone(Shape):
    """A cone is defined by a circle and a height.

    Parameters
    ----------
    circle : tuple or :class:`compas.geometry.Circle`
        The base circle of the cone.
    height : float
        The height of the cone.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cone
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cone = Cone(circle, 7)

    """

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` - Schema of the data representation."""
        import schema
        return schema.Schema({
            'circle': {
                'plane': Plane.DATASCHEMA.fget(None),
                'radius': schema.And(float, lambda x: x > 0)
            },
            'height': schema.And(float, lambda x: x > 0)
        })

    @property
    def JSONSCHEMANAME(self):
        """str - Name of the  schema of the data representation in JSON format."""
        return 'cone'

    __slots__ = ['_circle', '_height']

    def __init__(self, circle, height, **kwargs):
        super(Cone, self).__init__(**kwargs)
        self._circle = None
        self._height = None
        self.circle = circle
        self.height = height

    @property
    def data(self):
        """dict - Returns the data dictionary that represents the cone.
        """
        return {'circle': self.circle.data, 'height': self.height}

    @data.setter
    def data(self, data):
        self.circle = Circle.from_data(data['circle'])
        self.height = data['height']

    @property
    def plane(self):
        """:class:`Plane` - The plane of the cone."""
        return self.circle.plane

    @plane.setter
    def plane(self, plane):
        self.circle.plane = Plane(*plane)

    @property
    def circle(self):
        """float - The circle of the cone."""
        return self._circle

    @circle.setter
    def circle(self, circle):
        self._circle = Circle(*circle)

    @property
    def radius(self):
        """float - The radius of the cone."""
        return self.circle.radius

    @radius.setter
    def radius(self, radius):
        self.circle.radius = float(radius)

    @property
    def height(self):
        """float - The height of the cone."""
        return self._height

    @height.setter
    def height(self, height):
        self._height = float(height)

    @property
    def normal(self):
        """:class:`Vector` (read-only) - The normal of the cone."""
        return self.plane.normal

    @property
    def diameter(self):
        """float (read-only) - The diameter of the cone."""
        return self.circle.diameter

    @property
    def center(self):
        """:class:`Point` - The center of the cone."""
        return self.circle.center

    @center.setter
    def center(self, point):
        self.circle.center = point

    @property
    def area(self):
        """float (read-only) - The surface area of the cone."""
        r = self.circle.radius
        return pi * r * (r + sqrt(self.height**2 + r**2))

    @property
    def volume(self):
        """float (read-only) - The volume of the cone."""
        return pi * self.circle.radius**2 * (self.height / 3)

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return 'Cone({0!r}, {1!r})'.format(self.circle, self.height)

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
        :class:`Cone`
            The constructed cone.

        Examples
        --------
        >>> from compas.geometry import Cone
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
        >>> cone = Cone.from_data(data)

        """
        cone = cls(Circle.from_data(data['circle']), data['height'])
        return cone

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, triangulated=False):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
        triangulated: bool, optional
            Flag indicating that the faces have to be triangulated.

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
        radius = self.circle.radius
        for i in range(u):
            x = radius * cos(i * a)
            y = radius * sin(i * a)
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

        if triangulated:
            triangles = []
            for face in faces:
                if len(face) == 4:
                    triangles.append(face[0:3])
                    triangles.append([face[0], face[2], face[3]])
                else:
                    triangles.append(face)
            faces = triangles

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
