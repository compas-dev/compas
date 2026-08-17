from dataclasses import dataclass
from typing import Callable
from typing import Iterator
from typing import Optional
from typing import TypeVar

from compas.tolerance import TOL

from .geometry import Geometry
from .intersections import intersection_line_line
from .intersections import intersection_line_plane
from .intersections import intersection_plane_plane
from .line import Line
from .plane import Plane
from .point import Point


@dataclass(frozen=True)
class IntersectionResult:
    """The geometry produced by an intersection operation.

    Parameters
    ----------
    geometry
        The intersection geometry.

    Examples
    --------
    >>> result = intersection(Line([0, 0, 0], [1, 0, 0]), Plane.worldYZ())
    >>> result.points
    (Point(x=0.000, y=0.000, z=0.000),)
    >>> bool(result)
    True

    """

    geometry: tuple[Geometry, ...] = ()

    def __bool__(self) -> bool:
        return bool(self.geometry)

    def __len__(self) -> int:
        return len(self.geometry)

    def __iter__(self) -> Iterator[Geometry]:
        return iter(self.geometry)

    @property
    def number_of_intersections(self) -> int:
        """The number of intersection geometries."""
        return len(self)

    @property
    def points(self) -> tuple[Point, ...]:
        """The point intersections."""
        return tuple(item for item in self.geometry if isinstance(item, Point))

    @property
    def lines(self) -> tuple[Line, ...]:
        """The line intersections."""
        return tuple(item for item in self.geometry if isinstance(item, Line))


HandlerType = TypeVar("HandlerType", bound=Callable[..., IntersectionResult])


class Intersection:
    """Symmetric type-based dispatch for geometry intersections.

    The predefined `intersection` instance is the public entry point for
    computing intersections. Call it with two supported geometry objects. It
    returns an `IntersectionResult`, which can be inspected through its
    `geometry`, `points`, and `lines` properties, or iterated directly.

    Use `register` to add a handler for a pair of geometry types. A registered
    handler receives the two geometry objects in registration order, followed
    by the tolerance.

    Examples
    --------
    Compute the intersection of a line and a plane with the predefined
    dispatcher.

    >>> from compas.geometry import intersection
    >>> line = Line([0, 0, -1], [0, 0, 1])
    >>> result = intersection(line, Plane.worldXY())
    >>> result.points
    (Point(x=0.000, y=0.000, z=0.000),)
    >>> result.number_of_intersections
    1

    The order of the input objects does not matter.

    >>> intersection(Plane.worldXY(), line) == result
    True

    Create a separate dispatcher and register a custom handler when extending
    the supported type combinations.

    >>> dispatcher = Intersection()
    >>> @dispatcher.register(Line, Plane)
    ... def line_plane(line, plane, tol=None):
    ...     return IntersectionResult((line.start,))
    >>> dispatcher(Plane.worldXY(), Line([0, 0, 0], [1, 0, 0])).points
    (Point(x=0.000, y=0.000, z=0.000),)

    """

    def __init__(self) -> None:
        self._registry: dict[tuple[type[object], type[object]], Callable[..., IntersectionResult]] = {}

    def register(self, type_a: type[Geometry], type_b: type[Geometry]) -> Callable[[HandlerType], HandlerType]:
        """Register an intersection handler for a pair of geometry types.

        Parameters
        ----------
        type_a
            The first geometry type expected by the handler.
        type_b
            The second geometry type expected by the handler.

        Returns
        -------
        Callable[[HandlerType], HandlerType]
            A decorator that registers and returns the handler.

        Raises
        ------
        ValueError
            If either ordering of the type pair is already registered.

        """

        def decorator(handler: HandlerType) -> HandlerType:
            key = type_a, type_b
            reverse_key = type_b, type_a
            if key in self._registry or reverse_key in self._registry:
                raise ValueError("An intersection handler is already registered for {0} and {1}.".format(type_a.__name__, type_b.__name__))
            self._registry[key] = handler
            return handler

        return decorator

    def __call__(self, a: Geometry, b: Geometry, tol: Optional[float] = None) -> IntersectionResult:
        """Compute the intersection of two geometry objects.

        Parameters
        ----------
        a
            The first geometry object.
        b
            The second geometry object.
        tol
            The tolerance used by the intersection handler.

        Returns
        -------
        IntersectionResult
            The intersection geometry.

        Raises
        ------
        TypeError
            If no handler is registered for the geometry-type pair.

        """
        mro_a = type(a).__mro__
        mro_b = type(b).__mro__
        for candidate_a in mro_a:
            for candidate_b in mro_b:
                handler = self._registry.get((candidate_a, candidate_b))
                if handler is not None:
                    return handler(a, b, tol)
                handler = self._registry.get((candidate_b, candidate_a))
                if handler is not None:
                    return handler(b, a, tol)
        raise TypeError("Intersection is not implemented for {0} and {1}.".format(type(a).__name__, type(b).__name__))


intersection = Intersection()


@intersection.register(Line, Line)
def _intersection_line_line(a: Line, b: Line, tol: Optional[float] = None) -> IntersectionResult:
    point1, point2 = intersection_line_line(a, b, tol=tol)
    if point1 is None or point2 is None or not TOL.is_allclose(point1, point2, atol=tol):
        return IntersectionResult()
    return IntersectionResult((Point(point1[0], point1[1], point1[2]),))


@intersection.register(Line, Plane)
def _intersection_line_plane(line: Line, plane: Plane, tol: Optional[float] = None) -> IntersectionResult:
    point = intersection_line_plane(line, plane, tol=tol)
    if point is None:
        return IntersectionResult()
    return IntersectionResult((Point(point[0], point[1], point[2]),))


@intersection.register(Plane, Plane)
def _intersection_plane_plane(a: Plane, b: Plane, tol: Optional[float] = None) -> IntersectionResult:
    line = intersection_plane_plane(a, b, tol=tol)
    if line is None:
        return IntersectionResult()
    return IntersectionResult((Line(line[0], line[1]),))
