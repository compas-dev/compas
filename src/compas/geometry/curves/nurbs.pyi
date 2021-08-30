from schema import Schema
from typing import Dict
from typing import List
from typing import Tuple
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Transformation
from compas.geometry import Circle
from compas.geometry import Ellipse
from compas.geometry import Box

from ._curve import Curve


class NurbsCurve(Curve):

    @property
    def DATASCHEMA(self) -> Schema: ...

    @property
    def JSONSCHEMANAME(self): ...

    def __init__(self, name=None) -> None: ...

    def __eq__(self, other: 'NurbsCurve') -> bool: ...

    def __str__(self) -> str: ...

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self) -> Dict: ...

    @data.setter
    def data(self, data: Dict): ...

    @classmethod
    def from_data(cls, data: Dict) -> 'NurbsCurve': ...

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls,
                        points: List[Point],
                        weights: List[float],
                        knots: List[float],
                        multiplicities: List[int],
                        degree: int,
                        is_periodic: bool = False) -> 'NurbsCurve': ...

    @classmethod
    def from_points(cls, points: List[Point], degree: int = 3) -> 'NurbsCurve': ...

    @classmethod
    def from_interpolation(cls, points: List[Point], precision: float = 1e-3) -> 'NurbsCurve': ...

    @classmethod
    def from_step(cls, filepath: str) -> 'NurbsCurve': ...

    @classmethod
    def from_arc(cls, arc) -> 'NurbsCurve': ...

    @classmethod
    def from_circle(cls, circle: Circle) -> 'NurbsCurve': ...

    @classmethod
    def from_ellipse(cls, ellipse: Ellipse) -> 'NurbsCurve': ...

    @classmethod
    def from_line(cls, line) -> 'NurbsCurve': ...

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: str, schema: str = "AP203") -> None: ...

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self) -> List[Point]: ...

    @property
    def weights(self) -> List[float]: ...

    @property
    def knots(self) -> List[float]: ...

    @property
    def knotsequence(self) -> List[float]: ...

    @property
    def multiplicities(self) -> List[int]: ...

    @property
    def degree(self) -> int: ...

    @property
    def dimension(self) -> int: ...

    @property
    def domain(self) -> Tuple[float, float]: ...

    @property
    def order(self) -> int: ...

    @property
    def start(self) -> Point: ...

    @property
    def end(self) -> Point: ...

    @property
    def is_closed(self) -> bool: ...

    @property
    def is_periodic(self) -> bool: ...

    @property
    def is_rational(self) -> bool: ...

    @property
    def bounding_box(self) -> Box: ...

    @property
    def length(self) -> float: ...

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self) -> 'NurbsCurve': ...

    def transform(self, T: Transformation) -> None: ...

    def transformed(self, T: Transformation) -> 'NurbsCurve': ...

    def space(self, n: int = 10) -> List[float]: ...

    def xyz(self, n: int = 10) -> List[Point]: ...

    def locus(self, resolution: int = 100) -> List[Point]: ...

    def point_at(self, u: float) -> Point: ...

    def tangent_at(self, u: float) -> Vector: ...

    def curvature_at(self, u: float) -> Vector: ...

    def frame_at(self, u: float) -> Vector: ...

    def closest_point(self, point: Point, distance: float = None) -> Point: ...

    def divide_by_count(self, count: int) -> List['NurbsCurve']: ...

    def divide_by_length(self, length: float) -> List['NurbsCurve']: ...

    def fair(self) -> None: ...
