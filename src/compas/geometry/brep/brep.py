from collections.abc import Sequence
from os import PathLike
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal

from compas.geometry import Geometry

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import BrepEdge
    from compas.geometry import BrepFace
    from compas.geometry import BrepLoop
    from compas.geometry import BrepTrim
    from compas.geometry import BrepVertex
    from compas.geometry import Cone
    from compas.geometry import Curve
    from compas.geometry import Cylinder
    from compas.geometry import Frame
    from compas.geometry import Line
    from compas.geometry import Plane
    from compas.geometry import Point
    from compas.geometry import Polygon
    from compas.geometry import Polyline
    from compas.geometry import Sphere
    from compas.geometry import Surface
    from compas.geometry import Torus
    from compas.geometry import Vector

from .operations import brep_area
from .operations import brep_cap_planar_holes
from .operations import brep_centroid
from .operations import brep_classification
from .operations import brep_contains
from .operations import brep_contours
from .operations import brep_cull_unused_edges
from .operations import brep_cull_unused_faces
from .operations import brep_cull_unused_loops
from .operations import brep_cull_unused_vertices
from .operations import brep_fillet
from .operations import brep_fix
from .operations import brep_flip
from .operations import brep_frame
from .operations import brep_heal
from .operations import brep_make_solid
from .operations import brep_overlap
from .operations import brep_rebuild
from .operations import brep_sew
from .operations import brep_slice
from .operations import brep_split
from .operations import brep_tessellate
from .operations import brep_to_data
from .operations import brep_to_iges
from .operations import brep_to_step
from .operations import brep_to_stl
from .operations import brep_topology
from .operations import brep_trimmed
from .operations import brep_volume
from .operations import from_boolean_difference
from .operations import from_boolean_intersection
from .operations import from_boolean_union
from .operations import from_box
from .operations import from_brepfaces
from .operations import from_breps
from .operations import from_cone
from .operations import from_curves
from .operations import from_cylinder
from .operations import from_extrusion
from .operations import from_iges
from .operations import from_loft
from .operations import from_mesh
from .operations import from_native
from .operations import from_pipe
from .operations import from_plane
from .operations import from_planes
from .operations import from_polygons
from .operations import from_sphere
from .operations import from_step
from .operations import from_sweep
from .operations import from_torus


class BrepType:
    """Topological type of a Brep shape."""

    COMPOUND = 0
    COMPSOLID = 1
    SOLID = 2
    SHELL = 3
    FACE = 4
    WIRE = 5
    EDGE = 6
    VERTEX = 7
    SHAPE = 8


class BrepOrientation:
    """Topological orientation of a Brep shape."""

    FORWARD = 0
    REVERSED = 1
    INTERNAL = 2
    EXTERNAL = 3


class Brep(Geometry):
    """Backend-neutral boundary representation.

    A Brep instance owns a backend-native payload while its geometric operations
    are implemented by registered plugins. Backends extend this class at the
    operation level; they do not replace it with a backend-specific subclass.

    Parameters
    ----------
    native_brep
        The backend-native boundary representation, if available.
    name
        The optional object name.

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __dtype__(self) -> str:
        return "compas.geometry/Brep"

    @property
    def __data__(self) -> dict[str, Any]:
        return brep_to_data(self)

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> "Brep":
        brep = Brep()
        brep_rebuild(brep, data)
        return brep

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, native_brep: Any = None, name: str | None = None) -> None:
        super().__init__(name=name)
        self._native_brep = native_brep

    def __str__(self) -> str:
        lines = [
            "Brep",
            "-----",
            "Vertices: {}".format(len(self.vertices)),
            "Edges: {}".format(len(self.edges)),
            "Loops: {}".format(len(self.loops)),
            "Faces: {}".format(len(self.faces)),
            "Frame: {}".format(self.frame),
            "Area: {}".format(self.area),
            "Volume: {}".format(self.volume),
        ]
        return "\n".join(lines)

    def __sub__(self, other: "Brep") -> "Brep":
        """Compute the boolean difference with another Brep.

        Parameters
        ----------
        other
            The Brep to subtract.

        Returns
        -------
        Brep
            The difference.

        """
        return type(self).from_boolean_difference(self, other)

    def __and__(self, other: "Brep") -> "Brep":
        """Compute the boolean intersection with another Brep.

        Parameters
        ----------
        other
            The Brep to intersect with.

        Returns
        -------
        Brep
            The intersection.

        """
        return type(self).from_boolean_intersection(self, other)

    def __add__(self, other: "Brep") -> "Brep":
        """Compute the boolean union with another Brep.

        Parameters
        ----------
        other
            The Brep to combine with.

        Returns
        -------
        Brep
            The union.

        """
        return type(self).from_boolean_union(self, other)

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_brep(self) -> Any:
        """The backend-specific Brep object."""
        return self._native_brep

    @property
    def orientation(self) -> Literal[0, 1, 2, 3]:
        """The orientation as a `BrepOrientation` value."""
        return brep_classification(self)["orientation"]

    @property
    def type(self) -> Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]:
        """The topological type as a `BrepType` value."""
        return brep_classification(self)["type"]

    @property
    def is_valid(self) -> bool:
        """Whether the Brep is valid according to the backend."""
        return brep_classification(self)["is_valid"]

    @property
    def is_orientable(self) -> bool:
        """Whether the Brep is orientable."""
        return brep_classification(self)["is_orientable"]

    @property
    def is_closed(self) -> bool:
        """Whether the Brep has no naked boundaries."""
        return brep_classification(self)["is_closed"]

    @property
    def is_infinite(self) -> bool:
        """Whether the Brep represents an unbounded shape."""
        return brep_classification(self)["is_infinite"]

    @property
    def is_convex(self) -> bool:
        """Whether the Brep is convex."""
        return brep_classification(self)["is_convex"]

    @property
    def is_manifold(self) -> bool:
        """Whether the Brep is manifold."""
        return brep_classification(self)["is_manifold"]

    @property
    def is_surface(self) -> bool:
        """Whether the Brep represents a single surface."""
        return brep_classification(self)["is_surface"]

    @property
    def is_compound(self) -> bool:
        """Whether the Brep is a compound."""
        return brep_classification(self)["is_compound"]

    @property
    def is_compoundsolid(self) -> bool:
        """Whether the Brep is a compound solid."""
        return brep_classification(self)["is_compoundsolid"]

    @property
    def is_shell(self) -> bool:
        """Whether the Brep is a shell."""
        return brep_classification(self)["is_shell"]

    @property
    def is_solid(self) -> bool:
        """Whether the Brep is a solid."""
        return brep_classification(self)["is_solid"]

    # ==============================================================================
    # Geometric Components
    # ==============================================================================

    @property
    def points(self) -> list["Point"]:
        """The unique geometric points of the Brep vertices."""
        return [vertex.point for vertex in self.vertices]

    @property
    def curves(self) -> list["Curve | Line"]:
        """The edge curves."""
        return [edge.curve for edge in self.edges]

    @property
    def surfaces(self) -> list["Surface | Plane | Cylinder | Cone | Sphere | Torus"]:
        """The face surfaces."""
        return [face.surface for face in self.faces]

    # ==============================================================================
    # Topological Components
    # ==============================================================================

    @property
    def vertices(self) -> list["BrepVertex"]:
        """The topological vertices."""
        return brep_topology(self)["vertices"]

    @property
    def edges(self) -> list["BrepEdge"]:
        """The topological edges."""
        return brep_topology(self)["edges"]

    @property
    def trims(self) -> list["BrepTrim"]:
        """The parametric trims."""
        return brep_topology(self)["trims"]

    @property
    def loops(self) -> list["BrepLoop"]:
        """The boundary loops."""
        return brep_topology(self)["loops"]

    @property
    def faces(self) -> list["BrepFace"]:
        """The topological faces."""
        return brep_topology(self)["faces"]

    @property
    def shells(self) -> list["Brep"]:
        """The shells contained in the Brep."""
        return brep_topology(self)["shells"]

    @property
    def solids(self) -> list["Brep"]:
        """The solids contained in the Brep."""
        return brep_topology(self)["solids"]

    # ==============================================================================
    # Geometric Properties
    # ==============================================================================

    @property
    def frame(self) -> "Frame":
        """The local coordinate frame of the Brep."""
        return brep_frame(self)

    @property
    def area(self) -> float:
        """The total surface area."""
        return brep_area(self)

    @property
    def volume(self) -> float:
        """The enclosed volume."""
        return brep_volume(self)

    @property
    def centroid(self) -> "Point":
        """The volume centroid."""
        return brep_centroid(self)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_box(cls, box: "Box") -> "Brep":
        """Construct a Brep from a COMPAS box.

        Parameters
        ----------
        box
            The box.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_box(box)

    @classmethod
    def from_brepfaces(cls, faces: Sequence["BrepFace"]) -> "Brep":
        """Make a Brep from a list of Brep faces forming an open or closed shell.

        Parameters
        ----------
        faces
            The faces forming the shell.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_brepfaces(faces)

    @classmethod
    def from_breps(cls, breps: Sequence["Brep"], *args: Any, **kwargs: Any) -> "Brep":
        """Construct one compound Brep from a list of other Breps.

        Parameters
        ----------
        breps
            The Breps to combine.

        Returns
        -------
        Brep
            The compound Brep.

        """
        return from_breps(breps, *args, **kwargs)

    @classmethod
    def from_cone(cls, cone: "Cone", *args: Any, **kwargs: Any) -> "Brep":
        """Construct a Brep from a COMPAS cone.

        Parameters
        ----------
        cone
            The cone.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_cone(cone, *args, **kwargs)

    @classmethod
    def from_curves(cls, curves: Sequence["Curve"]) -> "Brep":
        """Construct a Brep from a set of closed, planar curves.

        Parameters
        ----------
        curves
            The closed planar curves.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_curves(curves)

    @classmethod
    def from_cylinder(cls, cylinder: "Cylinder") -> "Brep":
        """Construct a Brep from a COMPAS cylinder.

        Parameters
        ----------
        cylinder
            The cylinder.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_cylinder(cylinder)

    @classmethod
    def from_extrusion(cls, curve: "Curve | Polyline", vector: "Vector", cap_ends: bool = True) -> "Brep":
        """Construct a Brep by extruding a closed curve along a direction vector.

        Parameters
        ----------
        curve
            The curve to extrude.
        vector
            The extrusion vector.
        cap_ends
            If `True`, cap the planar ends of the extrusion when possible.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_extrusion(curve, vector, cap_ends)

    @classmethod
    def from_iges(cls, filename: str | PathLike[str]) -> "Brep":
        """Construct a Brep from the data contained in an IGES file.

        Parameters
        ----------
        filename
            The path to the IGES file.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_iges(filename)

    @classmethod
    def from_loft(cls, curves: Sequence["Curve"]) -> "Brep":
        """Construct a Brep by lofting a set of curves.

        Parameters
        ----------
        curves
            The section curves.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_loft(curves)

    @classmethod
    def from_mesh(cls, mesh: "Mesh") -> "Brep":
        """Construct a Brep from a COMPAS mesh.

        Parameters
        ----------
        mesh
            The mesh.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_mesh(mesh)

    @classmethod
    def from_native(cls, native_brep: Any) -> "Brep":
        """Creates a Brep from an instance of a native backend Brep type.

        Parameters
        ----------
        native_brep
            An instance of a native type from a supported Brep backend.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_native(native_brep)

    @classmethod
    def from_pipe(cls, path: "Curve", radius: float, *args: Any, **kwargs: Any) -> "Brep":
        """Construct a Brep by extruding a circle curve along the path curve.

        Parameters
        ----------
        path
            The path curve along which to construct the pipe.
        radius
            The radius of the pipe.
        *args
            Additional positional arguments passed to the backend.
        **kwargs
            Additional keyword arguments passed to the backend.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_pipe(path, radius, *args, **kwargs)

    @classmethod
    def from_plane(
        cls,
        plane: "Plane",
        domain_u: tuple[float, float] = (-1, +1),
        domain_v: tuple[float, float] = (-1, +1),
    ) -> "Brep":
        """Construct a Brep from one plane and its u and v domains.

        Parameters
        ----------
        plane
            A plane.
        domain_u
            The surface domain in the u direction.
        domain_v
            The surface domain in the v direction.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_plane(plane, domain_u=domain_u, domain_v=domain_v)

    @classmethod
    def from_planes(cls, planes: Sequence["Plane"]) -> "Brep":
        """Construct a Brep from a set of planes.

        Parameters
        ----------
        planes
            A list of planes.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_planes(planes)

    @classmethod
    def from_polygons(cls, polygons: Sequence["Polygon"], *args: Any, **kwargs: Any) -> "Brep":
        """Construct a Brep from a set of polygons.

        Parameters
        ----------
        polygons
            The polygons.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_polygons(polygons, *args, **kwargs)

    @classmethod
    def from_sphere(cls, sphere: "Sphere") -> "Brep":
        """Construct a Brep from a COMPAS sphere.

        Parameters
        ----------
        sphere
            The sphere.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_sphere(sphere)

    @classmethod
    def from_step(cls, filename: str | PathLike[str]) -> "Brep":
        """Construct a Brep from the data contained in a STEP file.

        Parameters
        ----------
        filename
            The path to the STEP file.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_step(filename)

    @classmethod
    def from_sweep(
        cls,
        profile: "BrepEdge | BrepFace",
        path: "BrepLoop",
        *args: Any,
        **kwargs: Any,
    ) -> "Brep":
        """Construct a Brep by sweeping a profile along a path.

        Parameters
        ----------
        profile
            The profile to sweep.
        path
            The path to sweep along.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_sweep(profile, path, *args, **kwargs)

    @classmethod
    def from_torus(cls, torus: "Torus") -> "Brep":
        """Construct a Brep from a COMPAS torus.

        Parameters
        ----------
        torus
            The torus.

        Returns
        -------
        Brep
            The constructed Brep.

        """
        return from_torus(torus)

    # ==============================================================================
    # Boolean Constructors
    # ==============================================================================

    @classmethod
    def from_boolean_difference(cls, brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
        """Construct a Brep from the boolean difference of two other Breps.

        Parameters
        ----------
        brep_a
            The Brep from which to subtract.
        brep_b
            The Brep to subtract.

        Returns
        -------
        Brep
            The resulting Brep.

        """
        return from_boolean_difference(brep_a, brep_b)

    @classmethod
    def from_boolean_intersection(cls, brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
        """Construct a Brep from the boolean intersection of two other Breps.

        Parameters
        ----------
        brep_a
            The first Brep.
        brep_b
            The second Brep.

        Returns
        -------
        Brep
            The resulting Brep.

        """
        return from_boolean_intersection(brep_a, brep_b)

    @classmethod
    def from_boolean_union(cls, brep_a: "Brep | list[Brep]", brep_b: "Brep | list[Brep]") -> "Brep":
        """Construct a Brep from the boolean union of two other Breps.

        Parameters
        ----------
        brep_a
            The first Brep.
        brep_b
            The second Brep.

        Returns
        -------
        Brep
            The resulting Brep.

        """
        return from_boolean_union(brep_a, brep_b)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_iges(self, filepath: str | PathLike[str]) -> bool:
        """Write the Brep shape to an IGES file.

        Parameters
        ----------
        filepath
            Location of the file.

        Returns
        -------
        bool
            `True` if writing succeeded.

        """
        return brep_to_iges(self, filepath)

    def to_meshes(self, u: int = 16, v: int = 16) -> list["Mesh"]:
        """Convert the faces of this Brep shape to meshes.

        Parameters
        ----------
        u
            The number of mesh faces in the U direction of the underlying surface geometry of every face of the Brep.
        v
            The number of mesh faces in the V direction of the underlying surface geometry of every face of the Brep.

        Returns
        -------
        list[Mesh]
            One mesh per Brep face.

        """
        mesh, _ = brep_tessellate(self, u=u, v=v)
        return [mesh]

    def to_polygons(self) -> list["Polygon"]:
        """Convert the faces of this Brep shape to polygons.

        Returns
        -------
        list[Polygon]
            One polygon per Brep face.

        """
        return [face.to_polygon() for face in self.faces]

    def to_step(self, filepath: str | PathLike[str]) -> None:
        """Write the Brep shape to a STEP file.

        Parameters
        ----------
        filepath
            Location of the file.

        """
        brep_to_step(self, filepath)

    def to_stl(self, filepath: str | PathLike[str]) -> bool:
        """Write the Brep shape to an STL file.

        Parameters
        ----------
        filepath
            Location of the file.

        Returns
        -------
        bool
            `True` if writing succeeded.

        """
        return brep_to_stl(self, filepath)

    def to_tesselation(
        self,
        linear_deflection: float | None = None,
        angular_deflection: float | None = None,
    ) -> tuple["Mesh", list["Polyline"]]:
        """Create a tessellation of the shape for visualization.

        Parameters
        ----------
        linear_deflection
            Allowable deviation between curved geometry and mesh discretisation.
        angular_deflection
            Allowable angular deviation between adjacent mesh facets.

        Returns
        -------
        tuple[Mesh, list[Polyline]]
            The tessellation mesh and discretized edge curves.

        """
        return brep_tessellate(
            self,
            linear_deflection=linear_deflection,
            angular_deflection=angular_deflection,
        )

    def to_viewmesh(
        self,
        linear_deflection: float | None = None,
        angular_deflection: float | None = None,
    ) -> tuple["Mesh", list["Polyline"]]:
        """Convert this Brep to a view mesh.

        Parameters
        ----------
        linear_deflection
            Allowable deviation between curved geometry and mesh discretisation.
        angular_deflection
            Allowable angular deviation between adjacent mesh facets.

        Returns
        -------
        tuple[Mesh, list[Polyline]]
            The view mesh and discretized edge curves.

        """
        return brep_tessellate(
            self,
            linear_deflection=linear_deflection,
            angular_deflection=angular_deflection,
        )

    # ==============================================================================
    # Relationships
    # ==============================================================================

    def vertex_neighbors(self, vertex: "BrepVertex") -> list["BrepVertex"]:
        """Identify the neighbouring vertices of a given vertex.

        Parameters
        ----------
        vertex
            The vertex.

        Returns
        -------
        list[BrepVertex]
            The neighboring vertices.

        """
        neighbors = []
        for edge in self.vertex_edges(vertex):
            neighbor = edge.last_vertex if edge.first_vertex is vertex else edge.first_vertex
            if neighbor not in neighbors:
                neighbors.append(neighbor)
        return neighbors

    def vertex_edges(self, vertex: "BrepVertex") -> list["BrepEdge"]:
        """Identify the edges connected to a given vertex.

        Parameters
        ----------
        vertex
            The vertex.

        Returns
        -------
        list[BrepEdge]
            The connected edges.

        """
        return [edge for edge in self.edges if vertex is edge.first_vertex or vertex is edge.last_vertex]

    def vertex_faces(self, vertex: "BrepVertex") -> list["BrepFace"]:
        """Identify the faces connected to a vertex.

        Parameters
        ----------
        vertex
            The vertex.

        Returns
        -------
        list[BrepFace]
            The connected faces.

        """
        return [face for face in self.faces if vertex in face.vertices]

    # ==============================================================================
    # Methods
    # ==============================================================================

    def contains(self, object: "Point | Curve | Surface") -> bool:
        """Check if the Brep contains a given geometric primitive.

        Parameters
        ----------
        object
            The object to check for containment.

        Returns
        -------
        bool
            True if the object is contained in the Brep, False otherwise.

        """
        return brep_contains(self, object)

    def trim(self, plane: "Plane | Frame") -> None:
        """Trim this Brep using the given trimming plane.

        Parameters
        ----------
        plane
            Defines the trimming plane.

        """
        self._replace_from(brep_trimmed(self, plane))

    def trimmed(self, plane: "Plane | Frame") -> "Brep":
        """Returns a trimmed copy of this Brep using the given trimming plane.

        Parameters
        ----------
        plane
            Defines the trimming plane.

        Returns
        -------
        Brep
            The trimmed copy.

        """
        return brep_trimmed(self, plane)

    def make_solid(self) -> None:
        """Convert the current shape to a solid if it is a shell."""
        self._replace_from(brep_make_solid(self))

    def sew(self) -> None:
        """Sew together the individual parts of the shape."""
        self._replace_from(brep_sew(self))

    def fix(self) -> None:
        """Fix the shell."""
        self._replace_from(brep_fix(self))

    def heal(self) -> None:
        """Heal the shape."""
        self._replace_from(brep_heal(self))

    def cull_unused_vertices(self) -> None:
        """Remove all unused vertices."""
        self._replace_from(brep_cull_unused_vertices(self))

    def cull_unused_edges(self) -> None:
        """Remove all unused edges."""
        self._replace_from(brep_cull_unused_edges(self))

    def cull_unused_loops(self) -> None:
        """Remove all unused loops."""
        self._replace_from(brep_cull_unused_loops(self))

    def cull_unused_faces(self) -> None:
        """Remove all unused faces."""
        self._replace_from(brep_cull_unused_faces(self))

    def contours(self, planes: Sequence["Plane"]) -> list[list["Polyline"]]:
        """Generate contour lines by slicing the Brep shape with a series of planes.

        Parameters
        ----------
        planes
            The slicing planes.

        Returns
        -------
        list[list[Polyline]]
            A list of polylines per plane.

        """
        return brep_contours(self, planes)

    def edge_faces(self, edge: "BrepEdge") -> list["BrepFace"]:
        """Identify the faces connected to a given edge.

        Parameters
        ----------
        edge
            The edge.

        Returns
        -------
        list[BrepFace]
            The connected faces.

        """
        return [face for face in self.faces if edge in face.edges]

    def edge_loops(self, edge: "BrepEdge") -> list["BrepLoop"]:
        """Identify the parent loops of a given edge.

        Parameters
        ----------
        edge
            The edge.

        Returns
        -------
        list[BrepLoop]
            The parent loops.

        """
        return [loop for loop in self.loops if edge in loop.edges]

    def fillet(self, radius: float, exclude: Sequence["BrepEdge"] | None = None) -> None:
        """Fillet the edges of the Brep.

        Parameters
        ----------
        radius
            The radius of the fillet.
        exclude
            Edges to exclude. If `None`, all edges are filleted.

        Raises
        ------
        BrepFilletError
            If the fillet operation fails.

        """
        self._replace_from(brep_fillet(self, radius, exclude=exclude))

    def filleted(self, radius: float, exclude: Sequence["BrepEdge"] | None = None) -> "Brep":
        """Construct a filleted copy of the Brep.

        Parameters
        ----------
        radius
            The radius of the fillet.
        exclude
            Edges to exclude. If `None`, all edges are filleted.

        Raises
        ------
        BrepFilletError
            If the fillet operation fails.

        Returns
        -------
        Brep
            The filleted copy.

        """
        return brep_fillet(self, radius, exclude=exclude)

    def flip(self) -> None:
        """Flip the orientation of all faces of the Brep."""
        self._replace_from(brep_flip(self))

    def slice(self, plane: "Plane | Frame") -> "Brep | None":
        """Slice through the Brep with a plane.

        Parameters
        ----------
        plane
            Defines the slicing plane.

        Returns
        -------
        Brep | None
            A Brep containing the section edges, or `None` if there is no intersection.

        """
        return brep_slice(self, plane)

    def split(self, cutter: "Brep") -> list["Brep"]:
        """Split the Brep with another Brep.

        Parameters
        ----------
        cutter
            Another Brep to use as a cutter.

        Returns
        -------
        list[Brep]
            The resulting Brep pieces.

        """
        return brep_split(self, cutter)

    def overlap(
        self,
        other: "Brep",
        linear_deflection: float | None = None,
        angular_deflection: float | None = None,
        tolerance: float = 0.0,
        relative: bool = False,
    ) -> tuple[list["BrepFace"], list["BrepFace"]]:
        """Compute the overlap between this Brep and another.

        Parameters
        ----------
        other
            The other Brep.
        linear_deflection
            Maximum linear deflection for proximity meshes.
        angular_deflection
            Maximum angular deflection for proximity meshes.
        tolerance
            Tolerance for overlap calculation.
        relative
            If `True`, compute face deflection relative to edge deflection.

        Returns
        -------
        tuple[list[BrepFace], list[BrepFace]]
            Corresponding overlapping faces from this Brep and the other Brep.

        """
        return brep_overlap(
            self,
            other,
            linear_deflection=linear_deflection,
            angular_deflection=angular_deflection,
            tolerance=tolerance,
            relative=relative,
        )

    def cap_planar_holes(self, tolerance: float | None = None) -> None:
        """Cap all planar holes in the Brep.

        Parameters
        ----------
        tolerance
            The precision to use for the operation. Defaults to `TOL.absolute`.

        Raises
        ------
        BrepError
            If the operation fails.

        """
        self._replace_from(brep_cap_planar_holes(self, tolerance=tolerance))

    # ==============================================================================
    # Private helpers
    # ==============================================================================

    def _replace_from(self, other: "Brep") -> None:
        """Replace the backend payload with the payload of another Brep."""
        self._native_brep = other.native_brep
