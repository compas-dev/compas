from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import cos, sin, pi

from compas.geometry import Frame
from compas.geometry import Circle
from .surface import Surface

PI2 = 2 * pi


class SphericalSurface(Surface):
    """A spherical surface is defined by a radius and a frame.

    Parameters
    ----------
    radius : float
        The radius of the sphere.
    frame : :class:`Frame`
        The frame of the sphere.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> from compas.geometry import SphericalSurface
    >>> frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> sphere = SphericalSurface(1.0, frame)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "radius": {"type": "number", "minimum": 0},
            "frame": Frame.JSONSCHEMA,
        },
        "required": ["radius", "frame"],
    }

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base surface class
    def __new__(cls, *args, **kwargs):
        surface = object.__new__(cls)
        surface.__init__(*args, **kwargs)
        return surface

    def __init__(self, radius, frame=None, **kwargs):
        super(SphericalSurface, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self.radius = radius

    def __repr__(self):
        return "SphericalSurface({0!r}, frame={1!r})".format(self.radius, self.frame)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.radius
        elif key == 1:
            return self.frame
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.radius = value
        elif key == 1:
            self.frame = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius])

    def __eq__(self, other):
        try:
            other_frame = other[0]
            other_radius = other[1]
        except Exception:
            return False
        return self.frame == other_frame and self.radius == other_radius

    @property
    def data(self):
        return {"radius": self.radius, "frame": self.frame}

    @data.setter
    def data(self, data):
        self.radius = data["radius"]
        self.frame = Frame.from_data(data["frame"])

    @property
    def center(self):
        return self.frame.point

    @center.setter
    def center(self, point):
        self.frame.point = point

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The radius of the surface has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The radius of a sphere should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def area(self):
        return 4 * 3.14159 * self.radius**2

    @property
    def volume(self):
        return 4 / 3 * 3.14159 * self.radius**3

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_radius(cls, plane, radius):
        """Construct a sphere from a plane and a radius.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the sphere.
        radius : float
            The radius of the sphere.

        Returns
        -------
        :class:`compas.geometry.SphericalSurface`
            A sphere.

        """
        return cls(radius, frame=Frame.from_plane(plane))

    @classmethod
    def from_three_points(cls, a, b, c):
        """Construct a sphere from three points.

        Parameters
        ----------
        a : :class:`compas.geometry.Point`
            The first point.
        b : :class:`compas.geometry.Point`
            The second point.
        c : :class:`compas.geometry.Point`
            The third point.

        Returns
        -------
        :class:`compas.geometry.SphericalSurface`
            A sphere.

        """
        circle = Circle.from_three_points(a, b, c)
        return cls(circle.radius, frame=circle.frame)

    @classmethod
    def from_points(cls, points):
        """Construct the sphere that best fits a set of points in the least squares sense.

        Parameters
        ----------
        points : list of :class:`compas.geometry.Point`
            The points.

        Returns
        -------
        :class:`compas.geometry.SphericalSurface`
            A sphere.

        """
        if len(points) < 3:
            raise ValueError("At least three points are required to construct a sphere.")

        if len(points) == 3:
            return cls.from_three_points(*points)

        from compas.geometry import bestfit_sphere_numpy

        center, radius = bestfit_sphere_numpy(points)
        return cls(radius, frame=Frame(center, [1, 0, 0], [0, 1, 0]))

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self, nu=16, nv=16, du=None, dv=None):
        """Convert the sphere to a list of vertices and faces.

        Parameters
        ----------
        nu : int, optional
            The number of faces in the u direction.
            Default is ``16``.
        nv : int, optional
            The number of faces in the v direction.
            Default is ``16``.
        du : tuple, optional
            The subset of the domain in the u direction.
            Default is ``None``, in which case the entire domain is used.
        dv : tuple, optional
            The subset of the domain in the v direction.
            Default is ``None``, in which case the entire domain is used.

        Returns
        -------
        vertices : list of :class:`compas.geometry.Point`
            The vertices of the sphere.
        faces : list of list of int
            The faces of the sphere as lists of vertex indices.

        """
        u_domain = self.u_domain
        v_domain = self.v_domain

        du = du or u_domain
        dv = dv or v_domain

        self.u_domain = du
        self.v_domain = dv

        vertices = []
        for u in self.u_space(n=nu + 1):
            for v in self.v_space(n=nv + 1):
                point = self.point_at(u, v)
                vertices.append(point)

        faces = []
        for i in range(nu):
            for j in range(nv):
                faces.append(
                    [
                        i * (nv + 1) + j,
                        (i + 1) * (nv + 1) + j,
                        (i + 1) * (nv + 1) + j + 1,
                        i * (nv + 1) + j + 1,
                    ]
                )

        self.u_domain = u_domain
        self.v_domain = v_domain

        return vertices, faces

    def to_polyhedron(self, nu=16, nv=16, du=None, dv=None):
        """Convert the sphere to a polyhedron.

        Parameters
        ----------
        nu : int, optional
            The number of faces in the u direction.
            Default is ``16``.
        nv : int, optional
            The number of faces in the v direction.
            Default is ``16``.
        du : tuple, optional
            The subset of the domain in the u direction.
            Default is ``None``, in which case the entire domain is used.
        dv : tuple, optional
            The subset of the domain in the v direction.
            Default is ``None``, in which case the entire domain is used.

        Returns
        -------
        :class:`compas.datastructures.Polyhedron`
            A polyhedron object.

        """
        from compas.geometry import Polyhedron

        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        return Polyhedron(vertices, faces)

    def to_mesh(self, nu=16, nv=16, du=None, dv=None):
        """Convert the sphere to a mesh.

        Parameters
        ----------
        nu : int, optional
            The number of faces in the u direction.
            Default is ``16``.
        nv : int, optional
            The number of faces in the v direction.
            Default is ``16``.
        du : tuple, optional
            The subset of the domain in the u direction.
            Default is ``None``, in which case the entire domain is used.
        dv : tuple, optional
            The subset of the domain in the v direction.
            Default is ``None``, in which case the entire domain is used.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def to_brep(self):
        """Convert the sphere to a BREP representation.

        Returns
        -------
        :class:`compas.geometry.Brep`
            A BREP object.

        """
        raise NotImplementedError

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, u, v):
        """Construct a point on the sphere.

        Parameters
        ----------
        u : float
            The first parameter.
            The parameter value should be between zero and one,
            and will be mapped to the corresponding angle between zero and pi.
        v : float
            The second parameter.
            The parameter value should be between zero and one,
            and will be mapped to the corresponding angle between zero and 2 * pi.

        Returns
        -------
        :class:`compas.geometry.Point`
            A point on the sphere.

        """
        u = u * pi
        v = v * PI2
        x = self.radius * cos(u) * sin(v)
        y = self.radius * sin(u) * sin(v)
        z = self.radius * cos(v)
        return self.frame.point + self.frame.xaxis * x + self.frame.yaxis * y + self.frame.zaxis * z

    def normal_at(self, u, v):
        """Construct a normal vector at a point on the sphere.

        Parameters
        ----------
        u : float
            The first parameter.
        v : float
            The second parameter.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector.

        """
        u = u * pi
        v = v * PI2
        x = cos(u) * sin(v)
        y = sin(u) * sin(v)
        z = cos(v)
        return self.frame.xaxis * x + self.frame.yaxis * y + self.frame.zaxis * z
