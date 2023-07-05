from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import transform_points
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Circle
from .shape import Shape


class Sphere(Shape):
    """A sphere is defined by a point and a radius.

    Parameters
    ----------
    frame: :class:`~compas.geometry.Frame`, optional
        The local coordinates system, or "frame", of the sphere.
        Default is ``None``, in which case the sphere is constructed in world coordinates.
    radius: float, optional
        The radius of the sphere.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The coordinate system of the sphere.
    transformation : :class:`~compas.geometry.Transformation`
        The transformation of the sphere to global coordinates.
    radius : float
        The radius of the sphere.
    axis : :class:`~compas.geometry.Line`, read-only
        The central axis of the sphere.
    base : :class:`~compas.geometry.Point`, read-only
        The base point of the sphere.
        The base point is at the origin of the local coordinate system.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the sphere.
        The base point of the plane is at the origin of the local coordinate system.
        The normal of the plane is in the direction of the z-axis of the local coordinate system.
    circle : :class:`~compas.geometry.Circle`, read-only
        The base circle of the sphere.
        The center of the circle is at the origin of the local coordinate system.
    diameter : float, read-only
        The diameter of the sphere.
    area : float, read-only
        The surface area of the sphere.
    volume : float, read-only
        The volume of the sphere.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Sphere
    >>> sphere1 = Sphere(frame=Frame.worldXY(), radius=5)
    >>> sphere1 = Sphere(radius=5)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius"],
    }

    def __init__(self, frame=None, radius=None, point=None, **kwargs):
        super(Sphere, self).__init__(frame=frame, **kwargs)
        self._radius = 1.0
        self.radius = radius
        if point:
            self.frame.point = point

    def __repr__(self):
        return "Sphere(frame={0!r}, radius={1!r})".format(self.frame, self.radius)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius])

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "radius": self.radius}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.radius = data["radius"]

    # ==========================================================================
    # Properties
    # ==========================================================================

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
    def from_point_and_radius(cls, point, radius):
        """Construct a sphere from a point and a radius.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The center of the sphere.
        radius : float
            The radius of the sphere.

        Returns
        -------
        :class:`~compas.geometry.Sphere`
            The constructed sphere.

        """
        frame = Frame.worldXY()
        frame.point = point
        return cls(frame=frame, radius=radius)

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces

        The vertex positions are in world coordinates.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.
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
        if v < 3:
            raise ValueError("The value for v should be v > 3.")

        theta = pi / v
        phi = pi * 2 / u
        hpi = pi * 0.5

        x, y, z = self.frame.point

        vertices = []
        for i in range(1, v):
            for j in range(u):
                tx = self.radius * cos(i * theta - hpi) * cos(j * phi) + x
                ty = self.radius * cos(i * theta - hpi) * sin(j * phi) + y
                tz = self.radius * sin(i * theta - hpi) + z
                vertices.append([tx, ty, tz])

        vertices.append([x, y, z + self.radius])
        vertices.append([x, y, z - self.radius])

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

        if triangulated:
            triangles = []
            for face in faces:
                if len(face) == 4:
                    triangles.append(face[0:3])
                    triangles.append([face[0], face[2], face[3]])
                else:
                    triangles.append(face)
            faces = triangles

        # transform the vertices to world coordinates
        vertices = transform_points(vertices, self.transformation)

        return vertices, faces

    # =============================================================================
    # Transformations
    # =============================================================================

    # def transform(self, transformation):
    #     """Transform the sphere.

    #     Parameters
    #     ----------
    #     transformation : :class:`~compas.geometry.Transformation`
    #         The transformation used to transform the Sphere.
    #         Note that non-similarity preserving transformations will not change
    #         the sphere into an ellipsoid. In such case, the radius of the sphere
    #         will be scaled by the largest scale factor of the threee axis.

    #     Returns
    #     -------
    #     None

    #     Examples
    #     --------
    #     >>> from compas.geometry import Frame
    #     >>> from compas.geometry import Transformation
    #     >>> from compas.geometry import Sphere
    #     >>> sphere = Sphere(Point(1, 1, 1), 5)
    #     >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    #     >>> T = Transformation.from_frame(frame)
    #     >>> sphere.transform(T)

    #     """
    #     self.frame.transform(transformation)
    #     Sc, _, _, _, _ = transformation.decomposed()
    #     self.radius *= max([Sc[0, 0], Sc[1, 1], Sc[2, 2]])

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
        point : :class:`~compas.geometry.Point`
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
        points : list of :class:`~compas.geometry.Point`
            The points to test.
        tol : float, optional
            The tolerance for the test.

        Returns
        -------
        list
            A list of booleans indicating for each point if it is inside the sphere.

        """
        return [self.contains_point(point, tol=tol) for point in points]
