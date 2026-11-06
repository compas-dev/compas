from numbers import Integral
from typing import TYPE_CHECKING
from typing import Self

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.typing import PointLike
from compas.typing import PointsLike

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation


class Shape(Geometry):
    """Base class for geometric shapes.

    Shapes are parametrically defined with respect to a local coordinate frame.
    The default frame is the world XY frame.

    Shapes are finite, closed objects, with a boundary that separates the interior from the exterior.
    They have a well-defined surface area and volume.

    Conversion to a polygonal surface samples the parametric boundary into an independent
    `PolygonalSurface` while preserving its natural polygonal topology.
    Tessellation creates an ephemeral indexed triangular representation.
    Each concrete producer exposes resolution parameters appropriate to its
    own parameterization. Supported backends can convert a shape to a `Brep`.

    Breps support exact boolean operations.

    Parameters
    ----------
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the shape.

    """

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

    def _compute_vertices(self, resolution: tuple[int, ...]) -> tuple[PointLike, ...]:
        """Compute fresh vertex coordinates in world coordinates."""
        local_vertices = self._compute_local_vertices(resolution)
        return tuple(tuple(vertex) for vertex in transform_points(local_vertices, self.transformation))

    def _compute_local_vertices(self, resolution: tuple[int, ...]) -> list[PointLike]:
        """Compute fresh vertex coordinates in the local shape frame."""
        raise NotImplementedError

    def _compute_faces(self, resolution: tuple[int, ...]) -> list[list[int]]:
        """Compute fresh face cycles for the requested strategy."""
        raise NotImplementedError

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_polygonal_surface(self) -> "PolygonalSurface":
        """Convert the shape to its default polygonal boundary.

        Concrete shapes override this method with their producer-specific
        resolution keywords while preserving the no-argument default call.

        Returns
        -------
        PolygonalSurface
            The independent polygonal boundary.

        """
        raise NotImplementedError

    def to_tessellation(self) -> "Tessellation":
        """Convert the shape to its default indexed-triangle representation.

        Concrete shapes override this method with their producer-specific
        resolution keywords while preserving the no-argument default call.

        Returns
        -------
        Tessellation
            The indexed triangle representation.

        """
        raise NotImplementedError

    @staticmethod
    def _validate_resolution(value: int, name: str, minimum: int) -> int:
        if not isinstance(value, Integral) or isinstance(value, bool):
            raise TypeError(f"{name} should be an integer.")
        value = int(value)
        if value < minimum:
            raise ValueError(f"{name} should be at least {minimum}.")
        return value

    def _to_polygonal_surface(self, resolution: tuple[int, ...]) -> "PolygonalSurface":
        """Build an independent polygonal boundary at the given resolution."""
        from compas.geometry import PolygonalSurface

        return PolygonalSurface(
            list(self._compute_vertices(resolution)),
            [list(face) for face in self._compute_faces(resolution)],
        )

    def _to_tessellation(self, resolution: tuple[int, ...]) -> "Tessellation":
        """Triangulate the polygonal surface built at the given resolution."""
        return self._to_polygonal_surface(resolution).triangulated()

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

    def contains_point(self, point: PointLike) -> bool:
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

    def contains_points(self, points: PointsLike) -> list[bool]:
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
