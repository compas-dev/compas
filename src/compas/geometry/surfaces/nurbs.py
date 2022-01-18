from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import product

from compas.plugins import pluggable
from compas.geometry import Point
from compas.utilities import linspace
from compas.utilities import meshgrid

from .surface import Surface


@pluggable(category='factories')
def new_nurbssurface(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_parameters(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_points(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_fill(*args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_step(*args, **kwargs):
    raise NotImplementedError


class NurbsSurface(Surface):
    """A NURBS surface is defined by control points, weights, knots, and a degree, in two directions U and V.

    Parameters
    ----------
    name : str, optional
        The name of the surface.

    Attributes
    ----------
    points : list[list[:class:`compas.geometry.Point`]], read-only
        The control points as rows along the U direction.
    weights : list[float], read-only
        The weights of the control points.
    u_knots : list[float], read-only
        The knots in the U direction, without multiplicity.
    v_knots : list[float], read-only
        The knots in the V direction, without multiplicity.
    u_mults : list[int], read-only
        Multiplicity of the knots in the U direction.
    v_mults : list[int], read-only
        Multiplicity of the knots in the V direction.
    u_degree : int, read-only
        The degree of the curve in the U direction.
    v_degree : int, read-only
        The degree of the curve in the V direction.
    u_domain : tuple[float, float], read-only
        Min/Max values of the parameters in the U direction.
    v_domain : tuple[float, float], read-only
        Min/Max values of the parameters in the V direction.
    is_u_periodic : bool, read-only
        Flag indicating that the surface is periodic in the U direction.
    is_v_periodic : bool, read-only
        Flag indicating that the surface is periodic in the V direction.

    """

    def __new__(cls, *args, **kwargs):
        return new_nurbssurface(*args, **kwargs)

    def __init__(self, name=None):
        super(NurbsSurface, self).__init__(name=name)

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        lines = [
            'NurbsSurface',
            '------------',
            'Points: {}'.format(self.points),
            'Weights: {}'.format(self.weights),
            'U Knots: {}'.format(self.u_knots),
            'V Knots: {}'.format(self.v_knots),
            'U Mults: {}'.format(self.u_mults),
            'V Mults: {}'.format(self.v_mults),
            'U Degree: {}'.format(self.u_degree),
            'V Degree: {}'.format(self.v_degree),
            'U Domain: {}'.format(self.u_domain),
            'V Domain: {}'.format(self.v_domain),
            'U Periodic: {}'.format(self.is_u_periodic),
            'V Periodic: {}'.format(self.is_v_periodic),
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : The schema of the data representation."""
        from schema import Schema
        from compas.data import is_float3
        from compas.data import is_sequence_of_int
        from compas.data import is_sequence_of_float
        return Schema({
            'points': lambda points: all(is_float3(point) for point in points),
            'weights': is_sequence_of_float,
            'u_knots': is_sequence_of_float,
            'v_knots': is_sequence_of_float,
            'u_mults': is_sequence_of_int,
            'v_mults': is_sequence_of_int,
            'u_degree': int,
            'v_degree': int,
            'is_u_periodic': bool,
            'is_v_periodic': bool
        })

    @property
    def JSONSCHEMANAME(self):
        """dict : The schema of the data representation in JSON format."""
        raise NotImplementedError

    @property
    def dtype(self):
        """str : The type of the object in the form of a '2-level' import and a class name."""
        return 'compas.geometry/NurbsSurface'

    @property
    def data(self):
        """dict : Representation of the curve as a dict containing only native Python objects."""
        return {
            'points': [[point.data for point in row] for row in self.points],
            'weights': self.weights,
            'u_knots': self.u_knots,
            'v_knots': self.v_knots,
            'u_mults': self.u_mults,
            'v_mults': self.v_mults,
            'u_degree': self.u_degree,
            'v_degree': self.v_degree,
            'is_u_periodic': self.is_u_periodic,
            'is_v_periodic': self.is_v_periodic
        }

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`
            The constructed surface.

        """
        points = [[Point.from_data(point) for point in row] for row in data['points']]
        weights = data['weights']
        u_knots = data['u_knots']
        v_knots = data['v_knots']
        u_mults = data['u_mults']
        v_mults = data['v_mults']
        u_degree = data['u_degree']
        v_degree = data['v_degree']
        is_u_periodic = data['is_u_periodic']
        is_v_periodic = data['is_v_periodic']
        return cls.from_parameters(
            points,
            weights,
            u_knots, v_knots,
            u_mults, v_mults,
            u_degree, v_degree,
            is_u_periodic, is_v_periodic
        )

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls, points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic=False, is_v_periodic=False):
        """Construct a NURBS surface from explicit parameters.

        Parameters
        ----------
        points : list[list[[float, float, float], :class:`compas.geometry.Point`]]
            The control points.
        weights : list[list[float]]
            The weights of the control points.
        u_knots : list[float]
            The knots in the U direction, without multiplicity.
        v_knots : list[float]
            The knots in the V direction, without multiplicity.
        u_mults : list[int]
            Multiplicity of the knots in the U direction.
        v_mults : list[int]
            Multiplicity of the knots in the V direction.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_parameters(
            points,
            weights,
            u_knots,
            v_knots,
            u_mults,
            v_mults,
            u_degree,
            v_degree,
            is_u_periodic=is_u_periodic,
            is_v_periodic=is_v_periodic
        )

    @classmethod
    def from_points(cls, points, u_degree=3, v_degree=3):
        """Construct a NURBS surface from control points.

        Parameters
        ----------
        points : list[list[[float, float, float] or :class:`compas.geometry.Point`]]
            The control points.
        u_degree : int
            Degree in the U direction.
        v_degree : int
            Degree in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_points(points, u_degree=u_degree, v_degree=v_degree)

    @classmethod
    def from_meshgrid(cls, nu=10, nv=10):
        """Construct a NURBS surface from a mesh grid.

        Parameters
        ----------
        nu : int, optional
            Number of control points in the U direction.
        nv : int, optional
            Number of control points in the V direction.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        UU, VV = meshgrid(linspace(0, nu, nu + 1), linspace(0, nv, nv + 1))
        points = []
        for U, V in zip(UU, VV):
            row = []
            for u, v in zip(U, V):
                row.append(Point(u, v, 0.0))
            points.append(row)
        return cls.from_points(points=points)

    @classmethod
    def from_step(cls, filepath):
        """Load a NURBS surface from a STP file.

        Parameters
        ----------
        filepath : str

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_step(filepath)

    @classmethod
    def from_fill(cls, curve1, curve2):
        """Construct a NURBS surface from the infill between two NURBS curves.

        Parameters
        ----------
        curve1 : :class:`compas.geometry.NurbsCurve`
        curve2 : :class:`compas.geometry.NurbsCurve`

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return new_nurbssurface_from_fill(curve1, curve2)

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
        :class:`compas.datastructures.Mesh`

        """
        from compas.datastructures import Mesh

        nv = nv or nu
        vertices = [self.point_at(i, j) for i, j in product(self.u_space(nu + 1), self.v_space(nv + 1))]
        faces = [[
            i * (nv + 1) + j,
            (i + 1) * (nv + 1) + j,
            (i + 1) * (nv + 1) + j + 1,
            i * (nv + 1) + j + 1
        ] for i, j in product(range(nu), range(nv))]

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
        list[list[:class:`compas.geometry.Point`]]

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
    # Properties
    # ==============================================================================

    @property
    def points(self):
        raise NotImplementedError

    @property
    def weights(self):
        raise NotImplementedError

    @property
    def u_knots(self):
        raise NotImplementedError

    @property
    def v_knots(self):
        raise NotImplementedError

    @property
    def u_mults(self):
        raise NotImplementedError

    @property
    def v_mults(self):
        raise NotImplementedError

    @property
    def u_degree(self):
        raise NotImplementedError

    @property
    def v_degree(self):
        raise NotImplementedError

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
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the surface.

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        return NurbsSurface.from_parameters(
            self.points,
            self.weights,
            self.u_knots,
            self.v_knots,
            self.u_mults,
            self.v_mults,
            self.u_degree,
            self.v_degree,
            self.is_u_periodic,
            self.is_v_periodic
        )

    def transform(self, T):
        """Transform this surface.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed(self, T):
        """Transform an independent copy of this surface.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`

        Returns
        -------
        :class:`compas.geometry.NurbsSurface`

        """
        copy = self.copy()
        copy.transform(T)
        return copy

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
        :class:`compas.geometry.NurbsCurve`

        """
        raise NotImplementedError

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v.

        Parameters
        ----------
        v : float

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`

        """
        raise NotImplementedError

    def boundary(self):
        """Compute the boundary curves of the surface.

        Returns
        -------
        list[:class:`compas.geometry.NurbsCurve`]

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

    def closest_point(self, point, return_parameters=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The test point.
        return_parameters : bool, optional
            If True, return the UV parameters of the closest point in addition to the point location.

        Returns
        -------
        :class:`compas.geometry.Point` or tuple[:class:`compas.geometry.Point`, float, float]
            If `return_parameters` is False, only the point location is returned.
            If `return_parameters` is True, the point location and the corresponding parameter are returned.

        """
        raise NotImplementedError

    def aabb(self):
        """Compute the axis aligned bounding box of the surface.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

    def obb(self):
        """Compute the oriented bounding box of the surface.

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
            The intersection line.

        Returns
        -------
        :class:`compas.geometry.Point`
            The intersection point.

        """
        raise NotImplementedError
