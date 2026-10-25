from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.geometry import transform_points

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Brep
    from compas.geometry import Line
    from compas.geometry import Point
    from compas.geometry import Polygon
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation


class Shape(Geometry):
    """Base class for geometric shapes.

    Shapes are parametrically defined with respect to a local coordinate frame.
    The default frame is the world XY frame.

    Shapes are finite, closed objects, with a boundary that separates the interior from the exterior.
    They have a well-defined surface area and volume.

    Discretisation samples the parametric boundary into indexed vertices,
    edges, and polygon faces at a chosen resolution. These elements preserve
    the natural polygonal topology of the sampled representation. Direct
    conversion to `PolygonalSurface` or `Mesh` preserves that topology.

    Tessellation is the separate conversion of geometry to indexed triangles,
    with optional rendering attributes such as normals and texture
    coordinates. The cached `tessellation` property performs that conversion for
    visualization and triangle-based processing. Supported backends can
    convert a shape to a `Brep`.

    Breps support exact boolean operations.

    Parameters
    ----------
    frame
        The local coordinate frame. If `None`, the world XY frame is used.
    name
        The name of the shape.

    Notes
    -----
    Assigning a frame creates an independent copy. Mutating `shape.frame`
    afterwards changes the shape directly. Discretisation is computed in the
    local shape frame. Changing placement therefore invalidates only cached
    world-space vertices, not cached local vertices, edges, or faces.

    """

    def __init__(self, frame: Frame | None = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._frame: Frame | None = None
        self._resolution_u = 16
        self._resolution_v = 16
        self._local_vertex_cache: dict[tuple[int, int], tuple[CoordinateType, ...]] = {}
        self._vertex_cache: dict[tuple[int, int], tuple[CoordinateType, ...]] = {}
        self._edge_cache: dict[tuple[int, int], tuple[tuple[int, int], ...]] = {}
        self._face_cache: dict[tuple[int, int], tuple[tuple[int, ...], ...]] = {}
        self._tessellation_cache: Tessellation | None = None
        self._mesh_cache: Mesh | None = None
        self._cached_frame: tuple[float, ...] | None = None
        self.frame = frame

    # =============================================================================
    # Cache
    # =============================================================================

    def _invalidate_discretization(self) -> None:
        self._local_vertex_cache.clear()
        self._vertex_cache.clear()
        self._edge_cache.clear()
        self._face_cache.clear()
        self._tessellation_cache = None
        self._mesh_cache = None
        self._cached_frame = None

    def _invalidate_placement(self) -> None:
        self._vertex_cache.clear()
        self._tessellation_cache = None
        self._mesh_cache = None
        self._cached_frame = None

    def _ensure_placement_cache_is_current(self) -> None:
        frame = self.frame
        current = tuple(frame.point) + tuple(frame.xaxis) + tuple(frame.yaxis)
        if self._cached_frame != current:
            self._vertex_cache.clear()
            self._tessellation_cache = None
            self._mesh_cache = None
            self._cached_frame = current

    def _resolutions(self, u: int | None = None, v: int | None = None) -> tuple[int, int]:
        u = self.resolution_u if u is None else u
        v = self.resolution_v if v is None else v
        if u < 3:
            raise ValueError("The U resolution should be at least 3.")
        if v < 3:
            raise ValueError("The V resolution should be at least 3.")
        return u, v

    def _vertices(self, u: int, v: int) -> tuple[CoordinateType, ...]:
        self._ensure_placement_cache_is_current()
        key = u, v
        vertices = self._vertex_cache.get(key)
        if vertices is None:
            local_vertices = self._local_vertex_cache.get(key)
            if local_vertices is None:
                local_vertices = tuple(tuple(vertex) for vertex in self._compute_vertices(u, v))
                self._local_vertex_cache[key] = local_vertices
            vertices = tuple(tuple(vertex) for vertex in transform_points(local_vertices, self.transformation))
            self._vertex_cache[key] = vertices
        return vertices

    def _edges(self, u: int, v: int) -> tuple[tuple[int, int], ...]:
        key = u, v
        edges = self._edge_cache.get(key)
        if edges is None:
            edges = tuple(self.compute_edges(u, v))
            self._edge_cache[key] = edges
        return edges

    def _faces(self, u: int, v: int) -> tuple[tuple[int, ...], ...]:
        key = u, v
        faces = self._face_cache.get(key)
        if faces is None:
            faces = tuple(tuple(face) for face in self.compute_faces(u, v))
            self._face_cache[key] = faces
        return faces

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
        self._invalidate_placement()

    @property
    def transformation(self) -> Transformation:
        """The transformation from world XY to the shape frame."""
        return Transformation.from_frame(self.frame)

    @property
    def resolution_u(self) -> int:
        """The discretization resolution in the U direction."""
        return self._resolution_u

    @resolution_u.setter
    def resolution_u(self, u: int) -> None:
        if u < 3:
            raise ValueError("The U resolution should be at least 3.")
        self._resolution_u = u
        self._invalidate_discretization()

    @property
    def resolution_v(self) -> int:
        """The discretization resolution in the V direction."""
        return self._resolution_v

    @resolution_v.setter
    def resolution_v(self, v: int) -> None:
        if v < 3:
            raise ValueError("The V resolution should be at least 3.")
        self._resolution_v = v
        self._invalidate_discretization()

    @property
    def vertices(self) -> tuple[CoordinateType, ...]:
        """The cached vertices of the polygonal parametric representation."""
        return self._vertices(self.resolution_u, self.resolution_v)

    @property
    def edges(self) -> tuple[tuple[int, int], ...]:
        """The cached edges of the polygonal parametric representation."""
        return self._edges(self.resolution_u, self.resolution_v)

    @property
    def faces(self) -> tuple[tuple[int, ...], ...]:
        """The cached faces of the polygonal parametric representation."""
        return self._faces(self.resolution_u, self.resolution_v)

    @property
    def points(self) -> list["Point"]:
        """The vertices of the polygonal representation as points."""
        from compas.geometry import Point

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

    @property
    def tessellation(self) -> "Tessellation":
        """The cached triangular representation at the current resolution."""
        self._ensure_placement_cache_is_current()
        if self._tessellation_cache is None:
            self._tessellation_cache = self.compute_tessellation()
        return self._tessellation_cache

    @property
    def mesh(self) -> "Mesh":
        """The cached topology-preserving mesh at the current resolution.

        Notes
        -----
        The returned mesh is shared by subsequent property accesses. Use
        `compute_mesh()` when an independent mesh is required.

        """
        self._ensure_placement_cache_is_current()
        if self._mesh_cache is None:
            self._mesh_cache = self.compute_mesh()
        return self._mesh_cache

    # =============================================================================
    # Discretisation
    # =============================================================================

    def compute_vertices(self, u: int | None = None, v: int | None = None) -> list[CoordinateType]:
        """Compute the vertices of the polygonal parametric representation.

        Parameters
        ----------
        u
            The U resolution. If omitted, use `resolution_u`.
        v
            The V resolution. If omitted, use `resolution_v`.

        Returns
        -------
        list[CoordinateType]
            The computed vertex coordinates.

        """
        u, v = self._resolutions(u, v)
        return [vertex for vertex in transform_points(self._compute_vertices(u, v), self.transformation)]

    def _compute_vertices(self, u: int, v: int) -> list[CoordinateType]:
        """Compute uncached vertex coordinates in the local shape frame."""
        raise NotImplementedError

    def compute_edges(self, u: int | None = None, v: int | None = None) -> list[tuple[int, int]]:
        """Compute the edges of the polygonal parametric representation.

        Parameters
        ----------
        u
            The U resolution. If omitted, use `resolution_u`.
        v
            The V resolution. If omitted, use `resolution_v`.

        Returns
        -------
        list[tuple[int, int]]
            The unique edges as vertex-index pairs.

        """
        edges = []
        seen = set()
        for face in self.compute_faces(u, v):
            for index, start in enumerate(face):
                end = face[(index + 1) % len(face)]
                key = (start, end) if start < end else (end, start)
                if key not in seen:
                    seen.add(key)
                    edges.append((start, end))
        return edges

    def compute_faces(self, u: int | None = None, v: int | None = None) -> list[list[int]]:
        """Compute the faces of the polygonal parametric representation.

        Parameters
        ----------
        u
            The U resolution. If omitted, use `resolution_u`.
        v
            The V resolution. If omitted, use `resolution_v`.

        Returns
        -------
        list[list[int]]
            The computed faces as vertex-index cycles.

        """
        raise NotImplementedError

    # =============================================================================
    # Bounding boxes
    # =============================================================================

    @property
    def aabb(self) -> "Box":
        """The axis-aligned bounding box of the discretized shape.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import bounding_box

        vertices, _ = self.to_vertices_and_faces()
        return Box.from_bounding_box(bounding_box(vertices))

    @property
    def obb(self) -> "Box":
        """The oriented bounding box of the discretized shape.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box

        vertices, _ = self.to_vertices_and_faces()
        return Box.from_bounding_box(oriented_bounding_box(vertices))

    # =============================================================================
    # Conversions
    # =============================================================================

    def compute_tessellation(
        self,
        u: int | None = None,
        v: int | None = None,
    ) -> "Tessellation[list[CoordinateType], tuple[tuple[int, ...], ...]]":
        """Compute a triangular tessellation of the shape boundary.

        Parameters
        ----------
        u
            Number of faces in the U direction. If omitted, use
            `resolution_u`.
        v
            Number of faces in the V direction. If omitted, use
            `resolution_v`.

        Returns
        -------
        Tessellation
            The indexed triangular representation for visualization.

        """
        from compas.geometry import Tessellation

        u, v = self._resolutions(u, v)
        vertices = list(self._vertices(u, v))
        triangles = []
        for face in self._faces(u, v):
            if len(face) == 3:
                triangles.append(face)
            elif len(face) == 4:
                a, b, c, d = face
                triangles.append((a, b, c))
                triangles.append((a, c, d))
            else:
                raise ValueError("Shape tessellation requires triangular or quadrilateral faces.")
        return Tessellation(vertices, tuple(triangles))

    def to_vertices_and_faces(self, u: int | None = None, v: int | None = None) -> tuple[list[CoordinateType], list[list[int]]]:
        """Convert the shape to a list of vertices and faces.

        Parameters
        ----------
        u
            Number of faces in the "u" direction.
            If no value is provided, the value of `self.resolution_u` will be used.
        v
            Number of faces in the "v" direction.
            If no value is provided, the value of `self.resolution_v` will be used.

        Returns
        -------
        tuple[list[CoordinateType], list[list[int]]]
            The vertices and faces of the shape.

        """
        u, v = self._resolutions(u, v)
        return list(self._vertices(u, v)), [list(face) for face in self._faces(u, v)]

    def to_polygonal_surface(self, u: int | None = None, v: int | None = None) -> "PolygonalSurface":
        """Convert the discretized boundary to a polygonal surface.

        Parameters
        ----------
        u
            Number of faces in the u direction.
            If omitted, `resolution_u` is used.
        v
            Number of faces in the v direction.
            If omitted, `resolution_v` is used.

        Returns
        -------
        PolygonalSurface
            The lightweight polygonal boundary representation.

        Examples
        --------
        >>> from compas.geometry import Box
        >>> surface = Box(1.0).to_polygonal_surface()
        >>> surface.is_closed
        True

        """
        from compas.geometry import PolygonalSurface

        vertices, faces = self.to_vertices_and_faces(u=u, v=v)
        return PolygonalSurface(vertices, faces)

    def compute_mesh(self, u: int | None = None, v: int | None = None) -> "Mesh":
        """Compute a topology-preserving mesh representation of the shape.

        Parameters
        ----------
        u
            Number of faces in the "u" direction.
            If no value is provided, the value of `self.resolution_u` will be used.
        v
            Number of faces in the "v" direction.
            If no value is provided, the value of `self.resolution_v` will be used.

        Returns
        -------
        Mesh
            The mesh representation of the shape.

        Notes
        -----
        Parameters `u` and `v` define the resolution of the discretisation of curved geometry.
        If the geometry is not curved in a particular direction, the corresponding parameter will be ignored.
        For example, a cylinder has a resolution in the "u" direction, but not in the "v" direction.
        A sphere has a resolution in both the "u" and the "v" direction.
        A box has no resolution in either direction.

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(u=u, v=v)
        return Mesh.from_vertices_and_faces(vertices, faces)

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
        self._invalidate_placement()

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
