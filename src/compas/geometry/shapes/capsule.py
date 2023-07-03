from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import transform_points
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Line
from compas.geometry import Circle

from .shape import Shape


class Capsule(Shape):
    """A capsule is defined by a frame, radius, and height.

    The capsule is oriented along the z-axis of the frame.
    The base point (i.e. the centre of the base circle) is at the origin of the frame.
    Half of the capsule is above the local XY plane of the frame, the other half below.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system, or "frame", of the capsule.
        Default is ``None``, in which case the world coordinate system is used.
    radius : float, optional
        The radius of the capsule.
    height : float, optional
        The height of the capsule along the z-axis of the frame.
        Half of the capsule is above the XY plane of the frame, the other half below.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The local coordinate system of the capsule.
        The capsule is oriented along the local z-axis.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation of the capsule to global coordinates.
    radius : float
        The radius of the base circle of the capsule.
    height : float
        The height of the capsule.
    axis : :class:`~compas.geometry.Line`, read-only
        The central axis of the capsule.
    base : :class:`~compas.geometry.Point`, read-only
        The base point of the capsule.
        The base point is at the origin of the local coordinate system.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the capsule.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    circle : :class:`~compas.geometry.Circle`, read-only
        The base circle of the capsule.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the base circle of the capsule.
    area : float, read-only
        The surface area of the capsule.
    volume : float, read-only
        The volume of the capsule.

    Examples
    --------
    >>> frame = Frame.worldXY()
    >>> capsule = Capsule(frame=frame, radius=0.3, heigth=1.0)
    >>> capsule = Capsule(radius=0.3, heigth=1.0)
    >>> capsule = Capsule()

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius": {"type": "number", "minimum": 0},
            "height": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius", "height"],
    }

    def __init__(self, frame=None, radius=0.3, height=1.0, **kwargs):
        super(Capsule, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self._height = None
        self.radius = radius
        self.height = height

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "radius": self.radius, "height": self.height}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.radius = data["radius"]
        self.height = data["height"]

    @classmethod
    def from_data(cls, data):
        """Construct a capsule from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Capsule`
            The constructed capsule.

        Examples
        --------
        >>> data = {"frame": Frame.worldXY(), "radius": 0.3, "height": 1.0}
        >>> cone = Cone.from_data(data)
        >>> data = {"frame": None, "radius": 0.3, "height": 1.0}
        >>> cone = Capsule.from_data(data)

        """
        return cls(**data)

    # ==========================================================================
    # properties
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
        self._height = float(abs(height))

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
    def base(self):
        return self.frame.point.copy()

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.normal)

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
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "Capsule(frame={0!r}, radius={1!r}, height={2!r})".format(self.frame, self.radius, self.height)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius
        elif key == 2:
            return self.height
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.radius = value
        elif key == 2:
            self.height = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius, self.height])

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_line_and_radius(cls, line, radius):
        """Construct a capsule from a line and a radius.

        Parameters
        ----------
        line : :class:`~compas.geometry.Line`
            The line.
        radius : float
            The radius.

        Returns
        -------
        :class:`~compas.geometry.Capsule`
            The constructed capsule.

        See Also
        --------
        :meth:`Capsule.from_circle_and_height`

        Examples
        --------
        >>> line = Line(Point(0, 0, 0), Point(0, 0, 1))
        >>> capsule = Capsule.from_line_and_radius(line, 0.3)

        """
        frame = Frame.from_plane(Plane(line.midpoint, line.direction))
        return cls(frame=frame, radius=radius, height=line.length)

    @classmethod
    def from_circle_and_height(cls, circle, height):
        """Construct a capsule from a circle and a height.

        Parameters
        ----------
        circle : :class:`~compas.geometry.Circle`
            The circle.
        height : float
            The height.

        Returns
        -------
        :class:`~compas.geometry.Capsule`
            The constructed capsule.

        See Also
        --------
        :meth:`Capsule.from_line_and_radius`

        Examples
        --------
        >>> circle = Circle(Frame.worldXY(), 0.3)
        >>> capsule = Capsule.from_circle_and_height(circle, 1.0)

        """
        return cls(frame=circle.frame, radius=circle.radius, height=height)

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces.

        Note that the vertex coordinates are defined with respect to the global coordinate system,
        and not to the local coordinate system of the capsule.

        Parameters
        ----------
        u : int, optional
            Number of faces in the 'u' direction.
        v : int, optional
            Number of faces in the 'v' direction.
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
        if v < 3:
            raise ValueError("The value for v should be v > 3.")
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

    def transform(self, transformation):
        """Transform this `Capsule` using a given transformation.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the capsule.

        Returns
        -------
        None

        """
        self.frame.transform(transformation)
