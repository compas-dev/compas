from itertools import product
from math import isfinite
from typing import TYPE_CHECKING
from typing import Iterator
from typing import Literal
from typing import Optional
from typing import TypeVar
from typing import Union
from typing import overload

from typing_extensions import Self

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
    from compas.geometry import Curve
    from compas.geometry import Line
    from compas.geometry import Polyhedron

SurfaceType = TypeVar("SurfaceType", bound="Surface")
SurfaceCurve = Union["Curve", "Line"]


@pluggable(category="factories")
def surface_from_native(cls: type[SurfaceType], *args: object, **kwargs: object) -> SurfaceType:
    raise PluginNotInstalledError


class Surface(Geometry):
    """Class representing a general surface object.

    Parameters
    ----------
    frame
        The local coordinate frame. Default is the world XY frame.
    name
        The name of the surface.

    Notes
    -----
    Assigning a frame creates an independent copy. Mutating `surface.frame`
    afterwards changes the surface directly.

    """

    def __init__(self, frame: Optional[Frame] = None, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._frame: Optional[Frame] = None
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
    def frame(self, frame: Optional[Frame]) -> None:
        if frame is None:
            self._frame = None
        else:
            if not isinstance(frame, Frame):
                raise TypeError("The frame must be a Frame object or None.")
            self._frame = Frame(frame.point, frame.xaxis, frame.yaxis)

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
    def is_closed(self) -> bool:
        """Whether the surface is closed."""
        raise NotImplementedError

    @property
    def is_periodic_u(self) -> bool:
        """Whether the surface is periodic in the u-direction."""
        raise NotImplementedError

    @property
    def is_periodic_v(self) -> bool:
        """Whether the surface is periodic in the v-direction."""
        raise NotImplementedError

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
    # Conversions
    # ==============================================================================

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
        nu: int = 16,
        nv: int = 16,
        du: Optional[tuple[float, float]] = None,
        dv: Optional[tuple[float, float]] = None,
    ) -> tuple[list[Point], list[list[int]]]:
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
        tuple[list[Point], list[list[int]]]
            The vertices and quadrilateral faces of the discretization.

        Raises
        ------
        ValueError
            If either face count is less than one or a domain endpoint is not
            finite.

        """
        if nu < 1 or nv < 1:
            raise ValueError("Surface discretization requires at least one face in each parameter direction.")

        domain_u = self.domain_u if du is None else du
        domain_v = self.domain_v if dv is None else dv
        if not all(isfinite(value) for value in domain_u + domain_v):
            raise ValueError("Surface discretization requires finite parameter domains.")

        vertices = [
            self.point_at(i, j)
            for i, j in product(
                linspace(domain_u[0], domain_u[1], nu + 1),
                linspace(domain_v[0], domain_v[1], nv + 1),
            )
        ]
        faces = [
            [
                i * (nv + 1) + j,
                i * (nv + 1) + j + 1,
                (i + 1) * (nv + 1) + j + 1,
                (i + 1) * (nv + 1) + j,
            ]
            for i, j in product(range(nu), range(nv))
        ]

        return vertices, faces

    def to_triangles(
        self,
        nu: int = 16,
        nv: int = 16,
        du: Optional[tuple[float, float]] = None,
        dv: Optional[tuple[float, float]] = None,
    ) -> list[list[Point]]:
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
        list[list[Point]]
            The triangular faces as point lists.

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        triangles: list[list[Point]] = []
        for a, b, c, d in faces:
            triangles.append([vertices[a], vertices[b], vertices[c]])
            triangles.append([vertices[a], vertices[c], vertices[d]])
        return triangles

    def to_quads(
        self,
        nu: int = 16,
        nv: int = 16,
        du: Optional[tuple[float, float]] = None,
        dv: Optional[tuple[float, float]] = None,
    ) -> list[list[Point]]:
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
        list[list[Point]]
            The quadrilateral faces as point lists.

        """
        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        quads: list[list[Point]] = []
        for a, b, c, d in faces:
            quads.append([vertices[a], vertices[b], vertices[c], vertices[d]])
        return quads

    def to_polyhedron(
        self,
        nu: int = 16,
        nv: int = 16,
        du: Optional[tuple[float, float]] = None,
        dv: Optional[tuple[float, float]] = None,
    ) -> "Polyhedron":
        """Convert the surface to a polyhedron.

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
        Polyhedron
            A polyhedron object.

        """
        from compas.geometry import Polyhedron

        vertices, faces = self.to_vertices_and_faces(nu=nu, nv=nv, du=du, dv=dv)
        return Polyhedron(vertices, faces)

    def to_mesh(
        self,
        nu: int = 16,
        nv: int = 16,
        du: Optional[tuple[float, float]] = None,
        dv: Optional[tuple[float, float]] = None,
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
    # Methods continued
    # ==============================================================================

    @overload
    def closest_point(self, point: CoordinateType, return_parameters: Literal[False] = False) -> Optional[Point]: ...

    @overload
    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: Literal[True],
    ) -> Optional[tuple[Point, tuple[float, float]]]: ...

    def closest_point(
        self,
        point: CoordinateType,
        return_parameters: bool = False,
    ) -> Optional[Union[Point, tuple[Point, tuple[float, float]]]]:
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
