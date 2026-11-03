from typing import TYPE_CHECKING
from typing import Generic
from typing import Self
from typing import TypeVar
from typing import cast

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Native
from compas.geometry import TessellationStrategy
from compas.geometry import Transformation
from compas.geometry import UGrid
from compas.geometry import UVGrid
from compas.geometry import transform_points

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation

StrategyT = TypeVar("StrategyT", bound=TessellationStrategy)


class Shape(Geometry, Generic[StrategyT]):
    """Base class for geometric shapes.

    Shapes are parametrically defined with respect to a local coordinate frame.
    The default frame is the world XY frame.

    Shapes are finite, closed objects, with a boundary that separates the interior from the exterior.
    They have a well-defined surface area and volume.

    Polygonization samples the parametric boundary into an independent
    `PolygonalSurface` while preserving its natural polygonal topology.
    Tessellation creates an ephemeral indexed triangular representation.
    Polygonization requires an explicit strategy matching the dimensionality
    of the shape. Tessellation uses a deterministic strategy when none is
    provided. Supported backends can convert a shape to a `Brep`.

    Breps support exact boolean operations.

    Parameters
    ----------
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the shape.

    """

    _tessellation_strategy = "uv"

    def __init__(self, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._frame: Frame | None = None
        self.frame = frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def frame(self) -> Frame:
        """The local coordinate frame of the shape.

        Notes
        -----
        Assigning a `Frame` creates an independent copy. Assigning `None`
        resets the frame to world XY on the next access.

        """
        if self._frame is None:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame: Frame | None) -> None:
        if frame is None:
            self._frame = None
        else:
            self._frame = frame.copy(cls=Frame)

    @property
    def transformation(self) -> Transformation:
        """The transformation from world XY to the shape frame."""
        return Transformation.from_frame(self.frame)

    # =============================================================================
    # Discretisation
    # =============================================================================

    def _compute_vertices(self, strategy: StrategyT) -> tuple[CoordinateType, ...]:
        """Compute fresh vertex coordinates in world coordinates."""
        local_vertices = self._compute_local_vertices(strategy)
        return tuple(tuple(vertex) for vertex in transform_points(local_vertices, self.transformation))

    def _compute_local_vertices(self, strategy: StrategyT) -> list[CoordinateType]:
        """Compute fresh vertex coordinates in the local shape frame."""
        raise NotImplementedError

    def _compute_faces(self, strategy: StrategyT) -> list[list[int]]:
        """Compute fresh face cycles for the requested strategy."""
        raise NotImplementedError

    # =============================================================================
    # Conversions
    # =============================================================================

    def _validate_tessellation_strategy(self, strategy: TessellationStrategy) -> StrategyT:
        if self._tessellation_strategy == "native":
            if not isinstance(strategy, Native):
                raise TypeError(f"{type(self).__name__} requires Native tessellation.")
            return cast(StrategyT, strategy)
        if self._tessellation_strategy == "u":
            if not isinstance(strategy, UGrid):
                raise TypeError(f"{type(self).__name__} requires UGrid tessellation.")
            if strategy.u < 3:
                raise ValueError("The U resolution should be at least 3.")
            return cast(StrategyT, strategy)
        if not isinstance(strategy, UVGrid):
            raise TypeError(f"{type(self).__name__} requires UVGrid tessellation.")
        if strategy.u < 3:
            raise ValueError("The U resolution should be at least 3.")
        if strategy.v < 3:
            raise ValueError("The V resolution should be at least 3.")
        return cast(StrategyT, strategy)

    def _default_tessellation_strategy(self) -> TessellationStrategy:
        if self._tessellation_strategy == "native":
            return Native()
        if self._tessellation_strategy == "u":
            return UGrid(64)
        return UVGrid(64, 64)

    def polygonize(self, strategy: TessellationStrategy) -> "PolygonalSurface":
        """Polygonize the shape with an explicit approximation strategy.

        Parameters
        ----------
        strategy
            The polygonization strategy supported by this shape.

        Returns
        -------
        PolygonalSurface
            An independent polygonal boundary representation.

        """
        from compas.geometry import PolygonalSurface

        supported_strategy = self._validate_tessellation_strategy(strategy)
        return PolygonalSurface(
            list(self._compute_vertices(supported_strategy)),
            [list(face) for face in self._compute_faces(supported_strategy)],
        )

    def tessellate(
        self,
        strategy: TessellationStrategy | None = None,
    ) -> "Tessellation[list[CoordinateType], tuple[tuple[int, ...], ...]]":
        """Tessellate the shape.

        Parameters
        ----------
        strategy
            The tessellation strategy supported by this shape. If `None`,
            `Native()` is used for native shapes, `UGrid(64)` for
            one-parameter shapes, and `UVGrid(64, 64)` for two-parameter
            shapes.

        Returns
        -------
        Tessellation
            The ephemeral indexed triangular representation.

        """
        from compas.geometry import Tessellation

        supported_strategy = self._validate_tessellation_strategy(strategy if strategy is not None else self._default_tessellation_strategy())
        vertices = list(self._compute_vertices(supported_strategy))
        triangles = []
        for raw_face in self._compute_faces(supported_strategy):
            face = tuple(raw_face)
            if len(face) == 3:
                triangles.append(face)
            elif len(face) == 4:
                a, b, c, d = face
                triangles.append((a, b, c))
                triangles.append((a, c, d))
            else:
                raise ValueError("Shape tessellation requires triangular or quadrilateral faces.")
        return Tessellation(vertices, tuple(triangles))

    def to_brep(self) -> "Brep":
        """Convert the shape to a Brep.

        Returns
        -------
        Brep
            The Brep representation of the shape.

        """
        raise NotImplementedError

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation: Transformation) -> None:
        """Transform the shape.

        Transformations of a shape are performed by applying the transformation to the frame of the shape.
        Transformations of the shape with respect to its local coordinate system are not supported.
        For this reason, only (combinations of) translations and rotations are supported.
        To scale a shape, use the :meth:`Shape.scale` method.

        Parameters
        ----------
        transformation
            The transformation used to transform the shape.

        See Also
        --------
        translate
        rotate
        scale

        """
        self.frame.transform(transformation)

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the shape.

        Scale transformations are applied to the parameters of a shape rahter than to its frame.
        Only uniform scaling is supported.

        Parameters
        ----------
        x
            The uniform scaling factor.
        y
            Reserved for compatibility with the geometry interface.
        z
            Reserved for compatibility with the geometry interface.

        See Also
        --------
        scaled
        translate
        rotate
        transform

        """
        raise NotImplementedError

    def scaled(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Return a scaled copy of the shape.

        Parameters
        ----------
        x
            The uniform scaling factor.
        y
            Reserved for compatibility with the geometry interface.
        z
            Reserved for compatibility with the geometry interface.

        Returns
        -------
        Self
            The scaled shape.

        See Also
        --------
        scale

        """
        shape = self.copy()
        if y is None and z is None:
            shape.scale(x)
        else:
            shape.scale(x, y, z)
        return shape

    # =============================================================================
    # Methods
    # =============================================================================

    def area(self) -> float:
        """Compute the surface area of the shape."""
        raise NotImplementedError

    def volume(self) -> float:
        """Compute the volume enclosed by the shape."""
        raise NotImplementedError

    def contains_point(self, point: CoordinateType) -> bool:
        """Verify if a point is inside the shape.

        Parameters
        ----------
        point
            The point to test.

        Returns
        -------
        bool
            True if the point is inside the shape.
            False otherwise.

        """
        raise NotImplementedError

    def contains_points(self, points: CoordinatesType) -> list[bool]:
        """Verify if a list of points are inside the shape.

        Parameters
        ----------
        points
            The points to test.

        Returns
        -------
        list[bool]
            True if the point is inside the shape.
            False otherwise.

        """
        return [self.contains_point(point) for point in points]
