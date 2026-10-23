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
from compas.geometry import Transformation
from compas.geometry import Vector
from compas.itertools import linspace
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Brep
    from compas.geometry import Line
    from compas.geometry import Polygon
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation

SurfaceType = TypeVar("SurfaceType", bound="Surface")
type SurfaceCurve = compas.geometry.Curve | compas.geometry.Line


@pluggable(category="factories")
def surface_from_native(cls: type[SurfaceType], *args: object, **kwargs: object) -> SurfaceType:
    raise PluginNotInstalledError


class Surface(Geometry):
    """Class representing a general surface object.

    Discretisation samples a parameter domain into indexed vertices, edges,
    and polygon faces while preserving its polygonal grid topology.
    Tessellation is a separate conversion of that representation to indexed
    triangles with optional normals and texture coordinates.

    Parameters
    ----------
    frame
        The local coordinate frame. Default is the world XY frame.
    name
        The name of the surface.

    Notes
    -----
    Assigning a frame creates an independent copy. Mutating `surface.frame`
    afterwards changes the surface directly. Placement changes invalidate
    cached world-space vertices but leave the resolution-dependent edge and
    face topology cached.

    """

    def __init__(self, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._frame: Frame | None = None
        self._resolution_u = 16
        self._resolution_v = 16
        self._vertex_cache: dict[tuple[int, int, tuple[float, float], tuple[float, float]], tuple[CoordinateType, ...]] = {}
        self._edge_cache: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
        self._face_cache: dict[tuple[int, int], tuple[tuple[int, ...], ...]] = {}
        self._cached_frame: tuple[float, ...] | None = None
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
        self._invalidate_placement()

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
        self._invalidate_placement()

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

    @property
    def resolution_u(self) -> int:
        """The number of faces in the U parameter direction."""
        return self._resolution_u

    @resolution_u.setter
    def resolution_u(self, resolution: int) -> None:
        if resolution < 1:
            raise ValueError("The U resolution should be at least 1.")
        self._resolution_u = resolution
        self._invalidate_discretization()

    @property
    def resolution_v(self) -> int:
        """The number of faces in the V parameter direction."""
        return self._resolution_v

    @resolution_v.setter
    def resolution_v(self, resolution: int) -> None:
        if resolution < 1:
            raise ValueError("The V resolution should be at least 1.")
        self._resolution_v = resolution
        self._invalidate_discretization()

    @property
    def vertices(self) -> tuple[CoordinateType, ...]:
        """The cached vertices of the polygonal parametric representation."""
        return self._vertices(self.resolution_u, self.resolution_v, self.domain_u, self.domain_v)

    @property
    def edges(self) -> tuple[tuple[int, int], ...]:
        """The cached edges of the polygonal parametric representation."""
        key = self.resolution_u, self.resolution_v
        edges = self._edge_cache.get(key)
        if edges is None:
            edges = tuple(self.compute_edges())
            self._edge_cache[key] = edges
        return edges

    @property
    def faces(self) -> tuple[tuple[int, ...], ...]:
        """The cached faces of the polygonal parametric representation."""
        key = self.resolution_u, self.resolution_v
        faces = self._face_cache.get(key)
        if faces is None:
            faces = tuple(tuple(face) for face in self.compute_faces())
            self._face_cache[key] = faces
        return faces

    @property
    def points(self) -> list[Point]:
        """The vertices of the polygonal representation as points."""
        return [Point(vertex[0], vertex[1], vertex[2]) for vertex in self.vertices]

    @property
    def lines(self) -> list["Line"]:
        """The edges of the polygonal representation as lines."""
        from compas.geometry import Line

        points = self.points
        return [Line(points[u], points[v]) for u, v in self.edges]

    @property
    def polygons(self) -> list["Polygon"]:
        """The faces of the polygonal representation as polygons."""
        from compas.geometry import Polygon

        points = self.points
        return [Polygon([points[index] for index in face]) for face in self.faces]

    # ==============================================================================
    # Cache
    # ==============================================================================

    def _invalidate_discretization(self) -> None:
        self._vertex_cache.clear()
        self._edge_cache.clear()
        self._face_cache.clear()
        self._cached_frame = None

    def _invalidate_placement(self) -> None:
        self._vertex_cache.clear()
        self._cached_frame = None

    def _ensure_placement_cache_is_current(self) -> None:
        frame = self.frame
        current = tuple(frame.point) + tuple(frame.xaxis) + tuple(frame.yaxis)
        if self._cached_frame != current:
            self._vertex_cache.clear()
            self._cached_frame = current

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
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> tuple[int, int, tuple[float, float], tuple[float, float]]:
        nu = self.resolution_u if nu is None else nu
        nv = self.resolution_v if nv is None else nv
        if nu < 1 or nv < 1:
            raise ValueError("Surface discretization requires at least one face in each parameter direction.")
        domain_u = self.domain_u if du is None else du
        domain_v = self.domain_v if dv is None else dv
        if not all(isfinite(value) for value in domain_u + domain_v):
            raise ValueError("Surface discretization requires finite parameter domains.")
        return nu, nv, domain_u, domain_v

    def _vertices(
        self,
        nu: int,
        nv: int,
        domain_u: tuple[float, float],
        domain_v: tuple[float, float],
    ) -> tuple[CoordinateType, ...]:
        self._ensure_placement_cache_is_current()
        key = nu, nv, domain_u, domain_v
        vertices = self._vertex_cache.get(key)
        if vertices is None:
            vertices = tuple(tuple(vertex) for vertex in self.compute_vertices(nu, nv, domain_u, domain_v))
            self._vertex_cache[key] = vertices
        return vertices

    def compute_vertices(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> list[CoordinateType]:
        """Compute the vertices of the polygonal parametric representation.

        Parameters
        ----------
        nu
            The U resolution. If omitted, use `resolution_u`.
        nv
            The V resolution. If omitted, use `resolution_v`.
        du
            The U domain subset. If omitted, use `domain_u`.
        dv
            The V domain subset. If omitted, use `domain_v`.

        Returns
        -------
        list[CoordinateType]
            The computed vertex coordinates.

        """
        nu, nv, domain_u, domain_v = self._discretization_parameters(nu, nv, du, dv)
        parameters = product(
            linspace(domain_u[0], domain_u[1], nu + 1),
            linspace(domain_v[0], domain_v[1], nv + 1),
        )
        return [self.point_at(u, v) for u, v in parameters]

    def compute_faces(self, nu: int | None = None, nv: int | None = None) -> list[list[int]]:
        """Compute the faces of the polygonal parametric representation.

        Parameters
        ----------
        nu
            The U resolution. If omitted, use `resolution_u`.
        nv
            The V resolution. If omitted, use `resolution_v`.

        Returns
        -------
        list[list[int]]
            The quadrilateral faces as vertex-index cycles.

        """
        nu, nv, _, _ = self._discretization_parameters(nu, nv)
        return [
            [
                i * (nv + 1) + j,
                (i + 1) * (nv + 1) + j,
                (i + 1) * (nv + 1) + j + 1,
                i * (nv + 1) + j + 1,
            ]
            for i, j in product(range(nu), range(nv))
        ]

    def compute_edges(self, nu: int | None = None, nv: int | None = None) -> list[tuple[int, int]]:
        """Compute the edges of the polygonal parametric representation.

        Parameters
        ----------
        nu
            The U resolution. If omitted, use `resolution_u`.
        nv
            The V resolution. If omitted, use `resolution_v`.

        Returns
        -------
        list[tuple[int, int]]
            The unique edges as vertex-index pairs.

        """
        edges = []
        seen = set()
        for face in self.compute_faces(nu, nv):
            for index, start in enumerate(face):
                end = face[(index + 1) % len(face)]
                key = (start, end) if start < end else (end, start)
                if key not in seen:
                    seen.add(key)
                    edges.append((start, end))
        return edges

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def tessellated(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
        include_normals: bool = True,
        include_texture_coordinates: bool = True,
    ) -> "Tessellation[list[CoordinateType], list[list[int]]]":
        """Return a triangular tessellation of a parameter-domain subset.

        Parameters
        ----------
        nu
            The number of faces in the U direction.
        nv
            The number of faces in the V direction.
        du
            The U domain subset. If omitted, use the entire domain.
        dv
            The V domain subset. If omitted, use the entire domain.
        include_normals
            If True, include analytic vertex normals.
        include_texture_coordinates
            If True, include normalized UV coordinates.

        Returns
        -------
        Tessellation
            The indexed triangular representation for visualization.

        """
        from compas.geometry import Tessellation

        nu, nv, domain_u, domain_v = self._discretization_parameters(nu, nv, du, dv)

        parameters = list(
            product(
                linspace(domain_u[0], domain_u[1], nu + 1),
                linspace(domain_v[0], domain_v[1], nv + 1),
            )
        )
        vertices = list(self._vertices(nu, nv, domain_u, domain_v))
        normals = [self.normal_at(u, v) for u, v in parameters] if include_normals else None
        texture_coordinates = [[i / nu, j / nv] for i, j in product(range(nu + 1), range(nv + 1))] if include_texture_coordinates else None
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

    def to_vertices_and_faces(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> tuple[list[CoordinateType], list[list[int]]]:
        """Convert the surface to a list of vertices and faces.

        Parameters
        ----------
        nu
            The number of faces in the u direction.
            Default is `16`.
        nv
            The number of faces in the v direction.
            Default is `16`.
        du
            The subset of the domain in the u direction.
            Default is `None`, in which case the entire domain is used.
        dv
            The subset of the domain in the v direction.
            Default is `None`, in which case the entire domain is used.

        Returns
        -------
        tuple[list[CoordinateType], list[list[int]]]
            The vertices and quadrilateral faces of the discretization.

        Raises
        ------
        ValueError
            If either face count is less than one or a domain endpoint is not
            finite.

        """
        nu, nv, domain_u, domain_v = self._discretization_parameters(nu, nv, du, dv)
        vertices = list(self._vertices(nu, nv, domain_u, domain_v))
        faces = self.compute_faces(nu, nv)
        return vertices, faces

    def to_triangles(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> list[list[CoordinateType]]:
        """Convert the surface to a list of triangles.

        Parameters
        ----------
        nu
            The number of faces in the u direction.
            Default is `16`.
        nv
            The number of faces in the v direction.
            Default is `16`.
        du
            The subset of the domain in the u direction.
            Default is `None`, in which case the entire domain is used.
        dv
            The subset of the domain in the v direction.
            Default is `None`, in which case the entire domain is used.

        Returns
        -------
        list[list[CoordinateType]]
            The triangular faces as coordinate lists.

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        triangles: list[list[CoordinateType]] = []
        for a, b, c, d in faces:
            triangles.append([vertices[a], vertices[b], vertices[c]])
            triangles.append([vertices[a], vertices[c], vertices[d]])
        return triangles

    def to_quads(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> list[list[CoordinateType]]:
        """Convert the surface to a list of quads.

        Parameters
        ----------
        nu
            The number of faces in the u direction.
            Default is `16`.
        nv
            The number of faces in the v direction.
            Default is `16`.
        du
            The subset of the domain in the u direction.
            Default is `None`, in which case the entire domain is used.
        dv
            The subset of the domain in the v direction.
            Default is `None`, in which case the entire domain is used.

        Returns
        -------
        list[list[CoordinateType]]
            The quadrilateral faces as coordinate lists.

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        quads: list[list[CoordinateType]] = []
        for a, b, c, d in faces:
            quads.append([vertices[a], vertices[b], vertices[c], vertices[d]])
        return quads

    def to_polygonal_surface(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> "PolygonalSurface":
        """Convert a discretized parameter domain to a polygonal surface.

        Parameters
        ----------
        nu
            The number of faces in the u direction.
        nv
            The number of faces in the v direction.
        du
            The subset of the domain in the u direction.
            If omitted, the entire domain is used.
        dv
            The subset of the domain in the v direction.
            If omitted, the entire domain is used.

        Returns
        -------
        PolygonalSurface
            The lightweight polygonal approximation of the parameter domain.

        Examples
        --------
        >>> from compas.geometry import PlanarSurface
        >>> surface = PlanarSurface().to_polygonal_surface(nu=2, nv=2)
        >>> len(surface.faces)
        4

        """
        from compas.geometry import PolygonalSurface

        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        return PolygonalSurface(vertices, faces)

    def to_mesh(
        self,
        nu: int | None = None,
        nv: int | None = None,
        du: tuple[float, float] | None = None,
        dv: tuple[float, float] | None = None,
    ) -> "Mesh":
        """Convert the surface to a mesh.

        Parameters
        ----------
        nu
            The number of faces in the u direction.
            Default is `16`.
        nv
            The number of faces in the v direction.
            Default is `16`.
        du
            The subset of the domain in the u direction.
            Default is `None`, in which case the entire domain is used.
        dv
            The subset of the domain in the v direction.
            Default is `None`, in which case the entire domain is used.

        Returns
        -------
        Mesh
            A mesh object.

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        return Mesh.from_vertices_and_faces(vertices, faces)

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
        self._invalidate_placement()

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

    # ==============================================================================
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
