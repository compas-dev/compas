from itertools import product

from typing import Generator, Optional, Tuple, List, Dict

import numpy as np

from compas.geometry import Point, Vector, Line, Frame, Box
from compas.geometry import Transformation
from compas.utilities import meshgrid, linspace
from compas.datastructures import Mesh

from ..curves import NurbsCurve
from ._surface import Surface


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

    def __init__(self, name: str = None) -> None:
        super().__init__(name=name)
        self._points = None

    def __eq__(self, other: 'NurbsSurface') -> bool:
        raise NotImplementedError

    def __str__(self):
        lines = [
            'NurbsSurface',
            '--------------',
            f'Points: {self.points}',
            f'Weights: {self.weights}',
            f'U Knots: {self.u_knots}',
            f'V Knots: {self.v_knots}',
            f'U Mults: {self.u_mults}',
            f'V Mults: {self.v_mults}',
            f'U Degree: {self.u_degree}',
            f'V Degree: {self.v_degree}',
            f'U Domain: {self.u_domain}',
            f'V Domain: {self.v_domain}',
            f'U Periodic: {self.is_u_periodic}',
            f'V Periodic: {self.is_v_periodic}',
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self) -> Dict:
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
    def data(self, data: Dict):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data: Dict) -> 'NurbsSurface':
        """Construct a BSpline surface from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_occ.geometry.NurbsSurface`
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
    def from_parameters(cls,
                        points: List[List[Point]],
                        weights: List[List[float]],
                        u_knots: List[float],
                        v_knots: List[float],
                        u_mults: List[int],
                        v_mults: List[int],
                        u_degree: int,
                        v_degree: int,
                        is_u_periodic: bool = False,
                        is_v_periodic: bool = False) -> 'NurbsSurface':
        """Construct a NURBS surface from explicit parameters."""
        raise NotImplementedError

    @classmethod
    def from_points(cls,
                    points: List[List[Point]],
                    u_degree: int = 3,
                    v_degree: int = 3) -> 'NurbsSurface':
        """Construct a NURBS surface from control points."""
        raise NotImplementedError

    @classmethod
    def from_meshgrid(cls, nu: int = 10, nv: int = 10) -> 'NurbsSurface':
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
    def from_step(cls, filepath: str) -> 'NurbsSurface':
        """Load a NURBS surface from a STP file."""
        raise NotImplementedError

    @classmethod
    def from_fill(cls, curve1: NurbsCurve, curve2: NurbsCurve) -> 'NurbsSurface':
        """Construct a NURBS surface from the infill between two NURBS curves."""
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: str, schema: str = "AP203") -> None:
        """Write the surface geometry to a STP file."""
        raise NotImplementedError

    def to_mesh(self, nu: int = 100, nv: Optional[int] = None) -> Mesh:
        """Convert the surface to a quad mesh."""
        from itertools import product
        from functools import lru_cache

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

    def to_triangles(self, nu: int = 100, nv: Optional[int] = None) -> List[Tuple[float, float, float]]:
        """Convert the surface to a list of triangles."""
        from itertools import product
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
    def points(self) -> List[List[Point]]:
        raise NotImplementedError

    @property
    def weights(self) -> List[List[float]]:
        raise NotImplementedError

    @property
    def u_knots(self) -> List[float]:
        raise NotImplementedError

    @property
    def v_knots(self) -> List[float]:
        raise NotImplementedError

    @property
    def u_mults(self) -> List[int]:
        raise NotImplementedError

    @property
    def v_mults(self) -> List[int]:
        raise NotImplementedError

    @property
    def u_degree(self) -> int:
        raise NotImplementedError

    @property
    def v_degree(self) -> int:
        raise NotImplementedError

    @property
    def u_domain(self) -> int:
        raise NotImplementedError

    @property
    def v_domain(self) -> int:
        raise NotImplementedError

    @property
    def is_u_periodic(self) -> bool:
        raise NotImplementedError

    @property
    def is_v_periodic(self) -> bool:
        raise NotImplementedError

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self) -> 'NurbsSurface':
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

    def transform(self, T: Transformation) -> None:
        """Transform this surface."""
        raise NotImplementedError

    def transformed(self, T: Transformation) -> 'NurbsSurface':
        """Transform an independent copy of this surface."""
        copy = self.copy()
        copy.transform(T)
        return copy

    def intersections_with_line(self, line: Line) -> List[Point]:
        """Compute the intersections with a line."""
        raise NotImplementedError

    def u_space(self, n: int = 10) -> Generator[float, None, None]:
        """Compute evenly spaced parameters over the surface domain in the U direction.
        """
        umin, umax = self.u_domain
        return np.linspace(umin, umax, n)

    def v_space(self, n: int = 10) -> Generator[float, None, None]:
        """Compute evenly spaced parameters over the surface domain in the V direction.
        """
        vmin, vmax = self.v_domain
        return np.linspace(vmin, vmax, n)

    def u_isocurve(self, u: float) -> NurbsCurve:
        """Compute the isoparametric curve at parameter u."""
        raise NotImplementedError

    def v_isocurve(self, v: float) -> NurbsCurve:
        """Compute the isoparametric curve at parameter v."""
        raise NotImplementedError

    def boundary(self) -> List[NurbsCurve]:
        """Compute the boundary curves of the surface."""
        raise NotImplementedError

    def xyz(self, nu: int = 10, nv: int = 10) -> List[Point]:
        """Compute point locations corresponding to evenly spaced parameters over the surface domain.
        """
        U, V = np.meshgrid(self.u_space(nu), self.v_space(nv), indexing='ij')
        return [self.point_at(U[i, j], V[i, j]) for i, j in product(np.arange(nu), np.arange(nv))]

    def point_at(self, u: float, v: float) -> Point:
        """Compute a point on the surface.
        """
        raise NotImplementedError

    def curvature_at(self, u: float, v: float) -> Tuple[float, float, Point, Vector]:
        """Compute the curvature at a point on the surface.
        """
        raise NotImplementedError

    def frame_at(self, u: float, v: float) -> Frame:
        """Compute the local frame at a point on the curve.
        """
        raise NotImplementedError

    def closest_point(self, point, distance=None) -> Point:
        """Compute the closest point on the curve to a given point.
        """
        raise NotImplementedError

    def aabb(self, precision: float = 0.0, optimal: bool = False) -> Box:
        """Compute the axis aligned bounding box of the surface."""
        raise NotImplementedError

    def obb(self, precision: float = 0.0) -> Box:
        """Compute the oriented bounding box of the surface."""
        raise NotImplementedError
