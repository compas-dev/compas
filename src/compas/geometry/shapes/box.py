from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.geometry import centroid_points
from compas.geometry import transform_points

from .shape import Shape

if TYPE_CHECKING:
    from compas.geometry import Brep


class Box(Shape):
    """A box is defined by a frame and its dimensions along the frame's x-, y- and z-axes.

    The center of the box is positioned at the origin of the
    coordinate system defined by the frame. The box is axis-aligned to the frame.

    A box is a three-dimensional geometric shape with 8 vertices, 12 edges and 6
    faces. The edges of a box meet at its vertices at 90 degree angles. The
    faces of a box are planar. Faces which do not share an edge are parallel.

    Parameters
    ----------
    xsize
        The size of the box in the box frame's x direction.
    ysize
        The size of the box in the box frame's y direction.
        Defaults to the value of `xsize`.
    zsize
        The size of the box in the box frame's z direction.
        Defaults to the value of `xsize`.
    frame
        The frame of the box.
        Defaults to `Frame.worldXY()`.
    name
        The name of the shape.

    Examples
    --------
    >>> box = Box(1)
    >>> box.xsize
    1.0
    >>> box.ysize
    1.0
    >>> box.zsize
    1.0
    >>> box.volume()
    1.0
    >>> box.area()
    6.0

    >>> box = Box(1, 2, 3)
    >>> box.xsize
    1.0
    >>> box.ysize
    2.0
    >>> box.zsize
    3.0
    >>> box.volume()
    6.0
    >>> box.area()
    22.0

    """

    @property
    def __data__(self) -> dict:
        return {
            "xsize": self.xsize,
            "ysize": self.ysize,
            "zsize": self.zsize,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(
            xsize=data["xsize"],
            ysize=data["ysize"],
            zsize=data["zsize"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(
        self,
        xsize: float = 1.0,
        ysize: float | None = None,
        zsize: float | None = None,
        frame: Frame | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(frame=frame, name=name)
        self._xsize: float | None = None
        self._ysize: float | None = None
        self._zsize: float | None = None
        self.xsize = xsize
        self.ysize = xsize if ysize is None else ysize
        self.zsize = xsize if zsize is None else zsize

    def __repr__(self) -> str:
        return "{0}(xsize={1}, ysize={2}, zsize={3}, frame={4!r})".format(
            type(self).__name__,
            self.xsize,
            self.ysize,
            self.zsize,
            self.frame,
        )

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def xsize(self) -> float:
        """The size of the box along its local x-axis."""
        if self._xsize is None:
            raise ValueError("The size of the box along the local X axis is not set.")
        return self._xsize

    @xsize.setter
    def xsize(self, xsize: float) -> None:
        if xsize < 0:
            raise ValueError("The minimum value of the size of the box along the local X axis is zero.")
        self._xsize = float(xsize)
        self._invalidate_discretization()

    @property
    def ysize(self) -> float:
        """The size of the box along its local y-axis."""
        if self._ysize is None:
            raise ValueError("The size of the box along the local Y axis is not set.")
        return self._ysize

    @ysize.setter
    def ysize(self, ysize: float) -> None:
        if ysize < 0:
            raise ValueError("The minimum value of the size of the box along the local Y axis is zero.")
        self._ysize = float(ysize)
        self._invalidate_discretization()

    @property
    def zsize(self) -> float:
        """The size of the box along its local z-axis."""
        if self._zsize is None:
            raise ValueError("The size of the box along the local Z axis is not set.")
        return self._zsize

    @zsize.setter
    def zsize(self, zsize: float) -> None:
        if zsize < 0:
            raise ValueError("The minimum value of the size of the box along the local Z axis is zero.")
        self._zsize = float(zsize)
        self._invalidate_discretization()

    @property
    def width(self) -> float:
        """The size of the box along its local x-axis."""
        return self.xsize

    @property
    def depth(self) -> float:
        """The size of the box along its local y-axis."""
        return self.ysize

    @property
    def height(self) -> float:
        """The size of the box along its local z-axis."""
        return self.zsize

    @property
    def diagonal(self) -> Line:
        """The diagonal from the minimum to the maximum local corner."""
        a = self.frame.point + self.frame.xaxis * -0.5 * self.xsize + self.frame.yaxis * -0.5 * self.ysize + self.frame.zaxis * -0.5 * self.zsize
        b = self.frame.point + self.frame.xaxis * 0.5 * self.xsize + self.frame.yaxis * 0.5 * self.ysize + self.frame.zaxis * 0.5 * self.zsize
        return Line(a, b)

    @property
    def dimensions(self) -> list[float]:
        """The dimensions along the three axes of the box frame."""
        return [self.xsize, self.ysize, self.zsize]

    def area(self) -> float:
        """Compute the surface area of the box."""
        return 2 * self.xsize * self.ysize + 2 * self.ysize * self.zsize + 2 * self.zsize * self.xsize

    def volume(self) -> float:
        """Compute the volume of the box."""
        return self.xsize * self.ysize * self.zsize

    @property
    def points(self) -> list[Point]:
        """The eight defining corner points of the box."""
        return super().points

    @property
    def bottom(self) -> list[int]:
        """The vertex indices of the bottom face."""
        return [0, 1, 2, 3]

    @property
    def front(self) -> list[int]:
        """The vertex indices of the front face."""
        return [0, 3, 5, 4]

    @property
    def right(self) -> list[int]:
        """The vertex indices of the right face."""
        return [3, 2, 6, 5]

    @property
    def back(self) -> list[int]:
        """The vertex indices of the back face."""
        return [2, 1, 7, 6]

    @property
    def left(self) -> list[int]:
        """The vertex indices of the left face."""
        return [1, 0, 4, 7]

    @property
    def top(self) -> list[int]:
        """The vertex indices of the top face."""
        return [4, 5, 6, 7]

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_width_height_depth(cls, width: float, height: float, depth: float) -> Self:
        """Construct a box from its width, height and depth.

        Note that width is along the X-axis, height along Z-axis, and depth along the Y-axis.

        Parameters
        ----------
        width
            Width of the box.
        height
            Height of the box.
        depth
            Depth of the box.

        Returns
        -------
        Self
            The resulting box.

        Notes
        -----
        The box is axis-aligned to the world coordinate system and centered at the origin.

        Examples
        --------
        >>> box = Box.from_width_height_depth(1.0, 2.0, 3.0)

        """
        width = float(width)
        height = float(height)
        depth = float(depth)

        return cls(width, depth, height)

    @classmethod
    def from_bounding_box(cls, bbox: CoordinatesType) -> Self:
        """Construct a box from the result of a bounding box calculation.

        Parameters
        ----------
        bbox
            A list of 8 point locations, representing the corners of the bounding box.
            Positions 0, 1, 2, 3 are the bottom corners.
            Positions 4, 5, 6, 7 are the top corners.
            Both the top and bottom face are oriented in CCW direction, starting at the bottom, left-most point.

        Returns
        -------
        Self
            The box shape.

        Examples
        --------
        >>> from compas.geometry import bounding_box
        >>> bbox = bounding_box([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        >>> box = Box.from_bounding_box(bbox)
        >>> box.width
        1.0
        >>> box.height
        1.0
        >>> box.depth
        1.0

        """
        a = bbox[0]
        b = bbox[1]
        d = bbox[3]
        e = bbox[4]
        xaxis = Vector.from_start_end(a, b)
        yaxis = Vector.from_start_end(a, d)
        zaxis = Vector.from_start_end(a, e)
        xsize = xaxis.length
        ysize = yaxis.length
        zsize = zaxis.length
        frame = Frame(centroid_points(bbox), xaxis, yaxis)
        return cls(xsize=xsize, ysize=ysize, zsize=zsize, frame=frame)

    @classmethod
    def from_corner_corner_height(cls, corner1: CoordinateType, corner2: CoordinateType, height: float) -> Self:
        """Construct a box from the opposite corners of its base and its height.

        Parameters
        ----------
        corner1
            The XYZ coordinates of the bottom left corner of the base of the box.
        corner2
            The XYZ coordinates of the top right corner of the base of the box.
        height
            The height of the box.

        Returns
        -------
        Self
            The resulting box.

        Examples
        --------
        >>> box = Box.from_corner_corner_height([0.0, 0.0, 0.0], [1.0, 1.0, 0.0], 1.0)

        """
        if height == 0:
            raise Exception("The box should have a height.")

        x1, y1, z1 = corner1
        x2, y2, z2 = corner2

        if z1 != z2:
            raise Exception("Corners should be in the same horizontal plane.")

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        width = xaxis.length
        depth = yaxis.length
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), z1 + 0.5 * height]
        frame = Frame(point, xaxis, yaxis)

        return cls(xsize=width, ysize=depth, zsize=height, frame=frame)

    @classmethod
    def from_diagonal(cls, diagonal: Line | Sequence[CoordinateType]) -> Self:
        """Construct a box from its main diagonal.

        Parameters
        ----------
        diagonal
            The diagonal of the box, represented by a pair of points in space.

        Returns
        -------
        Self
            The resulting box.

        Examples
        --------
        >>> diagonal = [0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
        >>> box = Box.from_diagonal(diagonal)

        """
        d1, d2 = diagonal

        x1, y1, z1 = d1
        x2, y2, z2 = d2

        if z1 == z2:
            raise Exception("The box has no height.")

        xaxis = Vector(x2 - x1, 0, 0)
        yaxis = Vector(0, y2 - y1, 0)
        zaxis = Vector(0, 0, z2 - z1)
        width = xaxis.length
        depth = yaxis.length
        height = zaxis.length
        point = [0.5 * (x1 + x2), 0.5 * (y1 + y2), 0.5 * (z1 + z2)]
        frame = Frame(point, xaxis, yaxis)

        return cls(width, depth, height, frame)

    @classmethod
    def from_points(cls, points: CoordinatesType) -> Self:
        """Construct a box from a set of points.

        Parameters
        ----------
        points
            A list of points.

        Returns
        -------
        Self
            The resulting box.

        """
        from compas.geometry import bounding_box

        bbox = bounding_box(points)
        return cls.from_bounding_box(bbox)

    # ==========================================================================
    # Discretisation
    # ==========================================================================

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        dx = 0.5 * self.xsize
        dy = 0.5 * self.ysize
        dz = 0.5 * self.zsize
        return [
            [-dx, -dy, -dz],
            [-dx, +dy, -dz],
            [+dx, +dy, -dz],
            [+dx, -dy, -dz],
            [-dx, -dy, +dz],
            [+dx, -dy, +dz],
            [+dx, +dy, +dz],
            [-dx, +dy, +dz],
        ]

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the discrete representation of the box."""
        return [self.bottom, self.front, self.right, self.back, self.left, self.top]

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_brep(self) -> "Brep":
        """Return a BRep representation of the box.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_box(self)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    # def transform(self, transformation):
    #     """Transform the box.

    #     Parameters
    #     ----------
    #     transformation : :class:`Transformation`
    #         The transformation used to transform the Box.

    #     Returns
    #     -------
    #     None

    #     Examples
    #     --------
    #     >>> box = Box(Frame.worldXY(), 1.0, 2.0, 3.0)
    #     >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    #     >>> T = Transformation.from_frame(frame)
    #     >>> box.transform(T)

    #     """
    #     self.frame.transform(transformation)
    #     # Always local scaling, non-uniform scaling based on frame not yet considered.
    #     Sc, _, _, _, _ = transformation.decomposed()
    #     scalex = Sc[0, 0]
    #     scaley = Sc[1, 1]
    #     scalez = Sc[2, 2]
    #     self.xsize *= scalex
    #     self.ysize *= scaley
    #     self.zsize *= scalez

    def scale(self, x: float, y: float | None = None, z: float | None = None) -> None:
        """Scale the box.

        Parameters
        ----------
        x
            The scaling factor in x-direction. If no other factor is specified,
            this factor will be used for all directions.
        y
            The scaling factor in the y-direction.
            Defaults to `x`.
        z
            The scaling factor in the z-direction.
            Defaults to `x`.

        """
        self.xsize *= x
        self.ysize *= y if y is not None else x
        self.zsize *= z if z is not None else x

    def scaled(self, x: float, y: float | None = None, z: float | None = None) -> Self:
        """Return a scaled copy of the box.

        Parameters
        ----------
        x
            The scaling factor in the x-direction.
        y
            The scaling factor in the y-direction.
            Defaults to `x`.
        z
            The scaling factor in the z-direction.
            Defaults to `x`.

        Returns
        -------
        Self

        """
        box = self.copy()
        box.scale(x, y, z)
        return box

    # ==========================================================================
    # Methods
    # ==========================================================================

    def corner(self, index: int) -> Point:
        """Return one of the eight corners of the box.

        Parameters
        ----------
        index
            The index of the corner.

        Returns
        -------
        Point
            The corner point.

        Raises
        ------
        ValueError
            If the index is not between 0 and 7.

        """
        if index < 0 or index > 7:
            raise ValueError("Index should be between 0 and 7.")
        return self.points[index]

    def contains_point(self, point: CoordinateType, tol: float = 1e-6) -> bool:
        """Verify if the box contains a given point.

        Parameters
        ----------
        point
            The point to test.
        tol
            The tolerance for the point containment check.

        Returns
        -------
        bool

        See Also
        --------
        contains_points

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        x, y, z = transform_points([point], T)[0]

        dx = 0.5 * self.xsize + tol

        if x < -dx or x > +dx:
            return False

        dy = 0.5 * self.ysize + tol

        if y < -dy or y > +dy:
            return False

        dz = 0.5 * self.zsize + tol

        if z < -dz or z > +dz:
            return False

        return True

    def contains_points(self, points: CoordinatesType, tol: float = 1e-6) -> list[bool]:
        """Verify if the box contains the given points.

        Parameters
        ----------
        points
            A list of points.
        tol
            The tolerance for the point containment check.

        Returns
        -------
        list[bool]

        See Also
        --------
        contains_point

        Examples
        --------
        >>> from compas.geometry import Point, Box
        >>> box = Box(2.0, 2.0, 2.0)
        >>> points = [Point(0.0, 0.0, 0.0), Point(1.0, 1.0, 1.0)]
        >>> results = box.contains_points(points)
        >>> all(results)
        True

        """
        dx = 0.5 * self.xsize + tol
        dy = 0.5 * self.ysize + tol
        dz = 0.5 * self.zsize + tol

        T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
        points = transform_points(points, T)
        results = [False] * len(points)

        for index, (x, y, z) in enumerate(points):
            if x < -dx or x > +dx:
                continue

            if y < -dy or y > +dy:
                continue

            if z < -dz or z > +dz:
                continue

            results[index] = True

        return results
