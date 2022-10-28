from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Point

from ._shape import Shape


class Sphere(Shape):
    """A sphere is defined by a point and a radius.

    Parameters
    ----------
    point: [float, float, float] | :class:`~compas.geometry.Point`
        The center of the sphere.
    radius: float
        The radius of the sphere.

    Attributes
    ----------
    point : :class:`~compas.geometry.Point`
        The center of the sphere.
    radius : float
        The radius of the sphere.
    center : :class:`~compas.geometry.Point`, read-only
        The center of the sphere.
    area : float, read-only
        The surface area of the sphere.
    volume : float, read-only
        The volume of the sphere.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Sphere
    >>> sphere1 = Sphere(Point(1, 1, 1), 5)
    >>> sphere2 = Sphere((2, 4, 1), 2)
    >>> sphere3 = Sphere([2, 4, 1], 2)

    >>> from compas.geometry import Point
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere(Point(1, 1, 1), 5)
    >>> sdict = {'point': [1., 1., 1.], 'radius': 5.}
    >>> sdict == sphere.data
    True

    """

    __slots__ = ["_point", "_radius"]

    def __init__(self, point, radius, **kwargs):
        super(Sphere, self).__init__(**kwargs)
        self._point = None
        self._radius = None
        self.point = point
        self.radius = radius

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema
        from compas.data import is_float3

        return schema.Schema({"point": is_float3, "radius": schema.And(float, lambda x: x > 0)})

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "sphere"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the sphere."""
        return {"point": self.point.data, "radius": self.radius}

    @data.setter
    def data(self, data):
        self.point = Point.from_data(data["point"])
        self.radius = data["radius"]

    @classmethod
    def from_data(cls, data):
        """Construct a sphere from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Sphere`
            The constructed sphere.

        Examples
        --------
        >>> from compas.geometry import Sphere
        >>> data = {'point': [1., 2., 3.], 'radius': 4.}
        >>> sphere = Sphere.from_data(data)

        """
        sphere = cls(Point.from_data(data["point"]), data["radius"])
        return sphere

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = float(radius)

    @property
    def center(self):
        return self.point

    @property
    def area(self):
        return 4 * pi * self.radius**2

    @property
    def volume(self):
        return 4.0 / 3.0 * pi * self.radius**3

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "Sphere({0!r}, {1!r})".format(self.point, self.radius)

    def __len__(self):
        return 2

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
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, u=16, v=16, triangulated=False):
        """Returns a list of vertices and faces

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

        return vertices, faces

    def transform(self, transformation):
        """Transform the sphere.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the Sphere.
            Note that non-similarity preserving transformations will not change
            the sphere into an ellipsoid. In such case, the radius of the sphere
            will be scaled by the largest scale factor of the threee axis.

        Returns
        -------
        None

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
        Sc, _, _, _, _ = transformation.decomposed()
        self.radius *= max([Sc[0, 0], Sc[1, 1], Sc[2, 2]])
