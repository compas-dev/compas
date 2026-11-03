from collections.abc import Iterator
from itertools import product
from math import isfinite
from typing import TYPE_CHECKING
from typing import Literal
from typing import Self
from typing import TypeVar
from typing import overload

import compas.geometry
from compas._typing import CoordinateType
from compas._typing import FilePath
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Point
from compas.geometry import TessellationStrategy
from compas.geometry import Transformation
from compas.geometry import UVGrid
from compas.geometry import Vector
from compas.itertools import linspace
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation

SurfaceType = TypeVar("SurfaceType", bound="Surface")
type SurfaceCurve = compas.geometry.Curve | compas.geometry.Line


@pluggable(category="factories")
def surface_from_native(cls: type[SurfaceType], *args: object, **kwargs: object) -> SurfaceType:
    raise PluginNotInstalledError


class Surface(Geometry):
    """Class representing a general surface object.

    Polygonization samples a parameter domain into an independent
    `PolygonalSurface` while preserving its polygonal grid topology.
    Tessellation creates an ephemeral indexed triangular representation with
    aligned normals and texture coordinates. Polygonization requires an
    explicit strategy. Tessellation uses `UVGrid(64, 64)` when none is
    provided.

    Parameters
    ----------
    frame
        The local coordinate frame. Default is the world XY frame.
    name
        The name of the surface.

    """

    def __init__(self, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._frame: Frame | None = None
        self.frame = frame

    def __repr__(self) -> str:
        return "{0}(frame={1!r}, domain_u={2}, domain_v={3})".format(
            type(self).__name__,
            self.frame,
            self.domain_u,
            self.domain_v,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def frame(self) -> Frame:
        """The local coordinate frame of the surface.

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
        """The transformation from world XY to the surface frame."""
        return Transformation.from_frame(self.frame)

    @property
    def point(self) -> Point:
        """The origin of the surface frame.

        Notes
        -----
        Assigning a point or three coordinates updates the frame origin and
        creates an independent point.

        """
        return self.frame.point

    @point.setter
    def point(self, point: CoordinateType) -> None:
        self.frame.point = point

    @property
    def xaxis(self) -> Vector:
        """The x-axis of the surface frame."""
        return self.frame.xaxis

    @property
    def yaxis(self) -> Vector:
        """The y-axis of the surface frame."""
        return self.frame.yaxis

    @property
    def zaxis(self) -> Vector:
        """The z-axis of the surface frame."""
        return self.frame.zaxis

    @property
    def dimension(self) -> int:
        """The dimension of the embedding space, which is always three."""
        return 3

    @property
    def domain_u(self) -> tuple[float, float]:
        """The parameter domain in the u-direction."""
        return 0.0, 1.0

    @property
    def domain_v(self) -> tuple[float, float]:
        """The parameter domain in the v-direction."""
        return 0.0, 1.0

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in the u-direction."""
        return False

    @property
    def is_periodic_v(self) -> bool:
        """Whether the surface is periodic in the v-direction."""
        return False

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, surface: object) -> Self:
        """Construct a parametric surface from a native surface geometry.

        Parameters
        ----------
        surface
            A CAD native surface object.

        Returns
        -------
        Self
            The constructed surface.

        """
        return surface_from_native(cls, surface)

    # ==============================================================================
    # Discretization
    # ==============================================================================

    def _discretization_parameters(
        self,
        strategy: TessellationStrategy,
    ) -> tuple[int, int, tuple[float, float], tuple[float, float]]:
        if not isinstance(strategy, UVGrid):
            raise TypeError(f"{type(self).__name__} discretization requires UVGrid.")
        nu = strategy.u
        nv = strategy.v
        if nu < 1 or nv < 1:
            raise ValueError("Surface discretization requires at least one face in each parameter direction.")
        domain_u = self.domain_u
        domain_v = self.domain_v
        if not all(isfinite(value) for value in domain_u + domain_v):
            raise ValueError("Surface discretization requires finite parameter domains.")
        return nu, nv, domain_u, domain_v

    def _compute_vertices(
        self,
        nu: int,
        nv: int,
        domain_u: tuple[float, float],
        domain_v: tuple[float, float],
    ) -> list[CoordinateType]:
        parameters = product(
            linspace(domain_u[0], domain_u[1], nu + 1),
            linspace(domain_v[0], domain_v[1], nv + 1),
        )
        return [self.point_at(u, v) for u, v in parameters]

    def _compute_faces(self, nu: int, nv: int) -> list[list[int]]:
        return [
            [
                i * (nv + 1) + j,
                (i + 1) * (nv + 1) + j,
                (i + 1) * (nv + 1) + j + 1,
                i * (nv + 1) + j + 1,
            ]
            for i, j in product(range(nu), range(nv))
        ]

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def polygonize(self, strategy: TessellationStrategy) -> "PolygonalSurface":
        """Polygonize the surface with an explicit approximation strategy.

        Parameters
        ----------
        strategy
            The polygonization strategy.

        Returns
        -------
        PolygonalSurface
            An independent polygonal surface with quadrilateral cells.

        Raises
        ------
        TypeError
            If the strategy is not `UVGrid`.

        """
        from compas.geometry import PolygonalSurface

        nu, nv, domain_u, domain_v = self._discretization_parameters(strategy)
        vertices = self._compute_vertices(nu, nv, domain_u, domain_v)
        faces = self._compute_faces(nu, nv)
        return PolygonalSurface(vertices, faces)

    def tessellate(
        self,
        strategy: TessellationStrategy | None = None,
    ) -> "Tessellation[list[CoordinateType], list[list[int]]]":
        """Tessellate the surface.

        Parameters
        ----------
        strategy
            The tessellation strategy. If `None`, `UVGrid(64, 64)` is used.

        Returns
        -------
        Tessellation
            The ephemeral indexed triangular representation, including
            analytic normals and normalized UV coordinates.

        Raises
        ------
        TypeError
            If the strategy is not `UVGrid`.

        """
        from compas.geometry import Tessellation

        nu, nv, domain_u, domain_v = self._discretization_parameters(strategy if strategy is not None else UVGrid(64, 64))
        parameters = list(
            product(
                linspace(domain_u[0], domain_u[1], nu + 1),
                linspace(domain_v[0], domain_v[1], nv + 1),
            )
        )
        vertices = self._compute_vertices(nu, nv, domain_u, domain_v)
        normals = [self.normal_at(u, v) for u, v in parameters]
        texture_coordinates = [[i / nu, j / nv] for i, j in product(range(nu + 1), range(nv + 1))]
        triangles = []
        for i, j in product(range(nu), range(nv)):
            a = i * (nv + 1) + j
            b = (i + 1) * (nv + 1) + j
            c = (i + 1) * (nv + 1) + j + 1
            d = i * (nv + 1) + j + 1
            triangles.append([a, b, c])
            triangles.append([a, c, d])
        return Tessellation(vertices, triangles, vertex_normals=normals, texture_coordinates=texture_coordinates)

    def to_step(self, filepath: FilePath, schema: str = "AP203") -> None:
        """Write the surface geometry to a STP file.

        Parameters
        ----------
        filepath
            The path to the output file.
        schema
            The STEP schema to use. Default is `"AP203"`.

        """
        raise NotImplementedError

    def to_brep(self) -> "Brep":
        """Convert the surface to a BREP representation.

        Returns
        -------
        Brep
            The boundary representation.

        """
        raise NotImplementedError

    # ==============================================================================
    # Transformations
    # ==============================================================================

    def transform(self, transformation: Transformation) -> None:
        """Transform the local coordinate system of the surface.

        Parameters
        ----------
        transformation
            The transformation.

        Notes
        -----
        The transformation matrix is applied to the local coordinate system of the surface.
        Transformations are limited to (combinations of) translations and rotations.
        All other components of the transformation matrix are ignored.

        """
        self.frame.transform(transformation)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def space_u(self, n: int = 10) -> Iterator[float]:
        """Compute evenly spaced parameters over the surface domain in the U direction.

        Parameters
        ----------
        n
            The number of parameters.

        Returns
        -------
        Iterator[float]

        """
        umin, umax = self.domain_u
        return linspace(umin, umax, n)

    def space_v(self, n: int = 10) -> Iterator[float]:
        """Compute evenly spaced parameters over the surface domain in the V direction.

        Parameters
        ----------
        n
            The number of parameters.

        Returns
        -------
        Iterator[float]

        """
        vmin, vmax = self.domain_v
        return linspace(vmin, vmax, n)

    def isocurve_u(self, u: float) -> SurfaceCurve:
        """Compute the isoparametric curve at a U parameter.

        Parameters
        ----------
        u
            The U parameter.

        Returns
        -------
        Curve | Line
            The isoparametric curve.

        """
        raise NotImplementedError

    def isocurve_v(self, v: float) -> SurfaceCurve:
        """Compute the isoparametric curve at a V parameter.

        Parameters
        ----------
        v
            The V parameter.

        Returns
        -------
        Curve | Line
            The isoparametric curve.

        """
        raise NotImplementedError

    def boundary(self) -> list[SurfaceCurve]:
        """Compute the boundary curves of the surface.

        Returns
        -------
        list[Curve | Line]
            The oriented boundary curves.

        """
        raise NotImplementedError

    def pointgrid(self, nu: int = 10, nv: int = 10) -> list[Point]:
        """Compute point locations corresponding to evenly spaced parameters over the surface domain.

        Parameters
        ----------
        nu
            The size of the grid in the U direction.
        nv
            The size of the grid in the V direction.

        Returns
        -------
        list[Point]
            The sampled points in row-major parameter order.

        """
        return [self.point_at(i, j) for i, j in product(self.space_u(nu), self.space_v(nv))]

    def point_at(self, u: float, v: float) -> Point:
        """Compute a point on the surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.

        Returns
        -------
        Point
            The point at the given parameters.

        """
        raise NotImplementedError

    def normal_at(self, u: float, v: float) -> Vector:
        """Compute a normal at a point on the surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.

        Returns
        -------
        Vector
            The surface normal at the given parameters.

        """
        raise NotImplementedError

    def frame_at(self, u: float, v: float) -> Frame:
        """Compute the local frame at a point on the surface.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.

        Returns
        -------
        Frame
            The frame at the given parameters.

        """
        raise NotImplementedError

    @overload
    def closest_point(self, point: CoordinateType, return_parameters: Literal[False] = False) -> Point | None: ...

    @overload
    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: Literal[True],
    ) -> tuple[Point, tuple[float, float]] | None: ...

    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: bool = False,
    ) -> Point | tuple[Point, tuple[float, float]] | None:
        """Compute the closest point on the surface to a given point.

        Parameters
        ----------
        point
            The point to project to the surface.
        return_parameters
            If `True`, also return the surface UV parameters.

        Returns
        -------
        Point | None
            The closest point if `return_parameters` is `False`, or `None` if
            the projection fails.
        tuple[Point, tuple[float, float]] | None
            The closest point and its UV parameters if `return_parameters` is
            `True`, or `None` if the projection fails.

        """
        raise NotImplementedError
