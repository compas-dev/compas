from os import PathLike
from typing import TYPE_CHECKING
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import TypeVar
from typing import Union
from typing import overload

from typing_extensions import Self

from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Plane
from compas.geometry import Transformation
from compas.itertools import linspace
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

from .._typing import TransformationType

if TYPE_CHECKING:
    from compas.geometry import Point
    from compas.geometry import Polygon
    from compas.geometry import Polyline
    from compas.geometry import Vector

CurveType = TypeVar("CurveType", bound="Curve")
FrameInput = Union[Frame, Sequence[CoordinateType]]
FilePath = Union[str, PathLike[str]]


@pluggable(category="factories")
def curve_from_native(cls: type[CurveType], *args: object, **kwargs: object) -> CurveType:
    raise PluginNotInstalledError


class Curve(Geometry):
    """Class representing a general parametric curve.

    Parameters
    ----------
    frame
        The local coordinate system of the curve.
        Default is the world coordinate system.
    name
        The name of the curve.

    See Also
    --------
    [`Arc`][compas.geometry.Arc], [`Circle`][compas.geometry.Circle],
    [`Ellipse`][compas.geometry.Ellipse], [`Line`][compas.geometry.Line],
    [`NurbsCurve`][compas.geometry.NurbsCurve], and
    [`Polyline`][compas.geometry.Polyline] are concrete curve types.

    Notes
    -----
    The curve is a "pluggable". This means that it does not provide an actual implementation
    of a parametric curve, but rather serves as an interface for different backends.
    If a backend is available, it will be used to construct the curve and provide its functionality.
    This backend is referred to as the "plugin" implementation of the curve.

    To activate the plugin mechanism, a backend should provide an implementation
    of `curve_from_native` and any other supported backend operation.

    """

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        if cls is Curve:
            raise TypeError("Making an instance of `Curve` using `Curve()` is not allowed. Please use one of the factory methods instead (`Curve.from_...`)")
        return object.__new__(cls)

    def __init__(self, frame: Optional[FrameInput] = None, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._frame: Optional[Frame] = None
        self._transformation: Optional[Transformation] = None
        if frame:
            self.frame = frame

    def __repr__(self) -> str:
        return "{0}(frame={1!r}, domain={2})".format(
            type(self).__name__,
            self.frame,
            self.domain,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def frame(self) -> Frame:
        """The local coordinate frame of the curve.

        Notes
        -----
        If no frame is assigned, the world XY frame is created on first access.
        Assigning a frame or three-item frame representation creates an
        independent `Frame` and invalidates the cached transformation.
        Assigning `None` restores the default world XY frame.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> source = Frame.worldYZ()
        >>> curve = Circle(radius=1, frame=source)
        >>> curve.frame == source and curve.frame is not source
        True
        >>> curve.frame = None
        >>> curve.frame == Frame.worldXY()
        True

        """
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame: Optional[FrameInput]) -> None:
        if not frame:
            self._frame = None
        else:
            self._frame = Frame(frame[0], frame[1], frame[2])
        self._transformation = None

    @property
    def transformation(self) -> Transformation:
        """The transformation from world XY to the curve frame.

        Notes
        -----
        The transformation is computed on first access and cached until the
        frame changes.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> curve = Circle(radius=1, frame=Frame.worldYZ())
        >>> curve.transformation is curve.transformation
        True

        """
        if not self._transformation:
            self._transformation = Transformation.from_frame_to_frame(Frame.worldXY(), self.frame)
        return self._transformation

    @property
    def plane(self) -> Plane:
        """The plane defined by the curve frame.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> curve = Circle(radius=1, frame=Frame.worldXY())
        >>> curve.plane == Plane.worldXY()
        True

        """
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def dimension(self) -> int:
        """The spatial dimension of the curve.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> Circle(radius=1).dimension
        3

        """
        return 3

    @property
    def domain(self) -> tuple[float, float]:
        """The parameter domain of the curve.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> Circle(radius=1).domain
        (0.0, 1.0)

        """
        return 0.0, 1.0

    @property
    def length(self) -> float:
        """The length of the curve."""
        raise NotImplementedError

    @property
    def is_closed(self) -> bool:
        """Whether the curve is closed."""
        raise NotImplementedError

    @property
    def is_periodic(self) -> bool:
        """Whether the curve is periodic."""
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, curve: object) -> Self:
        """Construct a parametric curve from a native curve geometry.

        Parameters
        ----------
        curve
            A native curve object.

        Returns
        -------
        Self
            A COMPAS curve.

        """
        return curve_from_native(cls, curve)

    @classmethod
    def from_obj(cls, filepath: FilePath) -> Self:
        """Load a curve from an OBJ file.

        Parameters
        ----------
        filepath
            The path to the file.

        Returns
        -------
        Self
            The loaded curve.

        """
        raise NotImplementedError

    @classmethod
    def from_step(cls, filepath: FilePath) -> Self:
        """Load a curve from a STP file.

        Parameters
        ----------
        filepath
            The path to the file.

        Returns
        -------
        Self
            The loaded curve.

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: FilePath, schema: str = "AP203") -> None:
        """Write the curve geometry to a STP file.

        Parameters
        ----------
        filepath
            The path of the output file.
        schema
            The STEP schema to use. Default is `"AP203"`.

        """
        raise NotImplementedError

    def to_obj(self, filepath: FilePath) -> None:
        """Write the curve geometry to an OBJ file.

        Parameters
        ----------
        filepath
            The path of the output file.

        """
        raise NotImplementedError

    def to_points(self, n: int = 10, domain: Optional[tuple[float, float]] = None) -> list["Point"]:
        """Convert the curve to a list of points.

        Parameters
        ----------
        n
            The number of points in the list.
            Default is `10`.
        domain
            Subset of the domain to use for the discretisation.
            Default is `None`, in which case the entire curve domain is used.

        Returns
        -------
        list[Point]
            The sampled points.

        """
        domain = domain or self.domain
        start, end = domain
        points = [self.point_at(t) for t in linspace(start, end, n)]
        return points

    def to_polyline(self, n: int = 128, domain: Optional[tuple[float, float]] = None) -> "Polyline":
        """Convert the curve to a polyline.

        Parameters
        ----------
        n
            The number of line segments in the polyline.
            Default is `128`.
        domain
            Subset of the domain to use for the discretisation.
            Default is `None`, in which case the entire curve domain is used.

        Returns
        -------
        Polyline
            The discretized curve.

        """
        from compas.geometry import Polyline

        points = self.to_points(n=n + 1, domain=domain)
        return Polyline(points)

    def to_polygon(self, n: int = 16) -> "Polygon":
        """Convert the curve to a polygon.

        Parameters
        ----------
        n
            The number of sides of the polygon.
            Default is `16`.

        Returns
        -------
        Polygon
            The discretized closed curve.

        Raises
        ------
        ValueError
            If the curve is not closed.

        """
        if not self.is_closed:
            raise ValueError("The curve is not closed.")

        from compas.geometry import Polygon

        points = self.to_points(n=n + 1)
        return Polygon(points[:-1])

    # ==============================================================================
    # Transformations
    # ==============================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform the local coordinate system of the curve.

        Parameters
        ----------
        transformation
            The transformation.

        Notes
        -----
        Transformations of frames are limited to rotations and translations.
        All other transformations have no effect.
        See [`Frame.transform`][compas.geometry.Frame.transform] for more information.

        """
        self.frame.transform(transformation)
        self._transformation = None

    # ==============================================================================
    # Methods
    # ==============================================================================

    def point_at(self, t: float) -> "Point":
        """Compute a point of the curve at a parameter.

        Parameters
        ----------
        t
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Point
            The corresponding point on the curve.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        [`Curve.normal_at`][compas.geometry.Curve.normal_at],
        [`Curve.tangent_at`][compas.geometry.Curve.tangent_at],
        [`Curve.frame_at`][compas.geometry.Curve.frame_at], and
        [`Curve.curvature_at`][compas.geometry.Curve.curvature_at].

        """
        raise NotImplementedError

    def normal_at(self, t: float) -> "Vector":
        """Compute the normal of the curve at a parameter.

        Parameters
        ----------
        t
            The value of the curve parameter.

        Returns
        -------
        Vector
            The corresponding normal vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        [`Curve.point_at`][compas.geometry.Curve.point_at],
        [`Curve.tangent_at`][compas.geometry.Curve.tangent_at],
        [`Curve.frame_at`][compas.geometry.Curve.frame_at], and
        [`Curve.curvature_at`][compas.geometry.Curve.curvature_at].

        """
        raise NotImplementedError

    def tangent_at(self, t: float) -> "Vector":
        """Compute the tangent vector of the curve at a parameter.

        Parameters
        ----------
        t
            The value of the curve parameter.

        Returns
        -------
        Vector
            The corresponding tangent vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        [`Curve.point_at`][compas.geometry.Curve.point_at],
        [`Curve.normal_at`][compas.geometry.Curve.normal_at],
        [`Curve.frame_at`][compas.geometry.Curve.frame_at], and
        [`Curve.curvature_at`][compas.geometry.Curve.curvature_at].

        """
        raise NotImplementedError

    def frame_at(self, t: float) -> Frame:
        """Compute the local frame of the curve at a parameter.

        Parameters
        ----------
        t
            The value of the curve parameter.

        Returns
        -------
        Frame
            The corresponding local frame.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        [`Curve.point_at`][compas.geometry.Curve.point_at],
        [`Curve.normal_at`][compas.geometry.Curve.normal_at],
        [`Curve.tangent_at`][compas.geometry.Curve.tangent_at], and
        [`Curve.curvature_at`][compas.geometry.Curve.curvature_at].

        """
        return Frame(self.point_at(t), self.tangent_at(t), self.normal_at(t))

    def curvature_at(self, t: float) -> "Vector":
        """Compute the curvature vector of the curve at a parameter.

        This is a vector pointing from the point on the curve at the specified parameter,
        to the center of the oscillating circle of the curve at that location.

        Note that this vector is parallel to the normal vector of the curve at that location.

        Parameters
        ----------
        t
            The value of the curve parameter.

        Returns
        -------
        Vector
            The corresponding curvature vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        [`Curve.point_at`][compas.geometry.Curve.point_at],
        [`Curve.normal_at`][compas.geometry.Curve.normal_at],
        [`Curve.tangent_at`][compas.geometry.Curve.tangent_at], and
        [`Curve.frame_at`][compas.geometry.Curve.frame_at].

        """
        raise NotImplementedError

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def reverse(self) -> None:
        """Reverse the parametrisation of the curve.

        See Also
        --------
        [`Curve.reversed`][compas.geometry.Curve.reversed]

        """
        raise NotImplementedError

    def reversed(self) -> Self:
        """Reverse a copy of the curve.

        Returns
        -------
        Self
            The reversed copy.

        See Also
        --------
        [`Curve.reverse`][compas.geometry.Curve.reverse]

        """
        copy = self.copy()
        copy.reverse()
        return copy

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[False] = False) -> "Point": ...

    @overload
    def closest_point(self, point: CoordinateType, return_parameter: Literal[True]) -> tuple["Point", float]: ...

    def closest_point(self, point: CoordinateType, return_parameter: bool = False) -> Union["Point", tuple["Point", float]]:
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point
            The test point.
        return_parameter
            If `True`, also return the parameter corresponding to the closest point.

        Returns
        -------
        Point | tuple[Point, float]
            The closest point, optionally paired with its curve parameter.

        """
        raise NotImplementedError

    @overload
    def divide_by_count(self, count: int, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_count(self, count: int, return_points: Literal[True]) -> tuple[list[float], list["Point"]]: ...

    def divide_by_count(self, count: int, return_points: bool = False) -> Union[list[float], tuple[list[float], list["Point"]]]:
        """Compute the curve parameters that divide the curve into a specific number of equal length segments.

        Parameters
        ----------
        count
            The number of segments.
        return_points
            If `True`, return the list of division parameters,
            and the points corresponding to those parameters.
            If `False`, return only the list of parameters.

        Returns
        -------
        list[float] | tuple[list[float], list[Point]]
            The division parameters, optionally paired with the corresponding points.

        See Also
        --------
        [`Curve.divide_by_length`][compas.geometry.Curve.divide_by_length]

        """
        raise NotImplementedError

    @overload
    def divide_by_length(self, length: float, return_points: Literal[False] = False) -> list[float]: ...

    @overload
    def divide_by_length(self, length: float, return_points: Literal[True]) -> tuple[list[float], list["Point"]]: ...

    def divide_by_length(self, length: float, return_points: bool = False) -> Union[list[float], tuple[list[float], list["Point"]]]:
        """Compute the curve parameters that divide the curve into segments of specified length.

        Parameters
        ----------
        length
            The length of the segments.
        return_points
            If `True`, return the list of division parameters,
            and the points corresponding to those parameters.
            If `False`, return only the list of parameters.

        Returns
        -------
        list[float] | tuple[list[float], list[Point]]
            The division parameters, optionally paired with the corresponding points.

        See Also
        --------
        [`Curve.divide_by_count`][compas.geometry.Curve.divide_by_count]

        """
        raise NotImplementedError
