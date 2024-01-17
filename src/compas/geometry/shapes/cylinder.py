from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import transform_points
from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Line

from .shape import Shape


class Cylinder(Shape):
    """A cylinder is defined by a frame, radius, and height.

    The cylinder is oriented along the z-axis of the frame.
    The base point of the cylinder (i.e. the centre of the base circle) is at the origin of the frame.
    Half of the cylinder is above the local XY plane of the frame, the other half below.

    Parameters
    ----------
    radius : float
        The radius of the cylinder.
    height : float
        The height of the cylinder along the z-axis of the frame.
        Half of the cylinder is above the XY plane of the frame, the other half below.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system, or "frame", of the cylinder.
        Default is ``None``, in which case the world coordinate system is used.

    Attributes
    ----------
    area : float, read-only
        The surface area of the cylinder.
    axis : :class:`compas.geometry.Line`, read-only
        The central axis of the cylinder.
    base : :class:`compas.geometry.Point`, read-only
        The base point of the cylinder.
        The base point is at the origin of the local coordinate system.
    circle : :class:`compas.geometry.Circle`, read-only
        The base circle of the cylinder.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the base circle of the cylinder.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the cylinder.
        The cylinder is oriented along the local z-axis.
    height : float
        The height of the cylinder.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the cylinder.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    radius : float
        The radius of the base circle of the cylinder.
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the cylinder to global coordinates.
    volume : float, read-only
        The volume of the cylinder.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> cylinder = Cylinder(frame=frame, radius=0.3, heigth=1.0)
    >>> cylinder = Cylinder(radius=0.3, heigth=1.0)
    >>> cylinder = Cylinder()

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
        super(Cylinder, self).__init__(frame=frame, **kwargs)
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
    # Data
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
    # Properties
    # ==========================================================================

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The cylinder radius has not been set.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The cylinder radius should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def height(self):
        if self._height is None:
            raise ValueError("The cylinder height has not been set.")
        return self._height

    @height.setter
    def height(self, height):
        if height < 0:
            raise ValueError("The cylinder height should be larger than or equal to zero.")
        self._height = float(height)

    @property
    def axis(self):
        return Line(self.frame.point, self.frame.point + self.frame.normal * self.height)

    @property
    def base(self):
        return self.frame.point.copy()

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.normal)

    @property
    def circle(self):
        return Circle(radius=self.radius, frame=self.frame)

    @property
    def diameter(self):
        return 2 * self.radius

    @property
    def area(self):
        return (self.circle.area * 2) + (self.circle.circumference * self.height)

    @property
    def volume(self):
        return self.circle.area * self.height

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line, radius):  # type: (...) -> Cylinder
        """Construct a cylinder from a line and a radius.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`
            The line.
        radius : float
            The radius.

        Returns
        -------
        :class:`compas.geometry.Cylinder`
            The cylinder.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> from compas.geometry import Cylinder
        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> cylinder = Cylinder.from_line_and_radius(line, radius=0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, height=line.length, radius=radius)

    @classmethod
    def from_circle_and_height(cls, circle, height):  # type: (...) -> Cylinder
        """Construct a cylinder from a circle and a height.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The circle.
        height : float
            The height.

        Returns
        -------
        :class:`compas.geometry.Cylinder`
            The cylinder.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> from compas.geometry import Cylinder
        >>> circle = Circle(radius=0.3)
        >>> cylinder = Cylinder.from_circle_and_height(circle, height=1.0)

        """
        return cls(frame=circle.frame, height=height, radius=circle.radius)

    # =============================================================================
    # Conversions
    # =============================================================================

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

        vertices = transform_points(vertices, self.transformation)

        return vertices, faces

    def to_brep(self):
        """Returns a BRep representation of the cylinder.

        Returns
        -------
        :class:`compas.brep.Brep`

        """
        from compas.geometry import Brep

        return Brep.from_cylinder(self)

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, factor):
        """Scale the cylinder by multiplying the radius and height by a factor.

        Parameters
        ----------
        factor : float
            The scaling factor.

        Returns
        -------
        None

        """
        self.radius *= factor
        self.height *= factor

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point, tol=1e-6):
        """Verify if a point is inside the cylinder.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point.
        tol : float, optional
            The tolerance for the verification.

        Returns
        -------
        bool
            True if the point is inside the cylinder.
            False otherwise.

        """
        point = self.frame.to_local_coordinates(point)
        x, y, z = point.x, point.y, point.z  # type: ignore

        if z > self.height / 2 + tol:
            return False
        if z < -self.height / 2 - tol:
            return False

        return x**2 + y**2 <= (self.radius + tol) ** 2
