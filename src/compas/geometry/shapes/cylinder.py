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

from ._shape import Shape


class Cylinder(Shape):
    """A cylinder is defined by a circle and a height.

    Parameters
    ----------
    circle: [plane, radius] | :class:`~compas.geometry.Circle`
        The circle of the cylinder.
    height: float
        The height of the cylinder.

    Attributes
    ----------
    plane : :class:`~compas.geometry.Plane`
        The plane of the cylinder.
    circle : :class:`~compas.geometry.Circle`
        The circle of the cylinder.
    center : :class:`~compas.geometry.Point`
        The center of the cylinder.
    radius : float
        The radius of the cylinder.
    height : float
        The height of the cylinder.
    normal : :class:`~compas.geometry.Vector`, read-only
        The normal of the cylinder.
    diameter : float, read-only
        The diameter of the cylinder.
    area : float, read-only
        The surface area of the cylinder.
    volume : float, read-only
        The volume of the cylinder.

    Examples
    --------
    >>> from compas.geometry import Plane
    >>> from compas.geometry import Cylinder
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> circle = Circle(plane, 5)
    >>> cylinder = Cylinder(circle, 7)

    """

    __slots__ = ["_circle", "_height"]

    def __init__(self, circle, height, **kwargs):
        super(Cylinder, self).__init__(**kwargs)
        self._circle = None
        self._height = None
        self.circle = circle
        self.height = height

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema

        return schema.Schema(
            {
                "circle": {
                    "plane": Plane.DATASCHEMA.fget(None),
                    "radius": schema.And(float, lambda x: x > 0),
                },
                "height": schema.And(float, lambda x: x > 0),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "cylinder"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the cylinder."""
        return {"circle": self.circle.data, "height": self.height}

    @data.setter
    def data(self, data):
        self.circle = Circle.from_data(data["circle"])
        self.height = data["height"]

    @classmethod
    def from_data(cls, data):
        """Construct a cylinder from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Cylinder`
            The constructed cylinder.

        Examples
        --------
        >>> from compas.geometry import Cylinder
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Plane
        >>> data = {'circle': Circle(Plane.worldXY(), 5).data, 'height': 7.}
        >>> cylinder = Cylinder.from_data(data)

        """
        cylinder = cls(Circle.from_data(data["circle"]), data["height"])
        return cylinder

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def plane(self):
        return self.circle.plane

    @plane.setter
    def plane(self, plane):
        self.circle.plane = Plane(*plane)

    @property
    def circle(self):
        return self._circle

    @circle.setter
    def circle(self, circle):
        self._circle = Circle(*circle)

    @property
    def radius(self):
        return self.circle.radius

    @radius.setter
    def radius(self, radius):
        self.circle.radius = float(radius)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = float(height)

    @property
    def normal(self):
        return self.plane.normal

    @property
    def diameter(self):
        return self.circle.diameter

    @property
    def center(self):
        return self.circle.center

    @center.setter
    def center(self, point):
        self.circle.center = point

    @property
    def area(self):
        return (self.circle.area * 2) + (self.circle.circumference * self.height)

    @property
    def volume(self):
        return self.circle.area * self.height

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "Cylinder({0!r}, {1!r})".format(self.circle, self.height)

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
            If True, triangulate the faces.

        Returns
        -------
        list[list[float]]
            A list of vertex locations.
        list[list[int]]
            And a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        if u < 3:
            raise ValueError("The value for u should be u > 3.")

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
        """Transform the cylinder.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the cylinder.

        Returns
        -------
        None

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
