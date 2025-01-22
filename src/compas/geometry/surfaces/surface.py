from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import product

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Point
from compas.geometry import Transformation
from compas.itertools import linspace
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable


@pluggable(category="factories")
def surface_from_native(cls, *args, **kwargs):
    raise PluginNotInstalledError


class Surface(Geometry):
    """Class representing a general surface object.

    Parameters
    ----------
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the surface.
        Default is the world coordinate system.
    transformation : :class:`compas.geometry.Transformation`, read-only
        The transformation from the surface's local coordinate system to the world coordinate system.
    domain_u : tuple[float, float], read-only
        The parameter domain of the surface in the U direction.
    domain_v : tuple[float, float], read-only
        The parameter domain of the surface in the V direction.
    is_periodic_u : bool, read-only
        Flag indicating if the surface is periodic in the U direction.
    is_periodic_v : bool, read-only
        Flag indicating if the surface is periodic in the V direction.

    """

    def __new__(cls, *args, **kwargs):
        if cls is Surface:
            raise TypeError("Making an instance of `Surface` using `Surface()` is not allowed. Please use one of the factory methods instead (`Surface.from_...`)")
        return object.__new__(cls)

    def __init__(self, frame=None, name=None):
        super(Surface, self).__init__(name=name)
        self._frame = None
        self._transformation = None
        self._domain_u = None
        self._domain_v = None
        self._point = None
        if frame:
            self.frame = frame

    def __repr__(self):
        return "{0}(frame={1!r}, domain_u={2}, domain_v={3})".format(
            type(self).__name__,
            self.frame,
            self.domain_u,
            self.domain_v,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        if not frame:
            self._frame = None
        else:
            self._frame = Frame(frame[0], frame[1], frame[2])
        self._transformation = None

    @property
    def transformation(self):
        if not self._transformation:
            self._transformation = Transformation.from_frame(self.frame)
        return self._transformation

    @property
    def point(self):
        if not self._point:
            return self.frame.point
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def xaxis(self):
        return self.frame.xaxis

    @property
    def yaxis(self):
        return self.frame.yaxis

    @property
    def zaxis(self):
        return self.frame.zaxis

    @property
    def dimension(self):
        return 3

    @property
    def domain_u(self):
        if not self._domain_u:
            self._domain_u = (0.0, 1.0)
        return self._domain_u

    @property
    def domain_v(self):
        if not self._domain_v:
            self._domain_v = (0.0, 1.0)
        return self._domain_v

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def is_periodic_u(self):
        raise NotImplementedError

    @property
    def is_periodic_v(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, surface):
        """Construct a parametric surface from a native surface geometry.

        Parameters
        ----------
        surface
            A CAD native surface object.

        Returns
        -------
        :class:`compas.geometry.Surface`
            A COMPAS surface.

        """
        return surface_from_native(cls, surface)

    @classmethod
    def from_obj(cls, filepath):
        """Load a surface from an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.geometry.Surface`

        """
        raise NotImplementedError

    @classmethod
    def from_step(cls, filepath):
        """Load a surface from a STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.geometry.Surface`

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the surface geometry to a STP file.

        Parameters
        ----------
        filepath : str
        schema : str, optional

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_vertices_and_faces(self, nu=16, nv=16, du=None, dv=None):
        """Convert the surface to a list of vertices and faces.

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
            The vertices of the surface discretisation.
        faces : list of list of int
            The faces of the surface discretisation as lists of vertex indices.

        """
        domain_u = du or self.domain_u
        domain_v = dv or self.domain_v

        vertices = [
            self.point_at(i, j)
            for i, j in product(
                linspace(domain_u[0], domain_u[1], nu + 1),
                linspace(domain_v[0], domain_v[1], nv + 1),
            )
        ]
        faces = [
            [
                i * (nv + 1) + j,
                i * (nv + 1) + j + 1,
                (i + 1) * (nv + 1) + j + 1,
                (i + 1) * (nv + 1) + j,
            ]
            for i, j in product(range(nu), range(nv))
        ]

        return vertices, faces

    def to_triangles(self, nu=16, nv=16, du=None, dv=None):
        """Convert the surface to a list of triangles.

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
        list[list[:class:`compas.geometry.Point`]]

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        triangles = []
        for a, b, c, d in faces:
            triangles.append([vertices[a], vertices[b], vertices[c]])
            triangles.append([vertices[a], vertices[c], vertices[d]])
        return triangles

    def to_quads(self, nu=16, nv=16, du=None, dv=None):
        """Convert the surface to a list of quads.

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
        list[list[:class:`compas.geometry.Point`]]

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        quads = []
        for a, b, c, d in faces:
            quads.append([vertices[a], vertices[b], vertices[c], vertices[d]])
        return quads

    def to_polyhedron(self, nu=16, nv=16, du=None, dv=None):
        """Convert the surface to a polyhedron.

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
        """Convert the surface to a mesh.

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
        """Convert the surface to a BREP representation.

        Returns
        -------
        :class:`compas.geometry.Brep`
            A BREP object.

        """
        raise NotImplementedError

    # ==============================================================================
    # Transformations
    # ==============================================================================

    def transform(self, T):
        """Transform the local coordinate system of the surface.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
            The transformation.

        Returns
        -------
        None
            The curve is modified in-place.

        Notes
        -----
        The transformation matrix is applied to the local coordinate system of the surface.
        Transformations are limited to (combinations of) translations and rotations.
        All other components of the transformation matrix are ignored.

        """
        self.frame.transform(T)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def space_u(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the U direction.

        Parameters
        ----------
        n : int, optional
            The number of parameters.

        Returns
        -------
        list[float]

        """
        umin, umax = self.domain_u
        return linspace(umin, umax, n)

    def space_v(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the V direction.

        Parameters
        ----------
        n : int, optional
            The number of parameters.

        Returns
        -------
        list[float]

        """
        vmin, vmax = self.domain_v
        return linspace(vmin, vmax, n)

    def isocurve_u(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`compas.geometry.Curve`

        """
        raise NotImplementedError

    def isocurve_v(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`compas_occ.geometry.Curve`

        """
        raise NotImplementedError

    def boundary(self):
        """Compute the boundary curves of the surface.

        Returns
        -------
        list[:class:`compas.geometry.Curve`]

        """
        raise NotImplementedError

    def pointgrid(self, nu=10, nv=10):
        """Compute point locations corresponding to evenly spaced parameters over the surface domain.

        Parameters
        ----------
        nu : int, optional
            The size of the grid in the U direction.
        nv : int, optional
            The size of the grid in the V direction.

        """
        return [self.point_at(i, j) for i, j in product(self.space_u(nu), self.space_v(nv))]

    def point_at(self, u, v):
        """Compute a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        raise NotImplementedError

    def normal_at(self, u, v):
        """Compute a normal at a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        raise NotImplementedError

    def curvature_at(self, u, v):
        """Compute the curvature at a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Vector`

        """
        raise NotImplementedError

    def frame_at(self, u, v):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`compas.geometry.Frame`

        """
        raise NotImplementedError

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def closest_point(self, point, return_parameters=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : Point
            The point to project to the surface.
        return_parameters : bool, optional
            If True, return the surface UV parameters in addition to the closest point.

        Returns
        -------
        :class:`compas.geometry.Point` | tuple[:class:`compas.geometry.Point`, tuple[float, float]]
            If `return_parameters` is False, the nearest point on the surface.
            If `return_parameters` is True, the UV parameters in addition to the nearest point on the surface.

        """
        raise NotImplementedError

    def aabb(self, precision=0.0, optimal=False):
        """Compute the axis aligned bounding box of the surface.

        Parameters
        ----------
        precision : float, optional
        optimal : bool, optional

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

    def obb(self, precision=0.0):
        """Compute the oriented bounding box of the surface.

        Parameters
        ----------
        precision : float, optional

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

    def intersections_with_line(self, line):
        """Compute the intersections with a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`

        Returns
        -------
        list[:class:`compas.geometry.Point`]

        """
        raise NotImplementedError

    def intersections_with_curve(self, curve):
        """Compute the intersections with a curve.

        Parameters
        ----------
        line : :class:`compas.geometry.Curve`

        Returns
        -------
        list[:class:`compas.geometry.Point`]

        """
        raise NotImplementedError

    def intersections_with_plane(self, plane):
        """Compute the intersections with a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`

        Returns
        -------
        list[:class:`compas.geometry.Curve`]

        """
        raise NotImplementedError
