from typing import Any
from typing import Optional

from typing_extensions import Self

from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector

from .surface import Surface


class PlanarSurface(Surface):
    """A planar surface is defined by a local coordinate system and a size.

    Parameters
    ----------
    frame
        The local coordinate system of the surface.
        If `None`, the world XY frame is used.
    xsize
        The size of the surface in the local X-direction.
    ysize
        The size of the surface in the local Y-direction.
    name
        The name of the surface.

    Examples
    --------
    >>> surface = PlanarSurface(xsize=2.0, ysize=3.0)
    >>> surface.point_at(0.5, 0.5)
    Point(x=1.000, y=1.500, z=0.000)

    A planar surface can also be constructed from a plane.

    >>> plane = Plane.worldXY()
    >>> PlanarSurface.from_plane_and_size(plane, 2.0, 3.0).to_plane() == plane
    True

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """The data representation of the planar surface."""
        return {
            "xsize": self.xsize,
            "ysize": self.ysize,
            "frame": self.frame.__data__,
    }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        return cls(
            xsize=data["xsize"],
            ysize=data["ysize"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        xsize: float = 1.0,
        ysize: float = 1.0,
        frame: Optional[Frame] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._xsize: Optional[float] = None
        self._ysize: Optional[float] = None
        self.xsize = xsize
        self.ysize = ysize

    def __repr__(self) -> str:
        return "{0}(xsize={1}, ysize={2}, frame={3!r})".format(
            type(self).__name__,
            self.xsize,
            self.ysize,
            self.frame,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlanarSurface):
            return False
        return self.xsize == other.xsize and self.ysize == other.ysize and self.frame == other.frame

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def xsize(self) -> float:
        """The size of the surface in its local X-direction."""
        if self._xsize is None:
            raise ValueError("The size of the surface in the local X-direction is not set.")
        return self._xsize

    @xsize.setter
    def xsize(self, xsize: float) -> None:
        if xsize < 0:
            raise ValueError("The size of the surface in the local X-direction should be at least zero.")
        self._xsize = float(xsize)

    @property
    def ysize(self) -> float:
        """The size of the surface in its local Y-direction."""
        if self._ysize is None:
            raise ValueError("The size of the surface in the local Y-direction is not set.")
        return self._ysize

    @ysize.setter
    def ysize(self, ysize: float) -> None:
        if ysize < 0:
            raise ValueError("The size of the surface in the local Y-direction should be at least zero.")
        self._ysize = float(ysize)

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_plane_and_size(cls, plane: Plane, xsize: float, ysize: float) -> Self:
        """Construct a planar surface from a plane and x and y sizes.

        Parameters
        ----------
        plane
            The plane of the surface.
        xsize
            The size of the surface in the local X-direction.
        ysize
            The size of the surface in the local Y-direction.

        Returns
        -------
        PlanarSurface
            A planar surface.

        """
        return cls(xsize, ysize, frame=Frame.from_plane(plane))

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_plane(self) -> Plane:
        """Convert the planar surface to a plane.

        Returns
        -------
        Plane
            The plane of the planar surface.

        """
        return Plane(self.frame.point, self.frame.zaxis)

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, u: float, v: float, world: bool = True) -> Point:
        """Compute a point on the planar surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.
        world
            If `True`, return the point in world coordinates.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        point = Point(u * self.xsize, v * self.ysize, 0)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(
        self,
        u: Optional[float] = None,
        v: Optional[float] = None,
        world: bool = True,
    ) -> Vector:
        """Compute the normal at a point on the planar surface.

        Parameters
        ----------
        u
            The U parameter. This is optional because the normal is constant.
        v
            The V parameter. This is optional because the normal is constant.
        world
            If `True`, return the normal in world coordinates.

        Returns
        -------
        Vector
            The normal vector.

        """
        if world:
            return self.frame.zaxis
        return Vector(0, 0, 1)

    def frame_at(self, u: float, v: float) -> Frame:
        """Compute a frame at a point on the planar surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.

        Returns
        -------
        Frame
            A new frame located at the given parameters and oriented like the
            surface frame.

        """
        return Frame(self.point_at(u, v), self.frame.xaxis, self.frame.yaxis)
