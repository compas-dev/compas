from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import transform_points

from .shape import Shape


class Sphere(Shape):
    """A sphere is defined by a point and a radius.

    Parameters
    ----------
    radius: float
        The radius of the sphere.
    frame: :class:`compas.geometry.Frame`, optional
        The local coordinates system, or "frame", of the sphere.
        Default is ``None``, in which case the sphere is constructed in world coordinates.
    point: :class:`compas.geometry.Point`, optional
        The center of the sphere.
        When provided, this point overwrites the location of the origin of the local coordinate system.
    name : str, optional
        The name of the shape.

    Attributes
    ----------
    area : float, read-only
        The surface area of the sphere.
    axis : :class:`compas.geometry.Line`, read-only
        The central axis of the sphere.
    base : :class:`compas.geometry.Point`, read-only
        The base point of the sphere.
        The base point is at the origin of the local coordinate system.
    circle : :class:`compas.geometry.Circle`, read-only
        The base circle of the sphere.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the sphere.
    frame : :class:`compas.geometry.Frame`
        The coordinate system of the sphere.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the sphere.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    radius : float
        The radius of the sphere.
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the sphere to global coordinates.
    volume : float, read-only
        The volume of the sphere.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Sphere
    >>> sphere1 = Sphere(frame=Frame.worldXY(), radius=5)
    >>> sphere1 = Sphere(radius=5)

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius=data["radius"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius, frame=None, point=None, name=None):
        super(Sphere, self).__init__(frame=frame, name=name)
        self._radius = 1.0
        self.radius = radius
        if point:
            self.frame.point = point

    def __repr__(self):
        return "{0}(radius={1}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def base(self):
        return self.frame.point

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The radius of the sphere is not set.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The radius of the sphere should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def start(self):
        return self.frame.point + self.frame.zaxis * -self.radius

    @property
    def end(self):
        return self.frame.point + self.frame.zaxis * +self.radius

    @property
    def axis(self):
        return Line(self.start, self.end)

    @property
    def circle(self):
        return Circle(self.frame, self.radius)

    @property
    def area(self):
        return 4 * pi * self.radius**2

    @property
    def volume(self):
        return 4.0 / 3.0 * pi * self.radius**3

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_radius(cls, point, radius):  # type: (...) -> Sphere
        """Construct a sphere from a point and a radius.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The center of the sphere.
        radius : float
            The radius of the sphere.

        Returns
        -------
        :class:`compas.geometry.Sphere`
            The constructed sphere.

        """
        frame = Frame.worldXY()
        frame.point = point
        return cls(frame=frame, radius=radius)

    # ==========================================================================
    # Discretisation
    # ==========================================================================

    def compute_vertices(self):  # type: () -> list[list[float]]
        """Compute the vertices of the discrete representation of the sphere.

        Returns
        -------
        list[list[float]]

        """
        u = self.resolution_u
        v = self.resolution_v

        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5

        x, y, z = 0, 0, 0

        vertices = []
        for i in range(1, v):
            for j in range(u):
                tx = self.radius * cos(i * theta - hpi) * cos(j * phi) + x
                ty = self.radius * cos(i * theta - hpi) * sin(j * phi) + y
                tz = self.radius * sin(i * theta - hpi) + z
                vertices.append([tx, ty, tz])

        vertices.append([x, y, z + self.radius])
        vertices.append([x, y, z - self.radius])

        vertices = transform_points(vertices, self.transformation)
        return vertices

    def compute_faces(self):  # type: () -> list[list[int]]
        """Compute the faces of the discrete representation of the sphere.

        Returns
        -------
        list[list[int]]

        """
        u = self.resolution_u
        v = self.resolution_v

        vertices = self.vertices

        faces = []

        # south pole triangle fan
        sp = len(vertices) - 1
        for j in range(u):
            faces.append([sp, (j + 1) % u, j])

        for i in range(v - 2):
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

        return faces

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self):
        """Returns a BRep representation of the sphere.

        Returns
        -------
        :class:`compas.brep.Brep`

        """
        from compas.geometry import Brep

        return Brep.from_sphere(self)

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, factor):
        """Scale the sphere.

        Parameters
        ----------
        factor : float
            The scaling factor.

        Returns
        -------
        None

        """
        self.radius *= factor

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point, tol=1e-6):
        """Verify if a point is inside the sphere.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point to test.
        tol : float, optional
            The tolerance for the test.

        Returns
        -------
        bool
            True if the point is inside the sphere.
            False otherwise.

        """
        return self.frame.point.distance_to_point(point) <= self.radius + tol

    def contains_points(self, points, tol=1e-6):
        """Verify if a list of points are inside the sphere.

        Parameters
        ----------
        points : list of :class:`compas.geometry.Point`
            The points to test.
        tol : float, optional
            The tolerance for the test.

        Returns
        -------
        list
            A list of booleans indicating for each point if it is inside the sphere.

        """
        return [self.contains_point(point, tol=tol) for point in points]
