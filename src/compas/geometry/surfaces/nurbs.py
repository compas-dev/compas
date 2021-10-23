from itertools import product

from compas.plugins import pluggable
from compas.geometry import Point
from compas.utilities import meshgrid, linspace

from .surface import Surface


@pluggable(category='factories')
def new_nurbssurface(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_parameters(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_points(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_fill(cls, *args, **kwargs):
    raise NotImplementedError


@pluggable(category='factories')
def new_nurbssurface_from_step(cls, *args, **kwargs):
    raise NotImplementedError


class NurbsSurface(Surface):
    """Class representing a NURBS surface.

    Attributes
    ----------
    points: List[Point]
        The control points of the surface.
    weights: List[float]
        The weights of the control points.
    u_knots: List[float]
        The knot vector, in the U direction, without duplicates.
    v_knots: List[float]
        The knot vector, in the V direction, without duplicates.
    u_mults: List[int]
        The multiplicities of the knots in the knot vector of the U direction.
    v_mults: List[int]
        The multiplicities of the knots in the knot vector of the V direction.
    u_degree: int
        The degree of the polynomials in the U direction.
    v_degree: int
        The degree of the polynomials in the V direction.
    u_domain: Tuple[float, float]
        The parameter domain in the U direction.
    v_domain: Tuple[float, float]
        The parameter domain in the V direction.
    is_u_periodic: bool
        True if the curve is periodic in the U direction.
    is_v_periodic: bool
        True if the curve is periodic in the V direction.

    """

    @property
    def DATASCHEMA(self):
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
        raise NotImplementedError

    def __new__(cls, *args, **kwargs):
        return new_nurbssurface(cls, *args, **kwargs)

    def __init__(self, name=None):
        super().__init__(name=name)
        self._points = None

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        lines = [
            'NurbsSurface',
            '--------------',
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
    def data(self):
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
        return NurbsSurface.from_parameters(
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
        """Construct a NURBS surface from explicit parameters."""
        return new_nurbssurface_from_parameters(points, weights, u_knots, v_knots, u_mults, v_mults, u_degree, v_degree, is_u_periodic=is_u_periodic, is_v_periodic=is_v_periodic)

    @classmethod
    def from_points(cls, points, u_degree=3, v_degree=3):
        """Construct a NURBS surface from control points."""
        return new_nurbssurface_from_points(points, u_degree=u_degree, v_degree=v_degree)

    @classmethod
    def from_meshgrid(cls, nu=10, nv=10):
        """Construct a NURBS surface from a mesh grid."""
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
        """Load a NURBS surface from a STP file."""
        return new_nurbssurface_from_step(filepath)

    @classmethod
    def from_fill(cls, curve1, curve2):
        """Construct a NURBS surface from the infill between two NURBS curves."""
        return new_nurbssurface_from_fill(curve1, curve2)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the surface geometry to a STP file."""
        raise NotImplementedError

    def to_mesh(self, nu=100, nv=None):
        """Convert the surface to a quad mesh."""
        import numpy as np
        from functools import lru_cache
        from compas.datastructures import Mesh

        @lru_cache(maxsize=None)
        def point_at(i, j):
            return self.point_at(i, j)

        nv = nv or nu
        V, U = np.meshgrid(self.v_space(nv + 1), self.u_space(nu + 1), indexing='ij')
        quads = [[
            point_at(U[i + 0][j + 0], V[i + 0][j + 0]),
            point_at(U[i + 0][j + 1], V[i + 0][j + 1]),
            point_at(U[i + 1][j + 1], V[i + 1][j + 1]),
            point_at(U[i + 1][j + 0], V[i + 1][j + 0])
        ] for i, j in product(range(nv), range(nu))]

        return Mesh.from_polygons(quads)

    def to_triangles(self, nu=100, nv=None):
        """Convert the surface to a list of triangles."""
        import numpy as np
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def point_at(i, j):
            return self.point_at(i, j)

        nv = nv or nu
        V, U = np.meshgrid(self.v_space(nv + 1), self.u_space(nu + 1), indexing='ij')

        tris = [None] * (6 * nu * nv)
        index = 0
        for i, j in product(range(nv), range(nu)):
            tris[index + 0] = point_at(U[i + 0][j + 0], V[i + 0][j + 0])
            tris[index + 1] = point_at(U[i + 0][j + 1], V[i + 0][j + 1])
            tris[index + 2] = point_at(U[i + 1][j + 1], V[i + 1][j + 1])
            tris[index + 3] = point_at(U[i + 0][j + 0], V[i + 0][j + 0])
            tris[index + 4] = point_at(U[i + 1][j + 1], V[i + 1][j + 1])
            tris[index + 5] = point_at(U[i + 1][j + 0], V[i + 1][j + 0])
            index += 6

        return tris

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
        """Make an independent copy of the surface."""
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
        """Transform this surface."""
        raise NotImplementedError

    def transformed(self, T):
        """Transform an independent copy of this surface."""
        copy = self.copy()
        copy.transform(T)
        return copy

    def intersections_with_line(self, line):
        """Compute the intersections with a line."""
        raise NotImplementedError

    def u_space(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the U direction.
        """
        import numpy as np
        umin, umax = self.u_domain
        return np.linspace(umin, umax, n)

    def v_space(self, n=10):
        """Compute evenly spaced parameters over the surface domain in the V direction.
        """
        import numpy as np
        vmin, vmax = self.v_domain
        return np.linspace(vmin, vmax, n)

    def u_isocurve(self, u):
        """Compute the isoparametric curve at parameter u."""
        raise NotImplementedError

    def v_isocurve(self, v):
        """Compute the isoparametric curve at parameter v."""
        raise NotImplementedError

    def boundary(self):
        """Compute the boundary curves of the surface."""
        raise NotImplementedError

    def xyz(self, nu=10, nv=10):
        """Compute point locations corresponding to evenly spaced parameters over the surface domain.
        """
        import numpy as np
        U, V = np.meshgrid(self.u_space(nu), self.v_space(nv), indexing='ij')
        return [self.point_at(U[i, j], V[i, j]) for i, j in product(np.arange(nu), np.arange(nv))]

    def point_at(self, u, v):
        """Compute a point on the surface.
        """
        raise NotImplementedError

    def curvature_at(self, u, v):
        """Compute the curvature at a point on the surface.
        """
        raise NotImplementedError

    def frame_at(self, u, v):
        """Compute the local frame at a point on the curve.
        """
        raise NotImplementedError

    def closest_point(self, point, distance=None):
        """Compute the closest point on the curve to a given point.
        """
        raise NotImplementedError

    def aabb(self, precision=0.0, optimal=False):
        """Compute the axis aligned bounding box of the surface."""
        raise NotImplementedError

    def obb(self, precision=0.0):
        """Compute the oriented bounding box of the surface."""
        raise NotImplementedError
