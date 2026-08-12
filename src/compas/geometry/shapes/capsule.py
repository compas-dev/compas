from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Transformation
from compas.geometry import transform_points

from .shape import Shape


class Capsule(Shape):
    """A capsule is defined by a frame, radius, and height.

    The capsule is oriented along the z-axis of the frame.
    The base point (i.e. the centre of the base circle) is at the origin of the frame.
    Half of the capsule is above the local XY plane of the frame, the other half below.

    Parameters
    ----------
    radius : float
        The radius of the capsule.
    height : float
        The height of the capsule along the z-axis of the frame.
        Half of the capsule is above the XY plane of the frame, the other half below.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system, or "frame", of the capsule.
        Default is ``None``, in which case the world coordinate system is used.
    name : str, optional
        The name of the shape.

    Attributes
    ----------
    area : float, read-only
        The surface area of the capsule.
    axis : :class:`compas.geometry.Line`, read-only
        The central axis of the capsule.
    base : :class:`compas.geometry.Point`, read-only
        The base point of the capsule.
        The base point is at the origin of the local coordinate system.
    circle : :class:`compas.geometry.Circle`, read-only
        The base circle of the capsule.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the base circle of the capsule.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the capsule.
        The capsule is oriented along the local z-axis.
    height : float
        The height of the capsule.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the capsule.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    radius : float
        The radius of the base circle of the capsule.
    transformation : :class:`compas.geometry.Transformation`
        The transformation of the capsule to global coordinates.
    volume : float, read-only
        The volume of the capsule.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> capsule = Capsule(radius=0.3, height=1.0, frame=frame)
    >>> capsule = Capsule(radius=0.3, height=1.0)
    >>> capsule = Capsule(3.0, 1.0)

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["radius", "height", "frame"],
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "height": self.height,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius=data["radius"],
            height=data["height"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius, height, frame=None, name=None):
        super(Capsule, self).__init__(frame=frame, name=name)
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
    # Properties
    # ==========================================================================

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The radius of the capsule is not set.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The radius of the capsule should be greater than or equal to zero.")
        self._radius = float(radius)

    @property
    def height(self):
        if self._height is None:
            raise ValueError("The capsule has no height.")
        return self._height

    @height.setter
    def height(self, height):
        if height < 0:
            raise ValueError("The height of the capsule should be greater than or equal to zero.")
        self._height = float((height))

    @property
    def length(self):
        return self.height

    @property
    def start(self):
        return self.frame.point - self.frame.zaxis * self.height / 2

    @property
    def end(self):
        return self.frame.point + self.frame.zaxis * self.height / 2

    @property
    def axis(self):
        return Line(self.start, self.end)

    @property
    def circle(self):
        return Circle(self.frame, self.radius)

    @property
    def volume(self):
        # cylinder plus 2 half spheres
        cylinder = self.radius**2 * pi * self.height
        caps = 4.0 / 3.0 * pi * self.radius**3
        return cylinder + caps

    @property
    def area(self):
        # cylinder minus caps plus 2 half spheres
        cylinder = self.radius * 2 * pi * self.height
        caps = 4 * pi * self.radius**2
        return cylinder + caps

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line, radius):  # type: (...) -> Capsule
        """Construct a capsule from a line and a radius.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`
            The line.
        radius : float
            The radius.

        Returns
        -------
        :class:`compas.geometry.Capsule`
            The constructed capsule.

        See Also
        --------
        :meth:`Capsule.from_circle_and_height`

        Examples
        --------
        >>> line = Line([0, 0, 0], [0, 0, 1])
        >>> capsule = Capsule.from_line_and_radius(line, 0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, radius=radius, height=line.length)

    @classmethod
    def from_circle_and_height(cls, circle, height):  # type: (...) -> Capsule
        """Construct a capsule from a circle and a height.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The circle.
        height : float
            The height.

        Returns
        -------
        :class:`compas.geometry.Capsule`
            The constructed capsule.

        See Also
        --------
        :meth:`Capsule.from_line_and_radius`

        Examples
        --------
        >>> circle = Circle(0.3)
        >>> capsule = Capsule.from_circle_and_height(circle, 1.0)

        """
        return cls(frame=circle.frame, radius=circle.radius, height=height)

    # =============================================================================
    # Discretisation
    # =============================================================================

    def compute_vertices(self):  # type: () -> list[list[float]]
        """Compute the vertices of the discrete representation of the capsule.

        Returns
        -------
        list[list[float]]

        """
        u = self.resolution_u
        v = self.resolution_v

        if v % 2 == 1:
            v += 1

        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5
        halfheight = self.height / 2
        sidemult = -1
        capswitch = 0

        vertices = []
        for i in range(1, v + 1):
            for j in range(u):
                a = i + capswitch
                tx = self.radius * cos(a * theta - hpi) * cos(j * phi)
                ty = self.radius * cos(a * theta - hpi) * sin(j * phi)
                tz = self.radius * sin(a * theta - hpi) + sidemult * halfheight
                vertices.append([tx, ty, tz])
            # switch from lower pole cap to upper pole cap
            if i == v / 2 and sidemult == -1:
                capswitch = -1
                sidemult *= -1

        vertices.append([0, 0, halfheight + self.radius])
        vertices.append([0, 0, -halfheight - self.radius])

        vertices = transform_points(vertices, self.transformation)
        return vertices

    def compute_faces(self):  # type: () -> list[list[int]]
        """Compute the faces of the discrete representation of the capsule.

        Returns
        -------
        list[list[int]]

        """
        u = self.resolution_u
        v = self.resolution_v

        if v % 2 == 1:
            v += 1

        vertices = self.vertices

        faces = []

        # south pole triangle fan
        sp = len(vertices) - 1
        for j in range(u):
            faces.append([sp, (j + 1) % u, j])

        for i in range(v - 1):
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

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Transformations
    # =============================================================================

    def scale(self, factor):
        """Scale the capsule.

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
        """Verify if a point is inside the capsule.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point.
        tol : float, optional
            The tolerance for the test.

        Returns
        -------
        bool
            True if the point is inside the capsule.
            False otherwise.

        See Also
        --------
        contains_points

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        x, y, z = transform_points([point], T)[0]
        h = 0.5 * self.height + tol

        if -h <= z <= +h:
            if x**2 + y**2 > (self.radius + tol) ** 2:
                return False

        if z > +h:
            x0, y0, z0 = self.end
            dx = x - x0
            dy = y - y0
            dz = z - z0
            if dx**2 + dy**2 + dz**2 > (self.radius + tol) ** 2:
                return False

        if z < -h:
            x0, y0, z0 = self.start
            dx = x - x0
            dy = y - y0
            dz = z - z0
            if dx**2 + dy**2 + dz**2 > (self.radius + tol) ** 2:
                return False

        return True

    def contains_points(self, points, tol=1e-6):
        """Verify if a list of points is inside the capsule.

        Parameters
        ----------
        points : list of :class:`compas.geometry.Point`
            The points.
        tol : float, optional
            The tolerance for the test.

        Returns
        -------
        list of bool
            For each point, True if the point is inside the capsule.
            False otherwise.

        See Also
        --------
        contains_point

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        points = transform_points(points, T)

        h = 0.5 * self.height + tol
        r2 = (self.radius + tol) ** 2
        results = [False] * len(points)

        for i, (x, y, z) in enumerate(points):
            if -h <= z <= +h:
                if x**2 + y**2 > r2:
                    continue

            if z > +h:
                x0, y0, z0 = self.end
                dx = x - x0
                dy = y - y0
                dz = z - z0
                if dx**2 + dy**2 + dz**2 > r2:
                    continue

            if z < -h:
                x0, y0, z0 = self.start
                dx = x - x0
                dy = y - y0
                dz = z - z0
                if dx**2 + dy**2 + dz**2 > r2:
                    continue

            results[i] = True

        return results
