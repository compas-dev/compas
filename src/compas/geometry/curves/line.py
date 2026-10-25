from math import isclose
from typing import Any
from typing import Literal
from typing import Self
from typing import overload

from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Vector
from compas.itertools import linspace

from .._typing import TransformationType
from .curve import Curve


class LineCurve(Curve):
    """A finite linear parametric curve defined by two endpoints.

    `LineCurve` provides the common `Curve` API for linear geometry, while
    [`Line`][compas.geometry.Line] remains the lightweight two-point geometry
    primitive.

    Parameters
    ----------
    start
        The start point of the curve.
    end
        The end point of the curve.
    name
        The name of the curve.

    Notes
    -----
    The parameter domain is `[0, 1]`. Linear curves have zero curvature and no
    unique normal, so `normal_at()` returns `None` and `frame_at()` raises
    `ValueError` through the shared `Curve` contract.

    Examples
    --------
    >>> curve = LineCurve([0, 0, 0], [2, 0, 0])
    >>> curve.point_at(0.5)
    Point(x=1.000, y=0.000, z=0.000)
    >>> curve.length
    2.0

    """

    @property
    def __data__(self) -> dict[str, Any]:
        return {"start": self.start.__data__, "end": self.end.__data__}

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(data["start"], data["end"])

    def __init__(self, start: CoordinateType, end: CoordinateType, name: str | None = None) -> None:
        super().__init__(name=name)
        self._line = Line(start, end)

    def __repr__(self) -> str:
        return "{0}({1!r}, {2!r})".format(type(self).__name__, self.start, self.end)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LineCurve):
            return False
        return self.start == other.start and self.end == other.end

    @property
    def frame(self) -> Frame:
        """The read-only world XY frame.

        Linear-curve endpoints are stored in world coordinates.

        """
        if self._frame is None:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame: Frame | None) -> None:
        raise AttributeError("The frame of a LineCurve is read-only.")

    @property
    def start(self) -> Point:
        """The start point of the curve."""
        return self._line.start

    @start.setter
    def start(self, point: CoordinateType) -> None:
        self._line.start = point

    @property
    def end(self) -> Point:
        """The end point of the curve."""
        return self._line.end

    @end.setter
    def end(self, point: CoordinateType) -> None:
        self._line.end = point

    @property
    def length(self) -> float:
        """The distance from the start point to the end point."""
        return self._line.length

    @property
    def direction(self) -> Vector:
        """The unit vector from the start point to the end point."""
        return self._line.direction

    @property
    def is_closed(self) -> bool:
        """Whether the endpoints coincide."""
        return self.start == self.end

    @property
    def is_periodic(self) -> bool:
        """Whether the curve is periodic, which is always `False`."""
        return False

    @classmethod
    def from_line(cls, line: Line) -> Self:
        """Construct a linear curve from a line primitive.

        Parameters
        ----------
        line
            The source line.

        Returns
        -------
        Self
            The constructed independent curve.

        """
        return cls(line.start, line.end)

    @classmethod
    def from_point_and_vector(cls, point: CoordinateType, vector: CoordinateType) -> Self:
        """Construct a linear curve from a point and vector.

        Parameters
        ----------
        point
            The start point.
        vector
            The vector from the start point to the end point.

        Returns
        -------
        Self
            The constructed curve.

        """
        return cls.from_line(Line.from_point_and_vector(point, vector))

    @classmethod
    def from_point_direction_length(cls, point: CoordinateType, direction: CoordinateType, length: float) -> Self:
        """Construct a linear curve from a point, direction, and length.

        Parameters
        ----------
        point
            The start point.
        direction
            The direction from the start point to the end point.
        length
            The curve length.

        Returns
        -------
        Self
            The constructed curve.

        """
        return cls.from_line(Line.from_point_direction_length(point, direction, length))

    def to_line(self) -> Line:
        """Convert the curve to an independent line primitive.

        Returns
        -------
        Line
            The line primitive.

        """
        return Line(self.start, self.end)

    def point_at(self, t: float, world: bool = True) -> Point:
        """Compute the point at a normalized parameter.

        Parameters
        ----------
        t
            The parameter in `[0, 1]`.
        world
            Included for consistency with the curve API. Endpoints are stored
            in world coordinates, so both values are equivalent.

        Returns
        -------
        Point
            The point at the parameter.

        Raises
        ------
        ValueError
            If `t` is outside `[0, 1]`.

        """
        self._validate_parameter(t)
        return self._line.point_at(t)

    def tangent_at(self, t: float, world: bool = True) -> Vector:
        """Compute the unit tangent at a normalized parameter."""
        self._validate_parameter(t)
        return self.direction.copy()

    def normal_at(self, t: float, world: bool = True) -> None:
        """Return `None` because a linear curve has no unique normal."""
        self._validate_parameter(t)
        return None

    def curvature_at(self, t: float) -> Vector:
        """Compute the zero curvature vector at a normalized parameter."""
        self._validate_parameter(t)
        return Vector(0.0, 0.0, 0.0)

    def reverse(self) -> None:
        """Reverse the parametrisation of the curve."""
        self._line.flip()

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[False] = False) -> Point: ...

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[True]) -> tuple[Point, float]: ...

    def closest_point(self, point: CoordinateType, return_parameter: bool = False) -> Point | tuple[Point, float]:
        """Compute the closest point on the finite curve.

        Parameters
        ----------
        point
            The test point.
        return_parameter
            If `True`, also return the corresponding normalized parameter.

        Returns
        -------
        Point
            The closest point if `return_parameter` is `False`.
        tuple[Point, float]
            The closest point and parameter if `return_parameter` is `True`.

        """
        _, parameter = self._line.closest_point(point, return_parameter=True)
        parameter = max(0.0, min(1.0, parameter))
        closest = self.point_at(parameter)
        if return_parameter:
            return closest, parameter
        return closest

    @overload
    def divide_by_count(self, count: int, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_count(self, count: int, return_points: Literal[True]) -> tuple[list[float], list[Point]]: ...

    def divide_by_count(self, count: int, return_points: bool = False) -> list[float] | tuple[list[float], list[Point]]:
        """Compute parameters dividing the curve into equal-count segments."""
        if count < 1:
            raise ValueError("The number of segments should be at least one.")
        parameters = list(linspace(0.0, 1.0, count + 1))
        if return_points:
            return parameters, [self.point_at(parameter) for parameter in parameters]
        return parameters

    @overload
    def divide_by_length(self, length: float, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_length(self, length: float, return_points: Literal[True]) -> tuple[list[float], list[Point]]: ...

    def divide_by_length(self, length: float, return_points: bool = False) -> list[float] | tuple[list[float], list[Point]]:
        """Compute parameters separated by a specified distance."""
        if length <= 0.0:
            raise ValueError("The segment length should be positive.")
        if self.length == 0.0:
            raise ValueError("A zero-length curve cannot be divided by length.")
        step = length / self.length
        parameters = [index * step for index in range(int(self.length / length) + 1)]
        if parameters[-1] < 1.0 and isclose(parameters[-1], 1.0):
            parameters[-1] = 1.0
        if return_points:
            return parameters, [self.point_at(parameter) for parameter in parameters]
        return parameters

    def transform(self, transformation: TransformationType) -> None:
        """Transform the curve endpoints.

        Parameters
        ----------
        transformation
            The transformation.

        """
        self._line.transform(transformation)

    @staticmethod
    def _validate_parameter(t: float) -> None:
        if t < 0.0 or t > 1.0:
            raise ValueError("The parameter should be in the domain [0, 1].")
