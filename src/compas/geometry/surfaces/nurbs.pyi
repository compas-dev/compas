from schema import Schema
from typing import Generator
from typing import Optional

import compas

from compas.geometry import Point, Vector, Line, Frame, Box
from compas.geometry import Transformation

from ..curves import NurbsCurve
from .surface import Surface


class NurbsSurface(Surface):

    @property
    def DATASCHEMA(self) -> Schema: ...

    @property
    def JSONSCHEMANAME(self): ...

    def __init__(self, name: str = None) -> None: ...

    def __eq__(self, other: 'NurbsSurface') -> bool: ...

    def __str__(self) -> str: ...

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self) -> dict: ...

    @data.setter
    def data(self, data: dict):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data: dict) -> 'NurbsSurface': ...

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls,
                        points: list[list[Point]],
                        weights: list[list[float]],
                        u_knots: list[float],
                        v_knots: list[float],
                        u_mults: list[int],
                        v_mults: list[int],
                        u_degree: int,
                        v_degree: int,
                        is_u_periodic: bool = False,
                        is_v_periodic: bool = False) -> 'NurbsSurface': ...

    @classmethod
    def from_points(cls,
                    points: list[list[Point]],
                    u_degree: int = 3,
                    v_degree: int = 3) -> 'NurbsSurface': ...

    @classmethod
    def from_meshgrid(cls, nu: int = 10, nv: int = 10) -> 'NurbsSurface': ...

    @classmethod
    def from_step(cls, filepath: str) -> 'NurbsSurface': ...

    @classmethod
    def from_fill(cls, curve1: NurbsCurve, curve2: NurbsCurve) -> 'NurbsSurface': ...

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: str, schema: str = "AP203") -> None: ...

    def to_mesh(self, nu: int = 100, nv: Optional[int] = None) -> 'compas.datastructures.Mesh': ...

    def to_triangles(self, nu: int = 100, nv: Optional[int] = None) -> list[Point]: ...

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self) -> list[list[Point]]: ...

    @property
    def weights(self) -> list[list[float]]: ...

    @property
    def u_knots(self) -> list[float]: ...

    @property
    def v_knots(self) -> list[float]: ...

    @property
    def u_mults(self) -> list[int]: ...

    @property
    def v_mults(self) -> list[int]: ...

    @property
    def u_degree(self) -> int: ...

    @property
    def v_degree(self) -> int: ...

    @property
    def u_domain(self) -> int: ...

    @property
    def v_domain(self) -> int: ...

    @property
    def is_u_periodic(self) -> bool: ...

    @property
    def is_v_periodic(self) -> bool: ...

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self) -> 'NurbsSurface': ...

    def transform(self, T: Transformation) -> None: ...

    def transformed(self, T: Transformation) -> 'NurbsSurface': ...

    def intersections_with_line(self, line: Line) -> list[Point]: ...

    def u_space(self, n: int = 10) -> Generator[float, None, None]: ...

    def v_space(self, n: int = 10) -> Generator[float, None, None]: ...

    def u_isocurve(self, u: float) -> NurbsCurve: ...

    def v_isocurve(self, v: float) -> NurbsCurve: ...

    def boundary(self) -> list[NurbsCurve]: ...

    def xyz(self, nu: int = 10, nv: int = 10) -> list[Point]: ...

    def point_at(self, u: float, v: float) -> Point: ...

    def curvature_at(self, u: float, v: float) -> tuple[float, float, Point, Vector]: ...

    def frame_at(self, u: float, v: float) -> Frame: ...

    def closest_point(self, point: Point, distance: float = None) -> Point: ...

    def aabb(self, precision: float = 0.0, optimal: bool = False) -> Box: ...

    def obb(self, precision: float = 0.0) -> Box: ...
