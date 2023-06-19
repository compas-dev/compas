from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import product

from compas.geometry import Geometry
from compas.plugins import pluggable
from compas.utilities import linspace


@pluggable(category="factories")
def new_surface(cls, *args, **kwargs):
    raise NotImplementedError


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

    def __init__(self, name=None):
        super(Surface, self).__init__(name=name)

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        return "<Surface with parameter domain {}>".format(self.domain)

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def u_domain(self):
        raise NotImplementedError

    @property
    def v_domain(self):
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

    def to_tesselation(self):
        """Convert the surface to a triangle mesh.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`

        """
        raise NotImplementedError

    def to_mesh(self, nu=100, nv=None):
        """Convert the surface to a quad mesh.

        Parameters
        ----------
        nu : int, optional
            Number of faces in the U direction.
        nv : int, optional
            Number of faces in the V direction.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`

        """
        from compas.datastructures import Mesh

        nv = nv or nu
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

        return Mesh.from_vertices_and_faces(vertices, faces)

    def to_triangles(self, nu=100, nv=None):
        """Convert the surface to a list of triangles.

        Parameters
        ----------
        nu : int, optional
            Number of quads in the U direction.
            Every quad has two triangles.
        nv : int, optional
            Number of quads in the V direction.
            Every quad has two triangles.

        Returns
        -------
        list[list[:class:`~compas.geometry.Point`]]

        """
        nv = nv or nu
        vertices = [self.point_at(i, j) for i, j in product(self.u_space(nu + 1), self.v_space(nv + 1))]
        triangles = []
        for i, j in product(range(nu), range(nv)):
            a = i * (nv + 1) + j
            b = (i + 1) * (nv + 1) + j
            c = (i + 1) * (nv + 1) + j + 1
            d = i * (nv + 1) + j + 1
            triangles.append([vertices[a], vertices[b], vertices[c]])
            triangles.append([vertices[a], vertices[c], vertices[d]])
        return triangles

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

    def xyz(self, nu=10, nv=10):
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
