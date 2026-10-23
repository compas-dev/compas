from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Self

from compas.data import Data
from compas.geometry import Polygon

if TYPE_CHECKING:
    from compas.geometry import Brep
    from compas.geometry import BrepEdge
    from compas.geometry import BrepLoop
    from compas.geometry import BrepVertex
    from compas.geometry import Cone
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import NurbsSurface
    from compas.geometry import Plane
    from compas.geometry import Point
    from compas.geometry import Sphere
    from compas.geometry import Surface
    from compas.geometry import Torus


class SurfaceType:
    """Geometric type of a Brep face surface."""

    PLANE = 0
    CYLINDER = 1
    CONE = 2
    SPHERE = 3
    TORUS = 4
    BEZIER_SURFACE = 5
    BSPLINE_SURFACE = 6
    SURFACE_OF_REVOLUTION = 7
    SURFACE_OF_EXTRUSION = 8
    OFFSET_SURFACE = 9
    OTHER_SURFACE = 10


class BrepFace(Data):
    """Interface for a topological face of a boundary representation."""

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def is_plane(self) -> bool:
        """Whether the face geometry is planar."""
        raise NotImplementedError

    @property
    def is_cylinder(self) -> bool:
        """Whether the face geometry is cylindrical."""
        raise NotImplementedError

    @property
    def is_sphere(self) -> bool:
        """Whether the face geometry is spherical."""
        raise NotImplementedError

    @property
    def is_torus(self) -> bool:
        """Whether the face geometry is toroidal."""
        raise NotImplementedError

    @property
    def is_cone(self) -> bool:
        """Whether the face geometry is conical."""
        raise NotImplementedError

    @property
    def is_bspline(self) -> bool:
        """Whether the face geometry is a B-spline surface."""
        raise NotImplementedError

    @property
    def vertices(self) -> list["BrepVertex"]:
        """The vertices of the face."""
        raise NotImplementedError

    @property
    def edges(self) -> list["BrepEdge"]:
        """The edges of the face."""
        raise NotImplementedError

    @property
    def loops(self) -> list["BrepLoop"]:
        """The boundary loops of the face, with the outer loop first."""
        raise NotImplementedError

    @property
    def surface(self) -> "Surface | Plane | Cylinder | Cone | Sphere | Torus":
        """The most specific supported geometry of the underlying surface."""
        raise NotImplementedError

    @property
    def native_face(self) -> Any:
        """The backend-specific face object."""
        raise NotImplementedError

    @property
    def nurbssurface(self) -> "NurbsSurface":
        """The underlying surface represented as a NURBS surface."""
        raise NotImplementedError

    @property
    def area(self) -> float:
        """The surface area of the trimmed face."""
        raise NotImplementedError

    @property
    def centroid(self) -> "Point":
        """The centroid of the trimmed face."""
        raise NotImplementedError

    @property
    def is_reversed(self) -> bool:
        """Whether the face orientation is reversed from its surface."""
        raise NotImplementedError

    @property
    def is_valid(self) -> bool:
        """Whether the face is valid according to the backend."""
        raise NotImplementedError

    @property
    def type(self) -> Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        """The surface type as a `SurfaceType` value."""
        raise NotImplementedError

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_plane(cls, plane: "Plane") -> Self:
        """Construct a face from a plane.

        Parameters
        ----------
        plane
            The plane.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    @classmethod
    def from_cylinder(cls, cylinder: "Cylinder") -> Self:
        """Construct a face from a cylinder.

        Parameters
        ----------
        cylinder
            The cylinder.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    @classmethod
    def from_cone(cls, cone: "Cone") -> Self:
        """Construct a face from a cone.

        Parameters
        ----------
        cone
            The cone.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    @classmethod
    def from_sphere(cls, sphere: "Sphere") -> Self:
        """Construct a face from a sphere.

        Parameters
        ----------
        sphere
            The sphere.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    @classmethod
    def from_torus(cls, torus: "Torus") -> Self:
        """Construct a face from a torus.

        Parameters
        ----------
        torus
            The torus.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    @classmethod
    def from_surface(cls, surface: "Surface") -> Self:
        """Construct a face from a parametric surface.

        Parameters
        ----------
        surface
            The surface.

        Returns
        -------
        Self
            The constructed face.

        """
        raise NotImplementedError

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_polygon(self) -> Polygon:
        """Convert the outer boundary to a polygon.

        Returns
        -------
        Polygon
            The polygon formed by the vertices of the first loop. Inner loops
            are not included.

        """
        return Polygon([vertex.point for vertex in self.loops[0].vertices])

    def to_polygons(self) -> list[Polygon]:
        """Convert all boundary loops to polygons.

        Returns
        -------
        list[Polygon]
            The outer boundary followed by the inner boundaries.

        """
        return [Polygon([vertex.point for vertex in loop.vertices]) for loop in self.loops]

    def to_plane(self) -> "Plane":
        """Return the face surface as a plane."""
        raise NotImplementedError

    def to_cylinder(self) -> "Cylinder":
        """Return the face surface as a cylinder."""
        raise NotImplementedError

    def to_cone(self) -> "Cone":
        """Return the face surface as a cone."""
        raise NotImplementedError

    def to_sphere(self) -> "Sphere":
        """Return the face surface as a sphere."""
        raise NotImplementedError

    def to_torus(self) -> "Torus":
        """Return the face surface as a torus."""
        raise NotImplementedError

    def to_nurbs(self) -> "NurbsSurface":
        """Return the face surface as a NURBS surface."""
        raise NotImplementedError

    # ==========================================================================
    # Methods
    # ==========================================================================

    def adjacent_faces(self) -> list[Self]:
        """Return the faces adjacent across the edges of this face."""
        raise NotImplementedError

    def as_brep(self) -> "Brep":
        """Return a Brep containing this face."""
        raise NotImplementedError

    def add_loop(self, loop: "BrepLoop", *args: object, **kwargs: object) -> None:
        """Add an inner boundary loop.

        Parameters
        ----------
        loop
            The loop to add.
        *args
            Additional backend-specific arguments.
        **kwargs
            Additional backend-specific keyword arguments.

        """
        raise NotImplementedError

    def add_loops(self, loops: Sequence["BrepLoop"], *args: object, **kwargs: object) -> None:
        """Add multiple inner boundary loops.

        Parameters
        ----------
        loops
            The loops to add.
        *args
            Additional backend-specific arguments.
        **kwargs
            Additional backend-specific keyword arguments.

        """
        raise NotImplementedError

    def frame_at(self, u: float, v: float) -> "Frame":
        """Compute the surface frame at UV parameters.

        Parameters
        ----------
        u
            The U parameter.
        v
            The V parameter.

        Returns
        -------
        Frame
            The surface frame.

        """
        raise NotImplementedError

    def try_get_nurbssurface(
        self,
        precision: float = 1e-3,
        continuity_u: int | None = None,
        continuity_v: int | None = None,
        maxdegree_u: int = 5,
        maxdegree_v: int = 5,
        maxsegments_u: int = 1,
        maxsegments_v: int = 1,
    ) -> "NurbsSurface | None":
        """Try to approximate the face surface with a NURBS surface.

        Parameters
        ----------
        precision
            The approximation precision.
        continuity_u
            The requested continuity in the U direction.
        continuity_v
            The requested continuity in the V direction.
        maxdegree_u
            The maximum degree in the U direction.
        maxdegree_v
            The maximum degree in the V direction.
        maxsegments_u
            The maximum number of segments in the U direction.
        maxsegments_v
            The maximum number of segments in the V direction.

        Returns
        -------
        NurbsSurface | None
            The approximated surface, or `None` when conversion is not
            possible.

        """
        raise NotImplementedError
