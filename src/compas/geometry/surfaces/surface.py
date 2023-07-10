from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import product

from compas.geometry import Geometry
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Point
from compas.plugins import pluggable
from compas.utilities import linspace


@pluggable(category="factories")
def new_surface(cls, *args, **kwargs):
    surface = object.__new__(cls)
    surface.__init__(*args, **kwargs)
    return surface


@pluggable(category="factories")
def new_surface_from_plane(cls, *args, **kwargs):
    raise NotImplementedError


class Surface(Geometry):
    """Class representing a general surface object.

    Parameters
    ----------
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The local coordinate system of the surface.
        Default is the world coordinate system.
    transformation : :class:`~compas.geometry.Transformation`, read-only
        The transformation from the surface's local coordinate system to the world coordinate system.
    u_domain : tuple[float, float], read-only
        The parameter domain of the surface in the U direction.
    v_domain : tuple[float, float], read-only
        The parameter domain of the surface in the V direction.
    is_u_periodic : bool, read-only
        Flag indicating if the surface is periodic in the U direction.
    is_v_periodic : bool, read-only
        Flag indicating if the surface is periodic in the V direction.

    """

    def __new__(cls, *args, **kwargs):
        return new_surface(cls, *args, **kwargs)

    def __init__(self, frame=None, u_domain=None, v_domain=None, name=None):
        super(Surface, self).__init__(name=name)
        self._frame = None
        self._transformation = None
        self._u_domain = None
        self._v_domain = None
        self._point = None
        if frame:
            self.frame = frame
        self.u_domain = u_domain or (0.0, 1.0)
        self.v_domain = v_domain or (0.0, 1.0)

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        return "<Surface with parameter domain U: {} and V: {}>".format(self.u_domain, self.v_domain)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        raise NotImplementedError

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        """Construct a surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Surface`
            The constructed surface.

        """
        return cls(**data)

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
    def u_domain(self):
        if not self._u_domain:
            self._u_domain = (0.0, 1.0)
        return self._u_domain

    @u_domain.setter
    def u_domain(self, domain):
        if not domain:
            self._u_domain = None
            return
        a, b = domain
        self._u_domain = a, b

    @property
    def v_domain(self):
        if not self._v_domain:
            self._v_domain = (0.0, 1.0)
        return self._v_domain

    @v_domain.setter
    def v_domain(self, domain):
        if not domain:
            self._v_domain = None
            return
        a, b = domain
        self._v_domain = a, b

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def is_u_periodic(self):
        raise NotImplementedError

    @property
    def is_v_periodic(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_step(cls, filepath):
        """Load a surface from a STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`~compas.geometry.Surface`

        """
        raise NotImplementedError

    @classmethod
    def from_obj(cls, filepath):
        """Load a surface from an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`~compas.geometry.Surface`

        """
        raise NotImplementedError

    @classmethod
    def from_plane(cls, plane, *args, **kwargs):
        """Construct a surface from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.

        Returns
        -------
        :class:`~compas.geometry.Surface`

        """
        return new_surface_from_plane(cls, plane, *args, **kwargs)

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
        u_domain = self.u_domain
        v_domain = self.v_domain

        du = du or u_domain
        dv = dv or v_domain

        self.u_domain = du
        self.v_domain = dv

        vertices = [self.point_at(i, j) for i, j in product(self.u_space(nu + 1), self.v_space(nv + 1))]
        faces = [
            [
                i * (nv + 1) + j,
                (i + 1) * (nv + 1) + j,
                (i + 1) * (nv + 1) + j + 1,
                i * (nv + 1) + j + 1,
            ]
            for i, j in product(range(nu), range(nv))
        ]

        self.u_domain = u_domain
        self.v_domain = v_domain

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
        list[list[:class:`~compas.geometry.Point`]]

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
        list[list[:class:`~compas.geometry.Point`]]

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

    def to_tesselation(self):
        """Convert the surface to a triangle mesh.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`

        """
        raise NotImplementedError

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
        T : :class:`~compas.geometry.Transformation`
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
        # T[0, 0] = 1
        # T[1, 1] = 1
        # T[2, 2] = 1
        # T[3, 3] = 1

        # T[0, 3] = 0
        # T[1, 3] = 0
        # T[2, 3] = 0

        # T[3, 0] = 0
        # T[3, 1] = 0
        # T[3, 2] = 0

        self.frame.transform(T)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def u_space(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the U direction.

        Parameters
        ----------
        n : int, optional
            The number of parameters.

        Returns
        -------
        list[float]

        """
        umin, umax = self.u_domain
        return linspace(umin, umax, n)

    def v_space(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the V direction.

        Parameters
        ----------
        n : int, optional
            The number of parameters.

        Returns
        -------
        list[float]

        """
        vmin, vmax = self.v_domain
        return linspace(vmin, vmax, n)

    def u_isocurve(self, u):
        """Compute the isoparametric curve at parameter u.

        Parameters
        ----------
        u : float

        Returns
        -------
        :class:`~compas.geometry.Curve`

        """
        raise NotImplementedError

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`~compas_occ.geometry.Curve`

        """
        raise NotImplementedError

    def boundary(self):
        """Compute the boundary curves of the surface.

        Returns
        -------
        list[:class:`~compas.geometry.Curve`]

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
        return [self.point_at(i, j) for i, j in product(self.u_space(nu), self.v_space(nv))]

    def point_at(self, u, v):
        """Compute a point on the surface.

        Parameters
        ----------
        u : float
        v : float

        Returns
        -------
        :class:`~compas.geometry.Point`

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
        :class:`~compas.geometry.Vector`

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
        :class:`~compas.geometry.Frame`

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
        :class:`~compas.geometry.Point` | tuple[:class:`~compas.geometry.Point`, tuple[float, float]]
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
        :class:`~compas.geometry.Box`

        """
        raise NotImplementedError

    def obb(self, precision=0.0):
        """Compute the oriented bounding box of the surface.

        Parameters
        ----------
        precision : float, optional

        Returns
        -------
        :class:`~compas.geometry.Box`

        """
        raise NotImplementedError

    def intersections_with_line(self, line):
        """Compute the intersections with a line.

        Parameters
        ----------
        line : :class:`~compas.geometry.Line`

        Returns
        -------
        list[:class:`~compas.geometry.Point`]

        """
        raise NotImplementedError

    def intersections_with_curve(self, curve):
        """Compute the intersections with a curve.

        Parameters
        ----------
        line : :class:`~compas.geometry.Curve`

        Returns
        -------
        list[:class:`~compas.geometry.Point`]

        """
        raise NotImplementedError

    def intersections_with_plane(self, plane):
        """Compute the intersections with a plane.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane`

        Returns
        -------
        list[:class:`~compas.geometry.Curve`]

        """
        raise NotImplementedError

    # def patch(self, u, v, du=1, dv=1):
    #     """Construct a NURBS surface patch from the surface at the given UV parameters.

    #     Parameters
    #     ----------
    #     u : float
    #     v : float
    #     du : int, optional
    #     dv : int, optional

    #     Returns
    #     -------
    #     :class:`~compas.geometry.NurbsSurface`

    #     """
    #     raise NotImplementedError
