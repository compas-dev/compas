from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin
from math import sqrt

from compas.utilities import pairwise
from compas.geometry import transform_points
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Line
from compas.geometry import Frame

from .shape import Shape


class Cone(Shape):
    """A cone is defined by a frame, radius, and height.

    The cone is oriented along the z-axis of the frame.
    The base point of the cone (i.e. the centre of the base circle) is at the origin of the frame.
    The entire cone is in the positive z-direction.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the cone.
        Default is ``None``, in which case the world coordinate system is used.
    radius : float, optional
        The radius of the base of the cone.
    height : float, optional
        The height of the cone along the z-axis of the frame.
        The base of the cone is at the origin of the frame.
        The entire cone is above the XY plane of the frame.

    Attributes
    ----------
    area : float, read-only
        The surface area of the cone.
    axis : :class:`compas.geometry.Line`, read-only
        The central axis of the cone.
    base : :class:`compas.geometry.Point`, read-only
        The base point of the cone.
        The base point is at the origin of the local coordinate system.
    circle : :class:`compas.geometry.Circle`, read-only
        The base circle of the cone.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the base circle of the cone.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the cone.
        The cone is oriented along the local z-axis.
    height : float
        The height of the cone.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the cone.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    radius : float
        The radius of the base circle of the cone.
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the cone to global coordinates.
    volume : float, read-only
        The volume of the cone.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> cone = Cone(frame=frame, radius=0.3, height=1.0)
    >>> cone = Cone(radius=0.3, height=1.0)
    >>> cone = Cone()

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0},
            "frame": Frame.JSONSCHEMA,
        },
        "required": ["radius", "height", "frame"],
    }

    def __init__(self, radius, height, frame=None, **kwargs):
        super(Cone, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self._height = None
        self.radius = radius
        self.height = height

    def __repr__(self):
        return "{0}(radius={1}, height={2}, frame={3!r})".format(
            type(self).__name__,
            self.radius,
            self.height,
            self.frame,
        )

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def data(self):
        return {
            "radius": self.radius,
            "height": self.height,
            "frame": self.frame.data,
        }

    @classmethod
    def from_data(cls, data):
        return cls(
            radius=data["radius"],
            height=data["height"],
            frame=Frame.from_data(data["frame"]),
        )

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The cone radius has not been set.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The cone radius should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def height(self):
        if self._height is None:
            raise ValueError("The cone height has not been set.")
        return self._height

    @height.setter
    def height(self, height):
        if height < 0:
            raise ValueError("The cone height should be larger than or equal to zero.")
        self._height = float(height)

    @property
    def axis(self):
        return Line(self.frame.point, self.frame.point + self.frame.normal * self.height)

    @property
    def circle(self):
        return Circle(self.radius, self.frame)

    @property
    def diameter(self):
        return 2 * self.radius

    @property
    def area(self):
        r = self.radius
        h = self.height
        return pi * r * (r + sqrt(h**2 + r**2))

    @property
    def volume(self):
        r = self.radius
        h = self.height
        return pi * r**2 * (h / 3)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line, radius):  # type: (...) -> Cone
        """Construct a cone from a line and a radius.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`
            The axis of the cone.
        radius : float
            The radius of the base circle of the cone.

        Returns
        -------
        :class:`compas.geometry.Cone`
            The cone.

        See Also
        --------
        :meth:`Cone.from_circle_and_height`

        Examples
        --------
        >>> line = Line(Point(0, 0, 0), Point(0, 0, 1))
        >>> cone = Cone.from_line_and_radius(line, 0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, radius=radius, height=line.length)

    @classmethod
    def from_circle_and_height(cls, circle, height):  # type: (...) -> Cone
        """Construct a cone from a circle and a height.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The base circle of the cone.
        height : float
            The height of the cone.

        Returns
        -------
        :class:`compas.geometry.Cone`
            The cone.

        See Also
        --------
        :meth:`Cone.from_line_and_radius`

        Examples
        --------
        >>> circle = Circle(Frame.worldXY(), 0.3)
        >>> cone = Cone.from_circle_and_height(circle, 1.0)

        """
        frame = circle.frame
        return cls(frame=frame, radius=circle.radius, height=height)

    # ==========================================================================
    # Conversions
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
        list[list[float]], list[list[int]]
            A list of vertex locations, and a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        if u < 3:
            raise ValueError("The value for u should be u > 3.")

        vertices = [[0, 0, 0]]
        a = 2 * pi / u
        radius = self.circle.radius
        for i in range(u):
            x = radius * cos(i * a)
            y = radius * sin(i * a)
            vertices.append([x, y, 0])  # type: ignore
        vertices.append([0, 0, self.height])  # type: ignore

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

        vertices = transform_points(vertices, self.transformation)

        return vertices, faces

    def to_brep(self):
        """Returns a BRep representation of the cone.

        Returns
        -------
        :class:`compas.brep.Brep`

        """
        from compas.geometry import Brep

        return Brep.from_cone(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    # ==========================================================================
    # Methods
    # ==========================================================================
